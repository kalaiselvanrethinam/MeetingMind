
from pathlib import Path
from app.loaders.transcript_loader import load_transcript

data_dir = Path("data/transcripts")

files = [
    ("2026-02-03_pricing-tiers-working-session.vtt", "m001"),
    ("2026-04-28_mobile-launch-readiness-update.srt", "m005"),
    ("2026-03-04_mobile-launch-replanning.txt", "m002"),
    ("2026-03-17_pricing-page-design-review_export.json", "m003"),
]

for filename, meeting_id in files:
    file_path = data_dir / filename

    turns = load_transcript(file_path, meeting_id)

    print(f"\nFile: {filename}")
    print(f"Parsed turns: {len(turns)}")
    print("First turn:", turns[0] if turns else "No turns found")
