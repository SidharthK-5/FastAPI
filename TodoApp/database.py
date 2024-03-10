from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
To use SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todospp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
"""

# To use PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://localhost:5432/TodoApplicationDatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
