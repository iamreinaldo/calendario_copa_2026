import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_KEY_FOOTBALL: str = os.getenv("API_KEY_FOOTBALL")


settings = Settings()