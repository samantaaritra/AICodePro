# src/parse_prs.py

import json
import os

# File paths
RAW_PR_FILE = os.path.join("data", "pr_data.json")
CLEAN_PR_FILE = os.path.join("data", "clean_prs.json")

def parse_prs():
    # Load raw PR data
    with open(RAW_PR_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = []

    for pr in raw_data:
        clean_data.append({
            "id": pr.get("id"),
            "number": pr.get("number"),
            "title": pr.get("title"),
            "body": pr.get("body"),
            "user": pr.get("user", {}).get("login"),
            "created_at": pr.get("created_at"),
            "state": pr.get("state"),
            "changed_files": pr.get("changed_files"),
            "mergeable": pr.get("mergeable"),
            "url": pr.get("html_url")
        })

    # Save cleaned data
    with open(CLEAN_PR_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4)

    print(f"✅ Cleaned PR data saved to {CLEAN_PR_FILE}")


if __name__ == "__main__":
    parse_prs()
