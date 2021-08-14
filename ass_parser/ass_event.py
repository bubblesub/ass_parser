"""AssEvent definition."""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ass_parser.observable_object_mixin import ObservableObjectMixin
from ass_parser.observable_sequence_mixin import (
    ObservableSequenceChangeEvent,
    ObservableSequenceItemModificationEvent,
)

if TYPE_CHECKING:
    from ass_parser.ass_sections import AssEventList  # pragma: no coverage


@dataclass
class AssEvent(ObservableObjectMixin):
    """ASS event (subtitle, comment etc.)."""

    start: int = 0
    end: int = 0
    style_name: str = ""
    actor: str = ""
    text: str = ""
    note: str = ""
    effect: str = ""
    layer: int = 0
    margin_left: int = 0
    margin_right: int = 0
    margin_vertical: int = 0
    is_comment: bool = False

    _parent: Optional["AssEventList"] = None
    _index: Optional[int] = None
    _note = ""
    _text = ""

    def get_text(self) -> str:
        """Return event text.

        :return: text
        """
        return self._text

    def set_text(self, value: str) -> None:
        """Set new event text.

        Normalizes \\n newline characters to \\\\N ASS hard line breaks.

        :param value: new text
        """
        self._text = value.replace("\n", "\\N")

    def get_note(self) -> str:
        """Return event note.

        :return: note
        """
        return self._note

    def set_note(self, value: str) -> None:
        """Set new event note.

        Normalizes \\n newline characters to \\\\N ASS hard line breaks.

        :param value: new note
        """
        self._note = value.replace("\n", "\\N")

    @property
    def parent(self) -> Optional["AssEventList"]:
        """Return parent list.

        :return: parent list
        """
        return self._parent

    @property
    def index(self) -> int:
        """Return event index within its parent list.

        If the event does not have a parent list, raises a ValueError.

        :return: index
        """
        if self._index is None:
            raise ValueError("AssEvent does not belong to any AssEventList")
        return self._index

    @property
    def number(self) -> int:
        """Return event index within its parent list, starting at 1.

        If event does not have a parent list, raises a ValueError.

        :return: index
        """
        return self.index + 1

    @property
    def prev(self) -> Optional["AssEvent"]:
        """Return previous event from its parent list.

        :return: previous event if has parent list, None otherwise
        """
        if not self.parent:
            return None
        if self.index == 0:
            return None
        return self.parent[self.index - 1]

    @property
    def next(self) -> Optional["AssEvent"]:
        """Return next event from its parent list.

        :return: next subtitle if has parent list, None otherwise
        """
        if not self.parent:
            return None
        if self.index == len(self.parent) - 1:
            return None
        return self.parent[self.index + 1]

    @property
    def duration(self) -> int:
        """Return subtitle duration in milliseconds.

        :return: duration
        """
        return self.end - self.start

    def _after_change(self) -> None:
        """Emit item modified event in the parent list."""
        super()._after_change()
        if self.parent is not None:
            self.parent.items_modified.emit(
                ObservableSequenceItemModificationEvent(
                    index=self.index, item=self
                )
            )
            self.parent.changed.emit(ObservableSequenceChangeEvent())

    def __copy__(self) -> "AssEvent":
        """Duplicate self.

        The copy is detached from the parent list.

        :return: duplicate of self
        """
        ret = type(self)()
        ret.__dict__.update(
            {
                key: value
                for key, value in self.__dict__.items()
                if not callable(value) and key != "_parent"
            }
        )
        return ret

    def __eq__(self, other: Any) -> bool:
        """Check for equality. Ignores parent list and event handlers.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssEvent):
            return False
        return all(
            key.startswith("_")
            or key == "parent"
            or getattr(self, key) == getattr(other, key)
            for key in self.__dataclass_fields__  # type: ignore
        )


AssEvent.text = property(AssEvent.get_text, AssEvent.set_text)  # type: ignore
AssEvent.note = property(AssEvent.get_note, AssEvent.set_note)  # type: ignore
