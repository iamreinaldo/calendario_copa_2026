from apscheduler.schedulers.blocking import BlockingScheduler
from app.database import SessionLocal
from app.services.sync import atualizar_resultados


def job():
    db = SessionLocal()
    atualizar_resultados(db)


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=8, minute=0)

print("Worker rodando...")

scheduler.start()