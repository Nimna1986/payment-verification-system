from sqlalchemy.orm import Session

from app.models.payments import Payments
from app.models.orders import Orders


def verify_payment_data(
    db: Session,
    payment_id: int,
    ocr_data: dict
) -> dict:

    # 1. Find payment
    payment = (
        db.query(Payments)
        .filter(Payments.id == payment_id)
        .first()
    )

    if payment is None:
        return {
            "status": "NOT_FOUND",
            "message": "Payment not found"
        }

    # Find the order associated with this payment
    order = (
        db.query(Orders)
        .filter(Orders.id == payment.order_id)
        .first()
    )

    if order is None:
        return {
            "status": "ORDER_NOT_FOUND",
            "message": "Order associated with this payment was not found",
            "payment_id": payment.id,
            "order_id": payment.order_id
        }
    if order.status == "PAID":
        return {
            "status": "ORDER_ALREADY_PAID",
            "message": "This order has already been paid",
            "order_id": order.id,
            "payment_id": payment.id
        }
    if order.status == "CANCELLED":
        return {
            "status": "ORDER_CANCELLED",
            "message": "Payment cannot be verified for a cancelled order",
            "order_id": order.id,
            "payment_id": payment.id
        }

    # 2. Check whether payment has already been processed
    if payment.status == "verified":
        return {
            "status": "ALREADY_VERIFIED",
            "message": "Payment has already been verified",
            "payment_id": payment.id
        }

    # 3. Get OCR values
    ocr_transaction_id = ocr_data.get("reference_number")
    existing_payment = (db.query(Payments).filter(
            Payments.transaction_id == str(ocr_transaction_id).strip(),
            Payments.id != payment.id
        )
        .first()
    )

    if existing_payment:
        return {
            "status": "DUPLICATE_TRANSACTION",
            "message": "This transaction ID is already associated with another payment",
            "payment_id": payment.id,
            "existing_payment_id": existing_payment.id,
            "transaction_id": ocr_transaction_id
        }

    ocr_amount = ocr_data.get("amount")
    ocr_payment_method = ocr_data.get("payment_option")

    # 4. Make sure required OCR fields exist
    missing_fields = []

    if not ocr_transaction_id:
        missing_fields.append("reference_number")

    if ocr_amount is None:
        missing_fields.append("amount")

    if not ocr_payment_method:
        missing_fields.append("payment_option")

    if missing_fields:
        return {
            "status": "INVALID_OCR",
            "message": "Required payment information could not be extracted",
            "missing_fields": missing_fields
        }

    # 5. Compare transaction/reference number
    transaction_match = (
        str(payment.transaction_id).strip()
        == str(ocr_transaction_id).strip()
    )

    # 6. Compare amount
    payment_amount_match = (
    float(payment.amount) == float(ocr_amount)
)

    order_amount_match = (
        float(order.expected_amount) == float(ocr_amount)
    )

    # 7. Compare payment method
    db_payment_method = payment.payment_method.strip().lower()
    ocr_payment_method = str(ocr_payment_method).strip().lower()

    payment_method_match = (
        db_payment_method in ocr_payment_method
        or ocr_payment_method in db_payment_method
    )

    # 8. Collect mismatches
    mismatches = []

    if not transaction_match:
        mismatches.append("Transaction ID does not match")

    if not payment_amount_match:
        mismatches.append("OCR amount does not match payment amount")

    if not order_amount_match:
        mismatches.append("OCR amount does not match order amount")

    if not payment_method_match:
        mismatches.append("Payment method does not match")

    # 9. Verification successful
    if not mismatches:

        payment.status = "verified"
        order.status = "PAID"

        db.commit()
        db.refresh(payment)

        return {
            "status": "VERIFIED",
            "message": "Payment verified successfully",
            "payment_id": payment.id,
            "transaction_id": payment.transaction_id,
            "order_id": order.id,
            "amount": payment.amount,
            "expected_amount": order.expected_amount,
            "payment_method": payment.payment_method
        }

    # 10. Verification failed
    payment.status = "rejected"

    db.commit()
    db.refresh(payment)

    return {
        "status": "REJECTED",
        "message": "Payment verification failed",
        "payment_id": payment.id,
        "mismatches": mismatches,
        "order_id": order.id,
        "expected_amount": order.expected_amount,
        "paid_amount": payment.amount
    }

