import os
import requests
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.models import Match


def normalizar_data_api(utc_date: str):
    dt_utc = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
    dt_br = dt_utc.astimezone(timezone(timedelta(hours=-3)))

    data = dt_br.strftime("%Y-%m-%d")
    hora = dt_br.strftime("%H:%M")

    return data, hora




API_KEY = os.getenv("API_KEY_FOOTBALL")
URL = "https://api.football-data.org/v4/competitions/WC/matches"

headers = {
    "X-Auth-Token": API_KEY
}


def vincular_external_id(db: Session):
    response = requests.get(URL, headers=headers)
    data = response.json()

    api_matches = data.get("matches", [])
    db_matches = db.query(Match).all()

    for api_m in api_matches:
        data_br, hora_br = normalizar_data_api(api_m["utcDate"])

        for db_m in db_matches:
            data_db = db_m.start_time.strftime("%Y-%m-%d")
            hora_db = db_m.start_time.strftime("%H:%M")

            if (
                data_db == data_br
                and hora_db == hora_br
            ):
                db_m.external_id = api_m["id"]
                break

    db.commit()
    print("External IDs vinculados!")

def atualizar_resultados(db: Session):
    response = requests.get(URL, headers=headers)
    data = response.json()

    api_matches = data.get("matches", [])

    for api_m in api_matches:
        external_id = api_m["id"]
        score_home = api_m["score"]["fullTime"]["home"]
        score_away = api_m["score"]["fullTime"]["away"]
        status = api_m["status"]

        # busca direto pelo id
        db_m = db.query(Match).filter(Match.external_id == external_id).first()

        if not db_m:
            continue

        # só atualiza se tiver placar
        if score_home is not None:
            db_m.score_home = score_home
            db_m.score_away = score_away

            if status == "FINISHED":
                db_m.status = "finished"

    db.commit()
    print("Resultados atualizados!")