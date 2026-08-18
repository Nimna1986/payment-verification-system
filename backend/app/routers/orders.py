from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.orders import Orders
from app.schemas.orders import OrderCreate, OrderResponse, OrderPaymentResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    last_order = (
        db.query(Orders)
        .order_by(Orders.id.desc())
        .first()
    )

    if last_order:
        next_number = last_order.id + 1
    else:
        next_number = 1

    order_number = f"ORD-{next_number:04d}"

    new_order = Orders(
        order_number=order_number,
        customer_name=order.customer_name,
        expected_amount=order.expected_amount,
        status="PENDING"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Orders).filter(Orders.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db)
):
    orders = db.query(Orders).all()
    return orders


@router.get(
    "/{order_id}/payments",
    response_model=list[OrderPaymentResponse]
)
def get_order_payments(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Orders).filter(Orders.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order.payments