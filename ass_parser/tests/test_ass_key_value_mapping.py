"""Tests for the AssKeyValueMapping class."""
from unittest.mock import Mock

import pytest

from ass_parser import AssKeyValueMapping, CorruptAssError


def test_ass_key_value_mapping_emits_change_event() -> None:
    """Test that changing a section emits a change event."""
    subscriber = Mock()
    obj = AssKeyValueMapping(name="test section")
    obj.changed.subscribe(subscriber)
    obj["key"] = "value"
    subscriber.assert_called_once()


def test_ass_key_value_mapping_from_ass_string() -> None:
    """Test AssKeyValueMapping.from_ass_string function behavior."""
    result = AssKeyValueMapping.from_ass_string(
        """[Test Section]
;comment
Key 1: Value 1
;comment 2
Key 2: Value 2
"""
    )
    assert result.name == "Test Section"
    assert result["Key 1"] == "Value 1"
    assert result["Key 2"] == "Value 2"


@pytest.mark.parametrize(
    "source,expected_error",
    [
        ("", "corrupt ASS file"),
        ("xxx", "badly formatted header"),
        ("[section]\nno value", "expected a colon"),
    ],
)
def test_ass_key_value_mapping_from_invalid_ass_string(
    source: str, expected_error: str
) -> None:
    """Test AssKeyValueMapping.from_ass_string function behavior."""
    with pytest.raises(CorruptAssError) as exc:
        AssKeyValueMapping.from_ass_string(source)
    assert expected_error in str(exc)


def test_ass_key_value_mapping_to_ass_string() -> None:
    """Test AssKeyValueMapping.to_ass_string function behavior."""
    section = AssKeyValueMapping(name="Test Section")
    section["Key 1"] = "Value 1"
    section["Key 2"] = "Value 2"

    assert (
        section.to_ass_string()
        == """[Test Section]
Key 1: Value 1
Key 2: Value 2
"""
    )


def test_ass_key_value_mapping_equality() -> None:
    """Test that key value mappings can be easily compared."""
    assert AssKeyValueMapping(name="test") != 5
    assert AssKeyValueMapping(name="test") == AssKeyValueMapping(name="test")
    assert AssKeyValueMapping(name="test") != AssKeyValueMapping(
        name="changed"
    )

    mapping1 = AssKeyValueMapping(name="test")
    mapping2 = AssKeyValueMapping(name="test")
    mapping1["key"] = "value"
    mapping2["key"] = "value"
    assert mapping1 == mapping2

    mapping2["key"] = "changed"
    assert mapping1 != mapping2
