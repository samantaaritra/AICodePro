# src/label_prs.py

import json
import os

CLEAN_PR_FILE = os.path.join("data", "clean_prs.json")
PR_DIFF_FILE = os.path.join("data", "pr_diffs.json")
LABELED_DATA_FILE = os.path.join("data", "labeled_prs.json")


def label_prs():
    # Load cleaned PRs
    with open(CLEAN_PR_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    # Load PR diffs
    with open(PR_DIFF_FILE, "r", encoding="utf-8") as f:
        pr_diffs = json.load(f)

    labeled_data = []
    for pr in prs:
        number = pr.get("number")  # ✅ safely extract PR number
        changed_files = pr.get("changed_files") or 0
        additions = pr.get("additions") or 0
        deletions = pr.get("deletions") or 0

        # Find the corresponding diff entry
        pr_diff = next((d for d in pr_diffs if d["number"] == number), {"diff": ""})

        # Simple heuristic-based labeling
        if changed_files <= 10 and additions < 200:
            label = "small"
        elif changed_files <= 50 and additions < 1000:
            label = "medium"
        else:
            label = "large"

        labeled_entry = {
            "number": number,
            "title": pr.get("title"),
            "user": pr.get("user"),
            "changed_files": changed_files,
            "additions": additions,
            "deletions": deletions,
            "state": pr.get("state"),
            "mergeable": pr.get("mergeable"),
            "diff": pr_diff.get("diff", ""),
            "label": label,
        }
        labeled_data.append(labeled_entry)

    # Save labeled dataset
    os.makedirs("data", exist_ok=True)
    with open(LABELED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, indent=2)

    print(f"✅ Saved {len(labeled_data)} labeled PRs to {LABELED_DATA_FILE}")


if __name__ == "__main__":
    label_prs()
