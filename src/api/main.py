from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "personal finance API"}


@app.put("/investment-portfolios/tickers/{ticker}")
def update_portfolio(ticker: str):
    pass


@app.get('/investment-portfolios')
def get_portfolios():
    pass