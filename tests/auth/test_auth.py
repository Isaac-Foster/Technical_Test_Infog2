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
    assert isinstance(deleted, auth_repo.public), 'user not deleted'

def test_login_error(app_context,  auth_repo):
    client = app_context
    response = client.post(
        '/auth/login',
        data={
            'username': 'retesta@gmail.com',
            'password': 'P@55W0rld32@#',
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 401, 'login error failed'


def test_create_user_error_doc(app_context):
    client = app_context
    response = client.post(
        '/auth/register',
        json={
            "name": "your name",
            "email": "retest@gmail.com",
            "password": "P@55W0rld32@#",
            "document": "986.309.100-67",
            "roles": [
                "USER"
            ]
        },
    )

    assert response.status_code == 422, 'failed to create user'

def test_create_user_error_email(app_context):
    client = app_context
    response = client.post(
        '/auth/register',
        json={
            "name": "your name",
            "email": "retest@email.com",
            "password": "P@55W0rld32@#",
            "document": "986.309.100-67",
            "roles": [
                "USER"
            ]
        },
    )

    assert response.status_code == 422, 'failed to create user'


def test_create_user_error_password(app_context):
    client = app_context
    response = client.post(
        '/auth/register',
        json={
            "name": "your name",
            "email": "retest@email.com",
            "password": "senhafraca",
            "document": "986.309.100-67",
            "roles": [
                "USER"
            ]
        },
    )

    assert response.status_code == 422, 'failed to create user'