# src/ingest/news_ingest.py

import os
import requests
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_tech_news(limit=5):
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&category=technology&language=en"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("results", [])[:limit]
        news = []
        for item in articles:
            news.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "description": item.get("description", ""),
                "pubDate": item.get("pubDate", "")
            })
        logger.info(f"Fetched {len(news)} tech news articles.")
        return news
    except Exception as e:
        logger.error(f"Error fetching tech news: {e}")
        return []
