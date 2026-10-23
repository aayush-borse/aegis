"""Parse the supported, conservative requirements.txt subset."""

from dataclasses import dataclass
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement

from aegis.models import AnalysisIssue, Dependency


@dataclass(frozen=True)
class ParsedRequirement:
    """A dependency declaration found in a requirements file."""

    requirement: Requirement
    source: Path
    line_number: int


@dataclass(frozen=True)
class ParseIssue:
    """A problem encountered while parsing a requirements file."""

    source: Path
    line_number: int
    message: str
    content: str


@dataclass
class ParseResult:
    """Parsed dependency declarations and issues encountered."""

    requirements: list[ParsedRequirement]
    issues: list[ParseIssue]


def parse_requirements_file(path: str | Path) -> ParseResult:
    """Parse a requirements file without executing pip directives."""
    path = Path(path)
    requirements: list[ParsedRequirement] = []
    issues: list[ParseIssue] = []

    with path.open("r", encoding="utf-8-sig") as file:
        continuation = ""
        start_line = 0

        for line_number, raw in enumerate(file, start=1):
            content = raw.strip()

            if not content or content.startswith("#"):
                continue

            if content.endswith("\\"):
                if not continuation:
                    start_line = line_number

                continuation += content[:-1].strip() + " "
                continue

            content = continuation + content
            effective_line = start_line or line_number
            continuation = ""
            start_line = 0

            # Pip directives require additional context and are not
            # standard PEP 508 dependency declarations.
            if content.startswith(("-", "--")):
                issues.append(
                    ParseIssue(
                        source=path,
                        line_number=effective_line,
                        message=(
                            "pip option or include directive is not "
                            "supported by the static parser"
                        ),
                        content=content,
                    )
                )
                continue

            try:
                requirement = Requirement(content)
            except InvalidRequirement as exc:
                issues.append(
                    ParseIssue(
                        source=path,
                        line_number=effective_line,
                        message=str(exc),
                        content=content,
                    )
                )
                continue

            requirements.append(
                ParsedRequirement(
                    requirement=requirement,
                    source=path,
                    line_number=effective_line,
                )
            )

        if continuation:
            issues.append(
                ParseIssue(
                    source=path,
                    line_number=start_line,
                    message="Unfinished line continuation",
                    content=continuation.strip(),
                )
            )

    return ParseResult(
        requirements=requirements,
        issues=issues,
    )


def to_dependencies(
    result: ParseResult,
) -> tuple[list[Dependency], list[AnalysisIssue]]:
    """Convert parsed requirements into AEGIS dependency models."""
    dependencies = [
        Dependency(
            name=item.requirement.name,
            specifier=str(item.requirement.specifier),
            source=str(item.source),
            line_number=item.line_number,
            extras=tuple(sorted(item.requirement.extras)),
            marker=(str(item.requirement.marker) if item.requirement.marker else None),
            url=item.requirement.url,
        )
        for item in result.requirements
    ]

    issues = [
        AnalysisIssue(
            "REQUIREMENTS_PARSE",
            issue.message,
            str(issue.source),
            issue.line_number,
        )
        for issue in result.issues
    ]

    return dependencies, issues
