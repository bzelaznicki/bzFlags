import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.conf import settings


@pytest.mark.django_db
def test_api_create_project():
    client = APIClient()
    res = client.post('/api/projects', data={
        'name': 'testproject'
    }, 
                      headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY}
                      , format='json')

    assert res.status_code == 201
    assert res.data['name'] == 'testproject'
    assert res.data['api_key']

@pytest.mark.django_db
def test_api_invalid_admin_key():
    client = APIClient()
    res = client.post(path='/api/projects', data={'name': 'testproject'}, 
                      headers={'X-Admin-Key': 'i-dont-know-what-a-key-is'},
                      format='json')

    assert res.status_code == 401
    
@pytest.mark.django_db
def test_api_admin_key_missing():
    client = APIClient()
    res = client.post(path='/api/projects', data={'name': 'testproject'}, 
                      format='json')

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_duplicate_project_name():
    project = baker.make('flags.Project')

    client = APIClient()
    res = client.post('/api/projects', data={
        'name': project.name,
    }, 
                      headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY},
                      format='json')

    assert res.status_code == 409
