
from pathlib import Path
from app.loaders.database_loader import load_database

database_path = Path("data") / "orbit.db"
data = load_database(database_path)

print("Total people:", len(data["people"]))
print("Total projects:", len(data["projects"]))

print("\nFirst person:")
print(data["people"][0])

print("\nFirst project:")
print(data["projects"][0])
