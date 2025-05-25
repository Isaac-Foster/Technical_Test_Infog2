from datetime import datetime

from pydantic import BaseModel


class ProductOrderSchema(BaseModel):
    id: int
    quantity: int


class OrderCreateSchema(BaseModel):
    items: list[ProductOrderSchema]


class ProductSchema(BaseModel):
    product_id: int
    price_unit: float
    quantity: int
    total: float

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int
    customer_name: str
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[ProductSchema]

    class Config:
        from_attributes = True
