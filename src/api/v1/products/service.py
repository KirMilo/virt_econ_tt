import json
import pickle
from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.products.dependencies import get_user, get_product
from api.v1.products.schemas import UserModel
from core.caching.client import redis
from core.config import settings
from core.db import get_async_session
from core.db.models import Product, User, Transaction, Inventory
from core.enums import ProductTypeEnum, TransactionStatusEnum
from core.exceptions.exceptions import UsersBalanceNotEnough, TransactionError


async def execute_product_transaction(user: User, product: Product, session: AsyncSession):
    async with session.begin():
        user.balance -= product.price
        inventory_product = await session.execute(
            select(Inventory)
            .where(
                Inventory.user_id == user.id,
                Inventory.product_id == product.id
            )
        )
        product_in_inventory: Inventory = inventory_product.scalar_one_or_none()
        if product_in_inventory:
            if product.type == ProductTypeEnum.PERMANENT:
                raise TransactionError
            else:
                product_in_inventory.quantity += 1
        else:
            session.add(
                Inventory(
                    user=user,
                    product=product,
                    quantity=1,
                )
            )
        await session.flush()


async def purchase_product(
        user: User = Depends(get_user),
        product: Product = Depends(get_product),
        session: AsyncSession = Depends(get_async_session),
) -> Transaction | None:
    if user.balance < product.price:
        raise UsersBalanceNotEnough()

    transaction = Transaction(user=user, product=product, amount=1)
    session.add(transaction)
    await session.commit()
    try:
        await execute_product_transaction(user, product, session)
    except TransactionError:
        transaction.status = TransactionStatusEnum.FAILED
    else:
        transaction.status = TransactionStatusEnum.COMPLETED
    await session.commit()

    return transaction


async def caching_user_inventory(user_id: int, session: AsyncSession) -> None:
    stmt = select(Inventory.__table__).where(Inventory.user_id == user_id)
    response = await session.execute(stmt)
    inventory = response.mappings().all()
    key = f"{settings.cache.namespace.user_inventory}:{user_id}"
    await redis.set(key, pickle.dumps(inventory), 5 * 60)


async def handle_product_purchase(
        body: UserModel,
        transaction: Transaction = Depends(purchase_product),
        session: AsyncSession = Depends(get_async_session),
) -> Transaction:
    if transaction.status == TransactionStatusEnum.COMPLETED:
        await caching_user_inventory(body.user_id, session)
    return transaction


async def use_product(
        product_id: Annotated[int, Path(title="Product ID", ge=1)],
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
) -> Inventory:
    response = await session.execute(
        select(Inventory)
        .where(Inventory.user_id == user.id, Inventory.product_id == product_id)
    )
    product: Inventory | None = response.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail=f"User has no product {product_id} in inventory.")
    elif product.quantity is None:
        raise HTTPException(status_code=400, detail=f"Product {product_id} is not consumable.")
    elif product.quantity < 1:
        raise HTTPException(status_code=400, detail=f"Product {product_id} is not enough to use.")
    product.quantity -= 1
    await session.commit()
    return product
