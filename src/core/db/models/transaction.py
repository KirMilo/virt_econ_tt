from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enums import TransactionStatusEnum
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .product import Product


class Transaction(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    amount: Mapped[int] = mapped_column
    status: Mapped[TransactionStatusEnum] = mapped_column(SQLAlchemyEnum(TransactionStatusEnum))

    user: Mapped["User"] = relationship(back_populates="transactions")  # many-to-one
    product: Mapped["Product"] = relationship(back_populates="transactions")  # many-to-one
