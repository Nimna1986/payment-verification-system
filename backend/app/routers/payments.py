from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.payments import Payments
from app.models.user import User
from app.schemas.payments import PaymentUpdate, PaymentResponse, PaymentCreate
from app.services.payment_verification import verify_payment_data

from app.services.ocr_service import extract_text
from app.services.payment_parser import parse_payment_text

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.get("/", response_model=list[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(Payments).all()
    return payments

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == payment_data.user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    exsisting_payment = db.query(Payments).filter(Payments.transaction_id == payment_data.transaction_id).first()

    if exsisting_payment is not None:
        raise HTTPException(
            status_code=400,
            detail="Transaction ID already exists"
        )
    


    payment = Payments(
        amount = payment_data.amount,
        payment_method = payment_data.payment_method,
        transaction_id=payment_data.transaction_id,
        order_id=payment_data.order_id,
        status=payment_data.status,
        user_id=payment_data.user_id
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment

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

@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted successfully"
    }

@router.post("/{payment_id}/verify")
def verify_payment(
    payment_id: int,
    ocr_data: dict,
    db: Session = Depends(get_db)
):
    return verify_payment_data(
        db=db,
        payment_id=payment_id,
        ocr_data=ocr_data
    )

@router.post("/{payment_id}/upload")
async def upload_payment_image(
    payment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )


    file_path = f"uploads/payment_{payment_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    payment.image_path = file_path

    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment image uploaded successfully",
        "payment_id": payment.id,
        "image_path": payment.image_path
    }

@router.post("/{payment_id}/verify-image")
def verify_payment_image(
    payment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Save uploaded image temporarily
    image_path = f"uploads/{file.filename}"

    with open(image_path, "wb") as image_file:
        image_file.write(file.file.read())

    # 2. OCR
    extracted_text = extract_text(image_path)

    # 3. Parse OCR text
    ocr_data = parse_payment_text(extracted_text)

    # 4. Verify payment
    result = verify_payment_data(
        db=db,
        payment_id=payment_id,
        ocr_data=ocr_data
    )

    return result