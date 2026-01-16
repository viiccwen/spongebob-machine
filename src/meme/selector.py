"""Meme selection logic using alias search."""

import random
import logging
from typing import Dict, List, Optional

from meme.dataset import get_dataset

logger = logging.getLogger(__name__)

# Response templates
RESPONSE_TEMPLATES = {
    "default": ["這張給你！", "希望這張適合你", "找到了！"],
}


def select_meme(user_text: str, count: int = 3) -> Optional[List[Dict]]:
    """
    Select multiple memes for user input using alias search.

    Args:
        user_text: User input text
        count: Number of memes to return (default: 3)

    Returns:
        List of dictionaries with meme info, or None if no memes found
    """
    dataset = get_dataset()

    # Search by alias, get up to count results
    memes = dataset.search_by_alias(user_text, limit=count)

    if not memes:
        logger.warning("No memes found matching query")
        return None

    return memes


def select_meme_by_random(intent: str, count: int = 3) -> Optional[List[Dict]]:
    """
    Select random memes.

    Args:
        intent: Intent type (not used, kept for compatibility)
        count: Number of memes to return (default: 3)

    Returns:
        List of meme dictionaries, or None if no memes available
    """
    dataset = get_dataset()
    all_memes = dataset.get_all_memes()

    if not all_memes:
        return None

    # Random selection of count memes
    selected_memes = random.sample(all_memes, min(count, len(all_memes)))

    return selected_memes
