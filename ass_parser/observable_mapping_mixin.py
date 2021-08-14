"""ObservableMappingMixin definition."""
from collections.abc import Iterable, Iterator, Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any, TypeVar, Union, cast, overload

from ass_parser.observable import Event, Observable

TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


@dataclass
class ObservableMappingChangeEvent(Event):
    """Observable mapping item change event."""


class ObservableMappingMixin(MutableMapping[TKey, TValue]):
    """Observable mapping - a mapping that lets consumers to subscribe to
    collection change events.
    """

    changed = Observable[ObservableMappingChangeEvent]()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize self."""
        super().__init__(*args, **kwargs)  # type: ignore
        self._data: dict[TKey, TValue] = {}

    def __getitem__(self, key: TKey) -> TValue:
        """Get value under given key.

        :param key: key to get the value for
        :return: returns a value for the given key if it exists
        :raises: KeyError if there is no such key
        """
        return self._data[key]

    def __setitem__(self, key: TKey, value: TValue) -> None:
        """Set value under given key.

        :param key: key to set the value for
        :param value: the new value
        """
        if self._data.get(key) != value:
            self._data[key] = value
            self.changed.emit(ObservableMappingChangeEvent())

    def __delitem__(self, key: TKey) -> None:
        """Remove the specified key.

        :param key: key to remove
        """
        if key in self._data:
            del self._data[key]
            self.changed.emit(ObservableMappingChangeEvent())

    def __len__(self) -> int:
        """Return length of the contents.

        :return: length of the contents
        """
        return len(self._data)

    def __iter__(self) -> Iterator[TKey]:
        """Return contents as key-value tuples.

        :return: list of key-value tuples
        """
        return iter(self._data)

    def clear(self) -> None:
        """Clear conents."""
        self._data.clear()
        self.changed.emit(ObservableMappingChangeEvent())

    @overload
    def update(
        self, other: Mapping[TKey, TValue], /, **kwargs: TValue
    ) -> None:
        ...  # pragma: no cover

    @overload
    def update(
        self, other: Iterable[tuple[TKey, TValue]] = (), /, **kwargs: TValue
    ) -> None:
        ...  # pragma: no cover

    def update(
        self,
        other: Union[
            Mapping[TKey, TValue], Iterable[tuple[TKey, TValue]]
        ] = (),
        /,
        **kwargs: TValue,
    ) -> None:
        """Update self with new content.

        :param new_content: content to update with
        """
        if isinstance(other, Mapping):
            for key in other:
                self._data[key] = other[key]
        else:
            for key, value in other:
                self._data[key] = value
        for key, value in kwargs.items():
            self._data[cast(TKey, key)] = value
        self.changed.emit(ObservableMappingChangeEvent())
