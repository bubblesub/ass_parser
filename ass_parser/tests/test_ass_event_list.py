"""Tests for the AssEventList class."""
import pickle
from copy import copy, deepcopy
from unittest.mock import Mock

import pytest

from ass_parser.ass_event import AssEvent
from ass_parser.ass_event_list import AssEventList


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


def test_copying_event() -> None:
    """Test that copied events are detached from their original parents."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert copy(event).parent is None
    assert event.parent == events


def test_copying_event_list() -> None:
    """Test that events copied with their parents are still linked to their
    original parent.
    """
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    events_copy = copy(events)
    assert events[0].parent == events
    assert events_copy[0].parent == events


def test_deep_copying_event_list() -> None:
    """Test that events deep-copied with their parents are linked to their
    copied parent.
    """
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    events_copy = deepcopy(events)
    assert events[0].parent == events
    assert events_copy[0].parent == events_copy


def test_ass_event_list_append_reindex() -> None:
    """Test that event insertion populates the event.index property."""
    event1 = AssEvent()
    event2 = AssEvent()
    events = AssEventList()
    events.append(event2)
    events.insert(0, event1)
    assert event1.index == 0
    assert event2.index == 1
    assert event1.number == 1
    assert event2.number == 2


def test_ass_event_list_removal_reindex() -> None:
    """Test that event removal populates the event.index property."""
    event1 = AssEvent()
    event2 = AssEvent()
    event3 = AssEvent()
    events = AssEventList()
    events.extend([event1, event2, event3])
    del events[event2.index]
    assert event1.index == 0
    with pytest.raises(ValueError):
        event2.index  # pylint: disable=pointless-statement
    assert event3.index == 1
    assert event1.number == 1
    with pytest.raises(ValueError):
        event2.number  # pylint: disable=pointless-statement
    assert event3.number == 2


def test_prev_next_ass_event_without_parent() -> None:
    """Test AssEvent.prev and AssEvent.next property without a parent list."""
    event = AssEvent()
    assert event.prev is None
    assert event.next is None


def test_prev_next_ass_event_within_parent() -> None:
    """Test AssEvent.prev and AssEvent.next property within a parent list."""
    event1 = AssEvent()
    event2 = AssEvent()
    event3 = AssEvent()
    events = AssEventList()
    events.extend([event1, event2, event3])
    assert event1.prev is None
    assert event1.next == event2
    assert event2.prev == event1
    assert event2.next == event3
    assert event3.prev == event2
    assert event3.next is None


def test_modifying_event_emits_modification_event_in_parent() -> None:
    """Test that modifying an event emits a modification event in the context
    of its parent list.
    """
    subscriber = Mock()
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    events.items_modified.subscribe(subscriber)
    event.text = "new text"
    subscriber.assert_called_once()


def test_pickling_preserves_event_parenthood() -> None:
    """Test that pickling and unpickling a event list preserves the parenthood
    relationship with its children.
    """
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    new_events = pickle.loads(pickle.dumps(events))
    assert new_events[0].parent == new_events
    assert new_events[0].parent != events
