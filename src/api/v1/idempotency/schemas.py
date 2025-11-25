import uuid

from pydantic import BaseModel, Field


class IdempotencyKeyModel(BaseModel):
    idempotency_key: uuid.UUID | str = Field(default_factory=uuid.uuid4)
