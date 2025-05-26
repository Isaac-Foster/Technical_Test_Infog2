import pytest


def test_create_client(app_context, token):
    client = app_context
    response = client.post(
        '/clients',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "name": "yran van der graaf",
            "email": "retest@gmail.com",
            "document": "986.309.100-62",
        },
    )

    assert response.status_code == 200, 'failed to create client'


def test_create_client_invalid_email(app_context, token_commom):
    client = app_context
    response = client.post(
        '/clients',
        headers={'Authorization': f'Bearer {token_commom}'},
        json={
            "name": "yran van der graaf",
            "email": "retestemail.com",
            "document": "566.204.840-18",
        },
    )

    assert response.status_code == 422, 'passed email invalid'


def test_create_client_invalid_doc(app_context, token):
    client = app_context
    response = client.post(
        '/clients',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "name": "yran van der graaf",
            "email": "retest@gmail.com",
            "document": "566.204.890-18",
        },
    )

    assert response.status_code == 422, 'passed doc invalid'



def test_create_client_not_auth(app_context, token):
    client = app_context
    response = client.post(
        '/clients',
        json={
            "name": "yran van der graaf",
            "email": "retest@gmail.com",
            "document": "986.309.100-62",
        },
    )

    assert response.status_code == 401, 'you authorized'


def test_create_client_not_permission(app_context, token_commom):
    client = app_context
    response = client.post(
        '/clients',
        headers={'Authorization': f'Bearer {token_commom}'},
        json={
            "name": "yran van der graaf",
            "email": "retesasdt@gmail.com",
            "document": "566.204.840-18",
        },
    )

    assert response.status_code == 400, 'you have permission'

