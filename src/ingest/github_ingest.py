# src/ingest/github_ingest.py

import os
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import logging

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback logger if utils.logger doesn't exist
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def fetch_top_repos(language="python", limit=5):
    """Main function that combines different trending strategies"""
    logger.info(f"Fetching trending repos for language: {language}")
    
    all_repos = []
    
    # Strategy 1: Recently created repos with good traction
    new_trending = fetch_new_trending_repos(language=language, limit=3)
    all_repos.extend(new_trending)
    
    # Strategy 2: Recently active established repos  
    active_repos = fetch_recently_active_repos(language=language, limit=3)
    all_repos.extend(active_repos)
    
    # Strategy 3: Fallback to most starred if above strategies fail
    if len(all_repos) < limit:
        popular_repos = fetch_popular_repos(language=language, limit=limit)
        all_repos.extend(popular_repos)
    
    # Remove duplicates and format
    seen_repos = set()
    formatted_repos = []
    
    for repo in all_repos:
        if repo["name"] not in seen_repos:
            seen_repos.add(repo["name"])
            formatted_repos.append({
                "name": repo.get("full_name"),
                "url": repo.get("html_url"),
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "timestamp": datetime.utcnow(),
                "trending_reason": repo.get("trending_reason", "popular")
            })
    
    return formatted_repos[:limit]


def fetch_new_trending_repos(language="python", limit=5):
    """Get repos created in the last 30 days that are gaining traction"""
    logger.info(f"Fetching new trending repos for {language}")
    
    # Look at last 30 days for new repos
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language} created:>{thirty_days_ago} stars:>10",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    
    repos = make_github_request(url, params)
    
    # Add trending reason
    for repo in repos:
        repo["trending_reason"] = "new_trending"
    
    return repos


def fetch_recently_active_repos(language="python", limit=5):
    """Get established repos that have been active recently"""
    logger.info(f"Fetching recently active repos for {language}")
    
    # Look for repos updated in last 7 days with good star count
    last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language} pushed:>{last_week} stars:>100",
        "sort": "updated",
        "order": "desc",
        "per_page": limit
    }
    
    repos = make_github_request(url, params)
    
    # Add trending reason
    for repo in repos:
        repo["trending_reason"] = "recently_active"
    
    return repos


def fetch_popular_repos(language="python", limit=5):
    """Fallback: Get most popular repos (your original logic)"""
    logger.info(f"Fetching popular repos for {language}")
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    
    repos = make_github_request(url, params)
    
    # Add trending reason
    for repo in repos:
        repo["trending_reason"] = "popular"
    
    return repos


def make_github_request(url, params, max_retries=3):
    """Make GitHub API request with proper error handling and rate limiting"""
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
            
            # Check rate limits
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                
                logger.info(f"GitHub API rate limit: {remaining} requests remaining")
                
                if remaining < 5:
                    wait_time = max(0, reset_time - int(time.time())) + 5
                    logger.warning(f"Rate limit low. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
            
            # Handle different response codes
            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            
            elif response.status_code == 403:
                if 'rate limit' in response.text.lower():
                    logger.error("Rate limit exceeded")
                    if attempt < max_retries - 1:
                        time.sleep(60)  # Wait 1 minute before retry
                        continue
                else:
                    logger.error(f"GitHub API forbidden: {response.text}")
                return []
            
            elif response.status_code == 422:
                logger.error(f"GitHub API validation failed: {response.text}")
                return []
            
            else:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                return []
                
        except requests.exceptions.Timeout:
            logger.error(f"GitHub API timeout (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return []
            
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return []
    
    return []


def get_repo_languages():
    """Get list of popular programming languages for filtering"""
    popular_languages = [
        "python", "javascript", "typescript", "java", "go", "rust", 
        "cpp", "c", "csharp", "php", "ruby", "swift", "kotlin", 
        "scala", "dart", "r", "matlab", "shell", "powershell"
    ]
    return popular_languages


def fetch_trending_by_timeframe(language="python", timeframe="week", limit=5):
    """Get trending repos by different timeframes"""
    
    timeframe_days = {
        "day": 1,
        "week": 7, 
        "month": 30,
        "year": 365
    }
    
    days = timeframe_days.get(timeframe, 7)
    date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language} created:>{date_threshold}",
        "sort": "stars",
        "order": "desc", 
        "per_page": limit
    }
    
    repos = make_github_request(url, params)
    
    formatted_repos = []
    for repo in repos:
        formatted_repos.append({
            "name": repo.get("full_name"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "description": repo.get("description", ""),
            "language": repo.get("language", ""),
            "timestamp": datetime.utcnow(),
            "trending_reason": f"trending_{timeframe}"
        })
    
    return formatted_repos


# Legacy function for backwards compatibility
def fetch_trending_repos(language="python", sort="stars", order="desc", per_page=5):
    """Legacy function - redirects to new logic"""
    return [repo for repo in fetch_top_repos(language=language, limit=per_page)]


# Test function - only runs when script is executed directly
if __name__ == "__main__":
    print("🚀 Testing GitHub ingest...")
    
    # Test with Python repos
    try:
        repos = fetch_top_repos(language="python", limit=3)
        print(f"\n✅ Found {len(repos)} repos:")
        
        for repo in repos:
            print(f"  • {repo['name']} - ⭐ {repo['stars']} stars")
            print(f"    {repo['description'][:100]}..." if repo['description'] else "    No description")
            print(f"    Trending reason: {repo['trending_reason']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("🔧 Make sure you have GITHUB_TOKEN in your .env file!")