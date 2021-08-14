"""Tests for the AssStringTableSection class."""
import pytest

from ass_parser.ass_sections.ass_string_table_section import (
    AssStringTableSection,
)
from ass_parser.errors import CorruptAssError


def test_ass_string_table_section_from_ass_string() -> None:
    """Test AssStringTableSection.from_ass_string function behavior."""
    result = AssStringTableSection.from_ass_string(
        """[Test Section]
;comment
Format: abc,def
;comment 2
Item: value1,value2
Item: value3,value4
"""
    )
    assert result.name == "Test Section"
    assert result[0] == ("Item", {"abc": "value1", "def": "value2"})
    assert result[1] == ("Item", {"abc": "value3", "def": "value4"})


@pytest.mark.parametrize(
    "source,expected_error",
    [
        ("", "corrupt ASS file"),
        ("xxx", "badly formatted header"),
        ("[section]\nno value", "expected a colon"),
        ("[section]", "expected a table header"),
        (
            "[section]\nSomething else: derp",
            'expected the table header to be named "Format"',
        ),
        ("[section]\nFormat:abc,def\nno value", "expected a colon"),
        ("[section]\nFormat:abc,def,ghj\nItem: value", "expected 3 values"),
    ],
)
def test_ass_string_table_section_from_invalid_ass_string(
    source: str, expected_error: str
) -> None:
    """Test AssStringTableSection.from_ass_string function behavior."""
    with pytest.raises(CorruptAssError) as exc:
        AssStringTableSection.from_ass_string(source)
    assert expected_error in str(exc)
