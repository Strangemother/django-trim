"""
Test trim.templatetags.datetime module.

Simple tests for datetime template tags.
"""

import unittest
from datetime import datetime, timedelta

from trim.templatetags.datetime import (
    localize_timedelta,
    str_timedelta_tag,
    timedelta_tag,
)


class LocalizeTimedeltaTest(unittest.TestCase):
    """Test localize_timedelta function."""

    def test_only_seconds(self):
        # Setup
        delta = timedelta(seconds=45)

        # Execute & Assert
        self.assertEqual(localize_timedelta(delta), "45 seconds")

    def test_only_minutes(self):
        # Setup
        delta = timedelta(minutes=30)

        # Execute
        result = localize_timedelta(delta)

        # Assert
        self.assertIn("30 minutes", result)
        self.assertNotIn("second", result)

    def test_hours_and_minutes(self):
        # Setup
        delta = timedelta(hours=2, minutes=15)

        # Execute
        result = localize_timedelta(delta)

        # Assert
        self.assertIn("2 hours", result)
        self.assertIn("15 minutes", result)

    def test_days_hours_minutes(self):
        # Setup
        delta = timedelta(days=3, hours=4, minutes=20)

        # Execute
        result = localize_timedelta(delta)

        # Assert
        self.assertIn("3 days", result)
        self.assertIn("4 hours", result)
        self.assertIn("20 minutes", result)

    def test_with_years(self):
        # Setup
        delta = timedelta(days=400, hours=2)

        # Execute
        result = localize_timedelta(delta)

        # Assert
        self.assertIn("1 year", result)
        self.assertIn("35 days", result)

    def test_singular_forms(self):
        # Setup
        delta = timedelta(days=1, hours=1, minutes=1)

        # Execute
        result = localize_timedelta(delta)

        # Assert
        self.assertIn("1 day", result)
        self.assertIn("1 hour", result)
        self.assertIn("1 minute", result)
        self.assertNotIn("days", result)
        self.assertNotIn("hours", result)
        self.assertNotIn("minutes", result)


class TimedeltaTagTest(unittest.TestCase):
    """Test timedelta_tag function."""

    def test_returns_timedelta_object(self):
        # Setup
        early = datetime(2024, 1, 1, 10, 0, 0)
        late = datetime(2024, 1, 1, 12, 30, 0)

        # Execute
        result = timedelta_tag(late, early)

        # Assert
        self.assertIsInstance(result, timedelta)
        self.assertEqual(result, timedelta(hours=2, minutes=30))

    def test_calculates_difference(self):
        # Setup
        early = datetime(2024, 1, 1, 0, 0, 0)
        late = datetime(2024, 1, 3, 6, 0, 0)

        # Execute
        result = timedelta_tag(late, early)

        # Assert
        self.assertEqual(result.days, 2)
        self.assertEqual(result.seconds, 6 * 3600)


class StrTimedeltaTagTest(unittest.TestCase):
    """Test str_timedelta_tag function."""

    def test_returns_human_readable_string(self):
        # Setup
        early = datetime(2024, 1, 1, 10, 0, 0)
        late = datetime(2024, 1, 1, 12, 30, 0)

        # Execute
        result = str_timedelta_tag(late, early)

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn("2 hours", result)
        self.assertIn("30 minutes", result)

    def test_with_days(self):
        # Setup
        early = datetime(2024, 1, 1, 0, 0, 0)
        late = datetime(2024, 1, 4, 3, 15, 0)

        # Execute
        result = str_timedelta_tag(late, early)

        # Assert
        self.assertIn("3 days", result)
        self.assertIn("3 hours", result)
        self.assertIn("15 minutes", result)


if __name__ == "__main__":
    unittest.main()
