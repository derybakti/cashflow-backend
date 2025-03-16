from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import crud, schemas
from config import SECRET_KEY, ALGORITHM
from models import Transaction
from utils import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = crud.get_user_by_username(db, username)
#     if user is None:
#         raise credentials_exception
#     return user

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    current_user: schemas.UserRead = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction, current_user.id)

@router.get("/", response_model=list[schemas.TransactionRead])
def read_transactions(
    skip: int = 0, 
    limit: int = 10, 
    current_user: schemas.UserRead = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.get_transactions(db, skip, limit, current_user.id)

@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
def read_transaction(
    transaction_id: int, 
    current_user: schemas.UserRead = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionRead)
def update_transaction(
    transaction_id: int, 
    updated_transaction: schemas.TransactionCreate, 
    current_user: schemas.UserRead = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return crud.update_transaction(db, transaction_id, updated_transaction)

@router.delete("/{transaction_id}", response_model=schemas.TransactionRead)
def delete_transaction(
    transaction_id: int, 
    current_user: schemas.UserRead = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return crud.delete_transaction(db, transaction_id)
