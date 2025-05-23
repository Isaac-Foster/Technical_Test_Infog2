from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description='token de acesso')
    type_token: str = Field(description='token de acesso')