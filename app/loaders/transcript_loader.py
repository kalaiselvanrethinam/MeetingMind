
import json
import re
from pathlib import Path
from app.loaders.speaker_normalizer import resolve_speaker


def format_timestamp(total_seconds: float) -> str:
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:06.3f}"


def add_turn(
    turns: list[dict],
    meeting_id: str,
    timestamp: str,
    speaker: str | None,
    text: str,
) -> None:
    text = text.strip()

    if not text:
        return

    # Merge consecutive captions from the same speaker.
    if turns and turns[-1]["speaker"] == speaker:
        turns[-1]["text"] += " " + text
    else:
        turns.append({
            "meeting_id": meeting_id,
            "timestamp": timestamp,
            "speaker": speaker,
            "text": text,
        })


def parse_vtt(file_path: Path, meeting_id: str) -> list[dict]:
    content = file_path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", content.strip())
    turns = []

    for block in blocks:
        lines = block.strip().splitlines()

        if not lines:
            continue

        if lines[0].startswith(("WEBVTT", "NOTE")):
            continue

        timestamp_index = next(
            (i for i, line in enumerate(lines) if "-->" in line),
            None,
        )

        if timestamp_index is None:
            continue

        timestamp = lines[timestamp_index].split("-->")[0].strip()
        caption = " ".join(lines[timestamp_index + 1:]).strip()

        match = re.match(r"<v\s+([^>]+)>(.*?)</v>", caption)

        if match:
            speaker = match.group(1).strip()
            text = match.group(2).strip()
            add_turn(turns, meeting_id, timestamp, speaker, text)

    return turns


def parse_srt(file_path: Path, meeting_id: str) -> list[dict]:
    content = file_path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", content.strip())
    turns = []

    for block in blocks:
        lines = block.strip().splitlines()

        timestamp_index = next(
            (i for i, line in enumerate(lines) if "-->" in line),
            None,
        )

        if timestamp_index is None:
            continue

        raw_timestamp = lines[timestamp_index].split("-->")[0].strip()
        timestamp = raw_timestamp.replace(",", ".")
        caption = " ".join(lines[timestamp_index + 1:]).strip()

        # SRT captions may start with a speaker label, e.g. "TH: ..."
        match = re.match(r"^([^:\n]{1,60}):\s*(.+)$", caption)

        if match:
            speaker = match.group(1).strip()
            text = match.group(2).strip()
        else:
            speaker = None
            text = caption

        add_turn(turns, meeting_id, timestamp, speaker, text)

    return turns


def parse_txt(file_path: Path, meeting_id: str) -> list[dict]:
    content = file_path.read_text(encoding="utf-8-sig")
    turns = []

    pattern = re.compile(
        r"^\[(\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s*"
        r"([^:]+):\s*(.*)$"
    )

    for line in content.splitlines():
        match = pattern.match(line.strip())

        if not match:
            continue

        timestamp, speaker, text = match.groups()
        add_turn(
            turns,
            meeting_id,
            timestamp,
            speaker.strip(),
            text.strip(),
        )

    return turns


def parse_json(file_path: Path, meeting_id: str) -> list[dict]:
    with file_path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    segments = data.get("segments")

    if not isinstance(segments, list):
        raise ValueError(
            f"Expected a 'segments' list in {file_path.name}"
        )

    turns = []

    for segment in segments:
        if not isinstance(segment, dict):
            continue

        speaker = segment.get("spk")
        text = segment.get("content", "")
        start_ms = segment.get("start_ms")

        if start_ms is None:
            continue

        timestamp = format_timestamp(float(start_ms) / 1000)

        add_turn(
            turns,
            meeting_id,
            timestamp,
            speaker.strip() if isinstance(speaker, str) else None,
            text if isinstance(text, str) else "",
        )

    return turns



def load_transcript(
    file_path: Path,
    meeting_id: str,
    file_format: str | None = None,
    speaker_lookup: dict | None = None,
) -> list[dict]:
    file_format = (file_format or file_path.suffix.lstrip(".")).lower()

    parsers = {
        "vtt": parse_vtt,
        "srt": parse_srt,
        "txt": parse_txt,
        "json": parse_json,
    }

    parser = parsers.get(file_format)

    if parser is None:
        raise ValueError(f"Unsupported transcript format: {file_format}")

    turns = parser(file_path, meeting_id)

    # If no speaker lookup is provided, return the parsed turns.
    
    if speaker_lookup is None:
        return turns

    normalized_turns = []

    for turn in turns:
        person_id = resolve_speaker(
            turn["speaker"],
            speaker_lookup,
        )

        normalized_turns.append({
            "meeting_id": turn["meeting_id"],
            "timestamp": turn["timestamp"],
            "speaker": person_id,
            "text": turn["text"],
        })

    return normalized_turns


