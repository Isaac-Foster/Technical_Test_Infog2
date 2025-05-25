from fastapi import HTTPException

from src.core.domain.user import UserDomain
from src.adapter.repository.user import UserRepo
from src.security import hash_manager, jwt_manager
from src.interfaces.schema.token import Token
from src.interfaces.schema.auth import (
    UserRegisterSchema,
    UserLoginSchema,
    UserPublicSchema,
)


class UserController:
    def __init__(self):
        self.domain = UserDomain()
        self.repo = UserRepo()

    def create(self, data: UserRegisterSchema):
        self.domain.strong_password(data.password)

        if self.domain.strong_password(data.password) is not True:
            raise HTTPException(
                status_code=400,
                detail=str(data),
            )

        data.password = hash_manager.hash(data)
        data = self.repo.create(data)

        if type(data) is Exception:
            raise HTTPException(
                status_code=409,
                detail=str(data),
            )
        return UserPublicSchema(**data.__dict__)

    def auth(self, credential: UserLoginSchema):
        user = self.repo.find(email=credential.email)
        authenticate = False

        if user:
            authenticate = hash_manager.check(
                credential.password, user.password
            )

        if user is None or authenticate is False:
            raise HTTPException(
                status_code=401,
                detail='Username or password incorrect',
            )

        token = jwt_manager.create(dict(sub=credential.email))
        return Token(access_token=token, type_token='Bearer')

    def refresh(self, model):
        token = jwt_manager.create(dict(sub=model.email))
        return Token(access_token=token, type_token='Bearer')
