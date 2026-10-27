
from pathlib import Path
from app.loaders.manifest_loader import load_manifest

manifest_path = Path("data") / "manifest.json"
meetings = load_manifest(manifest_path)

print("Total manifest entries:", len(meetings))
print("First meeting:", meetings[0]["title"])
print("First meeting ID:", meetings[0]["meeting_id"])
