"""Test writer module."""
import io
import tempfile
from pathlib import Path

from ass_parser import read_ass, write_ass

DUMMY_ASS_FILE_REPARSED = """[Script Info]
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,55,&H00E7F4FF,&H000000FF,&H0025315A,&H00000000,-1,0,0,0,100,100,0,0,1,2.5,0,2,10,10,10,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
Dialogue: 0,0:00:06.21,0:00:07.22,Default,,0,0,0,,{TIME:6210,7220}Ako!{NOTE:アコ}
Dialogue: 0,0:00:08.71,0:00:10.95,Default,,0,0,0,,{TIME:8710,10950}- Shizu!\\N- Ako!

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

[Favorite Meals]
Format: Name,Rating
Cuisine: Pizza,10
Cuisine: Macaroni,8
Cuisine: Veggies,1
"""


def test_write_ass_to_stream(dummy_ass_file: str) -> None:
    """Test read_ass function when the target is a stream."""
    with io.StringIO() as handle:
        ass_file = read_ass(dummy_ass_file)
        write_ass(ass_file, handle)
        result = handle.getvalue()

    assert result == DUMMY_ASS_FILE_REPARSED


def test_write_ass_to_path(dummy_ass_file: str) -> None:
    """Test read_ass function when the target is a path."""
    with tempfile.NamedTemporaryFile() as temp_file:
        path = Path(temp_file.name)
        ass_file = read_ass(dummy_ass_file)
        write_ass(ass_file, path)
        result = path.read_text()

    assert result == DUMMY_ASS_FILE_REPARSED


def test_write_ass_to_string(dummy_ass_file: str) -> None:
    """Test read_ass function when the target is missing."""
    ass_file = read_ass(dummy_ass_file)
    result = write_ass(ass_file)
    assert result == DUMMY_ASS_FILE_REPARSED
