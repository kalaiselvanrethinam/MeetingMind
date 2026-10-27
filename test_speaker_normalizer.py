
from pathlib import Path

from app.loaders.database_loader import load_database
from app.loaders.speaker_normalizer import (
    build_speaker_lookup,
    resolve_speaker,
)

data = load_database(Path("data") / "orbit.db")
lookup = build_speaker_lookup(data["people"])

test_names = [
    "LM",
    "Lucas",
    "LUCAS MARTIN",
    "TH",
    "Tomas Herrera",
    "Tomás Herrera",
    "KW",
    "Unknown Person",
]

for name in test_names:
    result = resolve_speaker(name, lookup)
    print(f"{name:20} -> {result}")
