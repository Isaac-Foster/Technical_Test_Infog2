from fastapi import FastAPI

from src.infra.models import init_sql
from src.interfaces.routers import configure_app

app = FastAPI()

init_sql()
configure_app(app=app)
