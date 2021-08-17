"""ASS file writing routines."""
import io
from pathlib import Path
from typing import IO, Union, overload

from ass_parser.ass_file import AssFile


@overload
def write_ass(ass_file: AssFile, target: Path) -> None:
    ...  # pragma: no cover


@overload
def write_ass(ass_file: AssFile, target: IO[str]) -> None:
    ...  # pragma: no cover


@overload
def write_ass(ass_file: AssFile, target: None = None) -> str:
    ...  # pragma: no cover


def write_ass(
    ass_file: AssFile, target: Union[Path, IO[str], None] = None
) -> Union[str, None]:
    """Save ASS to the specified target.

    If target is not specified, returns the serialized ASS file as a string.

    :param ass_file: the file to save
    :param target: a path, a writable stream or None
    :return: serialized ASS contents if target is None
    """
    if isinstance(target, Path):
        with target.open("w", encoding="utf-8") as handle:
            write_ass(ass_file, handle)
            return None

    if target is None:
        with io.StringIO() as handle:
            write_ass(ass_file, handle)
            return handle.getvalue()

    print(ass_file.script_info.to_ass_string().rstrip(), file=target)
    print(file=target)
    print(ass_file.styles.to_ass_string().rstrip(), file=target)
    print(file=target)
    print(ass_file.events.to_ass_string().rstrip(), file=target)
    for section in ass_file.extra_sections:
        print(file=target)
        print(section.to_ass_string().rstrip(), file=target)

    return None
