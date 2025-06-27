from nicegui import ui
import pandas as pd
from sqlalchemy import create_engine

# SQLite connection
engine = create_engine("sqlite:///devradar.db")

# Page header
with ui.row().classes('w-full justify-between items-center'):
    ui.label('📊 DevRadar - Developer Trend Dashboard').classes('text-2xl font-bold')
    ui.label('Track trending GitHub repos, Reddit posts, and tech news.').classes('text-md text-gray-500')

# Section selector (GitHub / Reddit / Tech News)
section_selector = ui.radio(["GitHub", "Reddit", "Tech News"], value="GitHub").props('inline')
ui.separator()

# Main content container
main_content = ui.column().classes('w-full')

# === GitHub Section ===
def show_github_section():
    main_content.clear()
    ui.label("🔥 Trending GitHub Repositories").classes('text-xl font-semibold')

    lang_df = pd.read_sql("SELECT DISTINCT language FROM github_repos WHERE language IS NOT NULL", engine)
    languages = ["All"] + sorted(lang_df["language"].dropna().unique())

    selected_lang = ui.select(languages, value="All", label="Filter by Language").classes('w-64')

    table_container = ui.column().classes('w-full')

    def update_table():
        table_container.clear()
        query = "SELECT name, url, stars, description, language, timestamp FROM github_repos"
        if selected_lang.value != "All":
            query += f" WHERE language = '{selected_lang.value}'"

        df = pd.read_sql(query, engine)
        df = df.sort_values("stars", ascending=False).drop_duplicates("name")

        for _, row in df.iterrows():
            with table_container:
                ui.markdown(f"**[{row['name']}]({row['url']})**  ⭐ {row['stars']}")
                if row["description"]:
                    ui.label(row["description"])
                ui.label(f"Language: {row['language']} | Updated: {row['timestamp']}").classes('text-sm text-gray-400')
                ui.separator()

    selected_lang.on('update:model-value', lambda _: update_table())
    update_table()

# === Reddit Section ===
def show_reddit_section():
    main_content.clear()
    ui.label("👽 Top Reddit Posts about Developer Tools").classes('text-xl font-semibold')

    df = pd.read_sql("SELECT title, url, subreddit, score, created_utc FROM reddit_posts ORDER BY score DESC LIMIT 25", engine)

    for _, row in df.iterrows():
        with main_content:
            ui.markdown(f"**[{row['title']}]({row['url']})**  ⬆️ {row['score']}")
            ui.label(f"Subreddit: r/{row['subreddit']} | Posted: {row['created_utc']}").classes('text-sm text-gray-400')
            ui.separator()

# === Tech News Section ===
def show_tech_news_section():
    main_content.clear()
    ui.label("📰 Latest Tech News").classes('text-xl font-semibold')

    df = pd.read_sql("SELECT title, url, summary, source, published_at, sentiment FROM tech_news ORDER BY published_at DESC LIMIT 25", engine)

    for _, row in df.iterrows():
        with main_content:
            ui.markdown(f"**[{row['title']}]({row['url']})**")
            if row['summary']:
                ui.label(row['summary'])
            ui.label(f"🗞️ {row['source']} | {row['published_at']} | Sentiment: {row['sentiment']}").classes('text-sm text-gray-400')
            ui.separator()

# === Section switch handler ===
def update_section(e):
    selected = e.args  # this is the correct way to access the new value
    if selected == "GitHub":
        show_github_section()
    elif selected == "Reddit":
        show_reddit_section()
    elif selected == "Tech News":
        show_tech_news_section()


section_selector.on('update:model-value', update_section)

# Initial view
show_github_section()

# Run the app
ui.run(title="DevRadar Dashboard", reload=False)
