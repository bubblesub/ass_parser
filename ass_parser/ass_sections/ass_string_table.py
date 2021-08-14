"""AssStringTable definition."""
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.observable_sequence_mixin import ObservableSequenceMixin

AssStringTableItem = tuple[str, dict[str, str]]


class AssStringTable(
    ObservableSequenceMixin[AssStringTableItem],
    AssBaseTabularSection[AssStringTableItem],
):
    """Simple tabular string ASS section."""

    def consume_ass_table_row(
        self, item_type: str, item: dict[str, str]
    ) -> None:
        """Populate self from a dict created by parsing an ASS line.

        :param item_type: the part before the colon
        :param item: the dictified ASS line
        """
        self.append((item_type, item))

    def produce_ass_table_row(
        self, own_item: AssStringTableItem
    ) -> tuple[str, dict[str, str]]:
        """Produce a dict representation based on an own item.

        :return: a tuple of the part before the colon and a dictified ASS line
        """
        return own_item[0], own_item[1]
