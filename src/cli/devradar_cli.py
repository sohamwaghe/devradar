# src/cli/devradar_cli.py

import argparse
import os  # ✅ Fix: import os to use os.getenv
from ingest.github_ingest import fetch_top_repos
from ingest.reddit_ingest import fetch_top_posts
from ingest.news_ingest import fetch_tech_news
from transform.reddit_transform import normalize_posts
from transform.news_transform import summarize_text, get_sentiment_label

def show_github():
    repos = fetch_top_repos(limit=5)
    for repo in repos:
        print(f"{repo['name']} - ⭐ {repo['stars']} - {repo['url']}")

def show_reddit():
    posts = normalize_posts(fetch_top_posts(limit=5))
    for post in posts:
        print(f"{post['title']} - 👍 {post['score']}")

def show_news():
    api_key = os.getenv("NEWSDATA_API_KEY")  # ✅ use getenv safely
    if not api_key:
        print("❌ Error: NEWSDATA_API_KEY not found in environment.")
        return

    news = fetch_tech_news(api_key=api_key, limit=5)
    for article in news:
        summary = summarize_text(article["description"])
        sentiment = get_sentiment_label(article["description"])
        print(f"\n📌 {article['title']} ({sentiment})")
        print(f"🧠 {summary}")
        print(f"🔗 {article['link']}\n")

def main():
    parser = argparse.ArgumentParser(description="DevRadar CLI - Get quick trends from GitHub, Reddit, News")
    parser.add_argument("--github", action="store_true", help="Show top GitHub repos")
    parser.add_argument("--reddit", action="store_true", help="Show top Reddit posts")
    parser.add_argument("--news", action="store_true", help="Show top tech news")

    args = parser.parse_args()

    if args.github:
        show_github()
    elif args.reddit:
        show_reddit()
    elif args.news:
        show_news()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
