# src/storage/reddit_storage.py

from db.database import SessionLocal
from db.models import RedditPost
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

def save_reddit_to_db(posts):
    session = SessionLocal()
    try:
        for post in posts:
            record = RedditPost(
                title=post["title"],
                score=post["score"],
                url=post["url"],
                subreddit=post["subreddit"],
                timestamp=datetime.utcnow()
            )
            session.add(record)
        session.commit()
        logger.info(f"Saved {len(posts)} Reddit posts to database.")
    except Exception as e:
        logger.error(f"Error saving Reddit posts: {e}")
        session.rollback()
    finally:
        session.close()
