
from datetime import date


def validate_date(value: str | None, field_name: str) -> None:
    if value is None:
        return

    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD format."
        )

    # Reject formats such as 2026-7-1.
    if parsed_date.isoformat() != value:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD format."
        )


def validate_filters(
    project: str | None,
    speaker: str | None,
    date_from: str | None,
    date_to: str | None,
    as_of: str | None,
    projects: list[dict],
    people: list[dict],
) -> None:
    project_ids = {
        item["project_id"] for item in projects
    }

    person_ids = {
        item["person_id"] for item in people
    }

    if project and project not in project_ids:
        raise ValueError(f"Unknown project: {project}")

    if speaker and speaker not in person_ids:
        raise ValueError(f"Unknown speaker: {speaker}")

    validate_date(date_from, "date_from")
    validate_date(date_to, "date_to")
    validate_date(as_of, "as_of")

    if date_from and date_to and date_from > date_to:
        raise ValueError(
            "date_from cannot be later than date_to."
        )
