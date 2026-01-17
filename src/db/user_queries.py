"""Database operations for user queries and selections."""

import logging
from datetime import datetime, timezone
from typing import Optional


from db.connection import SessionLocal
from db.models import User, UserQuery

logger = logging.getLogger(__name__)


def get_or_create_user(telegram_user_id: int) -> User:
    """
    Get or create a user by Telegram user ID.

    Args:
        telegram_user_id: Telegram user ID

    Returns:
        User object
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        if not user:
            user = User(
                telegram_user_id=telegram_user_id,
                last_query_time=datetime.now(timezone.utc),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {telegram_user_id}")
        else:
            # Update last query time
            user.last_query_time = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
        return user
    except Exception as e:
        logger.error(f"Error getting/creating user: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


def create_user_query(
    telegram_user_id: int, query_text: Optional[str] = None
) -> Optional[UserQuery]:
    """
    Create a new user query record.

    Args:
        telegram_user_id: Telegram user ID
        query_text: User input text (None for /random command)

    Returns:
        UserQuery object or None if error
    """
    db = SessionLocal()
    try:
        # Get or create user in the same session
        user = db.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        if not user:
            user = User(
                telegram_user_id=telegram_user_id,
                last_query_time=datetime.now(timezone.utc),
            )
            db.add(user)
            db.flush()  # Flush to get user.id
            logger.info(f"Created new user: {telegram_user_id}")
        else:
            # Update last query time
            user.last_query_time = datetime.now(timezone.utc)

        user_query = UserQuery(
            user_id=user.id,
            query_text=query_text,
            created_at=datetime.now(timezone.utc),
        )
        db.add(user_query)
        db.commit()
        db.refresh(user_query)
        logger.info(f"Created user query for user {telegram_user_id}: {query_text}")
        return user_query
    except Exception as e:
        logger.error(f"Error creating user query: {e}", exc_info=True)
        db.rollback()
        return None
    finally:
        db.close()


def update_user_query_selection(
    telegram_user_id: int, meme_id: str, user_query_id: Optional[int] = None
) -> bool:
    """
    Update the selected meme_id for a user query.

    Args:
        telegram_user_id: Telegram user ID
        meme_id: Selected meme ID
        user_query_id: Optional user query ID. If None, updates the most recent query for the user.

    Returns:
        True if successful, False otherwise
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        if not user:
            logger.warning(f"User not found: {telegram_user_id}")
            return False

        if user_query_id:
            user_query = (
                db.query(UserQuery)
                .filter(UserQuery.id == user_query_id, UserQuery.user_id == user.id)
                .first()
            )
        else:
            # Get the most recent query without a selection
            user_query = (
                db.query(UserQuery)
                .filter(
                    UserQuery.user_id == user.id, UserQuery.selected_meme_id.is_(None)
                )
                .order_by(UserQuery.created_at.desc())
                .first()
            )

        if not user_query:
            logger.warning(f"No user query found for user {telegram_user_id}")
            return False

        user_query.selected_meme_id = meme_id
        user_query.updated_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Updated user query {user_query.id} with selected meme: {meme_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating user query selection: {e}", exc_info=True)
        db.rollback()
        return False
    finally:
        db.close()
