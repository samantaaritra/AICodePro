import requests
import json
import os

from src.db import SessionLocal, PullRequest  # 👈 import DB session + model

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

        # Save data to JSON
        os.makedirs("data", exist_ok=True)
        with open("data/pr_data.json", "w", encoding="utf-8") as f:
            json.dump(pr_data, f, indent=4)
        
        print(f"✅ Fetched {len(pr_data)} PRs and saved to data/pr_data.json")
        # --- Insert into DB ---
        session = SessionLocal()
        for pr in pr_data:
            # Fetch full PR details to get additions/deletions/files_changed
            pr_number = pr["number"]
            pr_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
            pr_response = requests.get(pr_url, headers=headers)

            if pr_response.status_code == 200:
                pr_full = pr_response.json()
                pr_entry = PullRequest(
                    pr_id=str(pr["id"]),    # unique GitHub PR ID
                    repo=f"{REPO_OWNER}/{REPO_NAME}",
                    author=pr["user"]["login"],
                    created_at=pr["created_at"],
                    merged_at=pr.get("merged_at"),
                    files_changed=pr_full.get("changed_files"),
                    lines_added=pr_full.get("additions"),
                    lines_deleted=pr_full.get("deletions")
                )
                session.merge(pr_entry)
            else:
                print(f"⚠️ Failed to fetch details for PR {pr_number}: {pr_response.status_code}")

        session.commit()
        session.close()
        print("✅ PR metadata (with stats) inserted into SQLite DB (pull_requests table)")


if __name__ == "__main__":
    fetch_pull_requests()
