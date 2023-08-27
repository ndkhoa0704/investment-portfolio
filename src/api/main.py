from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from datetime import datetime
import os
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .security import (
    verify_password,
    check_token,
    get_hashed_password, 
    create_access_token
)
from dotenv import load_dotenv

load_dotenv() 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), payload: dict = Depends(check_token)):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = payload.get('sub')
    if not username:
        raise cred_exception
    user = crud.get_user(db, username=username)
    if not user:
        raise cred_exception
    return user


@app.post('/token', response_model=schemas.Token)
def request_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    cred_except = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = crud.get_user(db, form_data.username)
    if not user:
        raise cred_except
    if not verify_password(form_data.password, user.password):
        raise cred_except
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"message": "personal finance API"}


@app.post("/investment-portfolios/tickers/{ticker}", response_model=schemas.portfolio_entry)
def update_portfolio(
    ticker: str, userid:int, volume: int,
    price: int, db: Session = Depends(get_db)
):
    updatedDT = datetime.now()
    return crud.update_portfolio(
        db, userid=userid, ticker=ticker, 
        volume=volume, price=price, updatedDT=updatedDT
    )


@app.get('/investment-portfolios', response_model=schemas.portfolio)
def get_portfolios(userid: str, skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    crud.get_portfolio(db, userid=userid, skip=skip, limit=limit)


@app.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(*, 
    db: Session = Depends(get_db),
    secret_key: str | None,
    user: schemas.User
):    
    if not verify_password(secret_key, os.getenv('SECRET_NEW_USER_KEY')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    user.password = get_hashed_password(user.password)
    user = crud.get_user(db, user.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    user = crud.create_user(db, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)        
    return {"detail": "User created"}