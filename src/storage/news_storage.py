# src/storage/news_storage.py

import os
import json
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

def save_news_to_json(news, directory="data/news"):
    os.makedirs(directory, exist_ok=True)
    filename = f"news_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(directory, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(news, f, indent=2)
    logger.info(f"Saved {len(news)} news items to {path}")
