from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enums import TransactionStatusEnum
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .product import Product


class Transaction(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    amount: Mapped[int] = mapped_column(default=1)
    status: Mapped[TransactionStatusEnum] = mapped_column(
        SQLAlchemyEnum(TransactionStatusEnum),
        default=TransactionStatusEnum.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(back_populates="transactions")  # many-to-one
    product: Mapped["Product"] = relationship(back_populates="transactions")  # many-to-one
