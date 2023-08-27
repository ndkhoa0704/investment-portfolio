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
    email = payload.get('sub')
    if not email:
        raise cred_exception
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise cred_exception
    return user


@app.post('/token', response_model=schemas.Token)
async def request_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    cred_except = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise cred_except
    if not verify_password(form_data.password, user.password):
        raise cred_except
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "personal finance API"}


@app.post(
    "/investment-portfolios",
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.portfolioReturn
)
async def update_portfolio(
    portfolio_entry: schemas.portfolioCreate, 
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user)
):
    return crud.update_portfolio(
        db, user, portfolio_entry
    )


@app.get('/investment-portfolios', response_model=list[schemas.portfolioReturn])
async def get_portfolios(
    skip: int=0, 
    limit: int=100, 
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user)
):
    return crud.get_portfolio(db, skip=skip, limit=limit)


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
async def create_user(*, 
    db: Session = Depends(get_db),
    user: schemas.UserCreate
):    
    user.password = get_hashed_password(user.password)
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    user = crud.create_user(db, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)        
    return user