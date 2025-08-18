# src/process_diffs.py

import json
import os
from collections import Counter

DIFF_FILE = os.path.join("data", "pr_diffs.json")
FEATURE_FILE = os.path.join("data", "pr_features.json")

KEYWORDS = ["fix", "bug", "test", "refactor", "doc", "readme", "typo"]

def process_diffs():
    # Load raw diffs
    with open(DIFF_FILE, "r", encoding="utf-8") as f:
        diffs = json.load(f)

    features = []
    for pr in diffs:
        pr_number = pr.get("number")
        files = pr.get("files", [])

        lines_added = 0
        lines_deleted = 0
        keywords_found = Counter()
        touches_docs = False

        for file in files:
            filename = file.get("filename", "")
            patch = file.get("patch", "")

            # Count additions and deletions
            if patch:
                for line in patch.splitlines():
                    if line.startswith("+") and not line.startswith("+++"):
                        lines_added += 1
                        for kw in KEYWORDS:
                            if kw in line.lower():
                                keywords_found[kw] += 1
                    elif line.startswith("-") and not line.startswith("---"):
                        lines_deleted += 1

            # Check if this PR touches documentation
            if filename.endswith((".md", ".rst", ".txt")):
                touches_docs = True

        features.append({
            "number": pr_number,
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "files_changed": len(files),
            "keywords": dict(keywords_found),
            "touches_docs": touches_docs
        })

    # Save features
    os.makedirs(os.path.dirname(FEATURE_FILE), exist_ok=True)
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        json.dump(features, f, indent=2)

    print(f"✅ Processed {len(features)} PRs and saved to {FEATURE_FILE}")


if __name__ == "__main__":
    process_diffs()
