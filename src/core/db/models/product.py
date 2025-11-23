from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enums import ProductTypeEnum
from .base import Base

if TYPE_CHECKING:
    from .transaction import Transaction
    from .inventory import Inventory


class Product(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int]
    type: Mapped[ProductTypeEnum] = mapped_column(SQLAlchemyEnum(ProductTypeEnum))
    is_active: Mapped[bool] = mapped_column(default=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="product",
        uselist=True,
    )
    inventories: Mapped[list["Inventory"]] = relationship(
        back_populates="product",
        uselist=True,
    )
