import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_FILE)


def get_required_setting(name: str, legacy_name: Optional[str] = None) -> str:
    value = os.getenv(name)
    if not value and legacy_name:
        value = os.getenv(legacy_name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Copy .env.example to .env and provide a value."
        )

    return value


DATABASE_URL = get_required_setting("DATABASE_URL")
# Keep the old lowercase name working while local environments migrate.
SECRET_KEY = get_required_setting("SECRET_KEY", legacy_name="secret_key")
ALGORITHM = "HS256"
