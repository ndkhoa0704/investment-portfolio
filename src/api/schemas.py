from pydantic import BaseModel


class portfolio(BaseModel):
    id: int
    ticker: str
    createdDT: str
    volume: int
    price: int
    userId: int
    class Config:
        orm_mode = True
        

class portfolio_entry(BaseModel):
    ticker: str
    volume: int
    price: int
    userId: int


class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    email: str
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str