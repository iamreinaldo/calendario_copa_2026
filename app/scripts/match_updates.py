from app.database import SessionLocal
from app.services.sync import atualizar_resultados

db = SessionLocal()

atualizar_resultados(db)