# src/storage/github_storage.py

from db.database import SessionLocal
from db.models import GitHubRepo
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

def save_github_to_db(repos):
    session = SessionLocal()
    try:
        for repo in repos:
            record = GitHubRepo(
                name=repo["name"],
                url=repo["url"],
                stars=repo["stars"],
                description=repo.get("description", ""),
                language=repo.get("language", ""),
                timestamp=datetime.utcnow()
            )
            session.add(record)
        session.commit()
        logger.info(f"Saved {len(repos)} GitHub repos to database.")
    except Exception as e:
        logger.error(f"Error saving GitHub repos: {e}")
        session.rollback()
    finally:
        session.close()
