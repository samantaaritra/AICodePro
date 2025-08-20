# src/db.py
from sqlalchemy import create_engine, Column, Integer, Float, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"
    pr_id = Column(String, primary_key=True)
    repo = Column(String, nullable=False)
    author = Column(String)
    created_at = Column(String)
    merged_at = Column(String)
    files_changed = Column(Integer)
    lines_added = Column(Integer)
    lines_deleted = Column(Integer)

class PRFile(Base):
    __tablename__ = "pr_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pr_id = Column(String, ForeignKey("pull_requests.pr_id"))
    path = Column(Text)
    language = Column(String)
    lines_added = Column(Integer)
    lines_deleted = Column(Integer)

class Feature(Base):
    __tablename__ = "features"
    pr_id = Column(String, ForeignKey("pull_requests.pr_id"), primary_key=True)
    feature_name = Column(String, primary_key=True)
    feature_value = Column(Float)

class Label(Base):
    __tablename__ = "labels"
    pr_id = Column(String, ForeignKey("pull_requests.pr_id"), primary_key=True)
    label = Column(String)  # "good" or "needs_fix"
    source = Column(String, default="manual")

class Prediction(Base):
    __tablename__ = "predictions"
    pr_id = Column(String, ForeignKey("pull_requests.pr_id"), primary_key=True)
    predicted_label = Column(String)
    probability = Column(Float)
    model_version = Column(String)
    created_at = Column(String)

# Create engine + session
def get_engine(db_path="sqlite:///data/aicodepro.db"):
    return create_engine(db_path, echo=True)

def init_db(db_path="sqlite:///data/aicodepro.db"):
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    return engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
