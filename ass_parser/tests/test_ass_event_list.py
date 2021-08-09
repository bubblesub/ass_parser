"""Tests for the AssEventList class."""
import pytest

from ass_parser.event import AssEvent
from ass_parser.event_list import AssEventList


def test_ass_event_list_append() -> None:
    """Test basic event appending."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert list(events) == [event]


def test_ass_event_list_length() -> None:
    """Test basic event length."""
    events = AssEventList()
    events.append(AssEvent())
    assert len(events) == 1


def test_ass_event_list_basic_delete() -> None:
    """Test basic event deleting."""
    events = AssEventList()
    events.append(AssEvent())
    del events[0]
    assert list(events) == []


def test_ass_event_list_slice_delete() -> None:
    """Test slice-based event deleting."""
    original_events = [AssEvent() for i in range(4)]
    events = AssEventList()
    events.extend(original_events)
    del events[1:3]
    assert list(events) == [original_events[0], original_events[2]]


def test_ass_event_list_basic_update() -> None:
    """Test basic event updating."""
    event1 = AssEvent()
    event2 = AssEvent()
    events = AssEventList()
    events.append(event1)
    events[0] = event2
    assert list(events) == [event2]


def test_ass_event_list_slice_update() -> None:
    """Test slice-based event updating."""
    original_events = [AssEvent() for i in range(4)]
    new_event = AssEvent()
    events = AssEventList()
    events.extend(original_events)
    events[1:3] = [new_event]
    assert list(events) == [original_events[0], new_event, original_events[2]]


def test_ass_event_list_slice_update_not_an_iterable() -> None:
    """Test slice-based event updating raises a TypeError when trying to assign
    a non-iterable.
    """
    original_events = [AssEvent() for i in range(4)]
    new_event = AssEvent()
    events = AssEventList()
    events.extend(original_events)
    with pytest.raises(TypeError):
        events[1:3] = new_event  # type: ignore
