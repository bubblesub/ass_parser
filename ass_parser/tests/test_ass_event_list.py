"""Tests for the AssEventList class."""
from unittest.mock import Mock

import pytest

from ass_parser.event import AssEvent
from ass_parser.event_list import AssEventList


def test_ass_event_list_append() -> None:
    """Test basic event appending."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert list(events) == [event]


def test_ass_event_list_append_emits_insertion_event() -> None:
    """Test that basic event appending emits an insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    event = AssEvent()
    events = AssEventList()
    events.items_about_to_be_inserted.subscribe(subscriber1)
    events.items_inserted.subscribe(subscriber2)
    events.append(event)
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_ass_event_list_extend_emits_single_insertion_event() -> None:
    """Test that batch event appending emits a single insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    events_to_insert = [AssEvent(), AssEvent()]
    events = AssEventList()
    events.items_about_to_be_inserted.subscribe(subscriber1)
    events.items_inserted.subscribe(subscriber2)
    events.extend(events_to_insert)
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


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


def test_ass_event_list_basic_delete_emits_removal_event() -> None:
    """Test that basic event deleting emits a removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    events = AssEventList()
    events.append(AssEvent())
    events.items_about_to_be_removed.subscribe(subscriber1)
    events.items_removed.subscribe(subscriber2)
    del events[0]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_ass_event_list_clear_emits_signle_removal_event() -> None:
    """Test that clearing events emits a single removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    events = AssEventList()
    events.append(AssEvent())
    events.append(AssEvent())
    events.items_about_to_be_removed.subscribe(subscriber1)
    events.items_removed.subscribe(subscriber2)
    events.clear()
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_ass_event_list_slice_delete() -> None:
    """Test slice-based event deleting."""
    original_events = [AssEvent() for i in range(4)]
    events = AssEventList()
    events.extend(original_events)
    del events[1:3]
    assert list(events) == [original_events[0], original_events[2]]


def test_ass_event_list_slice_delete_emits_removal_event() -> None:
    """Test that slice-based event deleting emits a removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    original_events = [AssEvent() for i in range(4)]
    events = AssEventList()
    events.extend(original_events)
    events.items_about_to_be_removed.subscribe(subscriber1)
    events.items_removed.subscribe(subscriber2)
    del events[1:3]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_ass_event_list_basic_update() -> None:
    """Test basic event updating."""
    event1 = AssEvent()
    event2 = AssEvent()
    events = AssEventList()
    events.append(event1)
    events[0] = event2
    assert list(events) == [event2]


def test_ass_event_list_basic_update_emits_removal_and_insertion_events() -> None:
    """Test that basic event updating emits a removal and an insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    subscriber3 = Mock()
    subscriber4 = Mock()
    event1 = AssEvent()
    event2 = AssEvent()
    events = AssEventList()
    events.append(event1)
    events.items_about_to_be_removed.subscribe(subscriber1)
    events.items_about_to_be_inserted.subscribe(subscriber2)
    events.items_removed.subscribe(subscriber3)
    events.items_inserted.subscribe(subscriber4)
    events[0] = event2
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()
    subscriber3.assert_called_once()
    subscriber4.assert_called_once()


def test_ass_event_list_slice_update() -> None:
    """Test slice-based event updating."""
    original_events = [AssEvent() for i in range(4)]
    new_event = AssEvent()
    events = AssEventList()
    events.extend(original_events)
    events[1:3] = [new_event]
    assert list(events) == [original_events[0], new_event, original_events[2]]


def test_ass_event_list_slice_update_emits_removal_and_insertion_events() -> None:
    """Test that slice-based event updating emits a removal and an insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    subscriber3 = Mock()
    subscriber4 = Mock()
    original_events = [AssEvent() for i in range(4)]
    new_event = AssEvent()
    events = AssEventList()
    events.extend(original_events)
    events.items_about_to_be_removed.subscribe(subscriber1)
    events.items_about_to_be_inserted.subscribe(subscriber2)
    events.items_removed.subscribe(subscriber3)
    events.items_inserted.subscribe(subscriber4)
    events[1:3] = [new_event]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()
    subscriber3.assert_called_once()
    subscriber4.assert_called_once()


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
