# src/github.py
import os
import requests
from dotenv import load_dotenv
from ingest.github_ingest import fetch_trending_repos

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def main():
    repos = fetch_trending_repos()
    for repo in repos:
        print(f"{repo['full_name']} - ⭐ {repo['stargazers_count']} stars")

if __name__ == "__main__":
    main()

def search_repositories(query="language:python", sort="stars", order="desc", per_page=5):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": per_page
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code != 200:
        print("Error:", data)
    else:
        for repo in data.get("items", []):
            print(f"{repo['full_name']} ⭐ {repo['stargazers_count']}")

if __name__ == "__main__":
    search_repositories()
