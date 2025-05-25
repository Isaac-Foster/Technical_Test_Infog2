from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Annotated

from pydantic import BaseModel, Field

from src.adapter.schema import ImageOut


class ProducCreatetSchema(BaseModel):
    name: Annotated[str, Field(default='', description='product name')]
    price: Annotated[
        Decimal,
        Field(
            description='product price',
            ge=Decimal('0.01'),
        ),
    ]
    barcode: Annotated[
        str,
        Field(
            default='',
            description='product barcode',
            max_length=20,
        ),
    ]
    section: Annotated[
        str,
        Field(
            default='',
            description='product section',
            max_length=255,
        ),
    ]
    stock: Annotated[
        int,
        Field(
            default=0,
            description='your stock product',
            ge=0,
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(
            default=None,
            description='product description',
            max_length=512,
        ),
    ]
    expiration_date: Annotated[
        Optional[date | None],
        Field(
            default=None,
            description='expiration date (YYYY-MM-DD)',
        ),
    ]

    """ images: Annotated[
        Optional[list[UploadFile]],
        Field(
            default=[],
            description='product images',
        ),
    ] """


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    barcode: str
    section: str
    stock: int
    description: str
    expiration_date: date | None
    disponibility: bool
    created_at: datetime
    updated_at: datetime
    images: list[ImageOut]  # <-- tem que estar declarado!

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field
from typing import Optional, Annotated
from decimal import Decimal
from datetime import date


class ProductUpdateSchema(BaseModel):
    name: Annotated[
        Optional[str],
        Field(default=None, description='product name')
    ]
    price: Annotated[
        Optional[Decimal],
        Field(
            default=None,
            description='product price',
            ge=Decimal('0.01'),
        ),
    ]
    barcode: Annotated[
        Optional[str],
        Field(
            default=None,
            description='product barcode',
            max_length=20,
        ),
    ]
    section: Annotated[
        Optional[str],
        Field(
            default=None,
            description='product section',
            max_length=255,
        ),
    ]
    stock: Annotated[
        Optional[int],
        Field(
            default=None,
            description='your stock product',
            ge=0,
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(
            default=None,
            description='product description',
            max_length=512,
        ),
    ]
    expiration_date: Annotated[
        Optional[date],
        Field(
            default=None,
            description='expiration date (YYYY-MM-DD)',
        ),
    ]
