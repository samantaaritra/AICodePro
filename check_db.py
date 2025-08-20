from src.db import SessionLocal, PullRequest

session = SessionLocal()
prs = session.query(PullRequest).all()
print(f"Total PRs stored: {len(prs)}")
for pr in prs[:5]:
    print(
        f"PR {pr.pr_id} by {pr.author} | "
        f"Files: {pr.files_changed}, +{pr.lines_added}/-{pr.lines_deleted}"
    )
