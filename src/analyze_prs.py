# src/analyze_prs.py

import json
import os
from collections import Counter

CLEAN_PR_FILE = os.path.join("data", "clean_prs.json")

def analyze_prs():
    # Load cleaned PR data
    with open(CLEAN_PR_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    total_prs = len(prs)
    open_prs = sum(1 for pr in prs if pr.get("state") == "open")
    closed_prs = sum(1 for pr in prs if pr.get("state") == "closed")
    merged_prs = sum(1 for pr in prs if pr.get("mergeable") is True)

    avg_changed_files = sum(pr.get("changed_files") or 0 for pr in prs) / total_prs if total_prs else 0

    # Most frequent contributors
    contributors = Counter(pr.get("user") for pr in prs if pr.get("user"))

    print("\n📊 PR Analysis Report")
    print("-" * 40)
    print(f"Total PRs: {total_prs}")
    print(f"Open PRs: {open_prs}")
    print(f"Closed PRs: {closed_prs}")
    print(f"Merged PRs: {merged_prs}")
    print(f"Average Changed Files per PR: {avg_changed_files:.2f}")
    print("\nTop 5 Contributors:")
    for user, count in contributors.most_common(5):
        print(f"  {user}: {count} PRs")


if __name__ == "__main__":
    analyze_prs()
