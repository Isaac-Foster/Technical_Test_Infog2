from src.infra.database.sql import Session
from src.infra.models.user import UserModel

from src.ports.public import IUBaseRepoPort


class UserRepo(IUBaseRepoPort):
    ...