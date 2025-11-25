from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.products.schemas import UserModel
from core.db import get_async_session
from core.db.models import Product, User
from core.exceptions.exceptions import ProductNotFound, UserNotFound


async def get_product(
        product_id: Annotated[int, Path(title="Product ID", ge=1)],
        session: AsyncSession = Depends(get_async_session),
) -> Product:
    product: Product | None = await session.get(Product, product_id)
    if product:
        return product
    raise ProductNotFound(product_id)



async def get_user(
        body: UserModel,
        session: AsyncSession = Depends(get_async_session),
) -> User:
    user: User | None = await session.get(User, body.user_id)
    if user:
        return user
    raise UserNotFound(body.user_id)