import unittest
import string

from trim.rand import rand_str


class RandTestCase(unittest.TestCase):
    """Test case for the trim rand module."""

    def test_rand_str_length(self):
        """Test that rand_str generates a string of the correct length."""
        length = 10
        result = rand_str(length)
        self.assertEqual(len(result), length)

    def test_rand_str_content(self):
        """Test that rand_str generates a string with valid characters."""
        result = rand_str()
        valid_chars = set(string.ascii_uppercase + string.digits)
        self.assertTrue(all(c in valid_chars for c in result))


class TestRandStr(unittest.TestCase):
    def setUp(self):
        # Setup: Prepare any required variables or state
        self.length = 6

    def test_rand_str_default_length(self):
        """Test rand_str returns a string of default length."""
        # Expected: String of length 6
        # Result: Call rand_str and check length
        result = rand_str()
        self.assertEqual(len(result), self.length)

    def test_rand_str_custom_length(self):
        """Test rand_str returns a string of specified length."""
        # Expected: String of custom length
        # Result: Call rand_str with custom length and check
        custom_length = 8
        result = rand_str(custom_length)
        self.assertEqual(len(result), custom_length)

    def test_rand_str_characters(self):
        """Test rand_str only uses uppercase letters and digits."""
        # Expected: All characters in result are valid
        # Result: Call rand_str and check character set
        result = rand_str()
        valid_chars = set(string.ascii_uppercase + string.digits)
        self.assertTrue(all(c in valid_chars for c in result))
