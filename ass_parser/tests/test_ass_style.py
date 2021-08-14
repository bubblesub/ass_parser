"""Tests for the AssStyle class."""
from unittest.mock import Mock

from ass_parser import AssStyle


def test_ass_style_default_properties() -> None:
    """Test default properties of an AssStyle."""
    style = AssStyle(name="test style")
    assert style.font_name == "Arial"
    assert style.font_size == 20
    assert style.primary_color.red == 255
    assert style.primary_color.green == 255
    assert style.primary_color.blue == 255
    assert style.primary_color.alpha == 0
    assert style.secondary_color.red == 255
    assert style.secondary_color.green == 0
    assert style.secondary_color.blue == 0
    assert style.secondary_color.alpha == 0
    assert style.outline_color.red == 32
    assert style.outline_color.green == 32
    assert style.outline_color.blue == 32
    assert style.outline_color.alpha == 0
    assert style.back_color.red == 32
    assert style.back_color.green == 32
    assert style.back_color.blue == 32
    assert style.back_color.alpha == 127
    assert style.bold is True
    assert style.italic is False
    assert style.underline is False
    assert style.strike_out is False
    assert style.scale_x == 100.0
    assert style.scale_y == 100.0
    assert style.spacing == 0.0
    assert style.angle == 0.0
    assert style.border_style == 1
    assert style.outline == 3.0
    assert style.shadow == 0.0
    assert style.alignment == 2
    assert style.margin_left == 20
    assert style.margin_right == 20
    assert style.margin_vertical == 20
    assert style.encoding == 1


def test_ass_style_scale() -> None:
    """Test scaling styles."""
    style = AssStyle(
        name="test style",
        font_size=1,
        outline=2,
        shadow=3,
        margin_left=4,
        margin_right=5,
        margin_vertical=6,
    )
    style.scale(2.5)
    assert style.font_size == 2
    assert style.outline == 5.0
    assert style.shadow == 7.5
    assert style.margin_left == 10
    assert style.margin_right == 12
    assert style.margin_vertical == 15


def test_ass_style_equality() -> None:
    """Test that styles can be easily compared."""
    assert AssStyle(name="test") != 5
    assert AssStyle(name="test") == AssStyle(name="test")
    assert AssStyle(name="test") != AssStyle(name="changed")

    subscriber = Mock()
    style1 = AssStyle(name="test")
    style2 = AssStyle(name="test")
    style1.changed.subscribe(subscriber)
    assert style1 == style2
    style1.name = "changed"
    assert style1 != style2
