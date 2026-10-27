import re


STOP_WORDS = {
    "a", "an", "the", "is", "was", "were", "are", "am",
    "what", "when", "where", "who", "why", "how",
    "did", "do", "does", "of", "to", "in", "on", "for",
    "and", "or", "it", "this", "that", "with", "about",
    "we", "they", "he", "she", "i", "you", "our", "their",
    "be", "been", "being", "by", "from", "as", "at",
    "have", "has", "had", "will", "would", "could",
    "should", "can", "may", "might", "not",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())

    return [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]


def get_question_intent(question: str) -> str:
    words = set(tokenize(question))

    if "who" in question.lower().split():
        return "person"

    if words & {"budget", "cost", "price", "spend", "expense"}:
        return "budget"

    if words & {"date", "when", "launch"}:
        return "date"

    if words & {"decision", "changed", "change", "moved", "replanned"}:
        return "decision"

    if words & {"responsible", "owner", "assigned"}:
        return "responsibility"

    if words & {"reason", "why"}:
        return "reason"

    return "general"


def retrieve_turns(
    meetings: list[dict],
    question: str,
    top_k: int = 10,
) -> list[dict]:
    """
    Retrieve transcript turns using keyword overlap.

    The scoring gives extra importance to words that indicate
    the type of information being requested.
    """

    question_words = set(tokenize(question))

    if not question_words:
        return []

    intent = get_question_intent(question)

    intent_words = {
        "person": {
            "responsible", "owner", "assigned",
            "handle", "lead", "manage", "campaign"
        },
        "budget": {
            "budget", "cost", "price", "spend", "expense",
            "amount", "dollar", "usd"
        },
        "date": {
            "date", "launch", "deadline", "submission",
            "may", "april", "march", "june"
        },
        "decision": {
            "decision", "move", "moved", "change", "changed",
            "replan", "replanned", "approved", "confirmed"
        },
        "responsibility": {
            "responsible", "owner", "assigned", "update",
            "handle", "lead", "manage", "campaign"
        },
        "reason": {
            "reason", "because", "risk", "issue", "problem",
            "rejection", "buffer"
        },
        "general": set(),
    }

    candidates = []

    for meeting in meetings:
        for turn in meeting["turns"]:

            turn_words = set(tokenize(turn["text"]))

            matched_words = question_words & turn_words
            intent_matches = intent_words[intent] & turn_words

            if not matched_words and not intent_matches:
                continue

            # Normal keyword overlap
            score = len(matched_words)

            # Give extra weight to intent-related evidence
            score += len(intent_matches) * 2

            # For person/responsibility questions, statements
            # containing action words are useful evidence.
            if intent in {"person", "responsibility"}:
                action_words = {
                "handle", "lead", "manage",
                "own", "assigned", "responsible"
                }

                if turn_words & action_words:
                    score += 2

            candidates.append({
                "meeting_id": meeting["meeting_id"],
                "meeting_date": meeting["date"],
                "timestamp": turn["timestamp"],
                "speaker": turn["speaker"],
                "text": turn["text"],
                "score": score,
            })

    candidates.sort(
        key=lambda item: (
            -item["score"],
            item["meeting_date"],
            item["timestamp"],
        )
    )

    return candidates[:top_k]