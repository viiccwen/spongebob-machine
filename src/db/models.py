"""Database models using SQLAlchemy."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import ARRAY, BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


def utc_now():
    """Get current UTC datetime with timezone awareness."""
    return datetime.now(timezone.utc)


class Meme(Base):  # type: ignore[misc, valid-type]
    """Meme model for database storage."""

    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meme_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )  # e.g., SS0001, SS0002
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)  # Name
    aliases: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), nullable=True
    )  # Aliases for search

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "meme_id": self.meme_id,
            "name": self.name,
            "aliases": self.aliases or [],
        }


class User(Base):  # type: ignore[misc, valid-type]
    """User model for storing Telegram user information."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )  # Telegram user ID
    last_query_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=utc_now, onupdate=utc_now
    )  # Last query time
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )

    # Relationship to user queries
    queries = relationship(
        "UserQuery", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "telegram_user_id": self.telegram_user_id,
            "last_query_time": (
                self.last_query_time.isoformat() if self.last_query_time else None
            ),
            "created_at": self.created_at.isoformat(),
        }


class UserQuery(Base):  # type: ignore[misc, valid-type]
    """User query model for storing user search queries and selected memes."""

    __tablename__ = "user_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )  # Foreign key to users
    query_text: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # User input text (null for /random)
    selected_meme_id: Mapped[Optional[str]] = mapped_column(
        String(50), ForeignKey("memes.meme_id", ondelete="SET NULL"), nullable=True
    )  # Selected meme ID (set when user makes selection)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now, index=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, onupdate=utc_now
    )

    # Relationships
    user = relationship("User", back_populates="queries")
    meme = relationship("Meme", foreign_keys=[selected_meme_id])

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query_text": self.query_text,
            "selected_meme_id": self.selected_meme_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
