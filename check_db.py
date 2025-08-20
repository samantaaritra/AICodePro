from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///data/aicodepro.db")
inspector = inspect(engine)

print("Tables in DB:", inspector.get_table_names())
