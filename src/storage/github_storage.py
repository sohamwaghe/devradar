import json
import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

def save_repos_to_json(repos, filename_prefix="github_repos"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    output_dir = "data/github"
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2)

    logger.info(f"Saved {len(repos)} repos to {filepath}")
