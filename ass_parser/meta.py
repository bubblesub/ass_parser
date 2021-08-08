"""ASS file metadata."""
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Iterable, Iterator, Mapping, Union, overload

from ass_parser.observable import Event, Observable


@dataclass
class AssMetaChangeEvent(Event):
    """ASS file metadata change event."""


class AssMeta(MutableMapping[str, str]):
    """ASS file metadata."""

    changed = Observable()

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self._data: dict[str, str] = {}

    def __getitem__(self, key: str) -> str:
        """Get value under given key.

        :param key: key to get the value for
        :return: returns a value for the given key if it exists
        :raises: KeyError if there is no such key
        """
        return self._data[key]

    def __setitem__(self, key: str, value: str) -> None:
        """Set value under given key.

        :param key: key to set the value for
        :param value: the new value
        """
        if self._data.get(key, None) != value:
            self._data[key] = value
            self.changed.emit(AssMetaChangeEvent())

    def __delitem__(self, key: str) -> None:
        """Remove the specified key.

        :param key: key to remove
        """
        if key in self._data:
            del self._data[key]
            self.changed.emit(AssMetaChangeEvent())

    def __len__(self) -> int:
        """Return length of the contents.

        :return: length of the contents
        """
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        """Return contents as key-value tuples.

        :return: list of key-value tuples
        """
        return iter(self._data)

    def clear(self) -> None:
        """Clear conents."""
        self._data.clear()
        self.changed.emit(AssMetaChangeEvent())

    @overload
    def update(self, other: Mapping[str, str], /, **kwargs: str) -> None:
        ...  # pragma: no cover

    @overload
    def update(
        self, other: Iterable[tuple[str, str]] = (), /, **kwargs: str
    ) -> None:
        ...  # pragma: no cover

    def update(
        self,
        other: Union[Mapping[str, str], Iterable[tuple[str, str]]] = (),
        /,
        **kwargs: str,
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
            self._data[key] = value
        self.changed.emit(AssMetaChangeEvent())
