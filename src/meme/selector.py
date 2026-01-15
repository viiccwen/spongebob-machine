"""Meme selection logic using alias search."""

import random
import logging
from typing import Dict, Optional

from meme.dataset import get_dataset

logger = logging.getLogger(__name__)

# Response templates
RESPONSE_TEMPLATES = {
    "default": ["這張給你！", "希望這張適合你", "找到了！"],
}


def select_meme(user_text: str) -> Optional[Dict]:
    """
    Select the best meme for user input using alias search.

    Args:
        user_text: User input text

    Returns:
        Dictionary with meme info and response text, or None
    """
    dataset = get_dataset()

    # Search by alias
    meme = dataset.search_by_alias(user_text)

    if not meme:
        logger.warning("No memes found matching query")
        return None

    # Generate response text
    response_text = random.choice(RESPONSE_TEMPLATES["default"])

    return {
        "meme": meme,
        "response_text": response_text,
    }


def select_meme_by_random(intent: str) -> Optional[Dict]:
    dataset = get_dataset()
    all_memes = dataset.get_all_memes()

    if not all_memes:
        return None

    # Random selection
    meme = random.choice(all_memes)

    response_text = random.choice(RESPONSE_TEMPLATES["default"])

    return {
        "meme": meme,
        "response_text": response_text,
    }
