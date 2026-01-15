"""Keyword expansion module for semantic search."""

from typing import List, Set


def expand_keywords(keywords: List[str]) -> Set[str]:
    """
    Expand keywords with synonyms and related terms.

    Args:
        keywords: Original keywords

    Returns:
        Set of expanded keywords including synonyms
    """
    expanded = set(keywords)

    # Simple synonym mapping (can be enhanced with word embeddings or thesaurus)
    synonym_map = {
        "累": ["疲憊", "疲倦", "好累", "累死", "不行了"],
        "生氣": ["氣", "不爽", "火大", "憤怒"],
        "開心": ["高興", "快樂", "爽", "愉快"],
        "難過": ["傷心", "悲傷", "失落", "沮喪"],
    }

    for keyword in keywords:
        if keyword in synonym_map:
            expanded.update(synonym_map[keyword])

    return expanded
