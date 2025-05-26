from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.security import get_current_user
from src.interfaces.schema.auth import UserLoginSchema
from src.adapter.controllers.user import UserController


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
async def login(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        data = UserLoginSchema(
            email=form_data.username, 
            password=form_data.password
        )
    except Exception as e:
        return Response(
            status_code=422,
            content=str({'message': str(e)}),
            media_type='application/json',
        )

    result = UserController().auth(data)

    if type(result) is Response:
        return result

    response.set_cookie(
        key='access_token',
        value=f'Bearer {result.access_token}',
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60 * 30,
    )
    return JSONResponse(status_code=200, content=result.dict())


@router.post('/refresh-token')
async def refresh(
    controller: UserController = Depends(UserController),
    current_user: str = Depends(get_current_user),
):
    response = controller.refresh(current_user)
    return response
