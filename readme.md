🚀 DevRadar - Real-time Developer Intelligence Dashboard

A full-stack Python application that aggregates trending GitHub repositories, Reddit discussions, and tech news into a unified, real-time dashboard for developers.



🎯 Project Overview
DevRadar solves the problem of information overload in the fast-paced tech world. Instead of checking GitHub trending, multiple subreddits, and tech news sites separately, developers get a single, beautiful dashboard with real-time updates.
✨ Key Features

🔥 Smart Trending Algorithm: Not just popular repos, but actually trending ones using multi-strategy analysis
💬 Community Insights: Real-time Reddit discussions from r/programming and other dev communities
📰 Tech News Pulse: Latest tech news with AI-powered sentiment analysis
🎨 Modern UI: Glassmorphism design with dark theme and responsive layout
⚡ Real-time Updates: Auto-refresh every 5 minutes with manual refresh option
🛡️ Production-Ready: Comprehensive error handling, rate limiting, and graceful degradation
📊 Live Analytics: Real-time stats and data freshness indicators

🏗️ Architecture
DevRadar/
├── 📁 src/
│   ├── 📁 ingest/          # API data collection
│   │   ├── github_ingest.py    # GitHub trending repos
│   │   ├── reddit_ingest.py    # Reddit posts
│   │   └── news_ingest.py      # Tech news
│   ├── 📁 storage/         # Data persistence layer
│   ├── 📁 transform/       # Data processing
│   ├── 📁 flows/           # Prefect workflows
│   └── 📁 dashboard/       # Frontend application
├── 📄 requirements.txt     # Dependencies
└── 📄 devradar.db         # SQLite database
🛠️ Tech Stack
LayerTechnologyPurposeFrontendNiceGUI + PythonModern, reactive web interfaceBackendPython + SQLAlchemyAPI integration and data processingDatabaseSQLiteLightweight, embedded databaseOrchestrationPrefectAutomated data pipeline schedulingAPIsGitHub REST, Reddit, News APIsReal-time data sourcesAnalyticsVaderSentimentNews sentiment analysis
🚀 Quick Start
Prerequisites

Python 3.10+
Git
10 minutes of your time

Installation

Clone the repository
bashgit clone https://github.com/yourusername/devradar.git
cd devradar

Set up virtual environment
bashpython -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

Install dependencies
bashpip install -r requirements.txt

Configure API keys
bashcp .env.example .env
# Edit .env with your API keys

Run the dashboard
bashpython src/dashboard/app.py

Open your browser
http://localhost:8080


🔑 Environment Setup
Create a .env file in the project root:
env# GitHub (Required)
GITHUB_TOKEN=your_github_personal_access_token

# Reddit (Required)  
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=DevRadar/1.0

# News API (Optional)
NEWS_API_KEY=your_news_api_key
Getting API Keys

GitHub Token: github.com/settings/tokens → Personal access tokens
Reddit API: reddit.com/prefs/apps → Create app
News API: newsapi.org → Get API key

📊 Features Deep Dive
GitHub Trending Intelligence

New Trending: Repos created in the last 30 days gaining traction
Recently Active: Established repos with recent commits
Language Filtering: Focus on specific programming languages
Smart Deduplication: Removes duplicate entries across strategies

Reddit Community Pulse

Real-time Posts: Latest discussions from developer communities
Score-based Ranking: Surface the most engaging conversations
Multiple Subreddits: r/programming, r/webdev, r/MachineLearning, etc.

Tech News with Sentiment

AI-Powered Analysis: Sentiment classification (Positive/Negative/Neutral)
Multiple Sources: TechCrunch, Hacker News, Dev.to, etc.
Smart Summarization: Condensed, relevant summaries

🎨 UI/UX Features

🌙 Dark Theme: Easy on developer eyes
💫 Glassmorphism: Modern, professional aesthetic
📱 Responsive: Works on desktop, tablet, and mobile
⚡ Live Updates: Real-time data refresh without page reload
🎯 Status Indicators: Data freshness and system health
🔄 Manual Refresh: Force update with loading states

🚦 Development Workflow
Running in Development
bash# Start the dashboard
python src/dashboard/app.py

# Run data pipeline manually
python src/flows/devradar_flow.py

# Test individual ingest modules
python src/ingest/github_ingest.py
Data Pipeline
The application uses Prefect for automated data collection:
python# Runs every 15 minutes
@flow
def devradar_pipeline():
    github_data = fetch_github_repos()
    reddit_data = fetch_reddit_posts() 
    news_data = fetch_tech_news()
    
    store_data(github_data, reddit_data, news_data)
🔧 Production Deployment
Docker (Recommended)
bash# Build image
docker build -t devradar .

# Run container
docker run -p 8080:8080 --env-file .env devradar
Manual Deployment
bash# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8080 src.dashboard.app:app
📈 Monitoring & Observability

📊 Built-in Analytics: Track data freshness and API health
📝 Comprehensive Logging: Debug issues with detailed logs
⚠️ Error Handling: Graceful degradation when APIs are down
🔄 Auto-Recovery: Automatic retry logic for failed requests

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

🐛 Troubleshooting
Common Issues
Port already in use (8080)
bash# Kill existing processes
lsof -ti:8080 | xargs kill -9

# Or use different port
python src/dashboard/app.py --port 8081
Database locked
bash# Reset database
rm devradar.db
python src/flows/devradar_flow.py
API rate limits

Check your .env file has valid tokens
GitHub: 5000 requests/hour with token
Reddit: 60 requests/minute

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

GitHub API for repository data
Reddit API for community discussions
Various News APIs for tech news
NiceGUI for the beautiful Python web framework
Prefect for workflow orchestration

📞 Contact
Your Name - sohamwaghe47@gmail.com
Project Link: https://github.com/sohamwaghe/devradar

<div align="center">
⭐ If this project helped you, please give it a star! ⭐
Made with ❤️ and lots of ☕ by [Your Name]
</div>