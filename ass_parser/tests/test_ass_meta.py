"""Tests for the AssMeta class."""
from unittest.mock import Mock

from ass_parser.meta import AssMeta


def test_ass_meta_get_set() -> None:
    """Test that basic attribute getters and setters work."""
    meta = AssMeta()
    meta["key"] = "value"
    assert meta["key"] == "value"


def test_ass_meta_get_set_emits_change_event() -> None:
    """Test that basic attribute getters and setters emits a change event."""
    subscriber = Mock()
    meta = AssMeta()
    meta.changed.subscribe(subscriber)
    meta["key"] = "value"
    assert meta["key"] == "value"
    subscriber.assert_called_once()


def test_ass_meta_len() -> None:
    """Test that length returns contents size."""
    meta = AssMeta()
    meta["key"] = "value"
    assert len(meta) == 1


def test_ass_meta_iter() -> None:
    """Test iterating over contents."""
    meta = AssMeta()
    meta["key"] = "value"
    assert list(meta) == ["key"]


def test_ass_meta_delete() -> None:
    """Test that attribute removal works."""
    meta = AssMeta()
    meta["key"] = "value"
    del meta["key"]
    assert "key" not in meta


def test_ass_meta_delete_change_event() -> None:
    """Test that attribute removal emits a change event."""
    subscriber = Mock()
    meta = AssMeta()
    meta["key"] = "value"
    meta.changed.subscribe(subscriber)
    del meta["key"]
    subscriber.assert_called_once()


def test_ass_meta_clear() -> None:
    """Test that AssMeta.clear() method clears the contents."""
    meta = AssMeta()
    meta["key"] = "value"
    meta.clear()
    assert "key" not in meta


def test_ass_meta_clear_emits_change_event() -> None:
    """Test that AssMeta.clear() method emits a change event."""
    subscriber = Mock()
    meta = AssMeta()
    meta["key"] = "value"
    meta.changed.subscribe(subscriber)
    meta.clear()
    subscriber.assert_called_once()


def test_ass_meta_clear_emits_change_event_once() -> None:
    """Test that AssMeta.clear() method emits a change event once even if there
    are many items to remove.
    """
    subscriber = Mock()
    meta = AssMeta()
    meta["test1"] = "value1"
    meta["key2"] = "value2"
    meta.changed.subscribe(subscriber)
    meta.clear()
    subscriber.assert_called_once()


def test_ass_meta_update() -> None:
    """Test that AssMeta.update() method updates the contents when passed a dict."""
    meta = AssMeta()
    meta.update({"key1": "value1", "key2": "value2"})
    assert meta["key1"] == "value1"
    assert meta["key2"] == "value2"


def test_ass_meta_update_by_kwargs() -> None:
    """Test that AssMeta.update() method updates the contents when passed kwargs."""
    meta = AssMeta()
    meta.update(key1="value1", key2="value2")
    assert meta["key1"] == "value1"
    assert meta["key2"] == "value2"


def test_ass_meta_update_by_tuples() -> None:
    """Test that AssMeta.update() method updates the contents when passed a list of tuples."""
    meta = AssMeta()
    meta.update([("key1", "value1"), ("key2", "value2")])
    assert meta["key1"] == "value1"
    assert meta["key2"] == "value2"


def test_ass_meta_update_emits_change_event() -> None:
    """Test that AssMeta.update() method emits a change event."""
    subscriber = Mock()
    meta = AssMeta()
    meta.changed.subscribe(subscriber)
    meta.update({"key1": "value1"})
    subscriber.assert_called_once()


def test_ass_meta_update_emits_change_event_once() -> None:
    """Test that AssMeta.update() method emits a change event once even if there
    are many items to set.
    """
    subscriber = Mock()
    meta = AssMeta()
    meta.changed.subscribe(subscriber)
    meta.update({"key1": "value1", "key2": "value2"})
    subscriber.assert_called_once()
