"""Utility functions for bot operations."""

import asyncio
import io
import logging
import os
from functools import partial
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Cloudflare R2 configuration
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "spongebob-memes")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")

# Initialize R2 client
_r2_client: Optional[Any] = None


def get_r2_client():
    """Get or create R2 S3 client."""
    global _r2_client
    if _r2_client is None:
        if not all(
            [R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL]
        ):
            raise ValueError(
                "R2 configuration missing. Please set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, "
                "R2_SECRET_ACCESS_KEY, and R2_ENDPOINT_URL environment variables."
            )

        _r2_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )
    return _r2_client


async def get_image_from_r2(meme_id: str) -> Optional[io.BytesIO]:
    """
    Get image from Cloudflare R2.

    Args:
        meme_id: Meme ID (e.g., SK0001, SS0002)

    Returns:
        BytesIO object with image data, or None if not found
    """
    try:
        client = get_r2_client()
        key = f"{meme_id}.jpg"

        # Run synchronous boto3 call in executor to avoid blocking
        loop = asyncio.get_event_loop()
        get_object_func = partial(client.get_object, Bucket=R2_BUCKET_NAME, Key=key)
        response = await loop.run_in_executor(None, get_object_func)
        image_data = response["Body"].read()

        return io.BytesIO(image_data)
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            logger.warning(f"Image not found in R2: spongebob-memes/{meme_id}.jpg")
        else:
            logger.error(f"Error getting image from R2: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting image from R2: {e}")
        return None
