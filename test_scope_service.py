
from app.services.scope_service import is_out_of_scope

questions = [
    "Write an email to my manager asking for leave.",
    "What is the weather today?",
    "What was the mobile launch date?",
    "Who decided the launch date?",
]

for question in questions:
    result = is_out_of_scope(question)
    print(f"Question: {question}")
    print(f"Out of scope: {result}")
    print()
