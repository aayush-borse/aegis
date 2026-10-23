"""Read-only project analysis orchestration."""

from datetime import datetime, timezone
from pathlib import Path

from aegis.discovery.manifests import discover_manifests
from aegis.models import AnalysisIssue, AnalysisReport, DependencyFinding
from aegis.parsing.pyproject import parse_pyproject
from aegis.parsing.requirements import parse_requirements_file, to_dependencies
from aegis.remediation.candidates import suggest_fixed_versions
from aegis.vulnerability.osv import OSVError, query_vulnerabilities


def analyze_project(
    project: str | Path, check_vulnerabilities: bool = True, timeout: float = 12.0
) -> AnalysisReport:
    root = Path(project).expanduser().resolve()
    manifests = discover_manifests(root)
    report = AnalysisReport(
        project=str(root),
        generated_at=datetime.now(timezone.utc).isoformat(),
        manifests=[str(p) for p in manifests],
    )
    if not manifests:
        report.issues.append(
            AnalysisIssue(
                "NO_MANIFESTS",
                "No supported root-level dependency manifests were found.",
            )
        )
    for manifest in manifests:
        if manifest.name == "requirements.txt":
            parsed = parse_requirements_file(manifest)
            deps, issues = to_dependencies(parsed)
            report.dependencies.extend(deps)
            report.issues.extend(issues)
        elif manifest.name == "pyproject.toml":
            deps, issues = parse_pyproject(manifest)
            report.dependencies.extend(deps)
            report.issues.extend(issues)
    # Preserve duplicates and source provenance. Deduplicate network requests only.
    cache = {}
    for dep in report.dependencies:
        key = (dep.name.lower().replace("_", "-"), dep.specifier)
        finding = DependencyFinding(dependency=dep)
        if check_vulnerabilities:
            if key not in cache:
                try:
                    cache[key] = (query_vulnerabilities(dep, timeout), None)
                except OSVError as exc:
                    cache[key] = ([], str(exc))
            vulns, error = cache[key]
            finding.vulnerabilities = vulns
            finding.status = "checked" if error is None else "error"
            if error:
                report.issues.append(
                    AnalysisIssue(
                        "OSV_QUERY_FAILED",
                        f"Could not query OSV for {dep.name}: {error}",
                        dep.source,
                        dep.line_number,
                    )
                )
        finding.recommended_versions = suggest_fixed_versions(finding)
        report.findings.append(finding)
    report.complete = not any(i.severity == "error" for i in report.issues) and not any(
        i.code
        in {
            "REQUIREMENTS_PARSE",
            "PYPROJECT_REQUIREMENT",
            "PYPROJECT_SCOPE",
            "OSV_QUERY_FAILED",
        }
        for i in report.issues
    )
    return report
