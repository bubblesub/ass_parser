"""AssStyle definition."""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from ass_parser.ass_color import AssColor
from ass_parser.observable_object_mixin import ObservableObjectMixin
from ass_parser.observable_sequence_mixin import (
    ObservableSequenceChangeEvent,
    ObservableSequenceItemModificationEvent,
)

if TYPE_CHECKING:
    from ass_parser.ass_sections import AssStyleList  # pragma: no coverage


@dataclass
class AssStyle(ObservableObjectMixin):
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

    _parent: Optional["AssStyleList"] = None
    _index: Optional[int] = None

    def scale(self, factor: float) -> None:
        """Scale self by the given factor.

        :param factor: scale to scale self by
        """
        self.begin_update()
        self.font_size = int(self.font_size * factor)
        self.outline *= factor
        self.shadow *= factor
        self.margin_left = int(self.margin_left * factor)
        self.margin_right = int(self.margin_right * factor)
        self.margin_vertical = int(self.margin_vertical * factor)
        self.end_update()

    @property
    def parent(self) -> Optional["AssStyleList"]:
        """Return parent list.

        :return: parent list
        """
        return self._parent

    @property
    def index(self) -> int:
        """Return style index within its parent list.

        If the style does not have a parent list, raises a ValueError.

        :return: index
        """
        if self._index is None:
            raise ValueError("AssStyle does not belong to any AssStyleList")
        return self._index

    def _after_change(self) -> None:
        """Emit item modified event in the parent list."""
        super()._after_change()
        if self.parent is not None:
            self.parent.items_modified.emit(
                ObservableSequenceItemModificationEvent(
                    index=self.index, item=self
                )
            )
            self.parent.changed.emit(ObservableSequenceChangeEvent())

    def __copy__(self) -> "AssStyle":
        """Duplicate self.

        The copy is detached from the parent list.

        :return: duplicate of self
        """
        ret = type(self)(name=self.name)
        ret.__dict__.update(
            {
                key: value
                for key, value in self.__dict__.items()
                if not callable(value) and key != "_parent"
            }
        )
        return ret

    def __eq__(self, other: Any) -> bool:
        """Check for equality. Ignores parent list and event handlers.

        :param other: other object
        :return: whether objects are equal
        """
        if not isinstance(other, AssStyle):
            return False
        return all(
            key.startswith("_")
            or key == "parent"
            or getattr(self, key) == getattr(other, key)
            for key in self.__dataclass_fields__  # type: ignore
        )
