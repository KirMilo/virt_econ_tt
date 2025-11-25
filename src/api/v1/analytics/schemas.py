from pydantic import BaseModel, ConfigDict

from core.enums import ProductTypeEnum


class PopularProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: ProductTypeEnum
    purchases: int
