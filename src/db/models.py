"""Database models using SQLAlchemy."""

from typing import List, Optional

from sqlalchemy import ARRAY, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Meme(Base):  # type: ignore[misc, valid-type]
    """Meme model for database storage."""

    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)
    meme_id = Column(String(50), unique=True, nullable=False, index=True)
    file_path = Column(String(255), nullable=False)
    emotion: Optional[List[str]] = Column(ARRAY(String), nullable=True)  # type: ignore[assignment]
    intent: Optional[List[str]] = Column(ARRAY(String), nullable=True)  # type: ignore[assignment]
    tone: Optional[List[str]] = Column(ARRAY(String), nullable=True)  # type: ignore[assignment]
    keywords: Optional[List[str]] = Column(ARRAY(String), nullable=True)  # type: ignore[assignment]
    caption: Optional[str] = Column(Text, nullable=True)  # type: ignore[assignment]
    embedding = Column(Vector(384), nullable=True)  # Dimension depends on model

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.meme_id,
            "file": self.file_path,
            "emotion": self.emotion or [],
            "intent": self.intent or [],
            "tone": self.tone or [],
            "keywords": self.keywords or [],
            "caption": self.caption,
        }
