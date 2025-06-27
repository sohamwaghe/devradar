from nicegui import ui
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///devradar.db")

# === Layout grid ===
with ui.row().classes("w-full"):
    ui.label("📊 DevRadar - Developer Trend Dashboard").classes("text-2xl font-bold")
with ui.row().classes("w-full mb-4"):
    ui.label("Track trending GitHub repos, Reddit posts, and tech news.").classes("text-md text-gray-500")

with ui.grid(columns=2).classes("w-full gap-6"):
    
    # === Quadrant 1: Welcome ===
    with ui.card().classes("p-4"):
        ui.label("👋 Welcome to DevRadar").classes("text-xl font-semibold")
        ui.label("This dashboard tracks the pulse of the developer world in real-time.")
        ui.label("Explore trending GitHub projects, Reddit dev discussions, and recent tech news — all from one place.")

    # === Quadrant 2: GitHub Repos ===
    with ui.card().classes("p-4"):
        ui.label("🔥 Trending GitHub Repositories").classes("text-xl font-semibold")

        lang_df = pd.read_sql("SELECT DISTINCT language FROM github_repos WHERE language IS NOT NULL", engine)
        languages = ["All"] + sorted(lang_df["language"].dropna().unique())

        selected_lang = ui.select(languages, value="All", label="Filter by Language").classes("w-full")

        github_container = ui.column()

        def update_github():
            github_container.clear()
            query = "SELECT name, url, stars, description, language, timestamp FROM github_repos"
            if selected_lang.value != "All":
                query += f" WHERE language = '{selected_lang.value}'"
            df = pd.read_sql(query, engine).sort_values("stars", ascending=False).drop_duplicates("name")

            for _, row in df.iterrows():
                with github_container:
                    ui.markdown(f"**[{row['name']}]({row['url']})** ⭐ {row['stars']}")
                    if row["description"]:
                        ui.label(row["description"])
                    ui.label(f"{row['language']} | {row['timestamp']}").classes("text-sm text-gray-400")
                    ui.separator()

        selected_lang.on("update:model-value", lambda _: update_github())
        update_github()

    # === Quadrant 3: Reddit ===
    with ui.card().classes("p-4"):
        ui.label("👽 Top Reddit Dev Posts").classes("text-xl font-semibold")

        reddit_df = pd.read_sql("SELECT title, url, subreddit, score, created_utc FROM reddit_posts ORDER BY score DESC LIMIT 10", engine)
        for _, row in reddit_df.iterrows():
            ui.markdown(f"**[{row['title']}]({row['url']})** ⬆️ {row['score']}")
            ui.label(f"r/{row['subreddit']} | {row['created_utc']}").classes("text-sm text-gray-400")
            ui.separator()

    # === Quadrant 4: Tech News ===
    with ui.card().classes("p-4"):
        ui.label("📰 Latest Tech News").classes("text-xl font-semibold")

        news_df = pd.read_sql("SELECT title, url, summary, source, published_at, sentiment FROM tech_news ORDER BY published_at DESC LIMIT 10", engine)
        for _, row in news_df.iterrows():
            ui.markdown(f"**[{row['title']}]({row['url']})**")
            if row["summary"]:
                ui.label(row["summary"])
            ui.label(f"🗞 {row['source']} | {row['published_at']} | Sentiment: {row['sentiment']}").classes("text-sm text-gray-400")
            ui.separator()

ui.run(title="DevRadar Dashboard", reload=False)
