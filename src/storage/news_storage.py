# src/storage/news_storage.py

from db.database import SessionLocal
from db.models import TechNews
from utils.logger import get_logger

logger = get_logger(__name__)

def save_news_to_db(news_items):
    session = SessionLocal()
    try:
        for item in news_items:
            news = TechNews(
                title=item["title"],
                summary=item["summary"],
                sentiment=item["sentiment"],
                url=item["url"],
                published_at=item.get("published_at", "")
            )
            session.add(news)
        session.commit()
        logger.info(f"Saved {len(news_items)} news items to database.")
    except Exception as e:
        logger.error(f"Failed to save news: {e}")
        session.rollback()
    finally:
        session.close()
