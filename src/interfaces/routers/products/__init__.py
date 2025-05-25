from typing import Optional, Annotated, Union
from datetime import date
from decimal import Decimal

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    Query,
    HTTPException,
)

from src.adapter.schema import ImageIn
from src.security import get_current_user  # noqa
from src.infra.models.user import UserModel  # noqa
from src.interfaces.schema.product import (
    ProducCreatetSchema,
    ProductUpdateSchema,
)
from src.adapter.repository.product import ProductRepo
from src.infra.enums.user import RoleEnum


router = APIRouter(prefix='/products', tags=['products'])


@router.post('/')
async def create(
    name: Annotated[str, Form(max_length=255, description='Product name')],
    price: Decimal = Form(
        ge=Decimal('0.01'),
        default=Decimal('0.01'),
        description='Product price',
    ),
    barcode: str = Form(default='', description='Product barcode'),
    section: str = Form(default='', description='Product section'),
    stock: int = Form(default=0, description='Product stock'),
    description: Optional[str] = Form(
        default=None, description='Product description'
    ),
    expiration_date: Optional[date | str] = Form(
        default=None, description='Expiration date (YYYY-MM-DD)'
    ),
    names: Optional[list[str]] = Form(
        default=[], description='Comma-separated names for images'
    ),
    images: Union[list[bytes | UploadFile], str] = File(
        None, description='Product images'
    ),
    repository: ProductRepo = Depends(ProductRepo),
    current_user: UserModel = Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    # verificando se existe nome de imagens ou veio vazio
    names = [i for i in names[0].split(',') if i]

    # verificando se existe imagens ou veio vazio
    if not images[0] or all(isinstance(i, UploadFile) for i in images):
        images = []  # noqa
    elif any(isinstance(i, UploadFile) for i in images):
        return

    # verificando se o numero de nomes é igual ao numero de imagens
    if len(images) != len(names):
        return {'error': 'Número de nomes não corresponde ao número de images'}
    # tratando erro default de expiration_date
    if not expiration_date:
        expiration_date = None  # noqa

    data = ProducCreatetSchema(
        name=name,
        price=price,
        barcode=barcode,
        section=section,
        stock=stock,
        description=description,
        expiration_date=expiration_date,
        # images=image_files
    )

    images = [
        ImageIn(name=name, image=image.filename)
        for name, image in zip(names, images)
    ]

    return repository.create(data, images)


@router.get('/')
async def find_all(
    page: Annotated[int | None, Query(description='pagina atual')] = None,
    limit: Annotated[
        int | None, Query(description='quantidade de itens por pagina')
    ] = None,
    section: Annotated[str, Query(description='filter for section')] = None,
    price: Annotated[float, Query(description='filter for section')] = None,
    disponibility: Annotated[
        bool, Query(description='fiter fir disponibility')
    ] = None,
    repository: ProductRepo = Depends(ProductRepo),
    current_user: UserModel = Depends(get_current_user),
):
    return repository.find_all(
        page=page,
        limit=limit,
        section=section,
        price=price,
        disponibility=disponibility,
    )


@router.get('/{id}')
async def find(
    id: int,
    repository: ProductRepo = Depends(ProductRepo),
    current_user: UserModel = Depends(get_current_user),
):
    return repository.find(id=id)


@router.put('/{id}')
async def update(
    id: int,
    update: ProductUpdateSchema,
    repository: ProductRepo = Depends(ProductRepo),
    current_user: UserModel = Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return repository.update(id, **update.dict())


@router.delete('/{id}')
async def delete(
    id: int,
    repository: ProductRepo = Depends(ProductRepo),
    current_user: UserModel = Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return repository.delete(id=id)
