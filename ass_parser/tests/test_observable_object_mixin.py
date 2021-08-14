"""Tests for the ObservableObjectMixin class."""
from dataclasses import dataclass
from typing import Type
from unittest.mock import Mock

import pytest

from ass_parser.observable_object_mixin import ObservableObjectMixin


class DummyObject(ObservableObjectMixin):
    """Test ObservableObjectMixin implementation."""

    def __init__(self, name: str, count: int) -> None:
        super().__init__()
        self.name = name
        self.count = count


@dataclass
class DummyDataclassObject(ObservableObjectMixin):
    """Test ObservableObjectMixin implementation using @dataclass idiom."""

    name: str
    count: int


@pytest.mark.parametrize("cls", [DummyObject, DummyDataclassObject])
def test_property_change_emits_change_event(cls: Type[DummyObject]) -> None:
    """Test that basic property changing emits a change event."""
    subscriber = Mock()
    obj = cls(count=1, name="test")
    obj.changed.subscribe(subscriber)
    obj.count = 5
    subscriber.assert_called_once()


@pytest.mark.parametrize("cls", [DummyObject, DummyDataclassObject])
def test_throttling_property_updates(cls: Type[DummyObject]) -> None:
    """Test begin_update() and end_update() behavior."""
    subscriber = Mock()
    obj = cls(count=1, name="test")
    obj.changed.subscribe(subscriber)
    obj.begin_update()
    obj.count = 5
    subscriber.assert_not_called()
    obj.end_update()
    subscriber.assert_called_once()
