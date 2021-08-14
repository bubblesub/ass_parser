"""ASS parser main module."""
from ass_parser.ass_color import AssColor
from ass_parser.ass_event import AssEvent
from ass_parser.ass_file import AssFile
from ass_parser.ass_sections import (
    AssBaseSection,
    AssBaseTabularSection,
    AssEventList,
    AssKeyValueMapping,
    AssScriptInfo,
    AssStringTable,
    AssStyleList,
)
from ass_parser.ass_style import AssStyle
from ass_parser.errors import CorruptAssError, CorruptAssLineError
from ass_parser.observable_mapping_mixin import ObservableMappingChangeEvent
from ass_parser.observable_object_mixin import ObservableObjectChangeEvent
from ass_parser.observable_sequence_mixin import (
    ObservableSequenceItemInsertionEvent,
    ObservableSequenceItemModificationEvent,
    ObservableSequenceItemRemovalEvent,
)
from ass_parser.reader import read_ass
from ass_parser.writer import write_ass

__all__ = [
    "AssBaseSection",
    "AssBaseTabularSection",
    "AssColor",
    "AssEvent",
    "AssEventList",
    "AssFile",
    "AssKeyValueMapping",
    "AssScriptInfo",
    "AssStringTable",
    "AssStyle",
    "AssStyleList",
    "CorruptAssError",
    "CorruptAssLineError",
    "ObservableMappingChangeEvent",
    "ObservableObjectChangeEvent",
    "ObservableSequenceItemInsertionEvent",
    "ObservableSequenceItemModificationEvent",
    "ObservableSequenceItemRemovalEvent",
    "read_ass",
    "write_ass",
]
