"""ObservableObjectMixin definition."""
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from ass_parser.observable import Event, Observable

TItem = TypeVar("TItem")


@dataclass
class ObservableObjectChangeEvent(Event):
    """Observable object property change event."""


class ObservableObjectMixin:
    """An object that lets consumers to subscribe to its property change
    events.
    """

    changed = Observable[ObservableObjectChangeEvent]()

    def __setattr__(self, prop: str, new_value: Any) -> None:
        """Set attribute.

        Called whenever the user changes any of the class attributes.
        Changes to properties starting with _ won't be tracked.
        Changes to other properties will trigger self._after_change callback.

        :param prop: property name
        :param new_value: new value
        """
        if prop.startswith("_"):
            super().__setattr__(prop, new_value)
        else:
            try:
                old_value = getattr(self, prop)
            except AttributeError:
                super().__setattr__(prop, new_value)
            else:
                if new_value != old_value:
                    self._setattr_impl(prop, new_value)

    def _setattr_normal(self, prop: str, new_value: Any) -> None:
        """Regular implementation of attribute setter.

        Calls _before_change and _after_change immediately.

        :param prop: property name
        :param new_value: new value
        """
        self._before_change()
        super().__setattr__(prop, new_value)
        self._after_change()

    def _setattr_throttled(self, prop: str, new_value: Any) -> None:
        """Throttled implementation of attribute setter.

        Doesn't call _after_change until after the user calls the .end_update()
        method. Calls before_change if it wasn't called before.

        :param prop: property name
        :param new_value: new value
        """
        if not self._dirty:
            self._before_change()
        super().__setattr__(prop, new_value)
        self._dirty = True

    def begin_update(self) -> None:
        """Start throttling calls to ._after_change() method.

        Useful for batch object updates - rather than having .before_change()
        and .after_change() methods called after every change to the instance
        properties, they're getting called only once, on .begin_update() and
        .end_update(), and only if there was a change to the class properties.
        """
        setattr(self, "_setattr_impl", self._setattr_throttled)

    def end_update(self) -> None:
        """Stop throttling calls to ._after_change() method.

        If the object was modified in the meantime, calls ._after_change()
        method only once.
        """
        if self._dirty:
            self._after_change()
        setattr(self, "_setattr_impl", self._setattr_normal)
        self._dirty = False

    def _before_change(self) -> None:
        """Called before class properties have changed."""

    def _after_change(self) -> None:
        """Called after class properties have changed."""
        self.changed.emit(ObservableObjectChangeEvent())

    _dirty: bool = False
    _setattr_impl: Callable[
        ["ObservableObjectMixin", str, Any], None
    ] = _setattr_normal
