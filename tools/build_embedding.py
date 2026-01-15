"""Tool to build and save embeddings for memes."""

import json
import numpy as np
from pathlib import Path

from nlp.embedding import encode_texts


def build_embeddings(
    memes_file: str = "data/memes.json", output_file: str = "data/embeddings.npy"
):
    """
    Build embeddings for all memes and save to file.

    Args:
        memes_file: Path to memes.json
        output_file: Path to save embeddings
    """
    memes_path = Path(memes_file)
    if not memes_path.exists():
        print(f"Error: Memes file not found: {memes_file}")
        return

    # Load memes
    with open(memes_path, "r", encoding="utf-8") as f:
        memes = json.load(f)

    if not memes:
        print("No memes found in file")
        return

    # Prepare texts for embedding (use caption or keywords)
    texts = []
    for meme in memes:
        text = meme.get("caption", "") or " ".join(meme.get("keywords", []))
        if not text:
            text = " ".join(meme.get("emotion", []))
        texts.append(text)

    print(f"Building embeddings for {len(texts)} memes...")

    # Encode all texts
    embeddings = encode_texts(texts)

    # Save embeddings
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, embeddings)

    print(f"Saved embeddings to {output_file}")
    print(f"Embedding shape: {embeddings.shape}")


if __name__ == "__main__":
    build_embeddings()
