"""ASS events container."""
from ass_parser.ass_event import AssEvent
from ass_parser.observable_sequence_mixin import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequenceMixin,
)


class AssEventList(ObservableSequenceMixin[AssEvent]):
    """ASS events container."""

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_removed.subscribe(self._on_items_removal)

    def _on_items_insertion(self, event: ItemInsertionEvent[AssEvent]) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssEvent belongs to another AssEventList")
            item._parent = self  # pylint: disable=protected-access
        self._reindex()

    def _on_items_removal(self, event: ItemRemovalEvent[AssEvent]) -> None:
        for item in event.items:
            item._parent = None  # pylint: disable=protected-access
            item._index = None  # pylint: disable=protected-access
        self._reindex()

    def _reindex(self) -> None:
        for i, item in enumerate(self._data):
            item._index = i  # pylint: disable=protected-access
