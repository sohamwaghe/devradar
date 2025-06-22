# src/storage/db_helpers.py

from db.models import GitHubRepo, RedditPost, TechNews
from db.database import SessionLocal
from datetime import datetime

def save_github_to_db(repos):
    session = SessionLocal()
    try:
        for repo in repos:
            db_repo = GitHubRepo(
                name=repo["name"],
                url=repo["url"],
                stars=repo["stars"],  # ✅ this key must match exactly
                description=repo.get("description", ""),
                language=repo.get("language", ""),
                timestamp=repo["timestamp"]
            )
            session.add(db_repo)
        session.commit()
        print(f"✅ Saved {len(repos)} GitHub repos to DB.")
    except Exception as e:
        print(f"❌ Error saving GitHub repos: {e}")
        session.rollback()
    finally:
        session.close()

def save_reddit_to_db(posts):
    session = SessionLocal()
    try:
        for post in posts:
            entry = RedditPost(
                title=post["title"],
                score=post["score"],
                url=post["url"],
                subreddit=post.get("subreddit", ""),
                timestamp=datetime.utcnow()
            )
            session.add(entry)
        session.commit()
        print(f"✅ Saved {len(posts)} Reddit posts to DB.")
    except Exception as e:
        print(f"❌ Error saving Reddit posts: {e}")
        session.rollback()
    finally:
        session.close()

def save_news_to_db(news_items):
    session = SessionLocal()
    try:
        for article in news_items:
            entry = TechNews(
                title=article["title"],
                summary=article["summary"],
                sentiment=article["sentiment"],
                url=article["url"],
                published_at=article.get("published_at", datetime.utcnow().isoformat())
            )
            session.add(entry)
        session.commit()
        print(f"✅ Saved {len(news_items)} news articles to DB.")
    except Exception as e:
        print(f"❌ Error saving news: {e}")
        session.rollback()
    finally:
        session.close()
