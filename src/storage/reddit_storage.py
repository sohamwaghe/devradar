# src/storage/reddit_storage.py

import os
import json
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

def save_posts_to_json(posts, output_dir="data/reddit"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/reddit_posts_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
    
    logger.info(f"Saved {len(posts)} posts to {filename}")
