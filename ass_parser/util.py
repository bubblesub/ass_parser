"""Various ASS utilities."""
import re

TIMESTAMP_RE = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{2,3})")


def unescape_ass_tag(text: str) -> str:
    """Do the reverse operation to escape_ass_tag().

    :param text: text to unescape
    :return: unescaped text
    """
    return text.replace(r"\\", "\\").replace(r"\[", "{").replace(r"\]", "}")


def timestamp_to_ms(text: str) -> int:
    """Parse ASS text representation of time to milliseconds.

    :param text: text to parse
    :return: parsed time in number of milliseconds
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
