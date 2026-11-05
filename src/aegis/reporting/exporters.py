"""Export analysis reports to standard SBOM and SARIF formats."""

from __future__ import annotations

import json
from pathlib import Path

from aegis.models import AnalysisReport


def export_sbom(report: AnalysisReport, destination: str | Path) -> Path:
    """Export the dependency inventory as a lightweight CycloneDX-style SBOM."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    components = []
    for dep in report.dependencies:
        components.append(
            {
                "type": "library",
                "name": dep.name,
                "version": dep.specifier,
                "purl": f"pkg:pypi/{dep.name}@{dep.specifier.lstrip('=<>!~ ')}",
                "scope": "required" if dep.direct else "optional",
            }
        )

    sbom_data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "metadata": {
            "timestamp": report.generated_at,
            "tools": [
                {
                    "vendor": "AEGIS",
                    "name": "AEGIS Engine",
                    "version": "0.2",
                }
            ],
            "component": {
                "type": "application",
                "name": report.project,
            },
        },
        "components": components,
    }

    path.write_text(json.dumps(sbom_data, indent=2) + "\n", encoding="utf-8")
    return path


def export_sarif(report: AnalysisReport, destination: str | Path) -> Path:
    """Export security findings and issues as a SARIF report."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    results = []

    for finding in report.findings:
        for vuln in finding.vulnerabilities:
            results.append(
                {
                    "ruleId": vuln.id,
                    "level": "warning",
                    "message": {"text": vuln.summary},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {
                                    "uri": finding.dependency.source
                                },
                                "region": {
                                    "startLine": (
                                        finding.dependency.line_number or 1
                                    )
                                },
                            }
                        }
                    ],
                }
            )

    for issue in report.issues:
        results.append(
            {
                "ruleId": issue.code,
                "level": "error" if issue.severity == "error" else "warning",
                "message": {"text": issue.message},
                "locations": (
                    [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": issue.source},
                                "region": {
                                    "startLine": issue.line_number or 1
                                },
                            }
                        }
                    ]
                    if issue.source
                    else []
                ),
            }
        )

    sarif_data = {
        "$schema": (
            "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/"
            "master/Schemata/sarif-schema-2.1.0.json"
        ),
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "AEGIS",
                        "informationUri": (
                            "https://github.com/aayush-borse/aegis"
                        ),
                        "version": "0.2",
                    }
                },
                "results": results,
            }
        ],
    }

    path.write_text(json.dumps(sarif_data, indent=2) + "\n", encoding="utf-8")
    return path