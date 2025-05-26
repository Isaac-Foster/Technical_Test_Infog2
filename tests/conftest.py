import pytest
from fastapi.testclient import TestClient

from src import app
from src.adapter.repository.user import UserRepo

@pytest.fixture
def app_context():
    yield TestClient(app)

@pytest.fixture
def auth_repo():
    return UserRepo() 


@pytest.fixture
def token(app_context):
    client = app_context
    response = client.post(
        '/auth/login',
        data={
            'username': 'email@gmail.com', 
            'password': 'P@55W0rld32@#'
        },
    )
    return response.json()['access_token']


@pytest.fixture
def token_commom(app_context):
    client = app_context
    response = client.post(
        '/auth/login',
        data={
            'username': 'email1@gmail.com', 
            'password': 'P@55W0rld32@#'
        },
    )
    return response.json()['access_token']