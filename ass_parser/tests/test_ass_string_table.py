"""Tests for the AssStringTable class."""
import pytest

from ass_parser import AssStringTable, CorruptAssError


def test_ass_string_table_from_ass_string() -> None:
    """Test AssStringTable.from_ass_string function behavior."""
    result = AssStringTable.from_ass_string(
        """[Test Section]
;comment
Format: abc,def
;comment 2
Item: value1,value2
Item: value3,value4,trailing
"""
    )
    assert result.name == "Test Section"
    assert result[0] == ("Item", {"abc": "value1", "def": "value2"})
    assert result[1] == ("Item", {"abc": "value3", "def": "value4,trailing"})


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
def test_ass_string_table_from_invalid_ass_string(
    source: str, expected_error: str
) -> None:
    """Test AssStringTable.from_ass_string function behavior."""
    with pytest.raises(CorruptAssError) as exc:
        AssStringTable.from_ass_string(source)
    assert expected_error in str(exc)


def test_ass_key_value_mapping_to_ass_string() -> None:
    """Test AssKeyValueMapping.to_ass_string function behavior."""
    section = AssStringTable(name="Test Section")
    section.append(("Item", {"abc": "value1", "def": "value2"}))
    section.append(("Item", {"abc": "value3", "def": "value4"}))

    assert (
        section.to_ass_string()
        == """[Test Section]
Format: abc,def
Item: value1,value2
Item: value3,value4
"""
    )


def test_ass_key_value_mapping_to_ass_string_comma_fix() -> None:
    """Test that AssKeyValueMapping.to_ass_string replaces commas with semicolons."""
    section = AssStringTable(name="Test Section")
    section.append(("Item", {"abc": "term1,term2", "def": "term3,term4"}))

    assert (
        section.to_ass_string()
        == """[Test Section]
Format: abc,def
Item: term1;term2,term3,term4
"""
    )


def test_ass_key_value_mapping_to_ass_string_empty() -> None:
    """Test that AssKeyValueMapping.to_ass_string raises a TypeError when
    empty.
    """
    section = AssStringTable(name="Test Section")
    assert section.to_ass_string() == "[Test Section]\n"
