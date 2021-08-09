"""Observable containers and objects."""
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class Event:
    """An event that can be emitted."""

    source: Optional["Observable"] = field(
        init=False, repr=False, default=None
    )


Callback = Callable[[Event], None]


class Observable:
    """An observable that can be used to subscribe to events."""

    def __init__(self) -> None:
        """Initialize self."""
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
        event.source = self
        for callback in self.callbacks:
            callback(event)
