"""Tests for the AssEvent class."""
from unittest.mock import Mock

from ass_parser import AssEvent


def test_ass_event_default_text() -> None:
    """Test that an ASS event has empty text by default."""
    assert AssEvent().text == ""


def test_ass_event_default_note() -> None:
    """Test that an ASS event has empty note by default."""
    assert AssEvent().note == ""


def test_ass_event_text_replaces_newlines() -> None:
    """Test that setting text replaces \n into \\N."""
    assert AssEvent(text="line 1\nline 2").text == "line 1\\Nline 2"
    event = AssEvent()
    event.text = "line 1\nline 2"
    assert event.text == "line 1\\Nline 2"


def test_ass_event_note_replaces_newlines() -> None:
    """Test that setting note replaces \n into \\N."""
    assert AssEvent(note="line 1\nline 2").note == "line 1\\Nline 2"
    event = AssEvent()
    event.note = "line 1\nline 2"
    assert event.note == "line 1\\Nline 2"


def test_ass_event_text_emits_change_event() -> None:
    """Test that setting text emits a change event."""
    subscriber = Mock()
    event = AssEvent()
    event.changed.subscribe(subscriber)
    subscriber.assert_not_called()
    event.text = "line 1\nline 2"
    subscriber.assert_called_once()


def test_ass_event_note_emits_change_event() -> None:
    """Test that setting note emits a change event."""
    subscriber = Mock()
    event = AssEvent()
    event.changed.subscribe(subscriber)
    subscriber.assert_not_called()
    event.note = "line 1\nline 2"
    subscriber.assert_called_once()


def test_ass_event_duration() -> None:
    """Test that duration returns expected values."""
    assert AssEvent().duration == 0
    assert AssEvent(start=1, end=5).duration == 4


def test_ass_event_equality() -> None:
    """Test that events can be easily compared."""
    assert AssEvent() != 5
    assert AssEvent() == AssEvent()
    assert AssEvent(text="test") == AssEvent(text="test")
    assert AssEvent(note="test") == AssEvent(note="test")
    assert AssEvent(text="test") != AssEvent(text="changed")
    assert AssEvent(note="test") != AssEvent(note="changed")
    assert AssEvent(actor="test") != AssEvent(actor="changed")
    assert AssEvent(actor="test") != AssEvent(actor="changed")

    subscriber = Mock()
    event1 = AssEvent()
    event2 = AssEvent()
    event1.changed.subscribe(subscriber)
    assert event1 == event2
    event1.text = "changed"
    assert event1 != event2
