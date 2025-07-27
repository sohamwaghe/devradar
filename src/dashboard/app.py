from nicegui import ui
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import asyncio
import logging
# from flows.devradar_flow import devradar_pipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for modern look
ui.add_head_html('''
<style>
    body { background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); }
    .main-container { backdrop-filter: blur(10px); }
    .glass-card { 
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
    }
    .gradient-text {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .neon-border {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        border: 1px solid rgba(102, 126, 234, 0.5) !important;
    }
    .trending-badge {
        background: linear-gradient(45deg, #ff6b6b, #ffa500);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .error-state {
        background: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
    }
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
''')

engine = create_engine("sqlite:///devradar.db")

# Global state for auto-refresh
last_update_time = datetime.now()
is_refreshing = False

# Safe data loading with error handling
def safe_load_data(query, fallback_message="No data available"):
    """Safely load data from database with error handling"""
    try:
        df = pd.read_sql(query, engine)
        if df.empty:
            logger.warning(f"Empty result for query: {query[:50]}...")
            return None
        return df
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        ui.notify(f"⚠️ {fallback_message}", type="warning", timeout=3000)
        return None

# Get stats with error handling
def get_dashboard_stats():
    """Get dashboard statistics safely"""
    try:
        stats = {}
        
        # GitHub stats
        github_df = safe_load_data("SELECT COUNT(*) as count, MAX(timestamp) as last_update FROM github_repos")
        stats['github_count'] = github_df.iloc[0]['count'] if github_df is not None else 0
        stats['github_last_update'] = github_df.iloc[0]['last_update'] if github_df is not None else "Never"
        
        # Reddit stats  
        reddit_df = safe_load_data("SELECT COUNT(*) as count FROM reddit_posts")
        stats['reddit_count'] = reddit_df.iloc[0]['count'] if reddit_df is not None else 0
        
        # News stats
        news_df = safe_load_data("SELECT COUNT(*) as count FROM tech_news")
        stats['news_count'] = news_df.iloc[0]['count'] if news_df is not None else 0
        
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return {'github_count': 0, 'reddit_count': 0, 'news_count': 0, 'github_last_update': 'Error'}

# Initialize stats
dashboard_stats = get_dashboard_stats()

# === HEADER WITH STATS ===
with ui.row().classes("w-full justify-between items-center mb-8 p-6"):
    with ui.column():
        ui.label("🚀 DevRadar").classes("text-4xl font-bold gradient-text")
        ui.label("Real-time developer intelligence dashboard").classes("text-lg text-gray-300")
    
    # Live stats cards with refresh indicator
    stats_container = ui.row().classes("gap-4")
    
    def update_stats_display():
        """Update the stats display"""
        global dashboard_stats
        stats_container.clear()
        
        with stats_container:
            with ui.card().classes("glass-card p-3 text-center"):
                ui.label(str(dashboard_stats['github_count'])).classes("text-2xl font-bold text-blue-400")
                ui.label("Repos Tracked").classes("text-xs text-gray-400")
            
            with ui.card().classes("glass-card p-3 text-center"):
                ui.label(str(dashboard_stats['reddit_count'])).classes("text-2xl font-bold text-orange-400")
                ui.label("Reddit Posts").classes("text-xs text-gray-400")
            
            with ui.card().classes("glass-card p-3 text-center"):
                ui.label(str(dashboard_stats['news_count'])).classes("text-2xl font-bold text-green-400")
                ui.label("News Articles").classes("text-xs text-gray-400")
            
            # Last updated indicator
            with ui.card().classes("glass-card p-3 text-center"):
                last_update_str = dashboard_stats.get('github_last_update', 'Never')
                if last_update_str and last_update_str != 'Never':
                    try:
                        last_update_dt = datetime.fromisoformat(str(last_update_str).replace('Z', '+00:00'))
                        time_diff = datetime.now() - last_update_dt.replace(tzinfo=None)
                        if time_diff.seconds < 300:  # Less than 5 minutes
                            status_color = "text-green-400"
                            status_text = "LIVE"
                        elif time_diff.seconds < 3600:  # Less than 1 hour
                            status_color = "text-yellow-400" 
                            status_text = f"{time_diff.seconds//60}m ago"
                        else:
                            status_color = "text-red-400"
                            status_text = "STALE"
                    except:
                        status_color = "text-gray-400"
                        status_text = "Unknown"
                else:
                    status_color = "text-gray-400"
                    status_text = "No data"
                
                ui.label(status_text).classes(f"text-lg font-bold {status_color}")
                ui.label("Data Status").classes("text-xs text-gray-400")

update_stats_display()

# === MAIN DASHBOARD GRID ===
with ui.grid(columns="1fr 1fr").classes("w-full gap-6 p-6"):

    # === TRENDING GITHUB REPOS ===
    with ui.card().classes("glass-card neon-border p-6"):
        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label("🔥 Trending This Week").classes("text-2xl font-bold text-white")
            ui.html('<span class="trending-badge">LIVE</span>')
        
        # Language filter with modern styling
        try:
            lang_df = safe_load_data("SELECT DISTINCT language FROM github_repos WHERE language IS NOT NULL")
            languages = ["All"] + sorted(lang_df["language"].dropna().unique()) if lang_df is not None else ["All"]
        except:
            languages = ["All", "Python", "JavaScript", "Go", "Rust"]
        
        selected_lang = ui.select(languages, value="All", label="Language").classes("w-full").props("dark outlined")
        github_container = ui.column().classes("gap-3 mt-4")

        def update_github():
            """Update GitHub repos section with error handling"""
            github_container.clear()
            
            try:
                # Show loading state
                with github_container:
                    ui.html('<div class="loading-spinner"></div>')
                    ui.label("Loading trending repos...").classes("text-center text-gray-400")
                
                # Load data
                query = "SELECT name, url, stars, description, language, timestamp FROM github_repos"
                if selected_lang.value != "All":
                    query += f" WHERE language = '{selected_lang.value}'"
                
                df = safe_load_data(query)
                
                # Clear loading state
                github_container.clear()
                
                if df is None or df.empty:
                    with github_container:
                        with ui.card().classes("error-state p-4 text-center"):
                            ui.label("⚠️ No GitHub data available").classes("text-yellow-400 font-bold")
                            ui.label("Try refreshing or check your data pipeline").classes("text-gray-400 text-sm")
                    return
                
                # Process data
                df = df.sort_values("stars", ascending=False).drop_duplicates("name").head(5)

                for i, row in df.iterrows():
                    with github_container:
                        with ui.card().classes("bg-gray-800 p-4 hover:bg-gray-700 transition-colors"):
                            with ui.row().classes("w-full justify-between items-start"):
                                with ui.column().classes("flex-grow"):
                                    # Repo name and stars
                                    with ui.row().classes("items-center gap-2"):
                                        ui.html(f'<a href="{row["url"]}" target="_blank" class="text-blue-400 hover:text-blue-300 font-bold text-lg no-underline">{row["name"]}</a>')
                                        ui.html(f'<span class="bg-yellow-500 text-black px-2 py-1 rounded text-sm">⭐ {row["stars"]:,}</span>')
                                    
                                    # Description
                                    if row["description"]:
                                        desc = str(row["description"])[:100] + "..." if len(str(row["description"])) > 100 else str(row["description"])
                                        ui.label(desc).classes("text-gray-300 text-sm mt-1")
                                    
                                    # Language and time
                                    ui.html(f'<span class="text-xs text-gray-500">{row["language"]} • {str(row["timestamp"])[:19]}</span>')
                                
                                # Trending indicator
                                ui.html('<div class="text-2xl">📈</div>')
                        
            except Exception as e:
                logger.error(f"Error updating GitHub section: {str(e)}")
                github_container.clear()
                with github_container:
                    with ui.card().classes("error-state p-4 text-center"):
                        ui.label("❌ Error loading GitHub data").classes("text-red-400 font-bold")
                        ui.label(f"Error: {str(e)[:100]}").classes("text-gray-400 text-sm")

        selected_lang.on("update:model-value", lambda _: update_github())
        update_github()

    # === REDDIT HOT TAKES ===
    with ui.card().classes("glass-card p-6"):
        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label("💬 Dev Community Buzz").classes("text-2xl font-bold text-white")
            ui.html('<span style="background: linear-gradient(45deg, #ff4500, #ff8c00); border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: bold;">r/programming</span>')
        
        reddit_container = ui.column().classes("gap-3")
        
        def update_reddit():
            """Update Reddit section with error handling"""
            reddit_container.clear()
            
            try:
                df = safe_load_data("SELECT title, url, subreddit, score, created_utc FROM reddit_posts ORDER BY score DESC")
                
                if df is None or df.empty:
                    with reddit_container:
                        with ui.card().classes("error-state p-4 text-center"):
                            ui.label("⚠️ No Reddit data available").classes("text-yellow-400 font-bold")
                    return
                
                df = df.drop_duplicates(subset="title").head(5)
                
                for i, row in df.iterrows():
                    with reddit_container:
                        with ui.card().classes("bg-gray-800 p-4 hover:bg-gray-700 transition-colors"):
                            with ui.row().classes("w-full justify-between items-start"):
                                with ui.column().classes("flex-grow"):
                                    title = str(row["title"])[:80] + "..." if len(str(row["title"])) > 80 else str(row["title"])
                                    ui.html(f'<a href="{row["url"]}" target="_blank" class="text-orange-400 hover:text-orange-300 font-semibold no-underline">{title}</a>')
                                    ui.html(f'<span class="text-xs text-gray-500">r/{row["subreddit"]} • Score: {row["score"]}</span>')
                                
                                # Score-based indicator
                                if row["score"] > 500:
                                    ui.html('<div class="text-xl">🔥</div>')
                                elif row["score"] > 200:
                                    ui.html('<div class="text-xl">📈</div>')
                                else:
                                    ui.html('<div class="text-xl">💬</div>')
                    
            except Exception as e:
                logger.error(f"Error updating Reddit section: {str(e)}")
                with reddit_container:
                    with ui.card().classes("error-state p-4 text-center"):
                        ui.label("❌ Error loading Reddit data").classes("text-red-400 font-bold")

        update_reddit()

# === NEWS SECTION (Full Width) ===
with ui.card().classes("glass-card p-6 mx-6 mb-6"):
    with ui.row().classes("w-full justify-between items-center mb-4"):
        ui.label("📰 Tech Pulse").classes("text-2xl font-bold text-white")
        ui.html('<span style="background: linear-gradient(45deg, #00ff88, #00d4ff); border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: bold; color: black;">AI • BLOCKCHAIN • STARTUPS</span>')
    
    news_container = ui.grid(columns=2).classes("gap-4")
    
    def update_news():
        """Update news section with error handling"""
        news_container.clear()
        
        try:
            df = safe_load_data("SELECT title, url, summary, source, published_at, sentiment FROM tech_news ORDER BY published_at DESC")
            
            if df is None or df.empty:
                with news_container:
                    with ui.card().classes("error-state p-4 text-center col-span-2"):
                        ui.label("⚠️ No tech news available").classes("text-yellow-400 font-bold")
                return
            
            df = df.drop_duplicates("title").head(6)
            
            for i, row in df.iterrows():
                with news_container:
                    with ui.card().classes("bg-gray-800 p-4 hover:bg-gray-700 transition-colors"):
                        # Sentiment badge
                        sentiment = str(row.get("sentiment", "Neutral"))
                        sentiment_colors = {"Positive": "green", "Negative": "red", "Neutral": "yellow"}
                        color = sentiment_colors.get(sentiment, "gray")
                        ui.html(f'<span class="bg-{color}-500 text-white px-2 py-1 rounded text-xs mb-2 inline-block">{sentiment}</span>')
                        
                        # Title
                        title = str(row["title"])[:100] + "..." if len(str(row["title"])) > 100 else str(row["title"])
                        ui.html(f'<a href="{row["url"]}" target="_blank" class="text-green-400 hover:text-green-300 font-semibold no-underline block mb-2">{title}</a>')
                        
                        # Summary
                        if row["summary"]:
                            summary = str(row["summary"])[:120] + "..." if len(str(row["summary"])) > 120 else str(row["summary"])
                            ui.label(summary).classes("text-gray-300 text-sm mb-2")
                        
                        # Time
                        ui.html(f'<span class="text-xs text-gray-500">{str(row["published_at"])[:19]}</span>')
        
        except Exception as e:
            logger.error(f"Error updating news section: {str(e)}")
            with news_container:
                with ui.card().classes("error-state p-4 text-center col-span-2"):
                    ui.label("❌ Error loading news data").classes("text-red-400 font-bold")

    update_news()

# === AUTO-REFRESH FUNCTIONALITY ===
async def auto_refresh_data():
    """Auto refresh data every 5 minutes"""
    global is_refreshing, dashboard_stats, last_update_time
    
    if is_refreshing:
        return
    
    is_refreshing = True
    
    try:
        logger.info("Auto-refreshing dashboard data...")
        
        # Update stats
        dashboard_stats = get_dashboard_stats()
        update_stats_display()
        
        # Update sections
        update_github()
        update_reddit() 
        update_news()
        
        last_update_time = datetime.now()
        ui.notify("📊 Dashboard updated", type="positive", timeout=2000)
        
    except Exception as e:
        logger.error(f"Auto-refresh failed: {str(e)}")
        ui.notify("⚠️ Auto-refresh failed", type="warning", timeout=3000)
    
    finally:
        is_refreshing = False

# Set up auto-refresh timer (5 minutes = 300 seconds)
ui.timer(300, auto_refresh_data)

# === MANUAL REFRESH BUTTON ===
def manual_refresh():
    """Manual refresh with loading dialog"""
    global is_refreshing
    
    if is_refreshing:
        ui.notify("⏳ Refresh already in progress", type="info")
        return
    
    with ui.dialog() as dialog, ui.card().classes("glass-card p-6"):
        ui.label("🔄 Refreshing live data...").classes("text-lg text-white")
        ui.html('<div class="loading-spinner mt-4"></div>')
        dialog.open()
        
        async def do_refresh():
            try:
                # Run pipeline if available
                # devradar_pipeline()  # Uncomment when ready
                await auto_refresh_data()
                ui.notify("✅ Manual refresh complete!", type="positive")
            except Exception as e:
                ui.notify(f"❌ Refresh failed: {str(e)}", type="negative")
            finally:
                dialog.close()
        
        ui.run_javascript('setTimeout(() => {}, 1000)')  # Small delay for UX
        asyncio.create_task(do_refresh())

ui.button("🔄 Refresh Live Data", on_click=manual_refresh).classes("fixed bottom-6 right-6 z-50").props("fab color=primary")

# === FOOTER WITH STATUS ===
with ui.row().classes("w-full justify-between items-center p-4 text-gray-400 text-sm"):
    ui.label("Built with 💻 Python • NiceGUI • Prefect • Real-time APIs")
    ui.label(f"Last auto-refresh: {last_update_time.strftime('%H:%M:%S')}")

ui.run(title="DevRadar - Live Developer Intelligence", dark=True, reload=False)