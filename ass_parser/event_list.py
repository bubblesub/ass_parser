"""ASS events container."""
from collections.abc import MutableSequence
from typing import Iterable, Union, overload

from ass_parser.event import AssEvent


class AssEventList(MutableSequence[AssEvent]):
    """ASS events container."""

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self._data: list[AssEvent] = []

    def __delitem__(self, index: Union[int, slice]) -> None:
        del self._data[index]

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

    def __len__(self) -> int:
        return len(self._data)

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
        if isinstance(index, int):
            assert isinstance(value, AssEvent)
            self._data[index] = value
        elif isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise TypeError("can only assign an iterable")
            self._data[index] = value

    def insert(self, index: int, value: AssEvent) -> None:
        self._data.insert(index, value)
