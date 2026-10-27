
from pathlib import Path

from app.config import (
    TRANSCRIPTS_DIR,
    MANIFEST_PATH,
    DB_PATH,
)
from app.loaders.database_loader import load_database
from app.loaders.manifest_loader import load_manifest
from app.loaders.speaker_normalizer import build_speaker_lookup
from app.loaders.transcript_loader import load_transcript


def load_meetings() -> list[dict]:
    manifest = load_manifest(MANIFEST_PATH)
    database = load_database(DB_PATH)

    speaker_lookup = build_speaker_lookup(
        database["people"]
    )

    meetings = []
    seen_meeting_ids = set()

    for entry in manifest:
        meeting_id = entry["meeting_id"]

        if meeting_id in seen_meeting_ids:
            continue

        filename = entry["file"]
        file_format = entry["format"]
        transcript_path = TRANSCRIPTS_DIR / filename

        if not transcript_path.exists():
            raise FileNotFoundError(
                f"Transcript not found: {transcript_path}"
            )

        turns = load_transcript(
            file_path=transcript_path,
            meeting_id=meeting_id,
            file_format=file_format,
            speaker_lookup=speaker_lookup,
        )

        unresolved = [
            turn for turn in turns
            if turn["speaker"] is None
        ]

        if unresolved:
            raise ValueError(
                f"{len(unresolved)} transcript turns in "
                f"{filename} have an unknown or missing speaker."
            )

        meeting = {
            "meeting_id": meeting_id,
            "title": entry["title"],
            "date": entry["date"],
            "project": entry["project"],
            "meeting_type": entry["meeting_type"],
            "format": entry["format"],
            "attendees": entry["attendees"],
            "duration_min": entry["duration_min"],
            "transcript_file": filename,
            "turns": turns,
        }

        meetings.append(meeting)
        seen_meeting_ids.add(meeting_id)

    return meetings
