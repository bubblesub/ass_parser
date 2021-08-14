"""ASS file writing routines."""
from pathlib import Path
from typing import IO, Union

from ass_parser.ass_file import AssFile


def write_ass(ass_file: AssFile, target: Union[Path, IO[str]]) -> None:
    """Save ASS to the specified target.

    :param ass_file: the file to save
    :param target: a writable stream or a path
    """
    if isinstance(target, Path):
        with target.open("w", encoding="utf-8") as handle:
            write_ass(ass_file, handle)
            return

    print(ass_file.script_info.to_ass_string().rstrip(), file=target)
    print(file=target)
    print(ass_file.styles.to_ass_string().rstrip(), file=target)
    print(file=target)
    print(ass_file.events.to_ass_string().rstrip(), file=target)
    for section in ass_file.extra_sections:
        print(file=target)
        print(section.to_ass_string().rstrip(), file=target)
