from typing import Annotated

from fastapi import Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.products.dependencies import get_user
from core.db import get_async_session
from core.db.models import User, Inventory


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
