# src/news.py

from ingest.news_ingest import fetch_tech_news
from transform.news_transform import summarize_text, analyze_sentiment
from storage.news_storage import save_news_to_json

def main():
    raw_articles = fetch_tech_news(limit=5)
    enriched_news = []

    for article in raw_articles:
        summary = summarize_text(article["description"])
        sentiment = analyze_sentiment(article["description"])
        enriched_news.append({
            "title": article["title"],
            "link": article["link"],
            "summary": summary,
            "sentiment_score": sentiment,
            "published": article["pubDate"]
        })

    for item in enriched_news:
        print(f"\n📌 {item['title']}\n🧠 {item['summary']}\n❤️ Sentiment: {item['sentiment_score']}\n🔗 {item['link']}\n")

    save_news_to_json(enriched_news)

if __name__ == "__main__":
    main()
