from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.sync import atualizar_resultados


def job():
    db = SessionLocal()
    atualizar_resultados(db)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', hour=8, minute=0)
    scheduler.start()