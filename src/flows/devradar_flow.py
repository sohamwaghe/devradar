# src/flows/devradar_flow.py

import os
from dotenv import load_dotenv
from prefect import flow, task
from ingest.github_ingest import fetch_top_repos
from ingest.reddit_ingest import fetch_top_posts
from ingest.news_ingest import fetch_tech_news
from transform.reddit_transform import normalize_posts
from transform.news_transform import summarize_text, get_sentiment_label
from storage.db_helpers import save_github_to_db, save_reddit_to_db, save_news_to_db
load_dotenv()

@task
def ingest_github():
    repos = fetch_top_repos()
    save_github_to_db(repos)

@task
def ingest_reddit():
    posts = normalize_posts(fetch_top_posts())
    save_reddit_to_db(posts)

@task
def ingest_news():
    api_key = os.getenv("NEWSDATA_API_KEY")
    articles = fetch_tech_news(api_key=api_key, limit=5)

    cleaned_articles = []
    for article in articles:
        summary = summarize_text(article.get("description", ""))
        sentiment = get_sentiment_label(article.get("description", ""))
        cleaned_articles.append({
            "title": article.get("title", ""),
            "summary": summary,
            "sentiment": sentiment,
            "url": article.get("link", ""),  # map correctly
            "published_at": article.get("pubDate", "")
        })

    save_news_to_db(cleaned_articles)


@flow(name="DevRadar Ingestion Flow")
def devradar_pipeline():
    ingest_github()
    ingest_reddit()
    ingest_news()

if __name__ == "__main__":
    devradar_pipeline()
