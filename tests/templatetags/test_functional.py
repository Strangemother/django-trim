"""
Test trim.templatetags.functional module.

Simple tests for dynamic function calling template tag.
"""

import unittest

from trim.templatetags.functional import functional


class FunctionalTagTest(unittest.TestCase):
    """Test functional template tag."""

    def test_calls_function_with_arg(self):
        # Setup & Execute
        result = functional("math.sqrt", 16)

        # Assert
        self.assertEqual(result, 4.0)

    def test_calls_function_with_multiple_args(self):
        # Setup & Execute
        result = functional("max", 3, 7, 2)

        # Assert
        self.assertEqual(result, 7)

    def test_accesses_module_constant(self):
        # Setup & Execute
        result = functional("math.pi")

        # Assert
        self.assertIn("3.14159", str(result))

    def test_returns_empty_for_nonexistent(self):
        # Setup & Execute
        result = functional("nonexistent.function.name")

        # Assert
        self.assertEqual(result, "")

    def test_returns_string_for_noncallable(self):
        # Setup & Execute
        result = functional("math.e")

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn("2.71828", result)

    def test_calls_with_kwargs(self):
        # Setup & Execute
        result = functional("str.replace", "hello world", "world", "Jay")

        # Assert
        self.assertEqual(result, "hello Jay")


if __name__ == "__main__":
    unittest.main()
