import pytest

def test_find_all(app_context, token):
    client = app_context
    response = client.get(
        '/products',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200, 'passed email invalid'
