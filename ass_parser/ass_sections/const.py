"""Various ASS sections constants."""
import re

SECTION_HEADING_RE = re.compile(r"^\[(?P<section_name>[^\]]+)\]$")
STYLES_SECTION_NAME = "V4+ Styles"
EVENTS_SECTION_NAME = "Events"
SCRIPT_INFO_SECTION_NAME = "Script Info"
