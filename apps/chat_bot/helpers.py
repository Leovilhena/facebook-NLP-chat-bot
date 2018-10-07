import traceback
from typing import TypeVar
from apps.chat_bot.config import version, username, password, url
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException
from watson_developer_cloud.tone_analyzer_v3 import ToneInput


T = TypeVar(ToneAnalyzerV3)

def get_tone_analyzer():
    return ToneAnalyzerV3(
        version=version,
        username=username,
        password=password,
        url=url
    )

def analyze_tone(tone_analyzer: T, text: str) -> dict:
    try:
        tone_input = ToneInput(text)
        return tone_analyzer.tone(
            tone_input,
            'application/json'
        ).get_result()

    # Return examples:
    # Sad:        {'document_tone': {'tones': [{'score': 0.916667, 'tone_id': 'sadness', 'tone_name': 'Sadness'}]}}
    # Neutral:    {'document_tone': {'tones': []}}
    except WatsonApiException:
        traceback.print_exc(limit=1)

def parse_analyzed_tone(tone_info: dict) -> int:
    try:
        tone = tone_info['document_tone']['tones'][0]['tone_id']
    except (ValueError, IndexError, KeyError):
        tone = None

    if tone in ['anger', 'fear', 'sadness']:
        return -1
    elif tone in ['joy', 'confident', 'tentative']:
        return 1
    else:
        return 0
