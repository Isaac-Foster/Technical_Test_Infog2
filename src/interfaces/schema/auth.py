import re
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator
from email_validator import validate_email, EmailNotValidError

from src.infra.enums.user import RoleEnum
from src.interfaces.validator import is_valid_document


class UserRegisterSchema(BaseModel):
    name: Annotated[
        str,
        Field(
            default='Luan Edson Sebastião Costa',
            description='your complete name',
            min_length=3,
            max_length=255,
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(default='email@gmail.com', description='email', max_length=256),
    ]

    password: Annotated[
        str,
        Field(
            default='P@55W0rld32@#',
            description='your strong password',
            min_length=8,
            max_length=256,
        ),
    ]

    document: Annotated[
        str,
        Field(
            default='805.456.630-16',
            description='your document',
            min_length=11,
            max_length=14,
            pattern=r'\d{3}(.)?\d{3}(.)?\d{3}(.)?\d{2}',
        ),
    ]

    roles: Annotated[
        Optional[list[RoleEnum]],
        Field(
            default=[RoleEnum.USER], 
            description='rule applied to the user [ADMIN, USER]',
        ),
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
    def clean_document_validate(cls, values):
        document = values.get('document')
        # Limpeza do CPF
        cleaned_document = re.sub(r'\D', '', document)
        values['document'] = cleaned_document

        # Validação do CPF
        if not is_valid_document(cleaned_document):
            raise ValueError('document invalid.')

        return values

    class Config:
        from_attributes = True


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    roles: list[RoleEnum]

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            default='email@gmail.com',
            description='email',
            max_length=256,
        ),
    ]
    password: Annotated[
        str,
        Field(
            default='P@55W0rld32@#',
            description='senha',
            min_length=8,
            max_length=256,
        ),
    ]

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Annotated[
        str,
        Field(
            default='your name',
            description='your complete name',
            min_length=3,
            max_length=255,
        ),
    ]

    password: Annotated[
        str,
        Field(
            default='P@55W0rld32@#',
            description='senha',
            min_length=8,
            max_length=256,
        ),
    ]

    roles: Annotated[
        Optional[list[RoleEnum]],
        Field(
            default=[RoleEnum.USER],
            description='rule applied to the user [ADMIN, USER]',
        ),
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

    class Config:
        from_attributes = True


responses_register = {
    201: {
        'model': UserPublicSchema,
        'description': 'User created',
    },
}
