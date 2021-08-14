"""Tests for the ObservableSequenceMixin class."""
from unittest.mock import Mock

import pytest

from ass_parser.observable_sequence_mixin import ObservableSequenceMixin


class DummySequence(ObservableSequenceMixin[int]):
    """Test ObservableSequenceMixin implementation."""


def test_append() -> None:
    """Test basic item appending."""
    item = 123
    seq = DummySequence()
    seq.append(item)
    assert list(seq) == [item]


def test_append_emits_insertion_event() -> None:
    """Test that basic item appending emits an insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    item = 123
    seq = DummySequence()
    seq.items_about_to_be_inserted.subscribe(subscriber1)
    seq.items_inserted.subscribe(subscriber2)
    seq.append(item)
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_extend_emits_single_insertion_event() -> None:
    """Test that batch item appending emits a single insertion event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    events_to_insert = [123, 234]
    seq = DummySequence()
    seq.items_about_to_be_inserted.subscribe(subscriber1)
    seq.items_inserted.subscribe(subscriber2)
    seq.extend(events_to_insert)
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_length() -> None:
    """Test basic sequence length."""
    seq = DummySequence()
    seq.append(123)
    assert len(seq) == 1


def test_basic_delete() -> None:
    """Test basic item deleting."""
    seq = DummySequence()
    seq.append(123)
    del seq[0]
    assert list(seq) == []


def test_basic_delete_emits_removal_event() -> None:
    """Test that basic item deleting emits a removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    seq = DummySequence()
    seq.append(123)
    seq.items_about_to_be_removed.subscribe(subscriber1)
    seq.items_removed.subscribe(subscriber2)
    del seq[0]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_clear_emits_signle_removal_event() -> None:
    """Test that clearing items emits a single removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    seq = DummySequence()
    seq.append(123)
    seq.append(234)
    seq.items_about_to_be_removed.subscribe(subscriber1)
    seq.items_removed.subscribe(subscriber2)
    seq.clear()
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_slice_delete() -> None:
    """Test slice-based event deleting."""
    original_items = list(range(4))
    seq = DummySequence()
    seq.extend(original_items)
    del seq[1:3]
    assert list(seq) == [original_items[0], original_items[3]]


def test_slice_delete_emits_removal_event() -> None:
    """Test that slice-based event deleting emits a removal event."""
    subscriber1 = Mock()
    subscriber2 = Mock()
    original_items = list(range(4))
    seq = DummySequence()
    seq.extend(original_items)
    seq.items_about_to_be_removed.subscribe(subscriber1)
    seq.items_removed.subscribe(subscriber2)
    del seq[1:3]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()


def test_basic_update() -> None:
    """Test basic event updating."""
    event1 = 123
    event2 = 234
    seq = DummySequence()
    seq.append(event1)
    seq[0] = event2
    assert list(seq) == [event2]


def test_basic_update_emits_removal_and_insertion_events() -> None:
    """Test that basic event updating emits a removal and an insertion
    event.
    """
    subscriber1 = Mock()
    subscriber2 = Mock()
    subscriber3 = Mock()
    subscriber4 = Mock()
    event1 = 123
    event2 = 234
    seq = DummySequence()
    seq.append(event1)
    seq.items_about_to_be_removed.subscribe(subscriber1)
    seq.items_about_to_be_inserted.subscribe(subscriber2)
    seq.items_removed.subscribe(subscriber3)
    seq.items_inserted.subscribe(subscriber4)
    seq[0] = event2
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()
    subscriber3.assert_called_once()
    subscriber4.assert_called_once()


def test_slice_update() -> None:
    """Test slice-based event updating."""
    original_items = list(range(4))
    new_item = 123
    seq = DummySequence()
    seq.extend(original_items)
    seq[1:3] = [new_item]
    assert list(seq) == [
        original_items[0],
        new_item,
        original_items[3],
    ]


def test_slice_update_emits_removal_and_insertion_events() -> None:
    """Test that slice-based event updating emits a removal and an
    insertion event.
    """
    subscriber1 = Mock()
    subscriber2 = Mock()
    subscriber3 = Mock()
    subscriber4 = Mock()
    original_items = list(range(4))
    new_item = 123
    seq = DummySequence()
    seq.extend(original_items)
    seq.items_about_to_be_removed.subscribe(subscriber1)
    seq.items_about_to_be_inserted.subscribe(subscriber2)
    seq.items_removed.subscribe(subscriber3)
    seq.items_inserted.subscribe(subscriber4)
    seq[1:3] = [new_item]
    subscriber1.assert_called_once()
    subscriber2.assert_called_once()
    subscriber3.assert_called_once()
    subscriber4.assert_called_once()


def test_slice_update_not_an_iterable() -> None:
    """Test slice-based event updating raises a TypeError when trying to
    assign a non-iterable.
    """
    original_items = list(range(4))
    new_item = 123
    seq = DummySequence()
    seq.extend(original_items)
    with pytest.raises(TypeError):
        seq[1:3] = new_item  # type: ignore
