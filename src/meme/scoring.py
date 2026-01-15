"""Meme scoring and ranking module."""

import logging
from typing import Any, Dict, List

from nlp.embedding import encode_text, cosine_similarity
from nlp.keyword_expansion import expand_keywords

logger = logging.getLogger(__name__)


def score_meme(meme: Dict, user_text: str, analysis: Dict) -> float:
    """
    Score a meme based on user input and analysis.

    Args:
        meme: Meme dictionary
        user_text: Original user input text
        analysis: Intent/emotion analysis result

    Returns:
        Score between 0 and 1
    """
    scores = []

    # Emotion matching score
    emotion_score = _score_emotion_match(meme, analysis.get("emotion", []))
    scores.append(emotion_score * 0.3)

    # Intent matching score
    intent_score = _score_intent_match(meme, analysis.get("intent", []))
    scores.append(intent_score * 0.3)

    # Keyword matching score
    keyword_score = _score_keyword_match(meme, analysis.get("keywords", []))
    scores.append(keyword_score * 0.2)

    # Semantic similarity score (using embeddings)
    semantic_score = _score_semantic_similarity(meme, user_text)
    scores.append(semantic_score * 0.2)

    total_score = sum(scores)
    return min(1.0, max(0.0, total_score))


def _score_emotion_match(meme: Dict, user_emotions: List[str]) -> float:
    """Score based on emotion matching."""
    meme_emotions = set(meme.get("emotion", []))
    user_emotions_set = set(user_emotions)

    if not meme_emotions or not user_emotions_set:
        return 0.5  # Neutral score

    intersection = meme_emotions & user_emotions_set
    if intersection:
        return 1.0
    return 0.0


def _score_intent_match(meme: Dict, user_intents: List[str]) -> float:
    """Score based on intent matching."""
    meme_intents = set(meme.get("intent", []))
    user_intents_set = set(user_intents)

    if not meme_intents or not user_intents_set:
        return 0.5

    intersection = meme_intents & user_intents_set
    if intersection:
        return 1.0
    return 0.0


def _score_keyword_match(meme: Dict, user_keywords: List[str]) -> float:
    """Score based on keyword matching."""
    meme_keywords = set(meme.get("keywords", []))
    expanded_user_keywords = expand_keywords(user_keywords)

    if not meme_keywords:
        return 0.5

    intersection = meme_keywords & expanded_user_keywords
    if not intersection:
        return 0.0

    # Score based on number of matching keywords
    match_ratio = len(intersection) / max(
        len(meme_keywords), len(expanded_user_keywords)
    )
    return min(1.0, match_ratio * 2)  # Boost score for multiple matches


def _score_semantic_similarity(meme: Dict, user_text: str) -> float:
    """Score based on semantic similarity using embeddings."""
    try:
        # Use meme caption or keywords for comparison
        meme_text = meme.get("caption", "") or " ".join(meme.get("keywords", []))
        if not meme_text:
            return 0.5

        # Encode both texts
        user_embedding = encode_text(user_text)
        meme_embedding = encode_text(meme_text)

        # Calculate cosine similarity
        similarity = cosine_similarity(user_embedding, meme_embedding)
        return float(similarity)
    except Exception as e:
        logger.warning(f"Error calculating semantic similarity: {e}")
        return 0.5


def rank_memes(
    memes: List[Dict], user_text: str, analysis: Dict, top_k: int = 5
) -> List[Dict]:
    """
    Rank memes by score and return top-k.

    Args:
        memes: List of meme dictionaries
        user_text: User input text
        analysis: Intent/emotion analysis
        top_k: Number of top memes to return

    Returns:
        List of top-k memes with scores
    """
    scored_memes: List[Dict[str, Any]] = []
    for meme in memes:
        score = score_meme(meme, user_text, analysis)
        scored_memes.append({"meme": meme, "score": score})

    # Sort by score (descending)
    scored_memes.sort(key=lambda x: float(x["score"]), reverse=True)

    # Return top-k
    return scored_memes[:top_k]
