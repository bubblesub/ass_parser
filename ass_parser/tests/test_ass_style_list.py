"""Tests for the AssStyleList class."""
import pickle
from copy import copy, deepcopy
from unittest.mock import Mock

import pytest

from ass_parser.ass_sections.ass_style_list import AssStyleList
from ass_parser.ass_style import AssStyle


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


def test_ass_style_list_get_by_name() -> None:
    """Test get_by_name function behavior."""
    style1 = AssStyle(name="dummy style 1")
    style2 = AssStyle(name="dummy style 2")
    styles = AssStyleList()
    styles.extend([style1, style2])
    assert styles.get_by_name("dummy style 1") == style1
    assert styles.get_by_name("dummy style 2") == style2
    assert styles.get_by_name("non-existing style") is None


def test_copying_style() -> None:
    """Test that copied styles are detached from their original parents."""
    style = AssStyle(name="test style")
    styles = AssStyleList()
    styles.append(style)
    assert copy(style).parent is None
    assert style.parent == styles


def test_copying_style_list() -> None:
    """Test that styles copied with their parents are still linked to their
    original parent.
    """
    style = AssStyle(name="test style")
    styles = AssStyleList()
    styles.append(style)
    styles_copy = copy(styles)
    assert styles[0].parent == styles
    assert styles_copy[0].parent == styles


def test_deep_copying_style_list() -> None:
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


def test_modifying_style_emits_modification_event_in_parent() -> None:
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


def test_pickling_preserves_style_parenthood() -> None:
    """Test that pickling and unpickling a style list preserves the parenthood
    relationship with its children.
    """
    style = AssStyle(name="dummy style")
    styles = AssStyleList()
    styles.append(style)
    new_styles = pickle.loads(pickle.dumps(styles))
    assert new_styles[0].parent == new_styles
    assert new_styles[0].parent != styles
