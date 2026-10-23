"""Shared, serializable data models used throughout AEGIS."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Dependency:
    name: str
    specifier: str = ""
    source: str = ""
    line_number: int | None = None
    direct: bool = True
    extras: tuple[str, ...] = ()
    marker: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class AnalysisIssue:
    code: str
    message: str
    source: str | None = None
    line_number: int | None = None
    severity: str = "warning"


@dataclass
class Vulnerability:
    id: str
    summary: str
    details: str = ""
    aliases: list[str] = field(default_factory=list)
    affected_ranges: list[dict[str, Any]] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    modified: str | None = None
    published: str | None = None
    severity: str | None = None
    fixed_versions: list[str] = field(default_factory=list)


@dataclass
class DependencyFinding:
    dependency: Dependency
    vulnerabilities: list[Vulnerability] = field(default_factory=list)
    recommended_versions: list[str] = field(default_factory=list)
    status: str = "not_checked"


@dataclass
class AnalysisReport:
    project: str
    generated_at: str
    manifests: list[str] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    findings: list[DependencyFinding] = field(default_factory=list)
    issues: list[AnalysisIssue] = field(default_factory=list)
    vulnerability_source: str = "OSV.dev API"
    complete: bool = True
    schema_version: str = "1.0"


def to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "__dataclass_fields__"):
        return {k: to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value
