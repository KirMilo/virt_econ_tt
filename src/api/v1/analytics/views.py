from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.analytics.schemas import PopularProductModel
from api.v1.analytics.service import get_most_popular_products
from core.config import settings
from core.db import get_async_session
from utils.custom_key_builder import custom_key_builder

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/popular-products", response_model=list[PopularProductModel])
@cache(
    expire=60 * 60,
    key_builder=custom_key_builder,  # noqa
    namespace=settings.cache.namespace.analytics,
)
async def get_popular_products(
        session: AsyncSession = Depends(get_async_session),
) -> list[PopularProductModel]:
    """Топ-5 товаров по количеству покупок за последние 7 дней Кэшировать на 1 час"""
    products = await get_most_popular_products(session)
    return [PopularProductModel.model_validate(product) for product in products]
