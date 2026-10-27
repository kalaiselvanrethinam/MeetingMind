
from app.loaders.database_loader import load_database
from app.config import DB_PATH
from app.services.validation_service import validate_filters


database = load_database(DB_PATH)

projects = database["projects"]
people = database["people"]


def run_test(test_name, **filters):
    try:
        validate_filters(
            project=filters.get("project"),
            speaker=filters.get("speaker"),
            date_from=filters.get("date_from"),
            date_to=filters.get("date_to"),
            as_of=filters.get("as_of"),
            projects=projects,
            people=people,
        )
        print(f"{test_name}: PASSED")
    except ValueError as error:
        print(f"{test_name}: REJECTED - {error}")


run_test(
    "Valid filters",
    project="pricing-v2",
    date_from="2026-01-01",
    date_to="2026-06-30",
)

run_test(
    "Unknown project",
    project="unknown-project",
)

run_test(
    "Unknown speaker",
    speaker="p999",
)

run_test(
    "Invalid date format",
    date_from="2026-7-1",
)

run_test(
    "Start date after end date",
    date_from="2026-06-01",
    date_to="2026-04-01",
)
