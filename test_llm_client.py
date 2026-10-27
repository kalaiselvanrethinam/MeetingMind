
from app.llm.client import ask_llm


sample_turns = [
    {
        "meeting_id": "m002",
        "meeting_date": "2026-03-04",
        "timestamp": "00:03:38",
        "speaker": "p01",
        "text": "We move the mobile launch to May 6.",
        "score": 3,
    }
]

result = ask_llm(
    question="What was the mobile launch date?",
    turns=sample_turns,
)

print("Route:", result["route"])
print("Answer:", result["answer"])
print("Turn numbers:", result["turn_numbers"])


empty_result = ask_llm(
    question="What was the mobile launch date?",
    turns=[],
)

print("\nEmpty evidence test:")
print("Route:", empty_result["route"])
print("Turn numbers:", empty_result["turn_numbers"])
