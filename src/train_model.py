# src/train_model.py

import json
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

LABELED_FILE = os.path.join("data", "labeled_prs.json")
MODEL_FILE = os.path.join("models", "pr_model.pkl")

def load_data():
    """Load labeled PRs and prepare features + labels."""
    with open(LABELED_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    X, y = [], []
    for pr in prs:
        features = [
            pr.get("additions", 0),
            pr.get("deletions", 0),
            pr.get("changed_files", 0),
        ]
        label = pr.get("label")
        if label:  # skip if label is missing
            X.append(features)
            y.append(1 if label == "small_pr" else 0)  # 1 = small, 0 = large

    return np.array(X), np.array(y)


def train_model():
    X, y = load_data()

    if len(X) == 0:
        print("❌ No training data found in labeled_prs.json")
        return

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("\n📊 Model Evaluation")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, MODEL_FILE)
    print(f"\n✅ Model saved to {MODEL_FILE}")


if __name__ == "__main__":
    train_model()
