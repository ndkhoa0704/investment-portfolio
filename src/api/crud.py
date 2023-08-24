from sqlalchemy.orm import Session
from . import models, schemas
import datetime as dt
def get_portfolios(db: Session, userid: int, skip: int = 0, limit: int = 100):
    return db.query(models.portfolios).offset(skip).limit(limit).all()


def update_portfolio(db: Session, entry: schemas.portfolio_entry, updatedDT: dt.datetime):
    porfolio_entry = models.portfolios(
        ticker=entry.ticker,
        createdDT=updatedDT,

    )
    db.add(entry)