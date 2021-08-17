"""Tests for the project documentation."""
import re
from pathlib import Path
from typing import Any, no_type_check

import black
import pytest


@no_type_check
def format_black(source: Any) -> str:
    """Format source using Black.

    :param source: a string to format
    :return: a formatted string
    """
    return black.format_str(
        str(source),
        mode=black.Mode(
            target_versions={black.mode.TargetVersion.PY39},
            line_length=79,
        ),
    )


@pytest.fixture(name="readme_content")
def fixture_readme_content(repo_dir: Path) -> str:
    """Get the README.md contents.

    :param repo_dir: the path to the repository
    :return: plain text content of README.md
    """
    path_to_readme = repo_dir / "README.md"
    assert path_to_readme.exists()
    return path_to_readme.read_text()


@pytest.fixture(name="readme_code_snippet")
def fixture_readme_code_snippet(readme_content: str) -> str:
    """Get the README.md example code snippet content.

    :param readme_content: plain text content of README.md
    :return: example code snippet
    """
    match = re.search(r"```python3([^`]*)```", readme_content, flags=re.DOTALL)
    assert match
    return match.group(1).lstrip()


@pytest.fixture(name="readme_code_result")
def fixture_readme_code_result(readme_content: str) -> str:
    """Get the README.md example result content.

    :param readme_content: plain text content of README.md
    :return: example result
    """
    match = re.search(r"```text([^`]*)```", readme_content, flags=re.DOTALL)
    assert match
    return match.group(1).lstrip()


def test_readme_code_up_to_date(
    capsys: Any, readme_code_snippet: str, readme_code_result: str
) -> None:
    """Test that the code example in the README.md matches the actual output
    from the library.
    """
    exec(readme_code_snippet)  # pylint: disable=exec-used
    actual_result = format_black(capsys.readouterr().out.strip())
    assert actual_result == readme_code_result


def test_readme_code_formatting(readme_code_snippet: str) -> None:
    """Test that the code example in the README.md is well-formatted."""
    assert readme_code_snippet == format_black(readme_code_snippet)
