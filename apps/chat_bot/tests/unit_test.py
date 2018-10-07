from src.webserver import app


def test_facebook_auth_handler_200():
    request, response =  app.test_client.get('/')
    assert response.status == 200

def test_facebbok_auth_handler_verify_token_200():
    test_string = 'test'
    params = {
        'hub.mode': 'subscribe',
        'hub.challenge': test_string,
        'hub.verify_token': '12345678unit9'
    }

    request, response =  app.test_client.get('/', params=params)
    assert response.status == 200
    assert request.args.get('hub.challenge') == test_string

def test_facebbok_auth_handler_verify_token_403():
    params = {
        'hub.mode': 'subscribe',
        'hub.challenge': 'test',
        'hub.verify_token': 'wrong_token'
    }

    request, response =  app.test_client.get('/', params=params)
    assert response.status == 403

