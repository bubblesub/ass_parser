"""ASS events container."""
from ass_parser.event import AssEvent
from ass_parser.observable import Event
from ass_parser.observable_sequence import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequence,
)


class AssEventList(ObservableSequence[AssEvent]):
    """ASS events container."""

    def __init__(self) -> None:
        super().__init__()
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_about_to_be_removed.subscribe(self._on_items_removal)

    def _on_items_insertion(self, event: Event) -> None:
        assert isinstance(event, ItemInsertionEvent)
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssEvent belongs to another AssEventList")
            item.parent = self

    @staticmethod
    def _on_items_removal(event: Event) -> None:
        assert isinstance(event, ItemRemovalEvent)
        for item in event.items:
            item.parent = None
