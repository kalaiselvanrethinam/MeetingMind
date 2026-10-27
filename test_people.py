from pathlib import Path
from app.loaders.database_loader import load_database

database_path = Path("data") / "orbit.db"
data = load_database(database_path)

for person in data["people"]:
    print(
        person["person_id"],
        "|",
        person["full_name"],
        "| aliases:",
        person["aliases"],
    )