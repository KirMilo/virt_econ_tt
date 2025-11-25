__all__ = (
    "users_router",
    "products_router",
    "analytics_router",
    "idempotency_router",
)

from .users.views import router as users_router
from .products.views import router as products_router
from .analytics.views import router as analytics_router
from .idempotency.views import router as idempotency_router
