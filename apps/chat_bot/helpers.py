import traceback
from typing import TypeVar
from apps.chat_bot.config import version, username, password, url
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException
from watson_developer_cloud.tone_analyzer_v3 import ToneInput

T = TypeVar(ToneAnalyzerV3)

bot_aswers = {
    'positive': [
        "Oh, that's very kind of you.",
        "That's great!",
        "Glad to hear.",
        "Hurra!",
        ":)"
    ],
    'neutral': [
        "Interesting. Ok.",
        "I see...",
        "Well...",
        "I don't know what to say.",
        "Hm..."
    ],
    'negative': [
        "I feel so bad about what you wrote.",
        "I'm sorry...",
        "That's not good.",
        "Please, don't say that."
        ":(",
    ]
}

def clamp(minimum: [int, float], x: [int, float], maximum: [int, float]) -> [int, float]:
    """Returns x according to mininmum and maximum limits"""
    return max(minimum, min(x, maximum))

def get_tone_analyzer() -> T:
    """Returns ToneAnalyzer object"""
    return ToneAnalyzerV3(
        version=version,
        username=username,
        password=password,
        url=url
    )

def analyze_tone(tone_analyzer: T, text: str) -> dict:
    """Analyzes text input with tone analyzer object"""
    try:
        tone_input = ToneInput(text)
        return tone_analyzer.tone(
            tone_input,
            'application/json'
        ).get_result()

    except WatsonApiException:
        traceback.print_exc(limit=1)

def parse_analyzed_tone(tone_info: dict) -> int:
    """Parses the tone info and translates it into integer"""
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


