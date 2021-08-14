"""Tests for the AssColor class."""
from typing import Union

import pytest

from ass_parser import AssColor


@pytest.mark.parametrize(
    "source,expected_result",
    [
        ("&H01020304", AssColor(red=4, green=3, blue=2, alpha=1)),
        ("&H10203040", AssColor(red=0x40, green=0x30, blue=0x20, alpha=0x10)),
        ("&H102030", AssColor(red=0x30, green=0x20, blue=0x10, alpha=0)),
        ("&H01020304&", AssColor(red=4, green=3, blue=2, alpha=1)),
        ("&H10203040&", AssColor(red=0x40, green=0x30, blue=0x20, alpha=0x10)),
        ("&H102030&", AssColor(red=0x30, green=0x20, blue=0x10, alpha=0)),
        ("&H1&", AssColor(red=1, green=0, blue=0, alpha=0)),
        ("&H&", ValueError),
        ("&HX&", ValueError),
        ("XX102030&", ValueError),
    ],
)
def test_ass_color_from_ass_string(
    source: str, expected_result: Union[type[Exception], AssColor]
) -> None:
    """Test AssColor.from_ass_string function behavior."""
    if isinstance(expected_result, AssColor):
        actual_result = AssColor.from_ass_string(source)
        assert actual_result == expected_result
    else:
        with pytest.raises(expected_result):
            AssColor.from_ass_string(source)
