from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from core.db.models import Transaction, Product
from core.enums import TransactionStatusEnum


async def get_most_popular_products(session: AsyncSession) -> Sequence[RowMapping]:
    stmt = (
        select(Product.__table__, count(1).label("purchases"))
        .select_from(Transaction)
        .join(Product, Transaction.product_id == Product.id)
        .where(
            Transaction.created_at > datetime.now() - timedelta(days=7),
            Transaction.status == TransactionStatusEnum.COMPLETED,
        )
        .group_by(Product.__table__)
        .order_by(count(1).desc())
        .limit(5)
    )
    response = await session.execute(stmt)
    result = response.mappings().all()
    return result
