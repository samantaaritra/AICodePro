import os
import requests
import tempfile
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze
from src.db import SessionLocal, PRFile, Feature
from sqlalchemy.exc import IntegrityError

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def fetch_raw_file(repo_full_name, file_path, ref="main"):
    """Fetch the raw content of a file from GitHub."""
    url = f"https://raw.githubusercontent.com/{repo_full_name}/{ref}/{file_path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"⚠️ Failed to fetch {file_path}: {response.status_code}")
        return None

def extract_code_metrics(code):
    """Compute Radon metrics for given code."""
    try:
        raw_metrics = analyze(code)
        complexity = sum(block.complexity for block in cc_visit(code)) / (len(cc_visit(code)) or 1)
        maintainability = mi_visit(code, True)
        return {
            "loc": raw_metrics.loc,
            "lloc": raw_metrics.lloc,
            "sloc": raw_metrics.sloc,
            "comments": raw_metrics.comments,
            "multi": raw_metrics.multi,
            "blank": raw_metrics.blank,
            "complexity": complexity,
            "maintainability": maintainability
        }
    except Exception as e:
        print(f"⚠️ Radon analysis failed: {e}")
        return None

def save_features(pr_id, feature_dict):
    """Save metrics into the features table."""
    session = SessionLocal()
    for name, value in feature_dict.items():
        f = Feature(pr_id=str(pr_id), feature_name=name, feature_value=value)
        try:
            session.add(f)
            session.commit()
        except IntegrityError:
            session.rollback()
    session.close()

def main():
    """Extract code metrics for each PR file in DB."""
    session = SessionLocal()
    pr_files = session.query(PRFile).all()
    session.close()

    for pf in pr_files:
        repo_full = pf.pr_id.split(":")[0] if ":" in pf.pr_id else "psf/requests"
        file_path =  pf.filename 
        if not file_path or not file_path.endswith(".py"):
            continue

        code = fetch_raw_file(repo_full, file_path)
        if code:
            metrics = extract_code_metrics(code)
            if metrics:
                save_features(pf.pr_id, metrics)
                print(f"✅ Saved metrics for {file_path} (PR {pf.pr_id})")

    print("🎯 Feature extraction complete!")

if __name__ == "__main__":
    main()
