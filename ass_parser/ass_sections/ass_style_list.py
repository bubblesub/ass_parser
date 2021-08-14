"""ASS styles container."""
from typing import Optional

from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.ass_style import AssStyle
from ass_parser.observable_sequence_mixin import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequenceMixin,
)


class AssStyleList(ObservableSequenceMixin[AssStyle], AssBaseSection):
    """ASS styles container."""

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_removed.subscribe(self._on_items_removal)

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
            item._parent = self  # pylint: disable=protected-access
        self._reindex()

    def _on_items_removal(self, event: ItemRemovalEvent[AssStyle]) -> None:
        for item in event.items:
            item._parent = None  # pylint: disable=protected-access
            item._index = None  # pylint: disable=protected-access
        self._reindex()

    def _reindex(self) -> None:
        for i, item in enumerate(self._data):
            item._index = i  # pylint: disable=protected-access
