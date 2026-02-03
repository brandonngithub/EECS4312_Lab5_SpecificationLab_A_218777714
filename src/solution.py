## Student Name: Brandon Ngo
## Student ID: 218777714

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    # Working hours and lunch break (24h format in minutes from midnight)
    WORK_START = 9 * 60       # 09:00
    LUNCH_START = 12 * 60     # 12:00
    LUNCH_END = 13 * 60       # 13:00
    WORK_END = 17 * 60        # 17:00

    STEP = 15  # minutes granularity for meeting starts

    def to_minutes(hhmm: str) -> int:
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    def to_hhmm(minutes: int) -> str:
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    if meeting_duration <= 0:
        return []

    # Build candidate working windows excluding lunch
    working_windows = [
        (WORK_START, LUNCH_START),
        (LUNCH_END, WORK_END),
    ]

    # Normalize and keep only relevant event intervals as minutes
    event_intervals: List[tuple[int, int]] = []
    for e in events:
        try:
            s = to_minutes(e["start"])
            t = to_minutes(e["end"])
        except Exception:
            # Skip malformed entries
            continue
        if t <= s:
            # Ignore zero or negative length events
            continue
        event_intervals.append((s, t))

    # Function to test overlap between [a_start, a_end) and [b_start, b_end)
    def overlaps_strict(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
        # Strict overlap only; touching at endpoints is allowed
        return (a_start < b_end) and (a_end > b_start)

    slots: List[str] = []

    for win_start, win_end in working_windows:
        # If meeting doesn't fit this window at all, skip
        if win_start + meeting_duration > win_end:
            continue

        # Generate candidate starts on 15-min steps within window
        start = win_start
        # Align start to nearest STEP grid just in case
        if start % STEP != 0:
            start += (STEP - (start % STEP))

        while start + meeting_duration <= win_end:
            meeting_start = start
            meeting_end = start + meeting_duration

            # Exclude if overlaps any event
            has_overlap = False
            for es, ee in event_intervals:
                # Base strict overlap
                if overlaps_strict(meeting_start, meeting_end, es, ee):
                    has_overlap = True
                    break
                # Additional constraint: for meetings 30+ minutes, don't start exactly at an event end
                if meeting_duration >= 30 and meeting_start == ee:
                    has_overlap = True
                    break

            if not has_overlap:
                slots.append(to_hhmm(meeting_start))

            start += STEP

    return sorted(slots)