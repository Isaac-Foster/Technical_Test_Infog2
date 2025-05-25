from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Query, Depends, HTTPException

from src.security import get_current_user
from src.adapter.repository.order import OrderRepo
from src.interfaces.schema.order import OrderCreateSchema
from src.infra.enums.order import OrderStatus
from src.infra.enums.user import RoleEnum

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/')
async def create(
    data: OrderCreateSchema,
    repository: Annotated[OrderRepo, Depends(OrderRepo)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    data = repository.create(data, current_user)
    return data


@router.get('/')
async def findall(
    start: Optional[str] = Query(
        None, description='Date start (ex: 01/05/2025)'
    ),
    end: Optional[str] = Query(None, description='Date end (ex: 20/05/2025)'),
    id: Optional[int] = Query(None, description='Order ID'),
    costumer_id: Optional[int] = Query(None, description=''),
    section: Optional[str] = Query(None, description='section products order'),
    status: Optional[OrderStatus] = Query(
        None, description='Status do pedido (ex: PENDING, PAID, CANCELED)'
    ),
    repository: OrderRepo = Depends(OrderRepo),
    current_user=Depends(get_current_user),
):
    if start:
        start = datetime.strptime(start, '%d/%m/%Y')
    if end:
        # finaliza o dia até 23h59
        end = datetime.strptime(end, '%d/%m/%Y')
        end = end.replace(hour=23, minute=59, second=59)

    data = repository.find_all(
        start=start,
        end=end,
        id=id,
        status=status,
    )

    return data


@router.get('/{id}')
async def find(
    id: int,
    repository: Annotated[OrderRepo, Depends(OrderRepo)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    return repository.find(id=id, customer_id=current_user.id)


@router.put('/{id}')
async def update(
    id: int,
    status: Optional[OrderStatus] = Query(
        None, description='Status do pedido'
    ),
    repository: OrderRepo = Depends(OrderRepo),
    current_user=Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=403, detail='Not enough permission.')
    if not status:
        return repository.find(id=id)
    try:
        status = OrderStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid status')

    return repository.update(id=id, status=status)


@router.delete('/{id}')
async def delete(
    id: int,
    repository: OrderRepo = Depends(OrderRepo),
    current_user=Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=403, detail='Not enough permission.')

    return repository.delete(id=id)
