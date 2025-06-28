# 📊 DevRadar

DevRadar is a lightweight developer trend dashboard that tracks the pulse of the programming world in real-time. It aggregates data from GitHub, Reddit, and tech news sources, giving you a single place to monitor what developers are building, discussing, and reading.

---

## 🚀 Features

- 🔥 **Trending GitHub Repositories**  
  View top-starred open-source projects, filterable by programming language.

- 👽 **Popular Reddit Developer Posts**  
  Track the most upvoted posts from subreddits like `r/programming` and `r/learnprogramming`.

- 📰 **Latest Tech News Summaries**  
  Stay updated with summarized news articles and sentiment analysis.

- 🔄 **One-Click Refresh**  
  Refresh your dashboard on demand using Prefect-powered backend ingestion.

---

## 🛠️ Tech Stack

| Layer        | Tools Used                               |
|--------------|-------------------------------------------|
| UI           | [NiceGUI](https://nicegui.io)            |
| Backend      | Python, Prefect, SQLAlchemy               |
| Database     | SQLite (easily switchable to PostgreSQL) |
| NLP          | Sumy (summarization), Vader (sentiment)  |
| Data Sources | GitHub API, Reddit API (PRAW), NewsData.io API |

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/devradar.git
cd devradar

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your NewsData.io API key
echo NEWSDATA_API_KEY=your_api_key >> .env

# 5. Run the dashboard
python -m src.dashboard.app
