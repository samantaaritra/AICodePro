import os
import json
import requests
from src.db import SessionLocal, PRFile  # 👈 our DB model for PR files
from sqlalchemy.exc import IntegrityError

# GitHub token (set in your environment for higher rate limits)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

REPO = "octocat/Hello-World"  # 👈 can later make dynamic

def fetch_pr_files(pr_number: int):
    """
    Fetch files changed in a given PR from GitHub API.
    """
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch files for PR {pr_number}: {response.text}")
        return []
    return response.json()

def save_pr_files(pr_number: int, files_data: list):
    """
    Save PR file details into SQLite DB.
    """
    session = SessionLocal()
    for f in files_data:
        pr_file = PRFile(
            pr_id=str(pr_number),
            filename=f["filename"],
            additions=f["additions"],
            deletions=f["deletions"],
            changes=f["changes"],
            status=f["status"]
        )
        try:
            session.add(pr_file)
            session.commit()
        except IntegrityError:
            session.rollback()
    session.close()

def main():
    """
    Iterate over PRs in DB, fetch & store file-level details.
    """
    from src.db import PullRequest  # avoid circular import

    session = SessionLocal()
    prs = session.query(PullRequest).all()
    session.close()

    all_files = {}

    for pr in prs:
        files_data = fetch_pr_files(pr.pr_id)
        save_pr_files(pr.pr_id, files_data)
        all_files[pr.pr_id] = files_data
        print(f"✅ Stored files for PR {pr.pr_id} ({len(files_data)} files)")

    # Optional: save all files into JSON
    os.makedirs("data", exist_ok=True)
    with open("data/pr_files.json", "w") as f:
        json.dump(all_files, f, indent=2)

    print("🎉 PR file details saved to DB and data/pr_files.json")

if __name__ == "__main__":
    main()
