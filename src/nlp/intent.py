"""Intent and emotion analysis module."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def analyze_intent_emotion(text: str) -> Dict[str, Any]:
    """
    Analyze user input for intent and emotion.

    Args:
        text: User input text

    Returns:
        Dictionary with emotion, intent, tone, and keywords
    """
    text_lower = text.lower()

    # Simple keyword-based analysis (can be enhanced with ML models)
    emotion = _detect_emotion(text_lower)
    intent = _detect_intent(text_lower)
    tone = _detect_tone(text_lower)
    keywords = _extract_keywords(text_lower)

    return {
        "emotion": emotion,
        "intent": intent,
        "tone": tone,
        "keywords": keywords,
        "original_text": text,
    }


def _detect_emotion(text: str) -> List[str]:
    """Detect emotions from text."""
    emotions = []

    # Emotion keywords mapping
    emotion_keywords = {
        "tired": [
            "累",
            "疲憊",
            "好累",
            "不行了",
            "撐不下去",
            "deadline",
            "加班",
            "社畜",
        ],
        "angry": ["生氣", "氣", "不爽", "火大", "煩", "討厭"],
        "happy": ["爽", "開心", "高興", "快樂", "讚", "好棒"],
        "sad": ["難過", "傷心", "哭", "悲傷", "失落"],
        "crazy": ["瘋", "抓狂", "崩潰", "爆炸", "受不了"],
    }

    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text for keyword in keywords):
            emotions.append(emotion)

    return emotions if emotions else ["neutral"]


def _detect_intent(text: str) -> List[str]:
    """Detect intent from text."""
    intents = []

    intent_keywords = {
        "complain": ["抱怨", "不爽", "煩", "討厭", "爛", "爛透了"],
        "celebrate": ["慶祝", "恭喜", "太棒", "讚", "成功"],
        "mock": ["嘲諷", "諷刺", "酸", "笑死"],
        "comfort": ["安慰", "加油", "支持", "陪伴"],
    }

    for intent, keywords in intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            intents.append(intent)

    return intents if intents else ["general"]


def _detect_tone(text: str) -> List[str]:
    """Detect tone from text."""
    tones = []

    if any(word in text for word in ["笑死", "哈哈", "XD", "www"]):
        tones.append("sarcastic")
    if any(word in text for word in ["可愛", "萌", "好萌"]):
        tones.append("cute")
    if any(word in text for word in ["黑暗", "絕望", "人生好難"]):
        tones.append("dark")

    return tones if tones else ["neutral"]


def _extract_keywords(text: str) -> List[str]:
    """Extract relevant keywords from text."""
    # Simple keyword extraction (can be enhanced with NLP libraries)
    # For now, return the text itself as a keyword
    return [text]
