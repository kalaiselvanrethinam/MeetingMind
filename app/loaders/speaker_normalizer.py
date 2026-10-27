    
import json
import re
import unicodedata


def normalize_text(value: str) -> str:
    """Normalize names for case- and accent-insensitive matching."""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )
    value = value.casefold()
    return re.sub(r"[^a-z0-9]", "", value)


def build_speaker_lookup(people: list[dict]) -> dict:
    lookup = {}

    for person in people:
        person_id = person["person_id"]
        full_name = person["full_name"]

        aliases = person.get("aliases", "[]")

        if isinstance(aliases, str):
            aliases = json.loads(aliases)

        names = [full_name, *aliases]

        for name in names:
            key = normalize_text(name)

            # Avoid silently assigning one alias to two different people.
            if key in lookup and lookup[key]["person_id"] != person_id:
                raise ValueError(f"Duplicate speaker alias: {name}")

            lookup[key] = {
                "person_id": person_id,
                "full_name": full_name,
            }

    return lookup



def resolve_speaker(speaker: str | None, lookup: dict) -> str | None:
    if not speaker or not speaker.strip():
        return None

    match = lookup.get(normalize_text(speaker))

    if match:
        return match["person_id"]

    return None

