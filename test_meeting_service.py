from pathlib import Path

from app.services.meeting_service import load_meetings


meetings = load_meetings()

print("Total manifest meetings:", len(meetings))

for meeting in meetings:
    print(
        f"{meeting['meeting_id']} | "
        f"{meeting['title']} | "
        f"{meeting['format']} | "
        f"turns={len(meeting['turns'])}"
    )

print("\nFirst 5 turns from the first meeting:")
for turn in meetings[0]["turns"][:5]:
    print(turn)