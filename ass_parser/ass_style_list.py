"""ASS styles container."""
from typing import Optional

from ass_parser.ass_style import AssStyle
from ass_parser.observable_sequence import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequence,
)


class AssStyleList(ObservableSequence[AssStyle]):
    """ASS styles container."""

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_about_to_be_removed.subscribe(self._on_items_removal)

    def get_by_name(self, name: str) -> Optional[AssStyle]:
        """Retrieve style by its name.

        :param name: name of the style to look for
        :return: style instance if one was found, None otherwise
        """
        for style in self._data:
            if style.name == name:
                return style
        return None

    def _on_items_insertion(self, event: ItemInsertionEvent[AssStyle]) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssStyle belongs to another AssStyleList")
            item.parent = self

    @staticmethod
    def _on_items_removal(event: ItemRemovalEvent[AssStyle]) -> None:
        for item in event.items:
            item.parent = None
