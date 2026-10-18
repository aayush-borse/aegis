"""Parse dependency declarations from requirements files"""

from dataclasses import dataclass
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement


@dataclass(frozen=True)
class ParsedRequirement:
    """A dependency declaration found in a requirement file."""

    requirement: Requirement
    source: Path
    line_number: int


@dataclass(frozen=True)
class ParseIssue:
    """A Problem encountered while parsing a requirements file"""

    source: Path
    line_number: int
    message: str
    content: str


@dataclass
class ParseResult:
    requirements: list[ParsedRequirement]
    issues: list[ParseIssue]


def parse_requirements_file(path: str | Path) -> ParseResult:
    path = Path(path)

    requirements = []
    issues = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            content = line.strip()

            if not content or content.startswith("#"):
                continue

            try:
                requirement = Requirement(content)
            except InvalidRequirement as error:
                issues.append(
                    ParseIssue(
                        source=path,
                        line_number=line_number,
                        message=str(error),
                        content=content,
                    )
                )
                continue

            requirements.append(
                ParsedRequirement(
                    requirement=requirement,
                    source=path,
                    line_number=line_number,
                )
            )

    return ParseResult(
        requirements=requirements,
        issues=issues,
    )
