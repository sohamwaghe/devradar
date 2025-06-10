# src/transform/github_transform.py

def normalize_repo(repo):
    return {
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "url": repo.get("html_url"),
        "description": repo.get("description"),
        "stars": repo.get("stargazers_count"),
        "language": repo.get("language"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "topics": repo.get("topics", [])
    }

def normalize_repos(repos):
    return [normalize_repo(repo) for repo in repos]
