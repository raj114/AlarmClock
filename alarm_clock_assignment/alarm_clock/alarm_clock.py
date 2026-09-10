#!/usr/bin/env python3
"""
Simple CLI Alarm Clock
30-minute assignment version: standard library only, no DB/web UI.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse
import time
import threading
import sys


@dataclass
class Alarm:
    alarm_id: int
    when: datetime
    label: str
    enabled: bool = True


class AlarmClock:
    def __init__(self):
        self.alarms: list[Alarm] = []
        self.next_id = 1
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def add_alarm(self, when: datetime, label: str = "") -> Alarm:
        with self._lock:
            alarm = Alarm(self.next_id, when, label or "Alarm")
            self.alarms.append(alarm)
            self.next_id += 1
            return alarm

    def list_alarms(self) -> list[Alarm]:
        with self._lock:
            return sorted(self.alarms, key=lambda a: a.when)

    def cancel_alarm(self, alarm_id: int) -> bool:
        with self._lock:
            for alarm in self.alarms:
                if alarm.alarm_id == alarm_id and alarm.enabled:
                    alarm.enabled = False
                    return True
        return False

    def _check_alarms(self):
        while not self._stop_event.is_set():
            now = datetime.now()
            triggered = []

            with self._lock:
                for alarm in self.alarms:
                    if alarm.enabled and alarm.when <= now:
                        alarm.enabled = False
                        triggered.append(alarm)

            for alarm in triggered:
                self._ring(alarm)

            # 0.5 sec polling keeps the implementation simple and responsive.
            self._stop_event.wait(0.5)

    @staticmethod
    def _ring(alarm: Alarm):
        print(f"\n\n*** ALARM {alarm.alarm_id}: {alarm.label} ***")
        print(f"Scheduled for: {alarm.when.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\a" * 3, flush=True)

    def run(self):
        print("Alarm Clock started. Press Ctrl+C to exit.")
        print("Commands: add HH:MM [label] | list | cancel ID | exit")

        worker = threading.Thread(target=self._check_alarms, daemon=True)
        worker.start()

        try:
            while True:
                command = input("\nalarm> ").strip()
                if not command:
                    continue
                if command.lower() in {"exit", "quit"}:
                    break
                self.handle_command(command)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
        finally:
            self._stop_event.set()

    def handle_command(self, command: str):
        parts = command.split(maxsplit=2)
        action = parts[0].lower()

        if action == "add":
            if len(parts) < 2:
                print("Usage: add HH:MM [label]")
                return
            try:
                when = parse_time(parts[1])
            except ValueError as exc:
                print(f"Error: {exc}")
                return

            label = parts[2] if len(parts) == 3 else "Alarm"
            alarm = self.add_alarm(when, label)
            print(
                f"Added alarm #{alarm.alarm_id} for "
                f"{alarm.when.strftime('%Y-%m-%d %H:%M:%S')} - {alarm.label}"
            )

        elif action == "list":
            alarms = self.list_alarms()
            if not alarms:
                print("No alarms.")
                return
            for alarm in alarms:
                status = "enabled" if alarm.enabled else "disabled"
                print(
                    f"#{alarm.alarm_id} | "
                    f"{alarm.when.strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"{status} | {alarm.label}"
                )

        elif action == "cancel":
            if len(parts) != 2 or not parts[1].isdigit():
                print("Usage: cancel ID")
                return
            if self.cancel_alarm(int(parts[1])):
                print(f"Alarm #{parts[1]} cancelled.")
            else:
                print(f"Active alarm #{parts[1]} not found.")

        else:
            print("Unknown command. Use: add, list, cancel, exit")


def parse_time(value: str) -> datetime:
    """Parse HH:MM as the next occurrence of that local time."""
    try:
        hour, minute = map(int, value.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        raise ValueError("time must be in HH:MM 24-hour format")

    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


def main():
    parser = argparse.ArgumentParser(description="CLI alarm clock")
    parser.add_argument(
        "--alarm",
        help="Start with one alarm, e.g. --alarm 18:30:00",
    )
    args = parser.parse_args()

    clock = AlarmClock()

    if args.alarm:
        try:
            when = datetime.strptime(args.alarm, "%H:%M:%S")
            now = datetime.now()
            when = now.replace(
                hour=when.hour, minute=when.minute, second=when.second, microsecond=0
            )
            if when <= now:
                when += timedelta(days=1)
            alarm = clock.add_alarm(when)
            print(f"Initial alarm #{alarm.alarm_id} scheduled.")
        except ValueError:
            print("Error: --alarm must use HH:MM:SS")
            sys.exit(2)

    clock.run()


if __name__ == "__main__":
    main()
