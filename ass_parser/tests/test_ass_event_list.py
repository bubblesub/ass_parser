"""Tests for the AssEventList class."""
import pickle
from copy import copy, deepcopy
from unittest.mock import Mock

import pytest

from ass_parser import AssEvent, AssEventList, CorruptAssError


def test_ass_event_list_constructor() -> None:
    """Test that constructor accepts a list of events."""
    event = AssEvent()
    events = AssEventList(data=[event])
    assert len(events) == 1
    assert event.parent == events


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
    assert len(events1) == 1
    assert len(events2) == 0
    assert event.parent == events1


def test_ass_event_list_copying_event() -> None:
    """Test that copied events are detached from their original parents."""
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    assert copy(event).parent is None
    assert event.parent == events


def test_ass_event_list_copying_event_list() -> None:
    """Test that events copied with their parents are still linked to their
    original parent.
    """
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    events_copy = copy(events)
    assert events[0].parent == events
    assert events_copy[0].parent == events


def test_ass_event_list_deep_copying_event_list() -> None:
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


def test_ass_event_list_prev_next_ass_event_without_parent() -> None:
    """Test AssEvent.prev and AssEvent.next property without a parent list."""
    event = AssEvent()
    assert event.prev is None
    assert event.next is None


def test_ass_event_list_prev_next_ass_event_within_parent() -> None:
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


def test_ass_event_list_modifying_event_emits_modification_event_in_parent() -> None:
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


def test_ass_event_list_pickling_preserves_event_parenthood() -> None:
    """Test that pickling and unpickling a event list preserves the parenthood
    relationship with its children.
    """
    event = AssEvent()
    events = AssEventList()
    events.append(event)
    new_events = pickle.loads(pickle.dumps(events))
    assert new_events[0].parent is new_events
    assert new_events[0].parent is not events


def test_ass_event_list_default_section_name() -> None:
    """Test that AssEventList.name defaults to a generic name."""
    assert AssEventList().name == "Events"


def test_ass_event_list_from_ass_string() -> None:
    """Test AssStringTable.from_ass_string function behavior."""
    result = AssEventList.from_ass_string(
        """[Test Section]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:08.71,0:00:10.95,Default,Manami,0,0,0,,Ayako!{NOTE:綾子}
Dialogue: 1,0:00:13.94,0:00:15.61,Default,Ayako,1,2,3,Effect,Good morning...
"""
    )
    assert result.name == "Test Section"
    assert len(result) == 2
    assert result[0].parent == result

    assert result[0].layer == 0
    assert result[0].start == 8710
    assert result[0].end == 10950
    assert result[0].style_name == "Default"
    assert result[0].actor == "Manami"
    assert result[0].margin_left == 0
    assert result[0].margin_right == 0
    assert result[0].margin_vertical == 0
    assert result[0].text == "Ayako!"
    assert result[0].note == "綾子"

    assert result[1].layer == 1
    assert result[1].start == 13940
    assert result[1].end == 15610
    assert result[1].style_name == "Default"
    assert result[1].actor == "Ayako"
    assert result[1].margin_left == 1
    assert result[1].margin_right == 2
    assert result[1].margin_vertical == 3
    assert result[1].effect == "Effect"
    assert result[1].text == "Good morning..."
    assert result[1].note == ""


def test_ass_event_list_from_ass_string_refines_time() -> None:
    """Test that {TIME:} tag refines times up to one centisecond."""
    result = AssEventList.from_ass_string(
        """[Test Section]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Comment: 0,0:00:13.94,0:00:15.61,,,0,0,0,,{TIME:13941,15619}
"""
    )
    assert result[0].start == 13941
    assert result[0].end == 15619


def test_ass_event_list_from_ass_string_does_not_refine_time_if_too_far_away() -> None:
    """Test that {TIME:} tag does not refine times if bigger than one
    centisecond.

    This is because this tag is very custom and if someone edits the file with
    an editor that does not support the TIME tag, the time written by that
    editor should take priority.
    """
    result = AssEventList.from_ass_string(
        """[Test Section]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Comment: 0,0:00:13.94,0:00:15.61,,,0,0,0,,{TIME:13950,15620}
"""
    )
    assert result[0].start == 13940
    assert result[0].end == 15610


def test_ass_event_list_from_ass_string_unknown_event() -> None:
    """Test that unknown events raise an error."""
    with pytest.raises(CorruptAssError):
        AssEventList.from_ass_string(
            """[Test Section]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Unknown: 0,0:00:13.94,0:00:15.61,,,0,0,0,,{TIME:13941,15619}
"""
        )


def test_ass_event_list_extending_with_another_list() -> None:
    """Test extending a list with another list.

    This demonstrates how to extend a list while dealing with the ownership
    shenanigans.
    """
    event = AssEvent()
    events1 = AssEventList()
    events2 = AssEventList()
    events2.append(event)
    assert len(events1) == 0
    assert len(events2) == 1
    events1.extend(map(copy, events2))
    assert len(events1) == 1


def test_ass_event_text_emits_change_event() -> None:
    """Test that setting text emits a change event."""
    subscriber = Mock()
    event = AssEvent()
    events = AssEventList(data=[event])
    events.changed.subscribe(subscriber)
    subscriber.assert_not_called()
    event.text = "line 1\nline 2"
    subscriber.assert_called_once()


def test_ass_event_note_emits_change_event() -> None:
    """Test that setting note emits a change event."""
    subscriber = Mock()
    event = AssEvent()
    events = AssEventList(data=[event])
    events.changed.subscribe(subscriber)
    subscriber.assert_not_called()
    event.note = "line 1\nline 2"
    subscriber.assert_called_once()


def test_ass_event_list_equality() -> None:
    """Test that event lists can be easily compared."""
    assert AssEventList() != 5
    assert AssEventList() == AssEventList()
    assert AssEventList() != AssEventList(name="changed")
    assert AssEventList(data=[AssEvent()]) == AssEventList(data=[AssEvent()])
    assert AssEventList(data=[AssEvent()]) != AssEventList(
        data=[AssEvent(actor="changed")]
    )
