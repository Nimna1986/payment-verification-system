from pydantic import BaseModel, Field
from enum import Enum

class PaymentStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class PaymentUpdate(BaseModel):
    amount: float | None = None
    payment_method: str | None = None
    transaction_id: str | None = None
    order_id: int | None = None
    status: PaymentStatus | None = None

class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str
    transaction_id: str
    order_id: int | None = None
    status: PaymentStatus
    user_id: int

class PaymentResponse(BaseModel):
    id: int
    amount: float
    payment_method: str
    transaction_id: str
    order_id: int | None = None
    status: PaymentStatus
    user_id: int

    class Config:
        from_attributes = True