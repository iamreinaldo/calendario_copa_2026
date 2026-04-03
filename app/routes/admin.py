


from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
def admin_panel(db: Session = Depends(get_db)):
    matches = db.query(Match).all()

    html = "<h1>Painel de Jogos</h1>"

    for m in matches:
        html += f"""
        <form method='post' action='/admin/update'>
            <p>{m.team_home} x {m.team_away}</p>
            <input type='hidden' name='match_id' value='{m.id}' />
            <input type='number' name='score_home' placeholder='Casa' />
            <input type='number' name='score_away' placeholder='Fora' />
            <button type='submit'>Salvar</button>
        </form>
        <hr>
        """

    return html


@router.post("/admin/update")
def update_match(
    match_id: int = Form(...),
    score_home: int = Form(...),
    score_away: int = Form(...),
    db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()

    match.score_home = score_home
    match.score_away = score_away
    match.status = "finished"

    db.commit()

    return {"ok": True}