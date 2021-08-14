"""AssEventList definition."""
import re
from typing import Any, Optional

from ass_parser.ass_event import AssEvent
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.ass_sections.const import EVENTS_SECTION_NAME
from ass_parser.observable_sequence_mixin import (
    ObservableSequenceItemInsertionEvent,
    ObservableSequenceItemRemovalEvent,
    ObservableSequenceMixin,
)
from ass_parser.util import (
    ass_timestamp_to_ms,
    escape_ass_tag,
    ms_to_ass_timestamp,
    unescape_ass_tag,
)


class AssEventList(
    ObservableSequenceMixin[AssEvent],
    AssBaseTabularSection[AssEvent],
):
    """ASS events container."""

    def __init__(
        self,
        name: str = EVENTS_SECTION_NAME,
        data: Optional[list[AssEvent]] = None,
    ) -> None:
        """Initialize self."""
        super().__init__(name=name)
        self.items_about_to_be_inserted.subscribe(self._before_items_insertion)
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_removed.subscribe(self._on_items_removal)
        if data:
            self.extend(data)

    @staticmethod
    def _before_items_insertion(
        event: ObservableSequenceItemInsertionEvent[AssEvent],
    ) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssEvent belongs to another AssEventList")

    def _on_items_insertion(
        self, event: ObservableSequenceItemInsertionEvent[AssEvent]
    ) -> None:
        for item in event.items:
            item._parent = self  # pylint: disable=protected-access
        self._reindex()

    def _on_items_removal(
        self, event: ObservableSequenceItemRemovalEvent[AssEvent]
    ) -> None:
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
        """Populate self from a dict created by parsing an ASS line.

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
        start = ass_timestamp_to_ms(item["Start"])
        end = ass_timestamp_to_ms(item["End"])

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

    def produce_ass_table_row(
        self, own_item: AssEvent
    ) -> tuple[str, dict[str, str]]:
        """Produce a dict representation based on an own item.

        :return: a tuple of the part before the colon and a dictified ASS line
        """
        text = own_item.text

        if own_item.start is not None and own_item.end is not None:
            text = "{TIME:%d,%d}" % (own_item.start, own_item.end) + text

        if own_item.note:
            text += "{NOTE:%s}" % escape_ass_tag(
                own_item.note.replace("\n", "\\N")
            )

        event_type = "Comment" if own_item.is_comment else "Dialogue"
        return event_type, {
            "Layer": str(own_item.layer),
            "Start": ms_to_ass_timestamp(own_item.start),
            "End": ms_to_ass_timestamp(own_item.end),
            "Style": str(own_item.style_name),
            "Name": str(own_item.actor),
            "MarginL": str(own_item.margin_left),
            "MarginR": str(own_item.margin_right),
            "MarginV": str(own_item.margin_vertical),
            "Effect": str(own_item.effect),
            "Text": text,
        }

    def __eq__(self, other: Any) -> bool:
        """Check for equality. Ignores event handlers.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssEventList):
            return False
        return self.name == other.name and tuple(self._data) == tuple(
            other._data
        )
