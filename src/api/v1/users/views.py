from typing import Annotated

from fastapi import APIRouter, Depends, Path

from api.v1.users.schemas import AddFundsResponseModel, UserInventoryResponseModel, UserInventoryModel
from api.v1.users.service import add_funds, get_user_inventory


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/{user_id}/add-funds")
async def post_add_funds(response: AddFundsResponseModel = Depends(add_funds)):
    """Пополнение баланса"""
    return response


@router.get("/{user_id}/inventory", response_model=UserInventoryResponseModel)
async def get_inventory(
        user_id: Annotated[int, Path(ge=1, title="User id")],
        inventory: UserInventoryModel = Depends(get_user_inventory)
) -> UserInventoryResponseModel:
    """Получение инвентаря"""
    return UserInventoryResponseModel(user_id=user_id, inventory=inventory)
