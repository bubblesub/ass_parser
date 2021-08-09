"""ASS events container."""
from collections.abc import MutableSequence
from dataclasses import dataclass
from typing import Iterable, Union, overload

from ass_parser.event import AssEvent
from ass_parser.observable import Event, Observable


@dataclass
class AssEventListRemovalEvent(Event):
    """ASS event list event removal event."""

    events: list[AssEvent]
    is_committed: bool


@dataclass
class AssEventListInsertionEvent(Event):
    """ASS event list event insertion event."""

    events: list[AssEvent]
    is_committed: bool


class AssEventList(MutableSequence[AssEvent]):
    """ASS events container."""

    items_about_to_be_removed = Observable()
    items_removed = Observable()

    items_about_to_be_inserted = Observable()
    items_inserted = Observable()

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self._data: list[AssEvent] = []

    def __len__(self) -> int:
        return len(self._data)

    @overload
    def __getitem__(self, index: int) -> AssEvent:
        ...  # pragma: no cover

    @overload
    def __getitem__(self, index: slice) -> list[AssEvent]:
        ...  # pragma: no cover

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[AssEvent, list[AssEvent]]:
        return self._data[index]

    def __delitem__(self, index: Union[int, slice]) -> None:
        values: list[AssEvent]
        if isinstance(index, slice):
            values = list(self._data[index])
        else:
            values = [self._data[index]]

        self.items_about_to_be_removed.emit(
            AssEventListRemovalEvent(events=values, is_committed=False)
        )
        del self._data[index]
        self.items_removed.emit(
            AssEventListRemovalEvent(events=values, is_committed=True)
        )

    @overload
    def __setitem__(self, index: int, value: AssEvent) -> None:
        ...  # pragma: no cover

    @overload
    def __setitem__(self, index: slice, value: Iterable[AssEvent]) -> None:
        ...  # pragma: no cover

    def __setitem__(
        self,
        index: Union[int, slice],
        value: Union[AssEvent, Iterable[AssEvent]],
    ) -> None:
        old_values: list[AssEvent]
        if isinstance(index, slice):
            old_values = list(self._data[index])
        else:
            old_values = [self._data[index]]
        if isinstance(value, Iterable):
            new_values = list(value)
        else:
            new_values = [value]

        self.items_about_to_be_removed.emit(
            AssEventListRemovalEvent(events=old_values, is_committed=False)
        )
        self.items_about_to_be_inserted.emit(
            AssEventListRemovalEvent(events=new_values, is_committed=False)
        )
        if isinstance(index, int):
            assert isinstance(value, AssEvent)
            self._data[index] = value
        elif isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise TypeError("can only assign an iterable")
            self._data[index] = value

        self.items_removed.emit(
            AssEventListRemovalEvent(events=old_values, is_committed=True)
        )
        self.items_inserted.emit(
            AssEventListRemovalEvent(events=new_values, is_committed=True)
        )

    def insert(self, index: int, value: AssEvent) -> None:
        values = [value]
        self.items_about_to_be_inserted.emit(
            AssEventListInsertionEvent(events=values, is_committed=False)
        )
        self._data.insert(index, value)
        self.items_inserted.emit(
            AssEventListInsertionEvent(events=values, is_committed=False)
        )

    def clear(self) -> None:
        values = self._data[:]
        self.items_about_to_be_removed.emit(
            AssEventListRemovalEvent(events=values, is_committed=False)
        )
        self._data.clear()
        self.items_removed.emit(
            AssEventListRemovalEvent(events=values, is_committed=True)
        )

    def extend(self, values: Iterable[AssEvent]) -> None:
        values = list(values)
        self.items_about_to_be_inserted.emit(
            AssEventListInsertionEvent(events=values, is_committed=False)
        )
        for value in values:
            self._data.append(value)
        self.items_inserted.emit(
            AssEventListInsertionEvent(events=values, is_committed=False)
        )
