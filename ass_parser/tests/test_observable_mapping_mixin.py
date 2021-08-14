"""Tests for the ObservableMappingMixin class."""
from unittest.mock import Mock

from ass_parser.observable_mapping_mixin import ObservableMappingMixin


class DummyMapping(ObservableMappingMixin[str, str]):
    """Test ObservableMappingMixin implementation."""


def test_get_set() -> None:
    """Test that basic attribute getters and setters work."""
    mapping = DummyMapping()
    mapping["key"] = "value"
    assert mapping["key"] == "value"


def test_get_set_emits_change_event() -> None:
    """Test that basic attribute getters and setters emits a change event."""
    subscriber = Mock()
    mapping = DummyMapping()
    mapping.changed.subscribe(subscriber)
    mapping["key"] = "value"
    assert mapping["key"] == "value"
    subscriber.assert_called_once()


def test_len() -> None:
    """Test that length returns contents size."""
    mapping = DummyMapping()
    mapping["key"] = "value"
    assert len(mapping) == 1


def test_iter() -> None:
    """Test iterating over contents."""
    mapping = DummyMapping()
    mapping["key"] = "value"
    assert list(mapping) == ["key"]


def test_delete() -> None:
    """Test that attribute removal works."""
    mapping = DummyMapping()
    mapping["key"] = "value"
    del mapping["key"]
    assert "key" not in mapping


def test_delete_change_event() -> None:
    """Test that attribute removal emits a change event."""
    subscriber = Mock()
    mapping = DummyMapping()
    mapping["key"] = "value"
    mapping.changed.subscribe(subscriber)
    del mapping["key"]
    subscriber.assert_called_once()


def test_clear() -> None:
    """Test that DummyMapping.clear() method clears the contents."""
    mapping = DummyMapping()
    mapping["key"] = "value"
    mapping.clear()
    assert "key" not in mapping


def test_clear_emits_change_event() -> None:
    """Test that DummyMapping.clear() method emits a change event."""
    subscriber = Mock()
    mapping = DummyMapping()
    mapping["key"] = "value"
    mapping.changed.subscribe(subscriber)
    mapping.clear()
    subscriber.assert_called_once()


def test_clear_emits_change_event_once() -> None:
    """Test that DummyMapping.clear() method emits a change event once even if
    there are many items to remove.
    """
    subscriber = Mock()
    mapping = DummyMapping()
    mapping["test1"] = "value1"
    mapping["key2"] = "value2"
    mapping.changed.subscribe(subscriber)
    mapping.clear()
    subscriber.assert_called_once()


def test_update() -> None:
    """Test that DummyMapping.update() method updates the contents when passed
    a dict.
    """
    mapping = DummyMapping()
    mapping.update({"key1": "value1", "key2": "value2"})
    assert mapping["key1"] == "value1"
    assert mapping["key2"] == "value2"


def test_update_by_kwargs() -> None:
    """Test that DummyMapping.update() method updates the contents when passed
    kwargs.
    """
    mapping = DummyMapping()
    mapping.update(key1="value1", key2="value2")
    assert mapping["key1"] == "value1"
    assert mapping["key2"] == "value2"


def test_update_by_tuples() -> None:
    """Test that DummyMapping.update() method updates the contents when passed
    a list of tuples.
    """
    mapping = DummyMapping()
    mapping.update([("key1", "value1"), ("key2", "value2")])
    assert mapping["key1"] == "value1"
    assert mapping["key2"] == "value2"


def test_update_emits_change_event() -> None:
    """Test that DummyMapping.update() method emits a change event."""
    subscriber = Mock()
    mapping = DummyMapping()
    mapping.changed.subscribe(subscriber)
    mapping.update({"key1": "value1"})
    subscriber.assert_called_once()


def test_update_emits_change_event_once() -> None:
    """Test that DummyMapping.update() method emits a change event once even if
    there are many items to set.
    """
    subscriber = Mock()
    mapping = DummyMapping()
    mapping.changed.subscribe(subscriber)
    mapping.update({"key1": "value1", "key2": "value2"})
    subscriber.assert_called_once()
