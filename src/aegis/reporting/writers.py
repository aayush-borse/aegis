"""JSON and Markdown report output."""

import json
from pathlib import Path

from aegis.models import AnalysisReport, to_jsonable
from aegis.vulnerability.advisories import group_advisories


def write_json(
    report: AnalysisReport,
    destination: str | Path,
) -> Path:
    """Write the complete analysis report to a JSON file."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(to_jsonable(report), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return path


def write_markdown(
    report: AnalysisReport,
    destination: str | Path,
) -> Path:
    """Write a human-readable Markdown analysis report."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# AEGIS Dependency Analysis",
        "",
        f"- **Project:** `{report.project}`",
        f"- **Generated:** {report.generated_at}",
        (
            f"- **Analysis complete:** "
            f"{'yes' if report.complete else 'no — review issues below'}"
        ),
        f"- **Manifests:** {len(report.manifests)}",
        f"- **Dependency declarations:** {len(report.dependencies)}",
        "",
    ]

    # Build an advisory summary while preserving every original OSV record.
    raw_record_count = sum(len(finding.vulnerabilities) for finding in report.findings)

    advisory_groups = [
        (finding, group)
        for finding in report.findings
        for group in group_advisories(finding.vulnerabilities)
    ]

    lines.extend(
        [
            "## Advisory Summary",
            "",
            f"- **Raw OSV records:** {raw_record_count}",
            f"- **Unique advisory groups:** {len(advisory_groups)}",
            "",
        ]
    )

    if advisory_groups:
        for finding, group in advisory_groups:
            lines.append(
                f"- **{finding.dependency.name} — {group.canonical_id}:** "
                f"{len(group.records)} OSV record(s)"
            )
            lines.append(f"  - **Identifiers:** {', '.join(group.identifiers)}")
    else:
        lines.append("No OSV advisory records were available to group.")

    lines.extend(["", "## Findings", ""])

    if not report.findings:
        lines.append("No dependency declarations were parsed.")

    for index, finding in enumerate(report.findings, 1):
        dep = finding.dependency
        location = f"{dep.source}" + (f":{dep.line_number}" if dep.line_number else "")

        lines.extend(
            [
                f"### {index}. {dep.name}{dep.specifier}",
                f"- **Source:** `{location}`",
                f"- **Vulnerability query:** {finding.status}",
            ]
        )

        if finding.recommended_versions:
            lines.append(
                "- **Candidate fixed versions (review required):** "
                f"{', '.join(finding.recommended_versions)}"
            )

        if finding.vulnerabilities:
            for vuln in finding.vulnerabilities:
                lines.extend(
                    [
                        f"- **OSV ID:** {vuln.id}",
                        f"  - **Summary:** {vuln.summary}",
                    ]
                )

                if vuln.aliases:
                    lines.append(f"  - **Aliases:** {', '.join(vuln.aliases)}")

                if vuln.fixed_versions:
                    lines.append(
                        "  - **Known fixed versions:** "
                        f"{', '.join(vuln.fixed_versions)}"
                    )

                if vuln.references:
                    lines.append(
                        f"  - **References:** {', '.join(vuln.references[:5])}"
                    )

        elif finding.status == "checked":
            lines.append(
                "- No OSV results were returned for this package query. "
                "This is not proof of security."
            )
        else:
            lines.append("- Vulnerability status was not established.")

        lines.append("")

    lines.extend(["## Issues and Limitations", ""])

    if not report.issues:
        lines.append("No analysis issues were recorded.")

    for issue in report.issues:
        loc = (
            f" ({issue.source}"
            + (f":{issue.line_number}" if issue.line_number else "")
            + ")"
            if issue.source
            else ""
        )

        lines.append(
            f"- **{issue.severity.upper()} — {issue.code}:** {issue.message}{loc}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "This report is decision support, not a guarantee that the "
                "project is secure. OSV results depend on network availability "
                "and source coverage. Static parsing does not resolve the "
                "complete environment, prove that a vulnerability affects "
                "runtime behavior, or verify application compatibility. "
                "Candidate fixed versions require independent review and "
                "compatibility testing. No dependency files were changed "
                "by this analysis."
            ),
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
