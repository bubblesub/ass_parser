"""ObservableSequenceMixin definition."""
from collections.abc import Iterable, MutableSequence
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, Union, overload

from ass_parser.observable import Event, Observable

TItem = TypeVar("TItem")


@dataclass
class ObservableSequenceItemRemovalEvent(Event, Generic[TItem]):
    """Observable sequence item removal event.

    Broadcast by ObservableSequenceMixin after and before an item was removed
    from it.
    """

    index: Union[int, slice]
    items: list[TItem]
    is_committed: bool


@dataclass
class ObservableSequenceItemInsertionEvent(Event, Generic[TItem]):
    """Observable sequence item insertion event.

    Broadcast by ObservableSequenceMixin after and before an item was inserted
    to it.
    """

    index: Union[int, slice]
    items: list[TItem]
    is_committed: bool


@dataclass
class ObservableSequenceItemModificationEvent(Event, Generic[TItem]):
    """Observable sequence item modification event.

    Broadcast by third party classes after an item within an
    ObservableSequenceMixin was modified.
    """

    index: Union[int, slice]
    item: TItem


@dataclass
class ObservableSequenceChangeEvent(Event):
    """Generic observable sequence change event."""


class ObservableSequenceMixin(MutableSequence[TItem]):
    """Observable sequence - a sequence that lets consumers to subscribe to
    collection change events.
    """

    items_about_to_be_removed = Observable[
        ObservableSequenceItemRemovalEvent[TItem]
    ]()
    items_about_to_be_inserted = Observable[
        ObservableSequenceItemInsertionEvent[TItem]
    ]()
    items_removed = Observable[ObservableSequenceItemRemovalEvent[TItem]]()
    items_inserted = Observable[ObservableSequenceItemInsertionEvent[TItem]]()
    items_modified = Observable[
        ObservableSequenceItemModificationEvent[TItem]
    ]()
    changed = Observable[ObservableSequenceChangeEvent]()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize self."""
        super().__init__(*args, **kwargs)  # type: ignore
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
            ObservableSequenceItemRemovalEvent[TItem](
                index=index, items=values, is_committed=False
            )
        )
        del self._data[index]
        self.items_removed.emit(
            ObservableSequenceItemRemovalEvent[TItem](
                index=index, items=values, is_committed=True
            )
        )
        self.changed.emit(ObservableSequenceChangeEvent())

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
            ObservableSequenceItemRemovalEvent[TItem](
                index=index, items=old_values, is_committed=False
            )
        )
        self.items_about_to_be_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
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
            ObservableSequenceItemRemovalEvent[TItem](
                index=index, items=old_values, is_committed=True
            )
        )
        self.items_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
                index=index, items=new_values, is_committed=True
            )
        )
        self.changed.emit(ObservableSequenceChangeEvent())

    def insert(self, index: int, value: TItem) -> None:
        values = [value]
        self.items_about_to_be_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
                index=index, items=values, is_committed=False
            )
        )
        self._data.insert(index, value)
        self.items_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
                index=index, items=values, is_committed=True
            )
        )
        self.changed.emit(ObservableSequenceChangeEvent())

    def clear(self) -> None:
        values = self._data[:]
        self.items_about_to_be_removed.emit(
            ObservableSequenceItemRemovalEvent[TItem](
                index=slice(-1), items=values, is_committed=False
            )
        )
        self._data.clear()
        self.items_removed.emit(
            ObservableSequenceItemRemovalEvent[TItem](
                index=slice(-1), items=values, is_committed=True
            )
        )
        self.changed.emit(ObservableSequenceChangeEvent())

    def extend(self, values: Iterable[TItem]) -> None:
        values = list(values)
        self.items_about_to_be_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
                index=slice(-1), items=values, is_committed=False
            )
        )
        for value in values:
            self._data.append(value)
        self.items_inserted.emit(
            ObservableSequenceItemInsertionEvent[TItem](
                index=slice(-1), items=values, is_committed=True
            )
        )
        self.changed.emit(ObservableSequenceChangeEvent())
