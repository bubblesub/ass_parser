"""ASS file metadata."""
from ass_parser.ass_sections.ass_base_section import AssBaseSection
from ass_parser.observable_mapping_mixin import ObservableMappingMixin


class AssMeta(ObservableMappingMixin[str, str], AssBaseSection):
    """ASS file metadata."""
