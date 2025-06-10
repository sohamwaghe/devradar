# src/github.py

import os
from dotenv import load_dotenv

from ingest.github_ingest import fetch_trending_repos
from storage.github_storage import save_repos_to_json
from transform.github_transform import normalize_repos

load_dotenv()

def main():
    # Step 1: Fetch raw GitHub repos
    raw_repos = fetch_trending_repos()

    # Step 2: Normalize repo data
    normalized = normalize_repos(raw_repos)

    # Step 3: Print summary
    for repo in normalized:
        print(f"{repo['full_name']} - ⭐ {repo['stars']} stars")

    # Step 4: Save to JSON
    save_repos_to_json(normalized)

if __name__ == "__main__":
    main()
