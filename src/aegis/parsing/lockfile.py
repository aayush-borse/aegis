"""Parse pinned dependency lockfiles (e.g., requirements.lock) for exact versions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement

from aegis.models import AnalysisIssue, Dependency


@dataclass(frozen=True)
class LockedRequirement:
    """A fully resolved and pinned dependency declaration from a lockfile."""

    requirement: Requirement
    source: Path
    line_number: int


@dataclass
class LockfileParseResult:
    """Parsed locked requirements and issues encountered."""

    requirements: list[LockedRequirement]
    issues: list[AnalysisIssue]


def parse_lockfile(path: str | Path) -> LockfileParseResult:
    """Parse a lockfile containing exact version pins without executing code."""
    path = Path(path)
    requirements: list[LockedRequirement] = []
    issues: list[AnalysisIssue] = []

    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        return LockfileParseResult(
            requirements=[],
            issues=[
                AnalysisIssue(
                    code="LOCKFILE_READ",
                    message=str(exc),
                    source=str(path),
                    severity="error",
                )
            ],
        )

    for line_number, raw in enumerate(lines, start=1):
        content = raw.strip()

        if not content or content.startswith("#") or content.startswith(("-", "--")):
            continue

        if " #" in content:
            content = content.split(" #", 1)[0].strip()

        try:
            req = Requirement(content)
        except (InvalidRequirement, TypeError) as exc:
            issues.append(
                AnalysisIssue(
                    code="LOCKFILE_REQUIREMENT",
                    message=f"Invalid lockfile entry {content!r}: {exc}",
                    source=str(path),
                    line_number=line_number,
                )
            )
            continue

        requirements.append(
            LockedRequirement(
                requirement=req,
                source=path,
                line_number=line_number,
            )
        )

    return LockfileParseResult(requirements=requirements, issues=issues)


def lockfile_to_dependencies(
    result: LockfileParseResult,
) -> tuple[list[Dependency], list[AnalysisIssue]]:
    """Convert parsed lockfile requirements into AEGIS Dependency models."""
    dependencies = [
        Dependency(
            name=item.requirement.name,
            specifier=str(item.requirement.specifier),
            source=str(item.source),
            line_number=item.line_number,
            direct=False,
            extras=tuple(sorted(item.requirement.extras)),
            marker=(
                str(item.requirement.marker)
                if item.requirement.marker
                else None
            ),
            url=item.requirement.url,
        )
        for item in result.requirements
    ]
    return dependencies, result.issues