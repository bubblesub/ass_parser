"""Fixtures."""
from pathlib import Path

import pytest

DUMMY_ASS_FILE = """\N{BOM}[Script Info]
; Script generated by Aegisub 3.2.2
; http://www.aegisub.org/
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[Aegisub Project Garbage]
Last Style Storage: Default
Audio File: [ReinForce] Saki -  Achiga-hen ~Episode of Side-A~ Kuro's Birthday (BDRip 1920x1080 x264 FLAC).mkv
Video File: [ReinForce] Saki -  Achiga-hen ~Episode of Side-A~ Kuro's Birthday (BDRip 1920x1080 x264 FLAC).mkv
Video AR Mode: 4
Video AR Value: 1.777778
Video Zoom Percent: 0.375000
Scroll Position: 33
Active Line: 47
Video Position: 7132

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,55,&H00E7F4FF,&H000000FF,&H0025315A,&H00000000,-1,0,0,0,100,100,0,0,1,2.5,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:06.21,0:00:07.22,Default,,0,0,0,,Ako!{NOTE:アコ}
Dialogue: 0,0:00:08.71,0:00:10.95,Default,,0,0,0,,- Shizu!\\N- Ako!

[Favorite Meals]
Format: Name,Rating
Cuisine: Pizza,10
Cuisine: Macaroni,8
Cuisine: Veggies,1
"""


@pytest.fixture(name="dummy_ass_file")
def fixture_dummy_ass_file() -> str:
    """A fixture that returns dummy ASS file text representation.

    :return: a dummy ASS file"""
    return DUMMY_ASS_FILE


@pytest.fixture(name="project_dir")
def fixture_project_dir() -> Path:
    """Return path to the Python project directory.

    :return: a path
    """
    return Path(__file__).parent.parent


@pytest.fixture(name="repo_dir")
def fixture_repo_dir(project_dir: Path) -> Path:
    """Return path to the parent git repository directory.

    :return: a path
    """
    return project_dir.parent
