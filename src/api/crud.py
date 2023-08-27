from sqlalchemy.orm import Session
from . import models, schemas
import datetime as dt


def get_portfolio(db: Session, userid: int, skip: int = 0, limit: int = 100):
    return db.query(models.portfolios)\
        .where(models.portfolios.userid == userid)\
        .offset(skip).limit(limit).all()


def update_portfolio(
    db: Session, 
    ticker: str,
    userid: int,
    volume: int,
    price: int, 
    updatedDT: dt.datetime
) -> schemas.portfolio:
    porfolio_entry = models.portfolios(
        ticker=ticker,
        userid=userid,
        volume=volume,
        price=price,
        createdDT=updatedDT
    )
    db.add(porfolio_entry)
    db.commit()
    porfolio_entry = db.refresh(porfolio_entry)
    return porfolio_entry


def get_user_by_email(db: Session, email: str):
    return db.query(models.user).filter(models.user.email == email).first()


def create_user(db: Session, user_data: schemas.UserCreate):
    hased_password = user_data.password + 'hashed'
    user = models.user(
        name=user_data.name,
        email=user_data.email,
        password=hased_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user