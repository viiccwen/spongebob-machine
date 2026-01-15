"""Meme selection logic."""

import random
import logging
from typing import Dict, Optional

from meme.dataset import get_dataset
from meme.scoring import rank_memes

logger = logging.getLogger(__name__)

# Response templates based on emotion/intent
RESPONSE_TEMPLATES = {
    "tired": ["來，這張給你 😭", "你需要這張", "社畜懂你", "撐住啊！"],
    "angry": ["這張很適合", "給你發洩一下", "我懂你的感受"],
    "happy": ["恭喜！", "太棒了！", "這張給你慶祝"],
    "sad": ["抱抱", "這張給你", "會好起來的"],
    "crazy": ["這張很適合現在的你", "瘋起來！"],
    "default": ["這張給你！", "希望這張適合你"],
}


def select_meme(user_text: str, analysis: Dict) -> Optional[Dict]:
    """
    Select the best meme for user input.

    Args:
        user_text: User input text
        analysis: Intent/emotion analysis result

    Returns:
        Dictionary with meme info and file path, or None
    """
    dataset = get_dataset()
    all_memes = dataset.get_all_memes()

    if not all_memes:
        logger.warning("No memes available in dataset")
        return None

    # Rank memes
    top_memes = rank_memes(all_memes, user_text, analysis, top_k=3)

    if not top_memes:
        return None

    # Select from top memes (with some randomness)
    selected = random.choice(top_memes[:2]) if len(top_memes) > 1 else top_memes[0]
    meme = selected["meme"]

    # Get file path
    file_path = dataset.get_file_path(meme)
    if not file_path:
        logger.warning(f"Meme file not found: {meme.get('file')}")
        return None

    # Generate response text
    emotions = analysis.get("emotion", [])
    emotion = emotions[0] if emotions else "default"
    response_text = random.choice(
        RESPONSE_TEMPLATES.get(emotion, RESPONSE_TEMPLATES["default"])
    )

    return {
        "meme": meme,
        "file_path": str(file_path),
        "score": selected["score"],
        "response_text": response_text,
    }


def select_meme_by_intent(intent: str) -> Optional[Dict]:
    """
    Select meme by direct intent mapping (for button clicks).

    Args:
        intent: Intent string (e.g., "tired", "angry", "happy")

    Returns:
        Dictionary with meme info and file path, or None
    """
    dataset = get_dataset()

    if intent == "random":
        # Random selection
        all_memes = dataset.get_all_memes()
        if not all_memes:
            return None
        meme = random.choice(all_memes)
    else:
        # Select by emotion
        memes = dataset.get_memes_by_emotion(intent)
        if not memes:
            # Fallback to all memes
            memes = dataset.get_all_memes()
        if not memes:
            return None
        meme = random.choice(memes)

    # Get file path
    file_path = dataset.get_file_path(meme)
    if not file_path:
        logger.warning(f"Meme file not found: {meme.get('file')}")
        return None

    # Generate response text
    response_text = random.choice(
        RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES["default"])
    )

    return {
        "meme": meme,
        "file_path": str(file_path),
        "response_text": response_text,
    }
