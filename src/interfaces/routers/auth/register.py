from fastapi import APIRouter, Depends

from src.adapter.controllers.user import UserController
from src.interfaces.schema.auth import UserRegisterSchema, responses_register

router = APIRouter(
    prefix='/auth',
    tags=[
        'auth',
    ],
)


@router.post('/register', responses=responses_register)
async def register(
    data: UserRegisterSchema,
    controller: UserController = Depends(UserController),
):
    data = controller.create(data)
    return data
