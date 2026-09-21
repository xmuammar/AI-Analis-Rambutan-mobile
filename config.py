import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _android_data_dir() -> Path:
    configured = os.getenv("AI_ANALISIS_DATA_DIR")
    if configured:
        return Path(configured)
    for variable in ("ANDROID_PRIVATE", "ANDROID_APP_PATH"):
        value = os.getenv(variable)
        if value:
            return Path(value) / "data"
    return BASE_DIR / "instance"


DATA_DIR = _android_data_dir()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATA_DIR / 'ai_analis_rambutan.sqlite3'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 12 * 1024 * 1024
    UPLOAD_FOLDER = DATA_DIR / "uploads"
    MODEL_FOLDER = Path(os.getenv("AI_ANALISIS_MODEL_DIR", DATA_DIR / "models"))
    ALLOWED_IMAGE_EXTENSIONS: ClassVar[set[str]] = {"jpg", "jpeg", "png", "webp"}
    # Development convenience only. Production databases must use `flask db upgrade`.
    AUTO_CREATE_SCHEMA = os.getenv("AUTO_CREATE_SCHEMA", "1") == "1"
