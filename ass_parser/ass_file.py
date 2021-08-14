"""AssFile definition."""
from dataclasses import dataclass
from typing import IO, Any

from ass_parser.ass_sections import (
    AssBaseSection,
    AssEventList,
    AssKeyValueMapping,
    AssScriptInfo,
    AssStringTable,
    AssStyleList,
)
from ass_parser.ass_sections.const import (
    EVENTS_SECTION_NAME,
    SCRIPT_INFO_SECTION_NAME,
    SECTION_HEADING_RE,
    STYLES_SECTION_NAME,
)
from ass_parser.errors import CorruptAssLineError


@dataclass
class _SectionInfo:
    name: str
    is_tabular: bool
    lines: list[tuple[int, str]]


def _collect_section_info_list(handle: IO[str]) -> list[_SectionInfo]:
    section_info_list: list[_SectionInfo] = []
    for line_num, line in enumerate(handle, start=1):
        if line.startswith("\N{BOM}"):
            line = line[len("\N{BOM}") :]
        line = line.strip()
        if not line:
            continue
        if line.startswith(";"):
            continue

        if match := SECTION_HEADING_RE.match(line):
            section_info_list.append(
                _SectionInfo(
                    name=match.group("section_name"),
                    is_tabular=False,
                    lines=[],
                )
            )
        elif not section_info_list:
            raise CorruptAssLineError(line_num, line, "expected a section")
        elif line.startswith("Format:"):
            section_info_list[-1].is_tabular = True
        section_info_list[-1].lines.append((line_num, line))
    return section_info_list


class AssFile:
    """ASS file (master container for all ASS stuff)."""

    def __init__(self) -> None:
        """Initialize self."""
        self.script_info = AssScriptInfo()
        self.events = AssEventList()
        self.styles = AssStyleList()
        self.extra_sections: list[AssBaseSection] = []

    def consume_ass_stream(self, handle: IO[str]) -> None:
        """Load ASS from the specified source.

        Clears the existing content.

        :param handle: a readable stream
        """
        self.script_info.clear()
        self.events.clear()
        self.styles.clear()
        self.extra_sections.clear()
        for section_info in _collect_section_info_list(handle):
            section: AssBaseSection
            if section_info.name == STYLES_SECTION_NAME:
                self.styles.consume_ass_lines(section_info.lines)
            elif section_info.name == EVENTS_SECTION_NAME:
                self.events.consume_ass_lines(section_info.lines)
            elif section_info.name == SCRIPT_INFO_SECTION_NAME:
                self.script_info.consume_ass_lines(section_info.lines)
            elif section_info.is_tabular:
                section = AssStringTable(name=section_info.name)
                section.consume_ass_lines(section_info.lines)
                self.extra_sections.append(section)
            else:
                section = AssKeyValueMapping(name=section_info.name)
                section.consume_ass_lines(section_info.lines)
                self.extra_sections.append(section)

    def __eq__(self, other: Any) -> bool:
        """Check for equality.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssFile):
            return False
        return (
            self.script_info == other.script_info
            and self.events == other.events
            and self.styles == other.styles
            and self.extra_sections == other.extra_sections
        )
