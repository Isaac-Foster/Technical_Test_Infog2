from fastapi import HTTPException

from src.core.domain.user import UserDomain
from src.adapter.repository.client import ClientRepo

from src.interfaces.schema.client import (
    ClientRegisterSchema,
)


class ClientController:
    def __init__(self):
        self.domain = UserDomain()
        self.repo = ClientRepo()

    def create(self, data: ClientRegisterSchema):
        data = self.repo.create(data)

        if type(data) is Exception:
            raise HTTPException(
                status_code=409,
                detail=str(data),
            )
        return data
