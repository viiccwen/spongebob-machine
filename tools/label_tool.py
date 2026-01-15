"""Semi-automatic labeling tool for memes."""

import json
import os
from pathlib import Path
from typing import Dict


def label_meme_interactive(image_path: str) -> Dict:
    """
    Interactive labeling for a single meme image.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary with meme metadata
    """
    print(f"\nImage: {os.path.basename(image_path)}")

    # Get emotion
    emotion_input = input(
        "emotion? [tired/angry/happy/sad/crazy] (comma-separated): "
    ).strip()
    emotions = [e.strip() for e in emotion_input.split(",") if e.strip()]

    # Get intent
    intent_input = input(
        "intent? [complain/celebrate/mock/comfort] (comma-separated): "
    ).strip()
    intents = [i.strip() for i in intent_input.split(",") if i.strip()]

    # Get tone
    tone_input = input("tone? [sarcastic/cute/dark] (comma-separated): ").strip()
    tones = [t.strip() for t in tone_input.split(",") if t.strip()]

    # Get keywords
    keywords_input = input("keywords (comma-separated): ").strip()
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    # Get caption
    caption = input("caption (optional): ").strip()

    # Generate ID
    meme_id = f"sb_{os.path.splitext(os.path.basename(image_path))[0]}"

    # Determine relative path
    rel_path = (
        f"images/{emotions[0] if emotions else 'other'}/{os.path.basename(image_path)}"
    )

    return {
        "id": meme_id,
        "file": rel_path,
        "emotion": emotions,
        "intent": intents,
        "tone": tones,
        "keywords": keywords,
        "caption": caption if caption else None,
    }


def main():
    """Main function for labeling tool."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tools/label_tool.py <images_directory>")
        sys.exit(1)

    images_dir = Path(sys.argv[1])
    if not images_dir.exists():
        print(f"Error: Directory not found: {images_dir}")
        sys.exit(1)

    # Find all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".gif"}
    image_files = [
        f for f in images_dir.rglob("*") if f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No image files found in {images_dir}")
        sys.exit(1)

    print(f"Found {len(image_files)} images")

    memes = []
    for image_file in image_files:
        try:
            meme_data = label_meme_interactive(str(image_file))
            memes.append(meme_data)

            # Ask if continue
            continue_labeling = input("\nContinue? [Y/n]: ").strip().lower()
            if continue_labeling == "n":
                break
        except KeyboardInterrupt:
            print("\n\nLabeling interrupted.")
            break
        except Exception as e:
            print(f"Error labeling {image_file}: {e}")
            continue

    # Save to JSON
    output_file = Path("data/memes.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing memes if file exists
    existing_memes = []
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            existing_memes = json.load(f)

    # Merge with new memes
    existing_ids = {m["id"] for m in existing_memes}
    new_memes = [m for m in memes if m["id"] not in existing_ids]
    all_memes = existing_memes + new_memes

    # Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_memes, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(new_memes)} new memes to {output_file}")
    print(f"Total memes: {len(all_memes)}")


if __name__ == "__main__":
    main()
