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

