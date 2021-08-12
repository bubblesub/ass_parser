"""Tests for the AssMeta class."""
from unittest.mock import Mock

from ass_parser.ass_meta import AssMeta


def test_ass_meta_emits_change_event() -> None:
    """Test that changing meta emits a change event."""
    subscriber = Mock()
    obj = AssMeta()
    obj.changed.subscribe(subscriber)
    obj["key"] = "value"
    subscriber.assert_called_once()
