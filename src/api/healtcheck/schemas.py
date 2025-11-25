from pydantic import BaseModel


class HealthcheckStatusModel(BaseModel):
    status: str = "ok"
