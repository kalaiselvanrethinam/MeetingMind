
from app.services.meeting_service import load_meetings
from app.services.filter_service import filter_meetings


meetings = load_meetings()

print("Total meetings:", len(meetings))

# Test 1: Filter by project
project_results = filter_meetings(
    meetings,
    project="mobile-app-launch",
)
print("Mobile project meetings:", len(project_results))

# Test 2: Filter by speaker
speaker_results = filter_meetings(
    meetings,
    speaker="p01",
)
print("Meetings containing speaker p01:", len(speaker_results))

# Verify that no other speaker's turns remain.
all_speakers = {
    turn["speaker"]
    for meeting in speaker_results
    for turn in meeting["turns"]
}
print("Speakers remaining after filter:", all_speakers)

# Test 3: Filter by date range
date_results = filter_meetings(
    meetings,
    date_from="2026-04-01",
    date_to="2026-05-31",
)
print("Meetings in date range:", len(date_results))

# Test 4: Apply the as_of date
as_of_results = filter_meetings(
    meetings,
    as_of="2026-04-30",
)
print("Meetings on or before April 30:", len(as_of_results))
