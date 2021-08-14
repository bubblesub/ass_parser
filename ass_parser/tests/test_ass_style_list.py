"""Tests for the AssStyleList class."""
# pylint: disable=line-too-long
import pickle
from copy import copy, deepcopy
from unittest.mock import Mock

import pytest

from ass_parser import AssStyle, AssStyleList, CorruptAssError


def test_ass_style_list_constructor() -> None:
    """Test that constructor accepts a list of styles."""
    style = AssStyle(name="dummy style")
    styles = AssStyleList(data=[style])
    assert len(styles) == 1
    assert style.parent == styles


def test_ass_style_list_append_sets_parent() -> None:
    """Test that style insertion sets the item parent."""
    style = AssStyle(name="dummy style")
    styles = AssStyleList()
    styles.append(style)
    assert style.parent == styles


def test_ass_style_list_removal_unsets_parent() -> None:
    """Test that style removal unsets the item parent."""
    style = AssStyle(name="dummy style")
    styles = AssStyleList()
    styles.append(style)
    assert style.parent == styles
    del styles[styles.index(style)]
    assert style.parent is None


def test_ass_style_list_double_parenthood() -> None:
    """Test that style insertion cannot reclaim parenthood from another list."""
    style = AssStyle(name="dummy style")
    styles1 = AssStyleList()
    styles2 = AssStyleList()
    styles1.append(style)
    with pytest.raises(TypeError):
        styles2.append(style)
    assert len(styles1) == 1
    assert len(styles2) == 0
    assert style.parent == styles1


def test_ass_style_list_get_by_name() -> None:
    """Test get_by_name function behavior."""
    style1 = AssStyle(name="dummy style 1")
    style2 = AssStyle(name="dummy style 2")
    styles = AssStyleList()
    styles.extend([style1, style2])
    assert styles.get_by_name("dummy style 1") == style1
    assert styles.get_by_name("dummy style 2") == style2
    assert styles.get_by_name("non-existing style") is None


def test_ass_style_list_copying_style() -> None:
    """Test that copied styles are detached from their original parents."""
    style = AssStyle(name="test style")
    styles = AssStyleList()
    styles.append(style)
    assert copy(style).parent is None
    assert style.parent == styles


def test_ass_style_list_copying_style_list() -> None:
    """Test that styles copied with their parents are still linked to their
    original parent.
    """
    style = AssStyle(name="test style")
    styles = AssStyleList()
    styles.append(style)
    styles_copy = copy(styles)
    assert styles[0].parent == styles
    assert styles_copy[0].parent == styles


def test_ass_style_list_deep_copying_style_list() -> None:
    """Test that styles deep-copied with their parents are linked to their
    copied parent.
    """
    style = AssStyle(name="test style")
    styles = AssStyleList()
    styles.append(style)
    styles_copy = deepcopy(styles)
    assert styles[0].parent == styles
    assert styles_copy[0].parent == styles_copy


def test_ass_style_list_append_reindex() -> None:
    """Test that style insertion populates the style.index property."""
    style1 = AssStyle(name="dummy style 1")
    style2 = AssStyle(name="dummy style 2")
    styles = AssStyleList()
    styles.append(style2)
    styles.insert(0, style1)
    assert style1.index == 0
    assert style2.index == 1


def test_ass_style_list_removal_reindex() -> None:
    """Test that style removal populates the style.index property."""
    style1 = AssStyle(name="dummy style 1")
    style2 = AssStyle(name="dummy style 2")
    style3 = AssStyle(name="dummy style 3")
    styles = AssStyleList()
    styles.extend([style1, style2, style3])
    del styles[style2.index]
    assert style1.index == 0
    with pytest.raises(ValueError):
        style2.index  # pylint: disable=pointless-statement
    assert style3.index == 1


def test_ass_style_list_modifying_style_emits_modification_event_in_parent() -> None:
    """Test that modifying an style emits a modification event in the context
    of its parent list.
    """
    subscriber = Mock()
    style = AssStyle(name="dummy style")
    styles = AssStyleList()
    styles.append(style)
    styles.items_modified.subscribe(subscriber)
    style.scale(3)
    subscriber.assert_called_once()


def test_ass_style_list_pickling_preserves_style_parenthood() -> None:
    """Test that pickling and unpickling a style list preserves the parenthood
    relationship with its children.
    """
    style = AssStyle(name="dummy style")
    styles = AssStyleList()
    styles.append(style)
    new_styles = pickle.loads(pickle.dumps(styles))
    assert new_styles[0].parent is new_styles
    assert new_styles[0].parent is not styles


def test_ass_style_list_from_ass_string() -> None:
    """Test AssStyleList.from_ass_string function behavior."""
    result = AssStyleList.from_ass_string(
        """[Test Section]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Rubik,24,&H0AE9F4F4,&H000000FF,&H00101010,&H7F202020,-1,0,0,0,100,125,0,0,1,2.5,0,2,15,15,15,1
"""
    )
    assert result.name == "Test Section"
    assert len(result) == 1
    assert result[0].parent == result

    assert result[0].name == "Default"
    assert result[0].font_name == "Rubik"
    assert result[0].font_size == 24
    assert result[0].primary_color.red == 0xF4
    assert result[0].primary_color.green == 0xF4
    assert result[0].primary_color.blue == 0xE9
    assert result[0].primary_color.alpha == 0x0A
    assert result[0].secondary_color.red == 0xFF
    assert result[0].secondary_color.green == 0x00
    assert result[0].secondary_color.blue == 0x00
    assert result[0].secondary_color.alpha == 0x00
    assert result[0].outline_color.red == 0x10
    assert result[0].outline_color.green == 0x10
    assert result[0].outline_color.blue == 0x10
    assert result[0].outline_color.alpha == 0x00
    assert result[0].back_color.red == 0x20
    assert result[0].back_color.green == 0x20
    assert result[0].back_color.blue == 0x20
    assert result[0].back_color.alpha == 0x7F
    assert result[0].bold is True
    assert result[0].italic is False
    assert result[0].underline is False
    assert result[0].strike_out is False
    assert result[0].scale_x == 100.0
    assert result[0].scale_y == 125.0
    assert result[0].spacing == 0.0
    assert result[0].angle == 0.0
    assert result[0].border_style == 1
    assert result[0].outline == 2.5
    assert result[0].shadow == 0.0
    assert result[0].alignment == 2
    assert result[0].margin_left == 15
    assert result[0].margin_right == 15
    assert result[0].margin_vertical == 15
    assert result[0].encoding == 1


def test_ass_style_list_from_ass_string_unknown_style() -> None:
    """Test that unknown styles raise an error."""
    with pytest.raises(CorruptAssError):
        AssStyleList.from_ass_string(
            """[Test Section]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Unknown: Default,Rubik,24,&H0AE9F4F4,&H000000FF,&H00101010,&H7F202020,-1,0,0,0,100,125,0,0,1,2.5,0,2,15,15,15,1
"""
        )


def test_ass_style_list_extending_with_another_list() -> None:
    """Test extending a list with another list.

    This demonstrates how to extend a list while dealing with the ownership
    shenanigans.
    """
    style = AssStyle(name="dummy style")
    styles1 = AssStyleList()
    styles2 = AssStyleList()
    styles2.append(style)
    assert len(styles1) == 0
    assert len(styles2) == 1
    styles1.extend(map(copy, styles2))
    assert len(styles1) == 1


def test_ass_style_list_equality() -> None:
    """Test that style lists can be easily compared."""
    assert AssStyleList() != 5
    assert AssStyleList() == AssStyleList()
    assert AssStyleList() != AssStyleList(name="changed")
    assert AssStyleList(data=[AssStyle(name="dummy style")]) == AssStyleList(
        data=[AssStyle(name="dummy style")]
    )
    assert AssStyleList(data=[AssStyle(name="dummy style")]) != AssStyleList(
        data=[AssStyle(name="changed")]
    )
