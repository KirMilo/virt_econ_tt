from fastapi import APIRouter

from .schemas import HealthcheckStatusModel

router = APIRouter()


@router.get("/healthcheck", response_model=HealthcheckStatusModel)
async def healthcheck() -> HealthcheckStatusModel:
    return HealthcheckStatusModel()
