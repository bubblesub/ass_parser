"""Tests for the Observable class."""
import pickle
from copy import deepcopy
from unittest.mock import Mock

from ass_parser.observable import Event, Observable


class DummyEvent(Event):
    """Dummy object change event."""


class DummyObject:
    """Dummy object."""

    changed = Observable[DummyEvent]()

    def __init__(self, prop: int) -> None:
        self._prop = prop

    @property
    def prop(self) -> int:
        """Return test property.

        :return: test property
        """
        return self._prop

    @prop.setter
    def prop(self, value: int) -> None:
        """Set test property.

        :param value: value to set
        """
        self._prop = value
        self.changed.emit(DummyEvent())


def test_observable_emiting() -> None:
    """Test that emitting an Observable triggers its subscribers."""
    subscriber = Mock()
    obj = DummyObject(5)
    obj.changed.subscribe(subscriber)
    obj.prop = 6
    subscriber.assert_called_once()
    assert obj.prop == 6


def test_copying_observable_ignores_subscribers() -> None:
    """Test that copying an object that has Observables does not attempt to
    copy the event subscribers.
    """
    subscriber = Mock()
    obj = DummyObject(5)
    obj.changed.subscribe(subscriber)
    clone = deepcopy(obj)
    clone.prop = 6
    assert obj.prop == 5
    assert clone.prop == 6
    subscriber.assert_not_called()


def test_pickling_observable_ignores_subscribers() -> None:
    """Test that pickling and unpickling an object that has Observables
    does not attempt to serialize the event subscribers.
    """
    subscriber = Mock()
    obj = DummyObject(5)
    obj.changed.subscribe(subscriber)
    clone = pickle.loads(pickle.dumps(obj))
    clone.prop = 6
    assert obj.prop == 5
    assert clone.prop == 6
    subscriber.assert_not_called()


def test_unpickled_observable_still_works() -> None:
    """Test that unpickling an object that has Observables does not break them."""
    subscriber = Mock()
    clone_subscriber = Mock()
    obj = DummyObject(5)
    obj.changed.subscribe(subscriber)
    clone = pickle.loads(pickle.dumps(obj))
    clone.changed.subscribe(clone_subscriber)
    clone.prop = 6
    assert obj.prop == 5
    assert clone.prop == 6
    subscriber.assert_not_called()
    clone_subscriber.assert_called_once()
