
from app.services.meeting_service import load_meetings
from app.services.filter_service import filter_meetings
from app.retrieval.retriever import retrieve_turns


meetings = load_meetings()

filtered_meetings = filter_meetings(
    meetings,
    project="mobile-app-launch",
    as_of="2026-04-01",
)

results = retrieve_turns(
    filtered_meetings,
    question = "Who was responsible for the campaign?",
    top_k=5,
)

print("Retrieved turns:", len(results))

for result in results:
    print("\nMeeting:", result["meeting_id"])
    print("Date:", result["meeting_date"])
    print("Timestamp:", result["timestamp"])
    print("Speaker:", result["speaker"])
    print("Score:", result["score"])
    print("Text:", result["text"])
