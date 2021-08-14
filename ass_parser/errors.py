"""Common error definitions."""


class CorruptAssError(ValueError):
    """An ASS file is corrupted and cannot be read."""

    def __init__(self, message: str = "") -> None:
        """Initialize self.

        :param message: additional message to show
        """
        prefix = "corrupt ASS file"
        super().__init__(f"{prefix}: {message}" if message else prefix)


class CorruptAssLineError(CorruptAssError):
    """An ASS file is corrupted and cannot be read."""

    def __init__(self, line_num: int, line: str, message: str = "") -> None:
        """Initialize self.

        :param line_num: line number that triggered the error
        :param line: line content that triggered the error
        :param message: additional message to show
        """
        prefix = f'error while parsing line #{line_num} ("{line}")'
        super().__init__(f"{prefix}: {message}" if message else prefix)
