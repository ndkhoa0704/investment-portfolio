from .database import Base
from sqlalchemy import (
    Column, ForeignKey, Integer, String, DateTime
)


class portfolios(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    createdDT = Column(DateTime, nullable=False)
    volume = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    userId = Column(Integer, ForeignKey('userInfo.id'), nullable=False)


class userInfo(Base):
    __tablename__ = 'userInfo'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)