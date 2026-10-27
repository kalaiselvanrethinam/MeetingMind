from app.services.citation_service import build_citations


turns = [
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
        "text": "Agreed. And the crash-free bar we set still applies.",
        "score": 2,
    },
]


print("One citation:")
print(build_citations(turns, [1]))


print("\nMultiple citations:")
print(build_citations(turns, [1, 2]))


print("\nDuplicate citation:")
print(build_citations(turns, [1, 1]))


print("\nInvalid turn number:")
print(build_citations(turns, [99]))