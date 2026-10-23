"""Read PEP 621 dependencies from pyproject.toml without executing project code."""

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from packaging.requirements import InvalidRequirement, Requirement

from aegis.models import AnalysisIssue, Dependency


def parse_pyproject(
    path: str | Path,
) -> tuple[list[Dependency], list[AnalysisIssue]]:
    path = Path(path)
    dependencies: list[Dependency] = []
    issues: list[AnalysisIssue] = []

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        return [], [
            AnalysisIssue(
                "PYPROJECT_READ",
                str(exc),
                str(path),
                severity="error",
            )
        ]

    project = data.get("project", {})
    declarations = list(project.get("dependencies", []))
    optional = project.get("optional-dependencies", {})

    for group, values in optional.items():
        declarations.extend(values)

    for index, raw in enumerate(declarations, start=1):
        try:
            req = Requirement(raw)
        except (InvalidRequirement, TypeError) as exc:
            issues.append(
                AnalysisIssue(
                    "PYPROJECT_REQUIREMENT",
                    f"Invalid dependency declaration: {raw!r}: {exc}",
                    str(path),
                    index,
                )
            )
            continue

        dependencies.append(
            Dependency(
                name=req.name,
                specifier=str(req.specifier),
                source=str(path),
                line_number=None,
                extras=tuple(sorted(req.extras)),
                marker=str(req.marker) if req.marker else None,
                url=req.url,
            )
        )

    if "project" not in data:
        issues.append(
            AnalysisIssue(
                "PYPROJECT_SCOPE",
                (
                    "No [project] table found; Poetry/PDM-specific dependency "
                    "declarations are not yet interpreted."
                ),
                str(path),
            )
        )
    elif "dependencies" not in project and not optional:
        issues.append(
            AnalysisIssue(
                "PYPROJECT_SCOPE",
                (
                    "No PEP 621 project.dependencies or optional-dependencies "
                    "found. Other build-system-specific formats may not "
                    "be supported."
                ),
                str(path),
            )
        )

    return dependencies, issues
