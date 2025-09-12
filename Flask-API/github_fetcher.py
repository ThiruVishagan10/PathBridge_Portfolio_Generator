import requests
import os
from dotenv import load_dotenv
from Portfolio.enhancer import enhance_content

# Load environment variables
load_dotenv()

# GitHub token for authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def fetch_github_repos(username: str, max_repos: int = 6) -> list[dict]:
    """
    Fetch top GitHub repositories for a given username, prioritized by engagement.

    Args:
        username (str): GitHub username.
        max_repos (int): Maximum number of repositories to fetch (4-6).

    Returns:
        list[dict]: List of top repository details prioritized by stars, forks, and activity.
    """
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=30"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        repos = response.json()

        # Filter out forks and empty repos, then prioritize
        filtered_repos = [
            repo for repo in repos 
            if not repo.get("fork", False) and repo.get("size", 0) > 0
        ]
        
        # Sort by priority: stars + forks + (recent activity boost)
        def priority_score(repo):
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            return stars * 2 + forks
        
        sorted_repos = sorted(filtered_repos, key=priority_score, reverse=True)

        projects = []
        for repo in sorted_repos[:max_repos]:
            description = repo.get("description", "")
            if not description:
                # Generate description based on repo name and language
                repo_name = repo.get("name", "")
                language = repo.get("language", "")
                description = enhance_content(
                    f"Create a professional project description for a {language} repository named '{repo_name}'. Make it concise and highlight potential features:",
                    f"{repo_name} - {language} project"
                )
            
            # Fetch commits and branches count
            repo_name = repo.get("name", "")
            commits_count = get_commits_count(username, repo_name)
            branches_count = get_branches_count(username, repo_name)
            
            projects.append({
                "name": repo.get("name", ""),
                "description": description,
                "url": repo.get("html_url", ""),
                "language": repo.get("language", "Not specified"),
                "commits": commits_count,
                "branches": branches_count,
            })
        return projects

    except requests.RequestException as e:
        print(f"Error fetching GitHub repos: {e}")
        return []

def get_commits_count(username: str, repo_name: str) -> int:
    """Get total commits count for a repository"""
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=1"
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            # Get total count from Link header if available
            link_header = response.headers.get('Link', '')
            if 'last' in link_header:
                import re
                match = re.search(r'page=(\d+)>; rel="last"', link_header)
                if match:
                    return int(match.group(1))
        return 0
    except:
        return 0

def get_branches_count(username: str, repo_name: str) -> int:
    """Get total branches count for a repository"""
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/branches"
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            branches = response.json()
            return len(branches)
        return 0
    except:
        return 0
