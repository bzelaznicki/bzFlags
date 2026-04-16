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
    baker.make('flags.Flag', project=project, key='bzflags-test', enabled=True, rollout_percentage=100)

    client = APIClient()
    res = client.post('/api/evaluate', data={
        'user_identifier': 'user_123',
        'flag_keys': ['bzflags-test']
    }, headers={'X-Api-Key': project.api_key}, format='json')

    assert res.status_code == 200
    assert 'bzflags-test' in res.data
    assert res.data['bzflags-test'] is True


@pytest.mark.django_db
def test_api_overrides_should_return_for_user_identifier():
    project = baker.make('flags.Project')
    flag = baker.make('flags.Flag', project=project, enabled=True, rollout_percentage=0)
    override = baker.make('flags.FlagOverride', flag=flag, enabled=True)


    client = APIClient()
    res = client.post('/api/evaluate', data={
        'user_identifier': override.user_identifier,
        'flag_keys': [flag.key],
    }, headers={'X-Api-Key': project.api_key}, format='json')

    assert res.status_code == 200
    assert res.data[flag.key] is True 
