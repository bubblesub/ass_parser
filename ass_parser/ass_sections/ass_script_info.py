"""ASS script info."""
from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.observable_mapping_mixin import ObservableMappingMixin


class AssScriptInfo(ObservableMappingMixin[str, str], AssBaseSection):
    """ASS script info."""
