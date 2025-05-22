import re
from typing import Annotated, Optional

from fastapi import Body
from pydantic import BaseModel, EmailStr, Field, root_validator
from email_validator import validate_email, EmailNotValidError

from src.infra.enums.user import RoleEnum


class UserRegisterSchema(BaseModel):
    name: Annotated[
    str,
    Field(
        default='your name',
        description='seu nome',
        min_length=3,
        max_length=255,
    )
    ]

    email: Annotated[EmailStr, Field(description='email', max_length=256)]
    password: Annotated[
        str,
        Field(
            default='P@55W0rld32@#',
            description='senha',
            min_length=8,
            max_length=256,
        ),
    ]

    document: Annotated[
        str,
        Field(
            default='123.123.123-08',
            description='cpf',
            min_length=11,
            max_length=14,
            pattern=r'\d{3}(.)?\d{3}(.)?\d{3}(.)?\d{2}'

        ),
    ]

    roles: Annotated[
        Optional[list[RoleEnum]],
        Field(
            default=[RoleEnum.CLIENT],
            description='regra aplicada ao usuário'
            )
        ]

    @root_validator(pre=True)
    def validate_email(cls, values):
        email = values.get('email')
        if email:
            try:
                validate_email(email)
            except EmailNotValidError as e:
                raise ValueError(f'Email inválido: {e}')
            except Exception as e:
                raise ValueError(f'error {e}')
        return values

    @root_validator(pre=True)
    def clean_document(cls, values):
        document = values.get('document')
        cleaned_document = re.sub(r'\D', '', document)
        values['document'] = cleaned_document
        return values