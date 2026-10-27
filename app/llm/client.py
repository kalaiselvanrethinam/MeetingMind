
import json
import urllib.error
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3:4b"


def ask_llm(question: str, turns: list[dict]) -> dict:
    if not turns:
        return {
            "route": "no_answer",
            "answer": (
                "I couldn't find relevant evidence in the available "
                "meetings. Please ask the meeting owner."
            ),
            "turn_numbers": [],
        }

    numbered_turns = []

    for number, turn in enumerate(turns, start=1):
        numbered_turns.append(
            f"[Turn {number}]\n"
            f"Meeting date: {turn['meeting_date']}\n"
            f"Meeting ID: {turn['meeting_id']}\n"
            f"Timestamp: {turn['timestamp']}\n"
            f"Speaker ID: {turn['speaker']}\n"
            f"Text: {turn['text']}"
        )

    transcript = "\n\n".join(numbered_turns)

    prompt = f"""
You are MeetingMind, an assistant that answers questions about team meetings.

Use only the meeting transcript evidence provided below.
Do not use outside knowledge or invent facts.

Rules:
- Answer only when the evidence supports the answer.
- If the evidence does not answer the question, use route "no_answer".
- Ignore uncertain suggestions such as "maybe" or "let's revisit".
- Prefer the latest confirmed decision when decisions change.
- Cite evidence using the turn numbers shown below.
- Do not invent turn numbers.
- If the question asks how a decision changed, list the confirmed changes chronologically.
- For meeting-related questions without sufficient evidence, explain that the available meetings do not contain the answer and suggest asking the meeting owner.
- Return only valid JSON, with no Markdown or extra text.

Return one complete JSON object with exactly these three fields:
- "route": a string, either "answer" or "no_answer"
- "answer": a string containing your actual answer, not placeholder text
- "turn_numbers": an array of integer turn numbers that support the answer

For example, if turn 1 confirms the answer, return:
{{
  "route": "answer",
  "answer": "The mobile launch was moved to May 6.",
  "turn_numbers": [1]
}}

If the evidence does not answer the question, return:
{{
  "route": "no_answer",
  "answer": "The available meetings do not contain this information. Please ask the meeting owner.",
  "turn_numbers": []
}}

Do not return the words "Your answer" or omit any of the three fields.

Question:
{question}

Meeting evidence:
{transcript}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
        "think": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 250,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(
            "Could not get a response from Ollama. "
            "Make sure Ollama is running and the model is available."
        ) from error

    try:
        llm_result = json.loads(result["message"]["content"])
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "Ollama returned an invalid JSON response."
        ) from error

    if llm_result.get("route") not in {"answer", "no_answer"}:
        raise RuntimeError("Ollama returned an invalid route.")

    answer = llm_result.get("answer")
    turn_numbers = llm_result.get("turn_numbers")
    print("OLLAMA MODEL OUTPUT:", repr(llm_result))
    print("ANSWER TYPE:", type(answer).__name__)
    print("TURN NUMBERS TYPE:", type(turn_numbers).__name__)

    if not isinstance(answer, str):
        raise RuntimeError(f"Answer is not a string: {type(answer).__name__}")

    if not isinstance(turn_numbers, list):
        raise RuntimeError(
            f"Turn numbers are not a list: {type(turn_numbers).__name__}"
        )

    valid_turn_numbers = [
        number
        for number in turn_numbers
        if isinstance(number, int)
        and not isinstance(number, bool)
        and 1 <= number <= len(turns)
    ]

    if llm_result["route"] == "no_answer":
        return {
            "route": "no_answer",
            "answer": answer,
            "turn_numbers": [],
        }

    if not valid_turn_numbers:
        return {
            "route": "no_answer",
            "answer": (
                "I couldn't find sufficient supporting evidence in the "
                "available meetings. Please ask the meeting owner."
            ),
            "turn_numbers": [],
        }

    return {
        "route": "answer",
        "answer": answer,
        "turn_numbers": list(dict.fromkeys(valid_turn_numbers)),
    }
