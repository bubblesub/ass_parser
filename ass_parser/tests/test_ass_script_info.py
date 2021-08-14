"""Tests for the AssScriptInfo class."""
from unittest.mock import Mock

from ass_parser import AssScriptInfo


def test_ass_script_info_emits_change_event() -> None:
    """Test that changing script info emits a change event."""
    subscriber = Mock()
    obj = AssScriptInfo()
    obj.changed.subscribe(subscriber)
    obj["key"] = "value"
    subscriber.assert_called_once()
