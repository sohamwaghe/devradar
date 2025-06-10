# src/transform/reddit_transform.py

def normalize_posts(posts):
    normalized = []
    for post in posts:
        normalized.append({
            "id": post["id"],
            "title": post["title"],
            "score": post["score"],
            "url": post["url"],
            "author": post["author"],
            "num_comments": post["num_comments"],
            "created_utc": post["created_utc"],
            "subreddit": post["subreddit"]
        })
    return normalized
