from sqlalchemy import Column, Integer, String, Text, DateTime
from db.database import Base  # ✅ Use shared Base

class GitHubRepo(Base):
    __tablename__ = "github_repos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)
    stars = Column(Integer)
    description = Column(Text)
    language = Column(String)
    timestamp = Column(DateTime)

class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    score = Column(Integer)
    url = Column(String)
    subreddit = Column(String)
    timestamp = Column(DateTime)

class TechNews(Base):
    __tablename__ = "tech_news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    summary = Column(Text)
    sentiment = Column(String)
    url = Column(String)
    published_at = Column(String)
