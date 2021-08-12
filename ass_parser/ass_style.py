"""ASS style."""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from ass_parser.ass_color import AssColor
from ass_parser.observable_object import ObservableObject

if TYPE_CHECKING:
    from ass_parser.ass_style_list import AssStyleList  # pragma: no coverage


@dataclass
class AssStyle(ObservableObject):
    """ASS style."""

    name: str
    font_name: str = "Arial"
    font_size: int = 20
    primary_color: AssColor = field(
        default_factory=lambda: AssColor(255, 255, 255, 0)
    )
    secondary_color: AssColor = field(
        default_factory=lambda: AssColor(255, 0, 0, 0)
    )
    outline_color: AssColor = field(
        default_factory=lambda: AssColor(32, 32, 32, 0)
    )
    back_color: AssColor = field(
        default_factory=lambda: AssColor(32, 32, 32, 127)
    )
    bold: bool = True
    italic: bool = False
    underline: bool = False
    strike_out: bool = False
    scale_x: float = 100.0
    scale_y: float = 100.0
    spacing: float = 0.0
    angle: float = 0.0
    border_style: int = 1
    outline: float = 3.0
    shadow: float = 0.0
    alignment: int = 2
    margin_left: int = 20
    margin_right: int = 20
    margin_vertical: int = 20
    encoding: int = 1

    parent: Optional["AssStyleList"] = None

    def scale(self, factor: float) -> None:
        """Scale self by the given factor.

        :param factor: scale to scale self by
        """
        self.font_size = int(self.font_size * factor)
        self.outline *= factor
        self.shadow *= factor
        self.margin_left = int(self.margin_left * factor)
        self.margin_right = int(self.margin_right * factor)
        self.margin_vertical = int(self.margin_vertical * factor)
