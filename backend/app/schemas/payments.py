from pydantic import BaseModel


class PaymentUpdate(BaseModel):
    amount: float | None = None
    payment_method: str | None = None
    transaction_id: str | None = None
    status: str | None = None

class PaymentResponse(BaseModel):
    id: int
    amount: float
    payment_method: str
    transaction_id: str
    status: str
    user_id: int

    class Config:
        from_attributes = True