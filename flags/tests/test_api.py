from rest_framework.test import APIClient

def test_api_should_return_401_on_invalid_api_key():
    client = APIClient()
    res = client.post('/api/evaluate', json={
        'user_identifier': 'user_123',
        'flag_key': 'bzflags-test'
    });

    assert res.status_code == 401
