from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String(255), unique=True, nullable=False)
    status = Column(String, nullable=False)
    payment_method = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_path = Column(String(500), nullable=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    user = relationship("User", back_populates="payments")
    order = relationship("Orders", back_populates="payments")