from pydantic import BaseModel
from datetime import datetime


class portfolioBase(BaseModel):
    ticker: str
    volume: int
    price: int


class portfolio(portfolioBase):
    id: int
    userid: int
    class Config:
        from_attributes = True


class portfolioCreate(portfolioBase):
    pass



class portfolioReturn(portfolioBase):
    created_at: datetime
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: int
    class Config:
        from_attributes = True


class UserReturn(UserBase):
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str