from database import engine, Base
from models import Transaction

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")