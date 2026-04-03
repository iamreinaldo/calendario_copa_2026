import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Match
from app.utils.translations import TRADUCAO_TIMES


def converter_para_brasil(data, time_str):
    hora, utc = time_str.split(" UTC")
    offset = int(utc)

    dt = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")

    diff = -3 - offset
    dt = dt + timedelta(hours=diff)

    return dt


def load_json(path="worldcup.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_and_save(db: Session, data):
    for jogo in data["matches"]:
        inicio = converter_para_brasil(jogo["date"], jogo["time"])
        fim = inicio + timedelta(hours=2)

        team_home = TRADUCAO_TIMES.get(jogo["team1"], jogo["team1"])
        team_away = TRADUCAO_TIMES.get(jogo["team2"], jogo["team2"])

        match = Match(
            start_time=inicio,
            end_time=fim,
            team_home=team_home,
            team_away=team_away,
            stage=jogo.get("round"),
            group=jogo.get("group"),
            stadium=jogo.get("ground"),
        )

        db.add(match)

    db.commit()
