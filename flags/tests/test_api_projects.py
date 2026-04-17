import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.conf import settings
import uuid


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


@pytest.mark.django_db
def test_api_get_list_of_projects():
    for _ in range(5):
        baker.make('flags.Project')

    client = APIClient()
    res = client.get(
                    path='/api/projects',
                    headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY},
                    )

    assert res.status_code == 200
    assert len(res.data) == 5

@pytest.mark.django_db
def test_api_empty_list_of_projects():
    client = APIClient()
    res = client.get('/api/projects',
                     headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY},
                     )
    assert res.status_code == 200
    assert res.data == []

@pytest.mark.django_db
def test_api_get_projects_invalid_admin_key():
    client = APIClient()
    res = client.get('/api/projects', 
                     headers={'X-Admin-Key': 'this-is-not-my-admin-key'}
                     )

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_get_projects_missing_admin_key():
    client = APIClient()
    res = client.get('/api/projects')

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_get_single_project():
    project = baker.make('flags.Project')
    client = APIClient()

    res = client.get(f'/api/projects/{project.id}', 
                     headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})

    assert res.status_code == 200
    assert project.name == res.data['name']
    assert project.api_key == res.data['api_key']
    assert str(project.id) == res.data['id']



@pytest.mark.django_db
def test_api_project_not_found():
    client = APIClient()

    res = client.get(f'/api/projects/{uuid.uuid4()}',
                     headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})


    assert res.status_code == 404

@pytest.mark.django_db
def test_api_get_single_project_invalid_admin_key():
    project = baker.make('flags.Project')
    client = APIClient()

    res = client.get(f'/api/projects/{project.id}', 
                     headers={'X-Admin-Key': 'invalid-key'})

    assert res.status_code == 401



@pytest.mark.django_db
def test_api_get_single_project_missing_admin_key():
    project = baker.make('flags.Project')
    client = APIClient()

    res = client.get(f'/api/projects/{project.id}')

    assert res.status_code == 401


@pytest.mark.django_db
def test_api_delete_project():
    project = baker.make('flags.Project')
    client = APIClient()

    res = client.delete(path=f'/api/projects/{project.id}',
                        headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})

    assert res.status_code == 204

@pytest.mark.django_db
def test_api_delete_project_not_found():
    client = APIClient()

    res = client.delete(path=f'/api/projects/{uuid.uuid4()}',
                        headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})

    assert res.status_code == 404
    
@pytest.mark.django_db
def test_api_delete_project_invalid_admin_key():
    project = baker.make('flags.Project')

    client = APIClient()

    res = client.delete(path=f'/api/projects/{project.id}',
                        headers={'X-Admin-Key': 'this-key-is-invalid'})

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_delete_project_missing_admin_key():
    project = baker.make('flags.Project')
    client = APIClient()

    res = client.delete(path=f'/api/projects/{project.id}')

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_delete_project_does_not_reappear():
    project = baker.make('flags.Project')

    client = APIClient()

    client.delete(path=f'/api/projects/{project.id}',
                  headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})

    res = client.get(f'/api/projects/{project.id}',
                        headers={'X-Admin-Key': settings.ADMIN_SECRET_KEY})

    assert res.status_code == 404

