from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str | None = None
    
    
class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    date: datetime
    
    class Config:
        from_atribute = True