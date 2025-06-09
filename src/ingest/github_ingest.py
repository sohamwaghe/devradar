# src/ingest/github_ingest.py
import requests
from utils.config import GITHUB_TOKEN
from utils.logger import get_logger

logger = get_logger(__name__)

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_trending_repos(query="language:python", sort="stars", order="desc", per_page=5):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": per_page
    }

    logger.info(f"Fetching trending repos with query: {query}")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        repos = response.json().get("items", [])
        logger.info(f"Fetched {len(repos)} repositories.")
        return repos
    else:
        logger.error(f"GitHub API error: {response.status_code} - {response.text}")
        return []
