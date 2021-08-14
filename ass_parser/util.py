"""Various ASS utilities."""
import re
from decimal import Decimal
from typing import Union

TIMESTAMP_RE = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{2,3})")


def escape_ass_tag(text: str) -> str:
    """Escape text so that it doesn't get treated as ASS tags.

    :param text: text to escape
    :return: escaped text
    """
    return text.replace("\\", r"\\").replace("{", r"\[").replace("}", r"\]")


def unescape_ass_tag(text: str) -> str:
    """Do the reverse operation to escape_ass_tag().

    :param text: text to unescape
    :return: unescaped text
    """
    return text.replace(r"\\", "\\").replace(r"\[", "{").replace(r"\]", "}")


def ms_to_times(milliseconds: int) -> tuple[int, int, int, int]:
    """Convert PTS to tuple a symbolizing human-readable time chunks.

    :param milliseconds: PTS
    :return: tuple with hours, minutes, seconds and milliseconds
    """
    milliseconds = int(round(max(0, milliseconds)))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return hours, minutes, seconds, milliseconds


def ms_to_ass_timestamp(milliseconds: int) -> str:
    """Convert milliseconds into a ASS text representation of time.

    :param text: milliseconds to convert
    :return: ASS text representation
    """
    hours, minutes, seconds, milliseconds = ms_to_times(milliseconds)
    return f"{hours:01d}:{minutes:02d}:{seconds:02d}.{milliseconds // 10:02d}"


def ass_timestamp_to_ms(text: str) -> int:
    """Convert ASS text representation of time to milliseconds.

    :param text: text to convert
    :return: milliseconds
    """
    match = TIMESTAMP_RE.match(text)
    assert match is not None

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    frac = match.group(4)

    milliseconds: int = int(frac) * 10 ** (3 - len(frac))
    milliseconds += seconds * 1000
    milliseconds += minutes * 60000
    milliseconds += hours * 3_600_000
    return milliseconds


def smart_float(value: Union[int, float]) -> str:
    """Convert a float to a string but discard trailing .0.

    :param value: an input value
    :return: string representation
    """
    dec = Decimal(str(value))
    if dec == dec.to_integral():
        return str(dec.quantize(Decimal(1)))
    return str(dec.normalize())
