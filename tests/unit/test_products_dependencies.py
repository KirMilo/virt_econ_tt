import pytest
from fastapi import HTTPException, status

from api.v1.products.dependencies import get_product, get_user
from api.v1.products.schemas import UserModel
from core.exceptions.exceptions import ProductNotFound, UserNotFound


@pytest.mark.asyncio(loop_scope="session")
async def test_get_existent_product(db_session):
    product_id = 1
    product = await get_product(
        product_id=product_id,
        session=db_session,
    )
    assert product is not None
    assert product.id == product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_product(db_session):
    product_id = 10000
    with pytest.raises(HTTPException) as exc:
        await get_product(
            product_id=product_id,
            session=db_session,
        )
    assert exc.type is ProductNotFound
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == f"Product {product_id} not found"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_existent_user(db_session):
    user_id = 1
    user = await get_user(
        UserModel(user_id=user_id),
        session=db_session
    )
    assert user is not None
    assert user.id == user_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existent_user(db_session):
    user_id = 10000
    with pytest.raises(HTTPException) as exc:
        await get_user(
            UserModel(user_id=user_id),
            session=db_session,
        )
    assert exc.type is UserNotFound
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == f"User {user_id} not found"
