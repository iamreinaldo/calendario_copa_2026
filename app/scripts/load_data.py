from app.database import SessionLocal
from app.services.parser import load_json, parse_and_save

db = SessionLocal()

data = load_json("worldcup.json")

parse_and_save(db, data)

print("Dados inseridos!")