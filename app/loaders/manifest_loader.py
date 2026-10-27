
import json
from pathlib import Path


def load_manifest(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest file not found: {manifest_path}"
        )

    with manifest_path.open("r", encoding="utf-8") as file:
        meetings = json.load(file)

    if not isinstance(meetings, list):
        raise ValueError(
            "The manifest must contain a list of meetings."
        )

    return meetings
