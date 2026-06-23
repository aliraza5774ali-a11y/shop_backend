from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Database_url = os.getenv("DATABASE_URL")
engine = create_engine(Database_url, pool_pre_ping=True)

localSession = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

