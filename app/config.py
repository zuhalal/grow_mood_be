import pathlib
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

from typing import Optional

basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / ".env")

class Settings(BaseSettings):
    app_name: str = "Grow Mood"
    env: str = os.getenv("ENV", "development")
    firebase_config_path: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./firebase-config.json")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

@lru_cache
def get_settings():
    return Settings()

