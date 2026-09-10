import unittest
from datetime import datetime, timedelta
from alarm_clock import AlarmClock, parse_time


class AlarmClockTests(unittest.TestCase):
    def test_add_alarm(self):
        clock = AlarmClock()
        when = datetime.now() + timedelta(minutes=5)
        alarm = clock.add_alarm(when, "Test")
        self.assertEqual(alarm.alarm_id, 1)
        self.assertEqual(alarm.label, "Test")
        self.assertTrue(alarm.enabled)

    def test_cancel_alarm(self):
        clock = AlarmClock()
        alarm = clock.add_alarm(datetime.now() + timedelta(minutes=5))
        self.assertTrue(clock.cancel_alarm(alarm.alarm_id))
        self.assertFalse(alarm.enabled)
        self.assertFalse(clock.cancel_alarm(alarm.alarm_id))

    def test_parse_time_returns_future_occurrence(self):
        result = parse_time("23:59")
        self.assertEqual(result.second, 0)
        self.assertEqual(result.microsecond, 0)


if __name__ == "__main__":
    unittest.main()
