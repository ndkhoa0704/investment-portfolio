from sqlalchemy.orm import Session
from . import models, schemas
import datetime as dt


def get_portfolio(
    db: Session, 
    user: schemas.User, 
    skip: int = 0, 
    limit: int = 100
) -> list[schemas.portfolioReturn]:
    return db.query(models.portfolio)\
        .where(models.portfolio.userid == user.id)\
        .offset(skip).limit(limit).all()


def update_portfolio(
    db: Session, 
    user: schemas.User,
    portfolio_entry: schemas.portfolioCreate
) -> schemas.portfolio:
    db_porfolio = models.portfolio(
        ticker=portfolio_entry.ticker,
        userid=user.id,
        volume=portfolio_entry.volume,
        price=portfolio_entry.price
    )
    db.add(db_porfolio)
    db.commit()
    db.refresh(db_porfolio)
    return db_porfolio


def get_user_by_email(db: Session, email: str):
    return db.query(models.user).filter(models.user.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    user = models.user(
        name=user.name,
        email=user.email,
        password=user.password,
        role=2
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user