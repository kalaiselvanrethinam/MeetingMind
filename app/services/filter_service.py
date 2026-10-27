
from datetime import date


def filter_meetings(
    meetings: list[dict],
    project: str | None = None,
    speaker: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    as_of: str = "2026-07-01",
) -> list[dict]:
    reference_date = date.fromisoformat(as_of)
    start_date = date.fromisoformat(date_from) if date_from else None
    end_date = date.fromisoformat(date_to) if date_to else None

    filtered_meetings = []

    for meeting in meetings:
        meeting_date = date.fromisoformat(meeting["date"])

        # Do not include meetings after the reference date.
        if meeting_date > reference_date:
            continue

        if start_date and meeting_date < start_date:
            continue

        if end_date and meeting_date > end_date:
            continue

        if project and meeting["project"] != project:
            continue

        filtered_meetings.append(meeting)

    # If a speaker filter is provided, keep only their turns.
    if speaker:
        result = []

        for meeting in filtered_meetings:
            matching_turns = [
                turn for turn in meeting["turns"]
                if turn["speaker"] == speaker
            ]

            if matching_turns:
                filtered_meeting = {
                    **meeting,
                    "turns": matching_turns,
                }
                result.append(filtered_meeting)

        return result

    return filtered_meetings
