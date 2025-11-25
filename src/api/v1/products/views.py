from typing import Annotated

from fastapi import APIRouter, Depends, Path

from api.v1.products.schemas import TransactionModel, InventoryModel
from api.v1.products.service import handle_product_purchase, use_product

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/{product_id}/purchase", response_model=TransactionModel)
async def post_purchase_product(
        transaction: TransactionModel = Depends(handle_product_purchase),
) -> TransactionModel:
    """
    Покупка товара.
    1. Проверка, что товар существует
    2. Проверка баланса пользователя 
    3. Создание транзакции с pending статусом
    4. Транзакция в БД: списание средств, запись в инвентарь, запись транзакции со статусом completed иначе failed
    5. Для consumable товаров увеличивать quantity, для permanent — проверять дубликаты
    6. Кэшировать инвентарь пользователя на 5 минут
    """
    return transaction


@router.post("/{product_id}/use", response_model=InventoryModel)
async def post_use_product(
        product: InventoryModel = Depends(use_product),
) -> InventoryModel:
    """Использование consumable товара
    Проверка, что товар доступен у пользователя
    Уменьшение quantity в инвентаре
    """
    return product
