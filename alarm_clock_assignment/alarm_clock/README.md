# Python CLI Alarm Clock

A small, production-minded 30-minute assignment implementation using only Python's standard library.

## Scope

- CLI only
- No web UI
- No database
- Multiple alarms
- Add alarm using `HH:MM`
- List alarms
- Cancel alarms
- One-shot alarms (an alarm disables itself after ringing)
- Background monitoring thread so the CLI remains interactive
- Basic unit tests
- Clean separation between command handling and alarm state

## Requirements

Python 3.10+.

## Run

```bash
python alarm_clock.py
```

Example:

```text
Alarm Clock started. Press Ctrl+C to exit.
Commands: add HH:MM [label] | list | cancel ID | exit

alarm> add 21:30 Team meeting
Added alarm #1 for 2026-09-10 21:30:00 - Team meeting

alarm> list
#1 | 2026-09-10 21:30:00 | enabled | Team meeting

alarm> cancel 1
Alarm #1 cancelled.
```

For a quick test, schedule the alarm 1–2 minutes ahead of the current time.

## Optional initial alarm

```bash
python alarm_clock.py --alarm 21:30:00
```

## Tests

```bash
python -m unittest -v
```

## Design decisions

1. **In-memory state:** The assignment explicitly says no database, so alarms exist for the process lifetime only.
2. **24-hour time:** `HH:MM` is unambiguous and keeps parsing simple.
3. **Next occurrence:** If today's requested time has already passed, the alarm is scheduled for tomorrow.
4. **One-shot behavior:** Once an alarm fires, it is disabled rather than repeatedly firing every day.
5. **Threading:** A daemon worker checks alarms every 500 ms while the main thread accepts CLI commands.
6. **Thread safety:** A lock protects the shared alarm collection.
7. **Standard library only:** No third-party dependencies, making the solution easy to run and review.

## Deliberately not implemented

For a 30-minute exercise, I would avoid persistence, recurring alarms, snooze, audio files, timezone handling, multiprocessing, and a complex command framework. Those are reasonable follow-up features but add scope without being necessary to demonstrate the core design.
