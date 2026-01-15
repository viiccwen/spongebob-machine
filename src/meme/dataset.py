"""Meme dataset loading and management from database."""

import logging
from typing import List, Dict, Optional

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from db.connection import SessionLocal
from db.models import Meme

logger = logging.getLogger(__name__)


class MemeDataset:
    """Manages meme metadata and dataset operations from database."""

    def __init__(self):
        """Initialize meme dataset from database."""
        self.db: Optional[Session] = None

    def _get_db(self) -> Session:
        """Get database session."""
        if self.db is None:
            self.db = SessionLocal()
        return self.db

    def get_all_memes(self) -> List[Dict]:
        """Get all memes from database."""
        db = self._get_db()
        try:
            memes = db.execute(select(Meme)).scalars().all()
            return [meme.to_dict() for meme in memes]
        except Exception as e:
            logger.error(f"Error loading memes from database: {e}")
            return []

    def get_meme_by_id(self, meme_id: str) -> Optional[Dict]:
        """Get meme by ID."""
        db = self._get_db()
        try:
            meme = db.execute(
                select(Meme).where(Meme.meme_id == meme_id)
            ).scalar_one_or_none()
            return meme.to_dict() if meme else None
        except Exception as e:
            logger.error(f"Error getting meme by ID: {e}")
            return None

    def search_by_alias(self, query: str) -> Optional[Dict]:
        """
        Search memes by alias using pg_trgm similarity.

        Args:
            query: Search query text

        Returns:
            Meme dictionary if found, None otherwise
        """
        db = self._get_db()
        try:
            stmt = text(
                """
                SELECT m.*,
                  MAX(similarity(a, :query)) AS score
                FROM memes m,
                     unnest(m.aliases) AS a
                GROUP BY m.id, m.meme_id, m.name, m.aliases
                HAVING MAX(similarity(a, :query)) > 0.3
                ORDER BY score DESC
                LIMIT 1
                """
            )
            result = db.execute(stmt, {"query": query}).mappings().first()
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Alias search error: {e}")
            return None


# Global dataset instance
_dataset: Optional[MemeDataset] = None


def get_dataset() -> MemeDataset:
    """Get or create global dataset instance."""
    global _dataset
    if _dataset is None:
        _dataset = MemeDataset()
    return _dataset
