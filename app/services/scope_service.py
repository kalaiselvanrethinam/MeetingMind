
def is_out_of_scope(question: str) -> bool:
    question_lower = question.lower().strip()

    out_of_scope_patterns = [
        "write an email",
        "draft an email",
        "send an email",
        "write a message",
        "draft a message",
        "write a poem",
        "tell me a joke",
        "give me a recipe",
        "what is the weather",
        "translate this",
        "write code",
    ]

    return any(
        pattern in question_lower
        for pattern in out_of_scope_patterns
    )
