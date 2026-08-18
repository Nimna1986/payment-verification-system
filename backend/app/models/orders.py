from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database.base import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    expected_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")

    payments = relationship(
        "Payments",
        back_populates="order"
    )