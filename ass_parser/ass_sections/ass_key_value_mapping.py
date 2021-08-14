"""AssKeyValueMapping definition."""
from collections.abc import Iterable
from typing import Any

from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.errors import CorruptAssLineError
from ass_parser.observable_mapping_mixin import ObservableMappingMixin


class AssKeyValueMapping(ObservableMappingMixin[str, str], AssBaseSection):
    """ASS key-value mapping section."""

    def consume_ass_body_lines(self, lines: list[tuple[int, str]]) -> None:
        """Populate self from ASS text representation of this section,
        excluding the ASS header line.

        :param lines: list of tuples (line_num, line)
        """
        self.clear()

        for line_num, line in lines:
            try:
                key, value = line.split(":", 1)
            except ValueError as exc:
                raise CorruptAssLineError(
                    line_num, line, "expected a colon"
                ) from exc
            else:
                self[key] = value.lstrip()

    def produce_ass_body_lines(self) -> Iterable[str]:
        """Produce ASS text representation of self, excluding the ASS header
        line.

        :return: a generator of ASS section body lines
        """
        for key, value in self.items():
            yield f"{key}: {value}"

    def __eq__(self, other: Any) -> bool:
        """Check for equality. Ignores event handlers.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssKeyValueMapping):
            return False
        return self.name == other.name and self._data == other._data
