"""AssStringTableSection definition."""
from ass_parser.ass_sections.ass_base_tabular_section import (
    AssBaseTabularSection,
)
from ass_parser.observable_sequence_mixin import ObservableSequenceMixin

AssStringTableSectionItem = tuple[str, dict[str, str]]


class AssStringTableSection(
    ObservableSequenceMixin[AssStringTableSectionItem],
    AssBaseTabularSection[AssStringTableSectionItem],
):
    """Simple tabular string ASS section."""

    def consume_ass_table_row(
        self, item_type: str, item: dict[str, str]
    ) -> None:
        """Populate self from a dict created by parsing an input ASS line.

        :param item_type: the part before the colon
        :param item: the dictified ASS line
        """
        self.append((item_type, item))
