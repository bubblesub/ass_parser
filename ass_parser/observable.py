"""Observable containers and objects."""
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Optional, Type, TypeVar, cast

TEvent = TypeVar("TEvent", bound="Event")


@dataclass
class Event:
    """An event that can be emitted."""

    source: Any = field(init=False, repr=False, default=None)


Callback = Callable[[TEvent], None]


class BoundObservable(Generic[TEvent]):
    """An observable that can be used to subscribe to events."""

    __slots__ = ["parent", "callbacks"]

    def __init__(self, parent: "Observable[TEvent]") -> None:
        """Initialize self.

        :parent: parent Observable
        """
        self.parent = parent
        self.callbacks: list[Callback[TEvent]] = []

    def subscribe(self, callback: Callback[TEvent]) -> None:
        """Subscribe to events.

        :param callback: user function to call.
            That function must take a single argument, the event.
        """
        self.callbacks.append(callback)

    def emit(self, event: TEvent) -> None:
        """Emit an event to the subscribed functions.

        :param event: event to broadcast.
        """
        event.source = self.parent
        for callback in self.callbacks:
            callback(event)

    def __getstate__(self) -> Any:
        """Return pickle compatible object representation.

        The pickled copy does not have subscribers.

        :return: object representation
        """
        return self.parent

    def __setstate__(self, state: Any) -> None:
        """Load class state from pickle compatible object representation.

        :param state: object representation
        """
        self.parent = state
        self.callbacks = []


class Observable(Generic[TEvent]):
    """A binding mechanism to associate BoundObservable to class instances.

    This class is meant to be used as a classvar.
    """

    __slots__ = ["public_name", "private_name"]

    def __init__(self) -> None:
        """Initialize self."""
        self.public_name = ""
        self.private_name = ""

    def __set_name__(self, owner: Type[object], name: str) -> None:
        """Remember bound property names."""
        self.public_name = name
        self.private_name = "_" + name

    def __get__(
        self, obj: object, objtype: Optional[Type[object]] = None
    ) -> BoundObservable[TEvent]:
        """Get a BoundObservable associated with this Observable.

        If there is no such BoundObservable yet, create and bind it to the
        owner class.
        """
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, BoundObservable[TEvent](self))
        return cast(BoundObservable[TEvent], getattr(obj, self.private_name))
