"""AssEventList definition."""
import re

from ass_parser.ass_event import AssEvent
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.ass_sections.const import EVENTS_SECTION_NAME
from ass_parser.observable_sequence_mixin import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequenceMixin,
)
from ass_parser.util import timestamp_to_ms, unescape_ass_tag


class AssEventList(
    ObservableSequenceMixin[AssEvent],
    AssBaseTabularSection[AssEvent],
):
    """ASS events container."""

    def __init__(self, name: str = EVENTS_SECTION_NAME) -> None:
        """Initialize self."""
        super().__init__(name=name)
        self.items_about_to_be_inserted.subscribe(self._before_items_insertion)
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_removed.subscribe(self._on_items_removal)

    @staticmethod
    def _before_items_insertion(event: ItemInsertionEvent[AssEvent]) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssEvent belongs to another AssEventList")

    def _on_items_insertion(self, event: ItemInsertionEvent[AssEvent]) -> None:
        for item in event.items:
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

    def consume_ass_table_row(
        self, item_type: str, item: dict[str, str]
    ) -> None:
        """Populate self from a dict created by parsing an input ASS line.

        :param item_type: the part before the colon
        :param item: the dictified ASS line
        """
        if item_type not in {"Comment", "Dialogue"}:
            raise ValueError(f'unknown event type: "{item_type}"')

        text = item["Text"]
        note = ""
        match = re.search(r"{NOTE:(?P<note>[^}]*)}", text)
        if match:
            text = text[: match.start()] + text[match.end() :]
            note = unescape_ass_tag(match.group("note"))

        # ASS tags have centisecond precision
        start = timestamp_to_ms(item["Start"])
        end = timestamp_to_ms(item["End"])

        # refine times down to millisecond precision using novelty {TIME:…} tag,
        # but only if the times match the regular ASS times. This is so that
        # subtitle times modified outside of bubblesub with editors that do not
        # write the novelty {TIME:…} tag are not overwritten.
        match = re.search(r"{TIME:(?P<start>-?\d+),(?P<end>-?\d+)}", text)
        if match:
            text = text[: match.start()] + text[match.end() :]
            start_ms = int(match.group("start"))
            end_ms = int(match.group("end"))
            if 0 <= start_ms - start < 10:
                start = start_ms
            if 0 <= end_ms - end < 10:
                end = end_ms

        self.append(
            AssEvent(
                layer=int(item["Layer"]),
                start=start,
                end=end,
                style_name=item["Style"],
                actor=item["Name"],
                margin_left=int(item["MarginL"]),
                margin_right=int(item["MarginR"]),
                margin_vertical=int(item["MarginV"]),
                effect=item["Effect"],
                text=text,
                note=note,
                is_comment=item_type == "Comment",
            )
        )
