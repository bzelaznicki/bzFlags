import pytest
from rest_framework.test import APIClient
from model_bakery import baker 

@pytest.mark.django_db
def test_api_should_return_401_on_invalid_api_key():
    client = APIClient()
    res = client.post('/api/evaluate', data={
        'user_identifier': 'user_123',
        'flag_keys': ['bzflags-test']
    }, 
                      format='json')

    assert res.status_code == 401

@pytest.mark.django_db
def test_api_should_not_return_non_existing_keys():
    project = baker.make('flags.Project')

    client = APIClient()
    res = client.post('/api/evaluate', data={
        'user_identifier': 'user_123',
        'flag_keys': ['does-not-exist']
    },
                      headers={'X-Api-Key': project.api_key},

                      format='json')

    assert res.status_code == 200
    assert res.data == {}

@pytest.mark.django_db
def test_api_should_return_existing_flag():
    project = baker.make('flags.Project')
    baker.make('flags.Flag', project=project, key='bzflags-test')

    client = APIClient()
    res = client.post('/api/evaluate', data={
        'user_identifier': 'user_123',
        'flag_keys': ['bzflags-test']
    }, headers={'X-Api-Key': project.api_key}, format='json')

    assert res.status_code == 200
    assert 'bzflags-test' in res.data
