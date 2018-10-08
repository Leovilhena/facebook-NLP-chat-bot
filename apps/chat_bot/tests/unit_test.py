import ujson
import pytest
from webserver import app
from apps.chat_bot.routes import prepare_data
from apps.chat_bot.classes import Bot
from apps.chat_bot.helpers import get_tone_analyzer, analyze_tone, parse_analyzed_tone, clamp, bot_aswers
from watson_developer_cloud import ToneAnalyzerV3

@pytest.fixture('module')
def bot():
    return Bot('unit9')

@pytest.fixture('module')
def data():
    return ujson.dumps({
        'recipient': {'id': 'id'},
        'message': {'text': 'text'}
    })

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
    test_data = ujson.dumps({
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
    test_data = ujson.dumps({
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

def test_clamp():
    assert clamp(-1, 4, 1) == 1
    assert clamp(-1, 0, 1) == 0
    assert clamp(-1, -4, 1) == -1

def test_bot(bot):
    assert bot.user_id == 'unit9'
    assert bot.mood == 'neutral'
    assert bot.mood_value == 0
    assert bot("Hello!") in bot_aswers[bot.mood]

def test_prepare_data(data):
    sender_id = 'id'
    text = 'text'
    prepared_data = prepare_data(sender_id, text)
    assert ujson.loads(prepared_data)
    assert prepared_data == data


