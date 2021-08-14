"""AssKeyValueSection definition."""
from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.errors import CorruptAssLineError
from ass_parser.observable_mapping_mixin import ObservableMappingMixin


class AssKeyValueSection(ObservableMappingMixin[str, str], AssBaseSection):
    """ASS key-value section."""

    def consume_ass_body_lines(self, lines: list[tuple[int, str]]) -> None:
        """Populate self from .ass lines representing this section, excluding
        the header.

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
