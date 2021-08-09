"""Observable containers and objects."""
from dataclasses import dataclass, field
from typing import Callable, Optional, Type, cast


@dataclass
class Event:
    """An event that can be emitted."""

    source: Optional["Observable"] = field(
        init=False, repr=False, default=None
    )


Callback = Callable[[Event], None]


class BoundObservable:
    """An observable that can be used to subscribe to events."""

    __slots__ = ["parent", "callbacks"]

    def __init__(self, parent: "Observable") -> None:
        """Initialize self."""
        self.parent = parent
        self.callbacks: list[Callback] = []

    def subscribe(self, callback: Callback) -> None:
        """Subscribe to events.

        :param callback: user function to call.
            That function must take a single argument, the event.
        """
        self.callbacks.append(callback)

    def emit(self, event: Event) -> None:
        """Emit an event to the subscribed functions.

        :param event: event to broadcast.
        """
        event.source = self.parent
        for callback in self.callbacks:
            callback(event)


class Observable:
    """A binding mechanism to associate BoundObservable to instances."""

    __slots__ = ["public_name", "private_name"]

    def __init__(self) -> None:
        self.public_name = ""
        self.private_name = ""

    def __set_name__(self, owner: Type[object], name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(
        self, obj: object, objtype: Optional[Type[object]] = None
    ) -> BoundObservable:
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, BoundObservable(self))
        return cast(BoundObservable, getattr(obj, self.private_name))
