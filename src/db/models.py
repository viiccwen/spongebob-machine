"""Database models using SQLAlchemy."""

from typing import List, Optional

from sqlalchemy import ARRAY, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meme(Base):  # type: ignore[misc, valid-type]
    """Meme model for database storage."""

    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meme_id = Column(
        String(50), unique=True, nullable=False, index=True
    )  # e.g., SS0001, SS0002
    name = Column(String(255), nullable=False, index=True)  # Name
    aliases: Optional[List[str]] = Column(ARRAY(String), nullable=True)  # type: ignore[assignment]  # Aliases for search

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "meme_id": self.meme_id,
            "name": self.name,
            "aliases": self.aliases or [],
        }
