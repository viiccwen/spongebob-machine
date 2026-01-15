"""Sentence embedding module using sentence-transformers."""

import os
import logging
import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Global model instance (lazy loading)
_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """Get or initialize the embedding model."""
    global _model
    if _model is None:
        model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        )
        logger.info(f"Loading embedding model: {model_name}")
        _model = SentenceTransformer(model_name)
    return _model


def encode_text(text: str) -> np.ndarray:
    """
    Encode text into embedding vector.

    Args:
        text: Input text to encode

    Returns:
        Numpy array of embedding vector
    """
    model = get_embedding_model()
    return model.encode(text, convert_to_numpy=True)


def encode_texts(texts: List[str]) -> np.ndarray:
    """
    Encode multiple texts into embedding vectors.

    Args:
        texts: List of input texts

    Returns:
        Numpy array of shape (len(texts), embedding_dim)
    """
    model = get_embedding_model()
    return model.encode(texts, convert_to_numpy=True)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0-1)
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)
