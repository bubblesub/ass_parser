"""Tests for the AssEvent class."""
from ass_parser.event import AssEvent


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


def test_ass_event_duration() -> None:
    """Test that duration returns expected values."""
    assert AssEvent().duration == 0
    assert AssEvent(start=1, end=5).duration == 4