
from app.llm.token_limiter import (
    encoding,
    MAX_TRANSCRIPT_TOKENS,
    limit_turns_by_tokens,
)

sample_turns = [
    {
        "meeting_id": "m002",
        "meeting_date": "2026-03-04",
        "timestamp": "00:03:38",
        "speaker": "p01",
        "text": "We move the mobile launch to May 6.",
        "score": 3,
    },
    {
        "meeting_id": "m002",
        "meeting_date": "2026-03-04",
        "timestamp": "00:04:01",
        "speaker": "p04",
        "text": "Agreed. The crash-free bar still applies.",
        "score": 2,
    },
]

limited_turns = limit_turns_by_tokens(sample_turns)

total_tokens = 0

for turn in limited_turns:
    transcript_text = (
        f"Meeting date: {turn['meeting_date']}\n"
        f"Timestamp: {turn['timestamp']}\n"
        f"Speaker: {turn['speaker']}\n"
        f"Text: {turn['text']}\n"
    )
    total_tokens += len(encoding.encode(transcript_text))

print("Original turns:", len(sample_turns))
print("Selected turns:", len(limited_turns))
print("Transcript tokens:", total_tokens)
print("Token budget:", MAX_TRANSCRIPT_TOKENS)
print("Within limit:", total_tokens <= MAX_TRANSCRIPT_TOKENS)
