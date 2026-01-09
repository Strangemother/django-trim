"""
Test trim.merge module.

Simple tests for file merging utility.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from trim.merge import split_i, FileExists, recombine


class SplitITest(unittest.TestCase):
    """Test split_i helper function."""

    def test_extracts_part_number(self):
        # Setup & Execute
        result = split_i("filename.part_0")

        # Assert
        self.assertEqual(result, 0)

    def test_extracts_higher_part_number(self):
        # Setup & Execute
        result = split_i("filename.part_42")

        # Assert
        self.assertEqual(result, 42)

    def test_sorts_correctly(self):
        # Setup
        files = ["file.part_2", "file.part_0", "file.part_1"]

        # Execute
        sorted_files = sorted(files, key=split_i)

        # Assert
        self.assertEqual(sorted_files, ["file.part_0", "file.part_1", "file.part_2"])


class FileExistsTest(unittest.TestCase):
    """Test FileExists exception."""

    def test_can_raise_exception(self):
        # Setup & Execute & Assert
        with self.assertRaises(FileExists):
            raise FileExists("/some/path")

    def test_stores_message(self):
        # Setup
        path = "/test/path"

        # Execute
        exc = FileExists(path)

        # Assert
        self.assertEqual(exc.args[0], path)


class RecombineTest(unittest.TestCase):
    """Test recombine function."""

    def test_merges_split_files(self):
        # Setup
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test split files
            (tmppath / "testfile.part_0").write_bytes(b"Hello ")
            (tmppath / "testfile.part_1").write_bytes(b"World")

            # Execute
            output = recombine(tmppath)

            # Assert
            self.assertTrue(output.exists())
            self.assertEqual(output.read_bytes(), b"Hello World")

    def test_raises_if_output_exists(self):
        # Setup
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create split files and output file
            (tmppath / "testfile.part_0").write_bytes(b"data")
            (tmppath / "testfile").write_bytes(b"existing")

            # Execute & Assert
            with self.assertRaises(FileExists):
                recombine(tmppath)


if __name__ == "__main__":
    unittest.main()
