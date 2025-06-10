# src/ingest/reddit_ingest.py

import os
import praw
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_top_posts(subreddit_name="programming", limit=10, time_filter="day"):
    logger.info(f"Fetching top {limit} posts from r/{subreddit_name}")
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.top(limit=limit, time_filter=time_filter):
            posts.append({
                "id": post.id,
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "created_utc": post.created_utc,
                "num_comments": post.num_comments,
                "author": str(post.author),
                "subreddit": subreddit_name
            })
        logger.info(f"Fetched {len(posts)} posts from r/{subreddit_name}")
        return posts
    except Exception as e:
        logger.error(f"Error fetching posts from r/{subreddit_name}: {e}")
        return []
