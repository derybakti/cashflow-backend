from fastapi import FastAPI
from routes import transactions
from fastapi.middleware.cors import CORSMiddleware
from routes import auth

app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa ganti "*" dengan ["http://localhost:5173"] untuk lebih aman
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, dll.)
    allow_headers=["*"],  # Mengizinkan semua header
)

app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
@app.get("/")
def home():
    return {"message": "Welcome to Cashflow API"}
