# database.py
# Sets up the database connection and session management.
# Uses SQLite for simplicity (file-based, no separate server).
# Uses SQLite by default; URL can be overridden via environment variable.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Read database URL from environment, default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# SQLite needs special connect args for multi-threaded use
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)



# SQLite database file will be created in the current directory
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

# Create engine with special SQLite settings for multi-threaded use
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal is a factory for database sessions (one per request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models (used in models.py)
class Base(DeclarativeBase):
    pass