from typing import Annotated

from fastapi import APIRouter, Query
 
router = APIRouter(
    prefix='/clients',
    tags=[
        'clients'
    ]
)

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