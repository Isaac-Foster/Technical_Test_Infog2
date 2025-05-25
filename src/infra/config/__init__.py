from os import getenv
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    SECRET_KEY_JWT = getenv('SECRET_KEY_JWT')
    ALGORITHM_JWT = getenv('ALGORITHM_JWT')
    EXPIRATION_TIME_JWT = int(getenv('EXPIRATION_TIME_JWT'))
    DATABASE = getenv('DATABASE')
