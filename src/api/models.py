from .database import Base
from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime
)


class portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    createdDT = Column(DateTime, nullable=False)
    volume = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    userId = Column(Integer, ForeignKey('userdb.id'), nullable=False)


class user(Base):
    __tablename__ = 'userdb'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)