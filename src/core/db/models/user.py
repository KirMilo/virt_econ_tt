from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .inventory import Inventory
    from .transaction import Transaction


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    inventories: Mapped[list["Inventory"]] = relationship(
        back_populates="user",
        uselist=True,
    )  # one-to-many
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user",
        uselist=True,
    )  # one-to-many
