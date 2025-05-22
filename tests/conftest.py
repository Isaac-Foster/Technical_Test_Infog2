import pytest
from fastapi.testclient import TestClient

from src import app

@pytest.fixture
async def app_context():
    yield TestClient(app)