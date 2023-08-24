from pydantic import BaseModel


class portfolios(BaseModel):
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

class User(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True