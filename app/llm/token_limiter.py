
import tiktoken

MAX_TRANSCRIPT_TOKENS = 2700

encoding = tiktoken.get_encoding("cl100k_base")


def limit_turns_by_tokens(turns: list[dict]) -> list[dict]:
    selected_turns = []
    total_tokens = 0

    for turn in turns:
        transcript_text = (
            f"Meeting date: {turn['meeting_date']}\n"
            f"Timestamp: {turn['timestamp']}\n"
            f"Speaker: {turn['speaker']}\n"
            f"Text: {turn['text']}\n"
        )

        token_count = len(encoding.encode(transcript_text))

        if total_tokens + token_count > MAX_TRANSCRIPT_TOKENS:
            continue

        selected_turns.append(turn)
        total_tokens += token_count

    return selected_turns
