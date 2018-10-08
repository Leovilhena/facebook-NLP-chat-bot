import random
from apps.chat_bot.helpers import get_tone_analyzer, analyze_tone, parse_analyzed_tone, bot_aswers, clamp


class Bot:
    def __init__(self, user_id: str, mood_value: int = 0) -> None:
        self.user_id = user_id
        self.tone_analyzer = get_tone_analyzer()
        self._mood_value = mood_value
        self.answers = bot_aswers

    def __call__(self, text: str) -> str:
        tone_score = self._analyze(text)
        self.mood_value += tone_score
        return self._get_answer(self.mood)

    def __str__(self):
        return f'Chat Bot v1 <id: {id(self)}, user_id: {self.user_id}, mood: {self.mood}>'

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'{self.user_id!r}, {self.mood_value!r})'

    def _analyze(self, text: str) -> int:
        tone_info = analyze_tone(self.tone_analyzer, text)
        return parse_analyzed_tone(tone_info)

    @property
    def mood_value(self) -> int:
        return self._mood_value

    @mood_value.setter
    def mood_value(self, tone_score: int) -> None:
        value = clamp(-1, tone_score, 1)
        self._mood_value = value

    def _get_answer(self, mood: str):
        return random.choice(self.answers[mood])

    @property
    def mood(self) -> str:
        """Returns mood_value as str"""
        moods = ['neutral', 'positive', 'negative']
        return moods[self.mood_value]
