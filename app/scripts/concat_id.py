from app.database import SessionLocal
from app.services.sync import vincular_external_id

db = SessionLocal()

vincular_external_id(db)