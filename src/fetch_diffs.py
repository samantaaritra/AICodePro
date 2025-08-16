# src/fetch_diffs.py

import json
import os
from github import Github

# Input and output paths
CLEAN_PR_FILE = os.path.join("data", "clean_prs.json")
DIFFS_FILE = os.path.join("data", "pr_diffs.json")

def fetch_diffs():
    """Fetch file diffs (additions, deletions, changes) for each PR."""
    # Load cleaned PRs
    with open(CLEAN_PR_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    token = os.getenv("GITHUB_TOKEN")  # Make sure GITHUB_TOKEN is set
    if not token:
        raise ValueError("GitHub token not found. Please set GITHUB_TOKEN environment variable.")

    gh = Github(token)

    repo_name = "psf/requests"  # demo repo (same as before)
    repo = gh.get_repo(repo_name)

    diffs = []

    for pr_data in prs:
        try:
            pr = repo.get_pull(pr_data["number"])
            diffs.append({
                "number": pr.number,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
            })
        except Exception as e:
            print(f"⚠️ Skipping PR {pr_data['number']}: {e}")

    # Save diffs
    with open(DIFFS_FILE, "w", encoding="utf-8") as f:
        json.dump(diffs, f, indent=2)

    print(f"✅ Saved PR diffs to {DIFFS_FILE}")


if __name__ == "__main__":
    fetch_diffs()
