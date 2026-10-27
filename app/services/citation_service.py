def build_citations(
    turns: list[dict],
    turn_numbers: list[int],
) -> list[dict]:
    """
    Convert LLM-selected turn numbers into trusted citations.

    The LLM only selects turn numbers.
    Python gets the actual citation information
    from the retrieved transcript turns.
    """

    citations = []

    for number in turn_numbers:
        if not isinstance(number, int):
            continue

        index = number - 1

        if index < 0 or index >= len(turns):
            continue

        turn = turns[index]

        citation = {
            "meeting_id": turn["meeting_id"],
            "timestamp": turn["timestamp"],
            "speaker": turn["speaker"],
        }

        if citation not in citations:
            citations.append(citation)

    return citations