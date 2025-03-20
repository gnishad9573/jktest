import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".")/'.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "Book Store"
    PROJECT_VERSION:str = "0.1.0"
    POSTGRES_USER:str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT:int = os.getenv("POSTGRES_PORT")
    POSTGRES_SERVER:str = os.getenv("POSTGRES_SERVER")
    POSTGRES_DB:str = os.getenv("POSTGRES_DB")
    POSTGRES_URL_DB:str=os.getenv("POSTGRES_URL_DB")
    postgres_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    postgres_url_db = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_URL_DB}"


settings = Settings()