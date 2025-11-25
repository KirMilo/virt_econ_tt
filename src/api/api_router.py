from fastapi import APIRouter
from .v1 import users_router, products_router, analytics_router, idempotency_router

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(users_router)
router_v1.include_router(products_router)
router_v1.include_router(analytics_router)
router_v1.include_router(idempotency_router)
