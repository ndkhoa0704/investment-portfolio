from .database import Base
from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime
)
from datetime import datetime

class portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    volume = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    userid = Column(Integer, ForeignKey('userdb.id'), nullable=False)


class user(Base):
    __tablename__ = 'userdb'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)