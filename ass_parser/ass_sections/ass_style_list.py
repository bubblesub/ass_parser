"""AssStyleList definition."""
from typing import Optional

from ass_parser.ass_color import AssColor
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.ass_sections.const import STYLES_SECTION_NAME
from ass_parser.ass_style import AssStyle
from ass_parser.observable_sequence_mixin import (
    ItemInsertionEvent,
    ItemRemovalEvent,
    ObservableSequenceMixin,
)


class AssStyleList(
    ObservableSequenceMixin[AssStyle], AssBaseTabularSection[AssStyle]
):
    """ASS styles container."""

    def __init__(self, name: str = STYLES_SECTION_NAME) -> None:
        """Initialize self."""
        super().__init__(name=name)
        self.items_about_to_be_inserted.subscribe(self._before_items_insertion)
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

    @staticmethod
    def _before_items_insertion(event: ItemInsertionEvent[AssStyle]) -> None:
        for item in event.items:
            if item.parent is not None:
                raise TypeError("AssStyle belongs to another AssStyleList")

    def _on_items_insertion(self, event: ItemInsertionEvent[AssStyle]) -> None:
        for item in event.items:
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

    def consume_ass_table_row(
        self, item_type: str, item: dict[str, str]
    ) -> None:
        """Populate self from a dict created by parsing an input .ass line.

        :param item_type: the part before the colon
        :param item: the dictified .ass line
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
