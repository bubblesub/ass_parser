"""Tests for the AssFile class."""
from ass_parser import AssFile


def test_ass_file_equality() -> None:
    """Test that ASS files can be easily compared."""
    assert AssFile() != 5
    assert AssFile() == AssFile()

    file1 = AssFile()
    file2 = AssFile()
    file1.script_info["key"] = "value"
    file2.script_info["key"] = "value"
    assert file1 == file2

    file2.script_info["key"] = "changed"
    assert file1 != file2
