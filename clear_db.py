from src.db import SessionLocal, PullRequest, PRFile

# Create a database session
db = SessionLocal()

# Delete all entries from both tables
deleted_prs = db.query(PullRequest).delete()
deleted_files = db.query(PRFile).delete()

# Commit and close
db.commit()
db.close()

print(f'? Cleared {deleted_prs} pull requests and {deleted_files} PR files from the database.')
