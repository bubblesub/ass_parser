"""ASS parser main module."""
from ass_parser.ass_color import AssColor
from ass_parser.ass_event import AssEvent
from ass_parser.ass_file import AssFile
from ass_parser.ass_sections import (
    AssBaseSection,
    AssBaseTabularSection,
    AssEventList,
    AssKeyValueSection,
    AssScriptInfo,
    AssStringTableSection,
    AssStyleList,
)
from ass_parser.ass_style import AssStyle
from ass_parser.errors import CorruptAssError, CorruptAssLineError
from ass_parser.reader import read_ass

__all__ = [
    "AssBaseSection",
    "AssBaseTabularSection",
    "AssColor",
    "AssEvent",
    "AssEventList",
    "AssFile",
    "AssKeyValueSection",
    "AssScriptInfo",
    "AssStringTableSection",
    "AssStyle",
    "AssStyleList",
    "CorruptAssError",
    "CorruptAssLineError",
    "read_ass",
]
