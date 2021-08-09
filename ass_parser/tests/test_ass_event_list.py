"""Tests for the AssEventList class."""
import pytest

from ass_parser.event import AssEvent
from ass_parser.event_list import AssEventList


def test_ass_event_list_append_sets_parent() -> None:
    """Test that event insertion sets the item parent."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert event.parent == events


def test_ass_event_list_removal_unsets_parent() -> None:
    """Test that event removal unsets the item parent."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert event.parent == events
    del events[events.index(event)]
    assert event.parent is None


def test_ass_event_list_double_parenthood() -> None:
    """Test that event insertion cannot reclaim parenthood from another list."""
    event = AssEvent()
    events1 = AssEventList()
    events2 = AssEventList()
    events1.append(event)
    with pytest.raises(TypeError):
        events2.append(event)
