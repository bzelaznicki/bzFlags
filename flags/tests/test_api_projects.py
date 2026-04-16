import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.mark.django_db
def test_api_create_project():
    client = APIClient()
    res = client.post('/api/projects', data={
        'name': 'testproject'
    })

    assert res.status_code == 201
    assert res.data['name'] == 'testproject'
    assert res.data['api_key']
