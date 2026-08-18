from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_name: str
    expected_amount: float


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_name: str
    expected_amount: float
    status: str

    class Config:
        from_attributes = True

class OrderPaymentResponse(BaseModel):
    id: int
    amount: float
    transaction_id: str
    status: str
    payment_method: str
    order_id: int | None = None

    class Config:
        from_attributes = True