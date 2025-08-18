# src/predict_prs.py

import json
import os
import joblib

LABELED_FILE = os.path.join("data", "labeled_prs.json")
MODEL_FILE = os.path.join("models", "pr_model.pkl")
OUTPUT_FILE = os.path.join("data", "predicted_prs.json")


def extract_features(pr):
    """Extract numerical features from PR data (must match training)."""
    return [
        int(pr.get("changed_files", 0) or 0),
        int(pr.get("additions", 0) or 0),
        int(pr.get("deletions", 0) or 0),
    ]


def predict_prs():
    # Load labeled PRs
    with open(LABELED_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    # Load trained model
    model = joblib.load(MODEL_FILE)

    predictions = []
    for pr in prs:
        features = [extract_features(pr)]
        predicted_label = model.predict(features)[0]

        predictions.append({
            "number": pr.get("number"),
            "title": pr.get("title"),
            "user": pr.get("user"),
            "predicted_label": int(predicted_label)
        })

    # Save predictions
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(predictions, f, indent=2)

    print(f"✅ Predictions saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    predict_prs()
