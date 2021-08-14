"""ASS parser main module."""
from ass_parser.ass_color import AssColor
from ass_parser.ass_event import AssEvent
from ass_parser.ass_sections import (
    AssEventList,
    AssScriptInfo,
    AssStringTableSection,
    AssStyleList,
)
from ass_parser.ass_style import AssStyle

__all__ = [
    "AssColor",
    "AssEvent",
    "AssEventList",
    "AssScriptInfo",
    "AssStringTableSection",
    "AssStyle",
    "AssStyleList",
]
