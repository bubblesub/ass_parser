"""ASS parser main module."""
from ass_parser.ass_color import AssColor
from ass_parser.ass_event import AssEvent
from ass_parser.ass_sections import AssEventList, AssScriptInfo, AssStyleList
from ass_parser.ass_style import AssStyle

__all__ = [
    "AssColor",
    "AssEvent",
    "AssEventList",
    "AssScriptInfo",
    "AssStyle",
    "AssStyleList",
]
