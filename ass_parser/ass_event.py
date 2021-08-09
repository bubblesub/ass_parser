"""ASS event (subtitle, comment etc.)."""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ass_parser.observable_object import ObservableObject

if TYPE_CHECKING:
    from ass_parser.ass_event_list import AssEventList  # pragma: no coverage


@dataclass
class AssEvent(ObservableObject):
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

    parent: Optional["AssEventList"] = None

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
    def duration(self) -> int:
        """Return subtitle duration in milliseconds.

        :return: duration
        """
        return self.end - self.start


AssEvent.text = property(AssEvent.get_text, AssEvent.set_text)  # type: ignore
AssEvent.note = property(AssEvent.get_note, AssEvent.set_note)  # type: ignore