import requests
from app.services.sync import normalizar_data_api
from app.core.settings import settings



API_KEY = settings.API_KEY_FOOTBALL

url = "https://api.football-data.org/v4/competitions/WC/matches"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(url, headers=headers)

data = response.json()

for match in data.get("matches", []):
    status = match["status"]

    # só jogos finalizados
    
    #if status != "FINISHED":
     #   continue

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    score_home = match["score"]["fullTime"]["home"]
    score_away = match["score"]["fullTime"]["away"]

    data_br, hora_br = normalizar_data_api(match["utcDate"])
    stadium = match.get("venue")
    stage = match.get("stage")
    group = match.get("group")
    match_id = match["id"]

    print(
        f"{home} {score_home} x {score_away} {away} | "
        f"{data_br} {hora_br} | {stadium} | {stage} | {group} | id={match_id}"
    )
