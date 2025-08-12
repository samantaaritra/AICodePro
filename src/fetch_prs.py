import requests
import json
import os

# Load token from environment variable for safety
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "octocat"   # Example owner
REPO_NAME = "Hello-World"  # Example repo

def fetch_pull_requests():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=all"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pr_data = response.json()
        
        # Save data to data/pr_data.json
        os.makedirs("data", exist_ok=True)
        with open("data/pr_data.json", "w", encoding="utf-8") as f:
            json.dump(pr_data, f, indent=4)
        
        print(f"✅ Fetched {len(pr_data)} PRs and saved to data/pr_data.json")
    else:
        print(f"❌ Failed to fetch PRs: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_pull_requests()
