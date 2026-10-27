
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def configured_path(variable_name: str, default_path: str) -> Path:
    value = Path(os.getenv(variable_name, default_path))

    if not value.is_absolute():
        value = BASE_DIR / value

    return value.resolve()


TRANSCRIPTS_DIR = configured_path(
    "TRANSCRIPTS_DIR",
    "./data/transcripts",
)

MANIFEST_PATH = configured_path(
    "MANIFEST_PATH",
    "./data/manifest.json",
)

DB_PATH = configured_path(
    "DB_PATH",
    "./data/orbit.db",
)

APP_TODAY = os.getenv("APP_TODAY", "2026-07-01")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
