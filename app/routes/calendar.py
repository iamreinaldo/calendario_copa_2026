from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import Response
from icalendar import Calendar, Event, Alarm
from datetime import timedelta
from datetime import datetime

from app.database import get_db
from app.models import Match

router = APIRouter()


@router.get("/copa.ics")
def get_calendar(db: Session = Depends(get_db)):
    cal = Calendar()
    cal.add('X-WR-CALNAME', 'Copa do Mundo - 2026')
    cal.add('X-APPLE-CALENDAR-COLOR', '#D4AF37')  # dourado

    matches = db.query(Match).all()

    for m in matches:
        event = Event()
        event.add('uid', f"match-{m.id}@copa2026")
        event.add('dtstamp', datetime.utcnow())
        if m.score_home is not None:
            nome = f"{m.team_home} {m.score_home} x {m.score_away} {m.team_away}"
        else:
            nome = f"{m.team_home} x {m.team_away}"

        event.add('summary', nome)
        event.add('last-modified', datetime.utcnow())
        event.add('sequence', m.score_home or 0)
        event.add('dtstart', m.start_time)
        event.add('dtend', m.end_time)
        event.add('location', m.stadium or "")
        event.add('description', f"{m.stage or ''} {m.group or ''}".strip())

        # 24 horas antes
        alarm_24h = Alarm()
        alarm_24h.add('action', 'DISPLAY')
        alarm_24h.add('description', 'Jogo em 24h')
        alarm_24h.add('trigger', timedelta(hours=-24))

        # 30 minutos antes
        alarm_30m = Alarm()
        alarm_30m.add('action', 'DISPLAY')
        alarm_30m.add('description', 'Jogo em 30 minutos')
        alarm_30m.add('trigger', timedelta(minutes=-30))

        event.add_component(alarm_24h)
        event.add_component(alarm_30m)

        cal.add_component(event)

    return Response(cal.to_ical(), media_type="text/calendar")