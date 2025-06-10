# src/ingest/github_ingest.py

import os
import requests
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def fetch_trending_repos(language="python", sort="stars", order="desc", per_page=5):
    logger.info(f"Fetching trending repos with query: language={language}")
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": sort,
        "order": order,
        "per_page": per_page
    }

    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        logger.error(f"GitHub API error: {response.status_code} - {response.text}")
        return []

    return response.json().get("items", [])
