
import sqlite3
from pathlib import Path


def load_database(database_path: Path) -> dict:
    if not database_path.exists():
        raise FileNotFoundError(
            f"Database file not found: {database_path}"
        )

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        people = [
            dict(row)
            for row in connection.execute("SELECT * FROM people")
        ]

        projects = [
            dict(row)
            for row in connection.execute("SELECT * FROM projects")
        ]

    return {
        "people": people,
        "projects": projects,
    }
