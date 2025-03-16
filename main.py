from fastapi import FastAPI
from routes import transactions
from routes import auth

app = FastAPI()

app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
@app.get("/")
def home():
    return {"message": "Welcome to Cashflow API"}
