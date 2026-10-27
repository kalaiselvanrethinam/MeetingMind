
from pathlib import Path

from app.loaders.database_loader import load_database
from app.loaders.speaker_normalizer import build_speaker_lookup
from app.loaders.transcript_loader import load_transcript

data_dir = Path("data")

database = load_database(data_dir / "orbit.db")
speaker_lookup = build_speaker_lookup(database["people"])

transcript_path = (
    data_dir / "transcripts" / "2026-05-13_mobile-weekly-sync.txt"
)

turns = load_transcript(
    file_path=transcript_path,
    meeting_id="m006",
    speaker_lookup=speaker_lookup,
)

print(f"Total turns: {len(turns)}")
print("\nFirst 5 turns:")

for turn in turns[:5]:
    print(turn)
