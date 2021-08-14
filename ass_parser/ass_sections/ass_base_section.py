"""AssBaseSection definition."""
from collections.abc import Iterable
from typing import TypeVar

from ass_parser.ass_sections.const import SECTION_HEADING_RE
from ass_parser.errors import CorruptAssError, CorruptAssLineError

TAssConcreteSection = TypeVar("TAssConcreteSection", bound="AssBaseSection")


class AssBaseSection:
    """Base ASS section.

    ASS is a glorified .ini container. It can be divided into two parts:
    key-value pair-based sections, and tabular sections.

    Each section knows how to serialize and deserialize itself.
    """

    def __init__(self, name: str) -> None:
        """Initialize self.

        :param name: section name
        """
        self.name = name

    @classmethod
    def from_ass_string(
        cls: type[TAssConcreteSection], source: str
    ) -> TAssConcreteSection:
        """Create an instance of self from an ASS text representation.

        :param source: string to parse
        :return: parsed self
        """
        result = cls(name="dummy")
        result.consume_ass_lines(
            [
                (line_num, line)
                for line_num, line in enumerate(source.splitlines(), start=1)
                if not line.startswith(";")
            ]
        )
        return result

    def to_ass_string(self) -> str:
        """Create an ASS text representation of itself.

        :return: ASS representation
        """
        return "\n".join(self.produce_ass_lines()) + "\n"

    def consume_ass_lines(self, lines: list[tuple[int, str]]) -> None:
        """Populate self from ASS text representation of this section,
        including the ASS header line.

        :param lines: list of tuples (line_num, line)
        """
        if not lines:
            raise CorruptAssError("expected a header")

        line_num, line = lines[0]
        match = SECTION_HEADING_RE.match(line)
        if not match:
            raise CorruptAssLineError(line_num, line, "badly formatted header")
        self.name = match.group("section_name")

        self.consume_ass_body_lines(lines[1:])

    def consume_ass_body_lines(self, lines: list[tuple[int, str]]) -> None:
        """Populate self from ASS text representation of this section,
        excluding the ASS header line.

        :param lines: list of tuples (line_num, line)
        """
        raise NotImplementedError("not implemented")  # pragma: no cover

    def produce_ass_lines(self) -> Iterable[str]:
        """Produce ASS text representation of self, including the ASS header
        line.

        :return: a generator of ASS section lines
        """
        yield f"[{self.name}]"
        yield from self.produce_ass_body_lines()

    def produce_ass_body_lines(self) -> Iterable[str]:
        """Produce ASS text representation of self, excluding the ASS header
        line.

        :return: a generator of ASS section body lines
        """
        raise NotImplementedError("not implemented")  # pragma: no cover
