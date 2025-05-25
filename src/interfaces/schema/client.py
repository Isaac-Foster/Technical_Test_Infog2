import re
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator
from email_validator import validate_email, EmailNotValidError

from src.interfaces.validator import is_valid_document


class ClientRegisterSchema(BaseModel):
    name: Annotated[
        str,
        Field(
            default='your name',
            description='seu nome',
            min_length=3,
            max_length=255,
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(default='email@gmail.com', description='email', max_length=256),
    ]

    """ password: Annotated[
        str,
        Field(
            default='P@55W0rld32@#',
            description='senha',
            min_length=8,
            max_length=256,
        ),
    ] """

    document: Annotated[
        str,
        Field(
            default='635.916.840-58',
            description='cpf',
            min_length=11,
            max_length=14,
            pattern=r'\d{3}(.)?\d{3}(.)?\d{3}(.)?\d{2}',
        ),
    ]

    """ roles: Annotated[
        Optional[list[RoleEnum]],
        Field(
            default=[RoleEnum.USER], description='regra aplicada ao usuário'
        ),
    ] """

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


class ClientPublicSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ClientUpdateSchema(BaseModel):
    name: Annotated[
        Optional[str | None],
        Field(
            default=None, description='your name', min_length=3, max_length=255
        ),
    ] = None
    email: Annotated[
        Optional[str | None],
        Field(default=None, description='email', max_length=256),
    ] = None
    document: Annotated[
        Optional[str | None],
        Field(
            default=None,
            description='your document -> cpf',
            min_length=11,
            max_length=14,
            pattern=r'\d{3}(.)?\d{3}(.)?\d{3}(.)?\d{2}',
        ),
    ] = None

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
        if not document:
            return values
        # Limpeza do CPF
        cleaned_document = re.sub(r'\D', '', document)
        values['document'] = cleaned_document

        # Validação do CPF
        if not is_valid_document(cleaned_document):
            raise ValueError('document invalid.')

        return values

    class Config:
        from_attributes = True
