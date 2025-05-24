from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException

from src.security import get_current_user
from src.infra.enums.user import RoleEnum
from src.infra.models.user import UserModel
from src.adapter.controllers.client import ClientController
from src.interfaces.schema.client import (
    ClientRegisterSchema,
    ClientUpdateSchema,
)

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/')
async def create(
    data: ClientRegisterSchema,
    controller: ClientController = Depends(ClientController),
    current_user: UserModel = Depends(get_current_user),
):
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return controller.create(data)


@router.get('/')
async def find_all(
    page: Annotated[int | None, Query(description='pagina atual')] = None,
    limit: Annotated[
        int | None, Query(description='quantidade de itens por pagina')
    ] = None,
    name: Annotated[int | None, Query(description='filtro por nome')] = None,
    email: Annotated[int | None, Query(description='filtro por email')] = None,
    controller: ClientController = Depends(ClientController),
    current_user: UserModel = Depends(get_current_user),
):  # noqa E501
    if RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')
    return controller.repo.find_all(
        page=page, limit=limit, name=name, email=email
    )


@router.get('/{id}')
async def find(
    id: int,
    controller: ClientController = Depends(ClientController),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != id and RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return controller.repo.find(id=id)


@router.put('/{id}')
async def update(
    id: int,
    update: ClientUpdateSchema,
    controller: ClientController = Depends(ClientController),
    current_user: UserModel = Depends(get_current_user),
    ):
    if current_user.id != id and RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return controller.repo.update(id=id, data=update)


@router.delete('/{id}')
async def delete(
    id: int, 
    controller: ClientController = Depends(ClientController),
    current_user: UserModel = Depends(get_current_user)):
    if current_user.id != id and RoleEnum.ADMIN not in current_user.roles:
        raise HTTPException(status_code=400, detail='Not enough permission')

    return controller.repo.delete(id=id)
