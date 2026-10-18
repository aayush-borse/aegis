import pytest
from packaging.requirements import Requirement

from aegis.parsing.requirements import parse_requirements_file


def test_parses_valid_requirements(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "requests>=2.31\nflask>=3.0\n",
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements_file)

    assert len(result.requirements) == 2
    assert result.issues == []
    assert result.requirements[0].requirement == Requirement("requests>=2.31")
    assert result.requirements[1].requirement == Requirement("flask>=3.0")


def test_records_invalid_requirement(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "requests>=2.31\nthis is not a valid requirement\nflask>=3.0\n",
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements_file)

    assert len(result.requirements) == 2
    assert len(result.issues) == 1
    assert result.issues[0].line_number == 2
    assert result.issues[0].content == "this is not a valid requirement"


def test_preserves_duplicate_declarations(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "requests>=2.31\nrequests<3.0\n",
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements_file)

    assert len(result.requirements) == 2
    assert result.requirements[0].requirement.specifier != (
        result.requirements[1].requirement.specifier
    )


def test_skips_blank_lines_and_comments(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "# Web dependencies\n\nrequests>=2.31\n   \n",
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements_file)

    assert len(result.requirements) == 1
    assert result.issues == []


def test_preserves_original_line_numbers(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(
        "# Dependencies\n\nrequests>=2.31\n",
        encoding="utf-8",
    )

    result = parse_requirements_file(requirements_file)

    assert result.requirements[0].line_number == 3


def test_missing_file_raises_error(tmp_path):
    requirements_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        parse_requirements_file(requirements_file)
