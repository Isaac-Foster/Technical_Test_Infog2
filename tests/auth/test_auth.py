import pytest

def test_existis_router(app_context):
    client = app_context
    response = client.get('/')
    assert response.status_code == 200, 'endpoint not found'


def test_create_user(app_context):
    client = app_context
    response = client.post(
        '/auth/register',
        json={
            "name": "your name",
            "email": "retest@gmail.com",
            "password": "P@55W0rld32@#",
            "document": "986.309.100-62",
            "roles": [
                "USER"
            ]
        },
    )

    assert response.status_code == 200, 'login failed'

def test_jwt_token(app_context):
    client = app_context
    response = client.post(
        '/auth/login',
        data={
            'username': 'retest@gmail.com',
            'password': 'P@55W0rld32@#',
        },
    )

    
    assert response.status_code == 200, 'login failed'

def test_login(app_context,  auth_repo):
    client = app_context
    response = client.post(
        '/auth/login',
        data={
            'username': 'retest@gmail.com',
            'password': 'P@55W0rld32@#',
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    deleted = auth_repo.delete(email='retest@gmail.com')
    assert response.status_code == 200, 'login failed'
    assert deleted is True, 'user not deleted'