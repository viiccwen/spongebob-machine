"""Meme dataset loading and management."""

import json
import os
import logging
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class MemeDataset:
    """Manages meme metadata and dataset operations."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize meme dataset.

        Args:
            data_dir: Directory containing memes.json and images/
        """
        self.data_dir = Path(data_dir)
        self.memes_file = self.data_dir / "memes.json"
        self.memes: List[Dict] = []
        self._load_memes()

    def _load_memes(self):
        """Load memes from JSON file."""
        if not self.memes_file.exists():
            logger.warning(
                f"Meme file not found: {self.memes_file}. Creating empty dataset."
            )
            self.memes = []
            self._create_sample_memes_file()
            return

        try:
            with open(self.memes_file, "r", encoding="utf-8") as f:
                self.memes = json.load(f)
            logger.info(f"Loaded {len(self.memes)} memes from {self.memes_file}")
        except Exception as e:
            logger.error(f"Error loading memes: {e}")
            self.memes = []

    def _create_sample_memes_file(self):
        """Create a sample memes.json file if it doesn't exist."""
        sample_memes = [
            {
                "id": "sb_001",
                "file": "images/tired/sb_001.jpg",
                "emotion": ["tired", "despair"],
                "intent": ["complain", "burnout"],
                "tone": ["sarcastic"],
                "keywords": ["累", "好煩", "不想做了", "下班", "人生好難"],
                "caption": "我真的不行了",
            }
        ]

        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.memes_file, "w", encoding="utf-8") as f:
            json.dump(sample_memes, f, ensure_ascii=False, indent=2)
        logger.info(f"Created sample memes file: {self.memes_file}")

    def get_all_memes(self) -> List[Dict]:
        """Get all memes."""
        return self.memes

    def get_meme_by_id(self, meme_id: str) -> Optional[Dict]:
        """Get meme by ID."""
        for meme in self.memes:
            if meme.get("id") == meme_id:
                return meme
        return None

    def get_memes_by_emotion(self, emotion: str) -> List[Dict]:
        """Get memes matching a specific emotion."""
        return [meme for meme in self.memes if emotion in meme.get("emotion", [])]

    def get_memes_by_intent(self, intent: str) -> List[Dict]:
        """Get memes matching a specific intent."""
        return [meme for meme in self.memes if intent in meme.get("intent", [])]

    def get_file_path(self, meme: Dict) -> Optional[Path]:
        """
        Get full file path for a meme.

        Args:
            meme: Meme dictionary with 'file' key

        Returns:
            Path object or None if file doesn't exist
        """
        file_path = self.data_dir / meme.get("file", "")
        if file_path.exists():
            return file_path
        return None


# Global dataset instance
_dataset: Optional[MemeDataset] = None


def get_dataset(data_dir: str = "data") -> MemeDataset:
    """Get or create global dataset instance."""
    global _dataset
    if _dataset is None:
        _dataset = MemeDataset(data_dir)
    return _dataset
