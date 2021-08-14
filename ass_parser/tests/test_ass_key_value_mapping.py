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
