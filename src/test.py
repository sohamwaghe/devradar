from ingest.github_ingest import fetch_top_repos
from storage.github_storage import save_github_to_db

repos = fetch_top_repos(limit=5)
save_github_to_db(repos)
