# src/reddit.py

import os
from dotenv import load_dotenv
from ingest.reddit_ingest import fetch_top_posts
from storage.reddit_storage import save_posts_to_json
from transform.reddit_transform import normalize_posts

load_dotenv()

def main():
    # Step 1: Fetch raw Reddit posts
    raw_posts = fetch_top_posts(subreddit_name="programming", limit=5, time_filter="day")

    # Step 2: Normalize them
    normalized_posts = normalize_posts(raw_posts)

    # Step 3: Print a preview
    for post in normalized_posts:
        print(f"{post['title']} - 👍 {post['score']}")

    # Step 4: Save to JSON
    save_posts_to_json(normalized_posts)

if __name__ == "__main__":
    main()
