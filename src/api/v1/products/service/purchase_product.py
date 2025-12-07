import pickle
from datetime import datetime, timezone
from typing import Mapping, Any, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.products.dependencies import get_user, get_product
from api.v1.products.schemas import UserModel
from core.caching.client import redis
from core.config import settings
from core.db import get_async_session
from core.db.models import Product, User, Transaction, Inventory
from core.enums import ProductTypeEnum, TransactionStatusEnum
from core.exceptions.exceptions import UsersBalanceNotEnough, RepeatPurchaseOfPermanentProduct


async def execute_product_transaction(
        user: User,
        product: Product,
        session: AsyncSession,
):
    async with session.begin():
        user.balance -= product.price
        if user.balance < 0:
            raise UsersBalanceNotEnough()

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
                raise RepeatPurchaseOfPermanentProduct(product.id)
            else:
                product_in_inventory.quantity += 1
                product_in_inventory.purchased_at = datetime.now(timezone.utc)
        else:
            session.add(
                Inventory(
                    user=user,
                    product=product,
                    quantity=1,
                )
            )


async def handle_product_purchase(
        user: User = Depends(get_user),
        product: Product = Depends(get_product),
        session: AsyncSession = Depends(get_async_session),
) -> Transaction | None:
    error = None
    transaction = Transaction(user=user, product=product, amount=1)
    session.add(transaction)
    await session.commit()
    try:
        await execute_product_transaction(user, product, session)
    except Exception as e:
        transaction.status = TransactionStatusEnum.FAILED
        error = e
    else:
        transaction.status = TransactionStatusEnum.COMPLETED
    await session.commit()

    if error:
        raise error

    return transaction


async def caching_user_inventory(user_id: int, inventory: Sequence[Mapping[str, Any]]) -> None:
    key = f"{settings.cache.namespace.user_inventory}:{user_id}"
    await redis.set(key, pickle.dumps(inventory), 5 * 60)


async def get_user_inventory(user_id: int, session: AsyncSession) -> Sequence[Mapping[str, Any]]:
    stmt = select(Inventory.__table__).where(Inventory.user_id == user_id)
    response = await session.execute(stmt)
    await session.commit()
    return response.mappings().all()


async def purchase_product(
        body: UserModel,
        transaction: Transaction = Depends(handle_product_purchase),
        session: AsyncSession = Depends(get_async_session),
) -> Transaction:
    inventory = await get_user_inventory(body.user_id, session)
    await caching_user_inventory(body.user_id, inventory)
    return transaction
