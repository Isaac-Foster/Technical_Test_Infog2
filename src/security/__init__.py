from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from zoneinfo import ZoneInfo

from jwt import encode, decode
from src.infra.config import Config
from src.adapter.repository.user import UserRepo

o2auth_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


class HashManager:
    def __init__(self):
        pass

    def hash(self, data) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data.password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf8'), password_hash.encode('utf8')
        )


class JWTManager:
    def __init__(self):
        pass

    def create(self, data: dict) -> str:
        to_encode = data.copy()

        to_encode.update(
            {
                'exp': datetime.now(tz=ZoneInfo('UTC'))
                + timedelta(minutes=Config.EXPIRATION_TIME_JWT)
            }
        )

        token = encode(
            to_encode, Config.SECRET_KEY_JWT, algorithm=Config.ALGORITHM_JWT
        )
        return token

    def validate(self, token: str) -> dict:
        data = decode(
            token, Config.SECRET_KEY_JWT, algorithms=[Config.ALGORITHM_JWT]
        )
        return data


jwt_manager = JWTManager()
hash_manager = HashManager()


def get_current_user(token: str = Depends(o2auth_schema)):
    try:
        payload = jwt_manager.validate(token)
        email = payload.get('sub')
        if not email:
            raise HTTPException(status_code=401, detail='Invalid credentials')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=str(e))

    repository = UserRepo()
    user = repository.find(email=email)

    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return user
