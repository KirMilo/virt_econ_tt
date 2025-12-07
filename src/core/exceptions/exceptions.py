from fastapi import HTTPException, status


class TransactionError(Exception):
    pass


class ProductNotFound(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )


class UserNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )


class UsersBalanceNotEnough(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not enough balance",
        )


class RepeatPurchaseOfPermanentProduct(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already purchased permanent product {product_id}",
        )
