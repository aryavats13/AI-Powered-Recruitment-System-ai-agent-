import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_github_stats(username):
    # Debug
    print("Loaded Token:", bool(GITHUB_TOKEN))

    url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
    response = requests.get(url, headers=headers)

    # Debug raw response
    print("GITHUB STATUS:", response.status_code)
    print("RAW:", response.text)

    if response.status_code != 200:
        return {"error": "GitHub user not found"}

    repos = response.json()

    repo_count = len(repos)
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)

    languages = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    last_active = max(r.get("updated_at") for r in repos)

    top_repos = sorted(
        repos, key=lambda x: x.get("stargazers_count", 0), reverse=True
    )[:3]

    cleaned_top = [
        {
            "name": r["name"],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "url": r["html_url"]
        }
        for r in top_repos
    ]

    return {
        "repo_count": repo_count,
        "stars": stars,
        "forks": forks,
        "languages": languages,
        "last_active": last_active,
        "top_repos": cleaned_top
    }
