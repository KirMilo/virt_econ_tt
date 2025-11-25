from functools import wraps
from typing import Annotated, Sequence
from itertools import groupby

from fastapi import Depends, Path
from sqlalchemy import select, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.db.models import User, Inventory
from core.exceptions.exceptions import UserNotFound
from .dependencies import get_user_inventory_from_cache, add_funds_payload
from .schemas import AddFundsModel, AddFundsResponseModel
from .utils.caching_transaction import CachingTransaction


async def execute_transaction(
        user_id: int,
        amount: int,
        session: AsyncSession,
        **kwargs,  # NOQA
) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise UserNotFound(user_id)
    user.balance += amount
    await session.commit()


async def add_funds(
        payload: AddFundsModel = Depends(add_funds_payload),
        session: AsyncSession = Depends(get_async_session),
) -> AddFundsResponseModel:
    caching_transaction = CachingTransaction(**payload.model_dump())
    from_cache = await caching_transaction.get_value()
    if from_cache:
        return from_cache

    await execute_transaction(**payload.model_dump(), session=session)

    response = AddFundsResponseModel(**payload.model_dump())
    await caching_transaction.set_value(response)
    return response


def group_by_quantity(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        inventory = await func(*args, **kwargs)

        consumable = []
        permanent = []
        for item in inventory:
            if item["quantity"]:
                consumable.append(item)
            else:
                permanent.append(item)

        consumable = [
            {"quantity": quantity, "products": list(products)}
            for quantity, products in groupby(consumable, key=lambda q: q["quantity"])
        ]

        return {"consumable": consumable, "permanent": permanent}

    return wrapper


@group_by_quantity
async def get_user_inventory(
        user_id: Annotated[int, Path(ge=1, title="User id")],
        from_cache: Sequence[RowMapping] | None = Depends(get_user_inventory_from_cache),
        session: AsyncSession = Depends(get_async_session),
) -> Sequence[RowMapping]:
    if from_cache:
        return from_cache
    response = await session.execute(
        select(Inventory.__table__).where(Inventory.user_id == user_id)
    )
    inventory = response.mappings().all()
    return inventory
