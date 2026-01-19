from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_ALCHEMY_DB_URL = f'postgresql://{settings.pg_user}:{settings.pg_password}@localhost/{settings.pg_db}'

# engine is what is responsible for connecting to the Postgres database
engine = create_engine(SQL_ALCHEMY_DB_URL)

# when we actually want to talk to the databse, we will use a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency injection : this function is called every time an operation needs to be completed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
