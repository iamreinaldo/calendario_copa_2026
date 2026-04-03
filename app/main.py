from fastapi import FastAPI
from app.routes.calendar import router as calendar_router
from app.routes.admin import router as admin_router

app = FastAPI()

app.include_router(calendar_router)
app.include_router(admin_router)