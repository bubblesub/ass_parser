"""AssStyleList definition."""
from typing import Any, Optional

from ass_parser.ass_color import AssColor
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.ass_sections.const import STYLES_SECTION_NAME
from ass_parser.ass_style import AssStyle
from ass_parser.observable_sequence_mixin import (
    ObservableSequenceItemInsertionEvent,
    ObservableSequenceItemRemovalEvent,
    ObservableSequenceMixin,
)
from ass_parser.util import smart_float


class AssStyleList(
    ObservableSequenceMixin[AssStyle], AssBaseTabularSection[AssStyle]
):
    """ASS styles container."""

    def __init__(
        self,
        data: Optional[list[AssStyle]] = None,
        name: str = STYLES_SECTION_NAME,
    ) -> None:
        """Initialize self."""
        super().__init__(name=name)
        self.items_about_to_be_inserted.subscribe(self._before_items_insertion)
        self.items_inserted.subscribe(self._on_items_insertion)
        self.items_removed.subscribe(self._on_items_removal)
        if data:
            self.extend(data)

    def get_by_name(self, name: str) -> Optional[AssStyle]:
        """Retrieve style by its name.

        :param name: name of the style to look for
        :return: style instance if one was found, None otherwise
        """
        for style in self._data:
            if style.name == name:
                return style
        return None

    @staticmethod
    def _before_items_insertion(
        event: ObservableSequenceItemInsertionEvent[AssStyle],
    ) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssStyle belongs to another AssStyleList")

    def _on_items_insertion(
        self, event: ObservableSequenceItemInsertionEvent[AssStyle]
    ) -> None:
        for item in event.items:
            item._parent = self  # pylint: disable=protected-access
        self._reindex()

    def _on_items_removal(
        self, event: ObservableSequenceItemRemovalEvent[AssStyle]
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
        if item_type != "Style":
            raise ValueError(f'unknown style type: "{item_type}"')

        self.append(
            AssStyle(
                name=item["Name"],
                font_name=item["Fontname"],
                font_size=int(float(item["Fontsize"])),
                primary_color=AssColor.from_ass_string(item["PrimaryColour"]),
                secondary_color=AssColor.from_ass_string(
                    item["SecondaryColour"]
                ),
                outline_color=AssColor.from_ass_string(item["OutlineColour"]),
                back_color=AssColor.from_ass_string(item["BackColour"]),
                bold=item["Bold"] == "-1",
                italic=item["Italic"] == "-1",
                underline=item["Underline"] == "-1",
                strike_out=item["StrikeOut"] == "-1",
                scale_x=float(item["ScaleX"]),
                scale_y=float(item["ScaleY"]),
                spacing=float(item["Spacing"]),
                angle=float(item["Angle"]),
                border_style=int(item["BorderStyle"]),
                outline=float(item["Outline"]),
                shadow=float(item["Shadow"]),
                alignment=int(item["Alignment"]),
                margin_left=int(float(item["MarginL"])),
                margin_right=int(float(item["MarginR"])),
                margin_vertical=int(float(item["MarginV"])),
                encoding=int(item["Encoding"]),
            )
        )

    def produce_ass_table_row(
        self, own_item: AssStyle
    ) -> tuple[str, dict[str, str]]:
        """Produce a dict representation based on an own item.

        :return: a tuple of the part before the colon and a dictified ASS line
        """
        return "Style", {
            "Name": own_item.name,
            "Fontname": own_item.font_name,
            "Fontsize": str(own_item.font_size),
            "PrimaryColour": own_item.primary_color.to_ass_string(),
            "SecondaryColour": own_item.secondary_color.to_ass_string(),
            "OutlineColour": own_item.outline_color.to_ass_string(),
            "BackColour": own_item.back_color.to_ass_string(),
            "Bold": "-1" if own_item.bold else "0",
            "Italic": "-1" if own_item.italic else "0",
            "Underline": "-1" if own_item.underline else "0",
            "StrikeOut": "-1" if own_item.strike_out else "0",
            "ScaleX": smart_float(own_item.scale_x),
            "ScaleY": smart_float(own_item.scale_y),
            "Spacing": smart_float(own_item.spacing),
            "Angle": smart_float(own_item.angle),
            "BorderStyle": str(own_item.border_style),
            "Outline": smart_float(own_item.outline),
            "Shadow": smart_float(own_item.shadow),
            "Alignment": str(own_item.alignment),
            "MarginL": str(own_item.margin_left),
            "MarginR": str(own_item.margin_right),
            "MarginV": str(own_item.margin_vertical),
            "Encoding": str(own_item.encoding),
        }

    def __eq__(self, other: Any) -> bool:
        """Check for equality. Ignores event handlers.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssStyleList):
            return False
        return self.name == other.name and tuple(self._data) == tuple(
            other._data
        )
