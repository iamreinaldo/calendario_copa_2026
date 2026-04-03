

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ajuste com seu usuário, senha e banco
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/copa2026"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# dependency para FastAPI (usar depois)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()