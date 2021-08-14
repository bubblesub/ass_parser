"""Test reader module."""
import io
import tempfile
from pathlib import Path

import pytest

from ass_parser import AssFile, AssStringTable, CorruptAssLineError, read_ass


def verify_result(result: AssFile) -> None:
    """Verifies that the result of parsing DUMMY_ASS_FILE is correct."""
    assert len(result.script_info) == 7
    assert result.script_info["Title"] == "Default Aegisub file"
    assert len(result.styles) == 1
    assert len(result.events) == 2
    assert len(result.extra_sections) == 2
    assert result.extra_sections[0].name == "Aegisub Project Garbage"
    assert result.extra_sections[1].name == "Favorite Meals"
    assert isinstance(result.extra_sections[1], AssStringTable)
    assert list(result.extra_sections[1]) == [
        ("Cuisine", {"Name": "Pizza", "Rating": "10"}),
        ("Cuisine", {"Name": "Macaroni", "Rating": "8"}),
        ("Cuisine", {"Name": "Veggies", "Rating": "1"}),
    ]


def test_read_ass_from_string(dummy_ass_file: str) -> None:
    """Test read_ass function when the source is a string."""
    result = read_ass(dummy_ass_file)
    verify_result(result)


def test_read_ass_from_stream(dummy_ass_file: str) -> None:
    """Test read_ass function when the source is a stream."""
    with io.StringIO(dummy_ass_file) as handle:
        result = read_ass(handle)
    verify_result(result)


def test_read_ass_from_path(dummy_ass_file: str) -> None:
    """Test read_ass function when the source is a filesystem path."""
    with tempfile.NamedTemporaryFile() as temp_file:
        path = Path(temp_file.name)
        path.write_text(dummy_ass_file)
        result = read_ass(path)
    verify_result(result)


def test_read_ass_corrupt_ass() -> None:
    """Test read_ass function raises an error when there are no sections."""
    with pytest.raises(CorruptAssLineError):
        read_ass("no sections")
