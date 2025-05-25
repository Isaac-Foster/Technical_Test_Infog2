from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(description='access token')
    type_token: str = Field(description='type token')
