# src/news.py

import os
from ingest.news_ingest import fetch_tech_news
from transform.news_transform import summarize_text, get_sentiment_label
from storage.news_storage import save_news_to_db
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

API_KEY = os.getenv("NEWSDATA_API_KEY")
BASE_URL = "https://newsdata.io/api/1/news"

def main():
    articles = fetch_tech_news(api_key=API_KEY, limit=5)


    if not articles:
        logger.warning("No news articles fetched.")
        return

    results = []
    for article in articles:
        summary = summarize_text(article["description"])
        sentiment = get_sentiment_label(article["description"])
        results.append({
            "title": article["title"],
            "summary": summary,
            "sentiment": sentiment,
            "url": article["link"]
        })

    for item in results:
        print(f"\n📌 {item['title']}")
        print(f"🧠 {item['summary']}")
        print(f"❤️ Sentiment: {item['sentiment']}")
        print(f"🔗 {item['url']}\n")

    save_news_to_db(results)

if __name__ == "__main__":
    main()
