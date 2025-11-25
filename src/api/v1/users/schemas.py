import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Header, Body, Path
from pydantic import BaseModel, field_validator, Field, ConfigDict


class InventoryModel(BaseModel):
    product_id: int
    purchased_at: datetime | None


class ConsumableItemsGroupedByQuantityModel(BaseModel):
    quantity: int
    products: list[InventoryModel]


class UserInventoryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    permanent: list[InventoryModel]
    consumable: list[ConsumableItemsGroupedByQuantityModel]


class UserInventoryResponseModel(BaseModel):
    user_id: int
    inventory: UserInventoryModel


class AddFundsBodyModel(BaseModel):
    amount: Annotated[int, Body(ge=1, title="Amount to add")]


class AddFundsModel(AddFundsBodyModel):
    idempotency_key: Annotated[uuid.UUID | str, Header(alias="Idempotency-Key")]
    user_id: Annotated[int, Path(ge=1, title="User ID")]

    @field_validator("idempotency_key", mode="after")
    def idempotency_key_to_str(cls, v: uuid.UUID) -> str:
        return str(v)


class AddFundsResponseModel(BaseModel):
    message: str = "Payment successfully processed."
    amount: int
    idempotency_key: str
    created_at: datetime = Field(default_factory=datetime.now)
