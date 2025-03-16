from sqlalchemy.orm import Session
from models import Transaction, User
from schemas import TransactionCreate, UserCreate
from utils import hash_password, verify_password


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# ========== USER CRUD ==========
def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# ========== TRANSACTION CRUD ==========
def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    """Buat transaksi dengan user_id"""
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 10, user_id: int = None):
    """Ambil transaksi berdasarkan user"""
    query = db.query(Transaction)
    if user_id:
        query = query.filter(Transaction.user_id == user_id)  # Filter transaksi milik user
    return query.offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int, user_id: int):
    """Ambil transaksi spesifik milik user"""
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

def update_transaction(db: Session, transaction_id: int, updated_data: TransactionCreate, user_id: int):
    """Update transaksi hanya jika milik user"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()
    if db_transaction:
        for key, value in updated_data.dict().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    """Hapus transaksi hanya jika milik user"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
