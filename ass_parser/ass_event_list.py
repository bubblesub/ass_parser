"""ASS events container."""
from ass_parser.ass_event import AssEvent
from ass_parser.observable_sequence import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequence,
)


class AssEventList(ObservableSequence[AssEvent]):
    """ASS events container."""

    def __init__(self) -> None:
        """Initialize self."""
        super().__init__()
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_about_to_be_removed.subscribe(self._on_items_removal)

    def _on_items_insertion(self, event: ItemInsertionEvent[AssEvent]) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssEvent belongs to another AssEventList")
            item.parent = self

    @staticmethod
    def _on_items_removal(event: ItemRemovalEvent[AssEvent]) -> None:
        for item in event.items:
            item.parent = None
