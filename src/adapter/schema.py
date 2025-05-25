from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageIn(BaseModel):
    name: str
    image: str


class ImageOut(BaseModel):
    id: int
    name: str
    image: str
    product_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
