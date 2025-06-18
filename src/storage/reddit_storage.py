# src/storage/reddit_storage.py

import json
import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

def save_posts_to_json(posts, directory="data/reddit"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reddit_posts_{timestamp}.json"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    logger.info(f"Saved {len(posts)} posts to {filepath}")
