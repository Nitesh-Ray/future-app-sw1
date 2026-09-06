# models.py
# Defines the SQLAlchemy ORM model (database table structure).

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Item(Base):
    """Item table schema: id, name, description, price"""
    __tablename__ = "items"   # table name in SQLite

    id = Column(Integer, primary_key=True, index=True)  # auto-increment primary key
    name = Column(String, index=True)                   # indexed for faster queries
    description = Column(String, nullable=True)         # optional field
    price = Column(Float)                               # required field


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
