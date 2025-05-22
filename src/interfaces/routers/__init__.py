from fastapi import FastAPI

from src.interfaces.routers import auth, clients, products, orders #noqa
from src.interfaces.routers.auth import register #noqa

def configure_app(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(register.router)
    app.include_router(products.router)
    app.include_router(orders.router)
    app.include_router(clients.router)