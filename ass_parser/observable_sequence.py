"""ObservableSequence definition."""
from collections.abc import Iterable, MutableSequence
from dataclasses import dataclass
from typing import Generic, TypeVar, Union, overload

from ass_parser.observable import Event, Observable

TItem = TypeVar("TItem")


@dataclass
class ItemRemovalEvent(Event, Generic[TItem]):
    """Observable sequence item removal event."""

    index: Union[int, slice]
    items: list[TItem]
    is_committed: bool


@dataclass
class ItemInsertionEvent(Event, Generic[TItem]):
    """Observable sequence item insertion event.

    Broadcast by ObservableSequence after and before an item was inserted to
    it.
    """

    index: Union[int, slice]
    items: list[TItem]
    is_committed: bool


@dataclass
class ItemModificationEvent(Event, Generic[TItem]):
    """Observable sequence item modification event.

    Broadcast by third party classes after an item within an ObservableSequence
    was modified.
    """

    index: Union[int, slice]
    item: TItem


class ObservableSequence(MutableSequence[TItem]):
    """Observable sequence - a sequence that lets consumers to subscribe to
    collection change events.
    """

    items_about_to_be_removed = Observable[ItemRemovalEvent[TItem]]()
    items_about_to_be_inserted = Observable[ItemInsertionEvent[TItem]]()
    items_removed = Observable[ItemRemovalEvent[TItem]]()
    items_inserted = Observable[ItemInsertionEvent[TItem]]()
    items_modified = Observable[ItemModificationEvent[TItem]]()

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self._data: list[TItem] = []

    def __len__(self) -> int:
        return len(self._data)

    @overload
    def __getitem__(self, index: int) -> TItem:
        ...  # pragma: no cover

    @overload
    def __getitem__(self, index: slice) -> list[TItem]:
        ...  # pragma: no cover

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[TItem, list[TItem]]:
        return self._data[index]

    def __delitem__(self, index: Union[int, slice]) -> None:
        values: list[TItem]
        if isinstance(index, slice):
            values = list(self._data[index])
        else:
            values = [self._data[index]]

        self.items_about_to_be_removed.emit(
            ItemRemovalEvent[TItem](
                index=index, items=values, is_committed=False
            )
        )
        del self._data[index]
        self.items_removed.emit(
            ItemRemovalEvent[TItem](
                index=index, items=values, is_committed=True
            )
        )

    @overload
    def __setitem__(self, index: int, value: TItem) -> None:
        ...  # pragma: no cover

    @overload
    def __setitem__(self, index: slice, value: Iterable[TItem]) -> None:
        ...  # pragma: no cover

    def __setitem__(
        self,
        index: Union[int, slice],
        value: Union[TItem, Iterable[TItem]],
    ) -> None:
        old_values: list[TItem]
        if isinstance(index, slice):
            old_values = list(self._data[index])
        else:
            old_values = [self._data[index]]
        if isinstance(value, Iterable):
            new_values = list(value)
        else:
            new_values = [value]

        self.items_about_to_be_removed.emit(
            ItemRemovalEvent[TItem](
                index=index, items=old_values, is_committed=False
            )
        )
        self.items_about_to_be_inserted.emit(
            ItemInsertionEvent[TItem](
                index=index, items=new_values, is_committed=False
            )
        )
        if isinstance(index, int):
            assert not isinstance(value, Iterable)
            self._data[index] = value
        elif isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise TypeError("can only assign an iterable")
            self._data[index] = value

        self.items_removed.emit(
            ItemRemovalEvent[TItem](
                index=index, items=old_values, is_committed=True
            )
        )
        self.items_inserted.emit(
            ItemInsertionEvent[TItem](
                index=index, items=new_values, is_committed=True
            )
        )

    def insert(self, index: int, value: TItem) -> None:
        values = [value]
        self.items_about_to_be_inserted.emit(
            ItemInsertionEvent[TItem](
                index=index, items=values, is_committed=False
            )
        )
        self._data.insert(index, value)
        self.items_inserted.emit(
            ItemInsertionEvent[TItem](
                index=index, items=values, is_committed=True
            )
        )

    def clear(self) -> None:
        values = self._data[:]
        self.items_about_to_be_removed.emit(
            ItemRemovalEvent[TItem](
                index=slice(-1), items=values, is_committed=False
            )
        )
        self._data.clear()
        self.items_removed.emit(
            ItemRemovalEvent[TItem](
                index=slice(-1), items=values, is_committed=True
            )
        )

    def extend(self, values: Iterable[TItem]) -> None:
        values = list(values)
        self.items_about_to_be_inserted.emit(
            ItemInsertionEvent[TItem](
                index=slice(-1), items=values, is_committed=False
            )
        )
        for value in values:
            self._data.append(value)
        self.items_inserted.emit(
            ItemInsertionEvent[TItem](
                index=slice(-1), items=values, is_committed=True
            )
        )
