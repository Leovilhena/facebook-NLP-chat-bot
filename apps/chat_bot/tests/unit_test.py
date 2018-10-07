import json
from webserver import app
from apps.chat_bot.helpers import get_tone_analyzer, analyze_tone, parse_analyzed_tone
from watson_developer_cloud import ToneAnalyzerV3


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

def test_facebook_message_handler_400():
    test_data = json.dumps({
        'sender': 'id',
        'message': {
            'text':'message'
        }
    })
    request, response = app.test_client.post('/')
    assert response.status == 400

    request, response = app.test_client.post('/', data=test_data)
    assert response.status == 400

def test_facebook_message_handler_500():
    test_data = json.dumps({
        'sender': {
            'id':'12'
        },
        'message': {
            'text': ''
        }
    })
    request, response = app.test_client.post('/', data=test_data)
    assert response.status == 500

def test_get_tone_analyzer():
    assert isinstance(get_tone_analyzer(), ToneAnalyzerV3)

def test_analyze_tone():
    tone_analyzer = get_tone_analyzer()
    text = "I'm sad"

    response_tone = analyze_tone(tone_analyzer, text)

    assert isinstance(response_tone, dict)
    assert 'document_tone' in response_tone
    assert 'tones' in response_tone['document_tone']
    assert len(response_tone['document_tone']['tones'])
    assert 'tone_id' in response_tone['document_tone']['tones'][0]
    assert response_tone['document_tone']['tones'][0]['tone_id'] == 'sadness'

def test_parse_analyzed_tone():
    test_tone_info = {
        'document_tone': {'tones': [{
            'tone_id': ''}]}
    }
    assert parse_analyzed_tone(test_tone_info) == 0

    test_tone_info['document_tone']['tones'][0]['tone_id'] = 'joy'
    assert parse_analyzed_tone(test_tone_info) == 1

    test_tone_info['document_tone']['tones'][0]['tone_id'] = 'sadness'
    assert parse_analyzed_tone(test_tone_info) == -1


