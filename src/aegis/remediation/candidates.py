"""Suggest and evaluate remediation candidates without changing dependency files."""

from __future__ import annotations

from dataclasses import dataclass, field

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from aegis.models import DependencyFinding


@dataclass
class RemediationCandidate:
    """A candidate package version and its supporting vulnerability evidence."""

    version: str
    fixes: list[str] = field(default_factory=list)
    compatible_with_constraint: bool | None = None
    reasons: list[str] = field(default_factory=list)


def suggest_fixed_versions(finding: DependencyFinding) -> list[str]:
    """Return valid fixed-version candidates reported by vulnerability records.

    Candidates are deduplicated and sorted using Python package version
    semantics. This function does not establish compatibility or security.
    """
    candidates: set[Version] = set()

    for vulnerability in finding.vulnerabilities:
        for version in vulnerability.fixed_versions:
            try:
                candidates.add(Version(version))
            except InvalidVersion:
                continue

    return [str(version) for version in sorted(candidates)]


def evaluate_candidates(
    finding: DependencyFinding,
) -> list[RemediationCandidate]:
    """Evaluate fixed-version candidates against the declared constraint.

    Each candidate retains the identifiers of records that reported that
    version as fixed. Constraint compatibility is a preliminary check only;
    it does not prove that the candidate resolves every vulnerability or
    that the application will work with it.
    """
    fixed_by_version: dict[Version, set[str]] = {}

    for vulnerability in finding.vulnerabilities:
        identifier = vulnerability.id or "UNKNOWN"

        for fixed_version in vulnerability.fixed_versions:
            try:
                parsed_version = Version(fixed_version)
            except InvalidVersion:
                continue

            fixed_by_version.setdefault(parsed_version, set()).add(identifier)

    constraint = finding.dependency.specifier.strip()
    specifier_set = None
    constraint_error = None

    if constraint:
        try:
            specifier_set = SpecifierSet(constraint)
        except InvalidSpecifier as exc:
            constraint_error = str(exc)

    results = []

    for version in sorted(fixed_by_version):
        candidate = RemediationCandidate(
            version=str(version),
            fixes=sorted(fixed_by_version[version]),
        )

        if not constraint:
            candidate.compatible_with_constraint = True
            candidate.reasons.append(
                "No version constraint was declared; compatibility is unknown."
            )
            # The flag means no declared constraint blocks this version.
            # It does not mean application compatibility has been verified.
        elif constraint_error:
            candidate.compatible_with_constraint = None
            candidate.reasons.append(
                f"Could not evaluate the declared constraint: {constraint_error}"
            )
        else:
            candidate.compatible_with_constraint = version in specifier_set

            if candidate.compatible_with_constraint:
                candidate.reasons.append(
                    f"Version satisfies the declared constraint: {constraint}."
                )
            else:
                candidate.reasons.append(
                    f"Version does not satisfy the declared constraint: {constraint}."
                )

        candidate.reasons.append(
            "Reported as fixed by OSV record(s); application compatibility "
            "and complete vulnerability coverage have not been verified."
        )

        results.append(candidate)

    return results
