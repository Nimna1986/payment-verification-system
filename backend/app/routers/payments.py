from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.payments import Payments
from app.schemas.payments import PaymentUpdate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    if payment_data.amount is not None:
        payment.amount = payment_data.amount

    if payment_data.payment_method is not None:
        payment.payment_method = payment_data.payment_method

    if payment_data.transaction_id is not None:
        payment.transaction_id = payment_data.transaction_id

    if payment_data.status is not None:
        payment.status = payment_data.status

    db.commit()
    db.refresh(payment)

    return payment