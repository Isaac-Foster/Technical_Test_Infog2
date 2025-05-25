from typing import Annotated  # noqa

from fastapi import APIRouter, Query  # noqa

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/')
async def create():
    return {}


@router.get('/{id}')
async def find(id: int):
    return {}


@router.put('/{id}')
async def update(id: int):
    return {}


@router.delete('/{id}')
async def delete(id: int):
    return {}
