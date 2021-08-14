"""AssBaseTabularSection definition."""
from collections.abc import Iterable, MutableSequence
from typing import Generic, TypeVar

from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.errors import CorruptAssError, CorruptAssLineError

TAssTableItem = TypeVar("TAssTableItem")


class AssBaseTabularSection(
    AssBaseSection, Generic[TAssTableItem], MutableSequence[TAssTableItem]
):
    """Base tabular ASS section.

    Items are generic so that there can be detailed specializations for events
    and items.
    """

    def consume_ass_body_lines(self, lines: list[tuple[int, str]]) -> None:
        """Populate self from ASS text representation of this section,
        excluding the ASS header line.

        :param lines: list of tuples (line_num, line)
        """
        if not lines:
            raise CorruptAssError("expected a table header")

        line_num, line = lines[0]
        try:
            item_type, rest = line.split(":", 1)
        except ValueError as exc:
            raise CorruptAssLineError(
                line_num, line, "expected a colon"
            ) from exc
        if item_type != "Format":
            raise CorruptAssLineError(
                line_num,
                line,
                'expected the table header to be named "Format"',
            )
        field_names = [p.strip() for p in rest.strip().split(",")]

        self.clear()

        for line_num, line in lines[1:]:
            try:
                item_type, rest = line.split(": ", 1)
            except (ValueError, IndexError) as exc:
                raise CorruptAssLineError(
                    line_num, line, "expected a colon"
                ) from exc
            field_values = rest.strip().split(",", len(field_names) - 1)
            if len(field_names) != len(field_values):
                raise CorruptAssLineError(
                    line_num, line, f"expected {len(field_names)} values"
                )
            item = dict(zip(field_names, field_values))
            try:
                self.consume_ass_table_row(item_type, item)
            except (ValueError, IndexError) as exc:
                raise CorruptAssLineError(line_num, line, str(exc)) from exc

    def consume_ass_table_row(
        self, item_type: str, item: dict[str, str]
    ) -> None:
        """Populate self from a dict created by parsing an ASS line.

        :param item_type: the part before the colon
        :param item: the dictified ASS line
        """
        raise NotImplementedError("not implemented")  # pragma: no cover

    def produce_ass_body_lines(self) -> Iterable[str]:
        """Produce ASS text representation of self, excluding the ASS header
        line.

        :return: a generator of ASS section body lines
        """
        header_output = False
        for own_item in self:
            item_type, item_dict = self.produce_ass_table_row(own_item)
            if not header_output:
                yield "Format: " + ",".join(item_dict.keys())
                header_output = True
            values = list(item_dict.values())
            last_value = values.pop()
            values = [value.replace(",", ";") for value in values]
            values.append(last_value)
            yield f"{item_type}: " + ",".join(values)

    def produce_ass_table_row(
        self, own_item: TAssTableItem
    ) -> tuple[str, dict[str, str]]:
        """Produce a dict representation based on an own item.

        :return: a tuple of the part before the colon and a dictified ASS line
        """
        raise NotImplementedError("not implemented")  # pragma: no cover
