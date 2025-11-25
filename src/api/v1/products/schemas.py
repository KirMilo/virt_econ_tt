from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, ConfigDict

from core.enums import TransactionStatusEnum


class UserModel(BaseModel):
    user_id: Annotated[int, Body(title="User ID", ge=1)]


class TransactionModel(BaseModel):
    user_id: int
    product_id: int
    amount: int
    status: TransactionStatusEnum


class InventoryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
