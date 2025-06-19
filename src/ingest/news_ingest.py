# src/ingest/news_ingest.py

import os
import requests
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def fetch_tech_news(api_key, limit=5):
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&category=technology&language=en"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("results", [])[:limit * 2]  # fetch more and filter

        tech_keywords = [
            "ai", "machine learning", "nvidia", "intel", "microsoft", "google",
            "meta", "apple", "iphone", "android", "chip", "cpu", "gpu",
            "software", "cloud", "developer", "devops", "openai", "quantum",
            "processor", "framework", "llama", "transformer", "coding", "chatgpt",
            "artificial intelligence", "blockchain", "cybersecurity"
        ]

        news = []
        for item in articles:
            title = (item.get("title") or "").lower()
            description = (item.get("description") or "").lower()
            if not description:
                continue

            if any(keyword in title or keyword in description for keyword in tech_keywords):
                news.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "description": item.get("description", ""),
                    "pubDate": item.get("pubDate", "")
                })
            if len(news) >= limit:
                break

        logger.info(f"Fetched {len(news)} tech news articles.")
        return news

    except Exception as e:
        logger.error(f"Error fetching tech news: {e}")
        return []
