"""Tests for applicability-aware remediation candidate evaluation."""

from aegis.models import Dependency, DependencyFinding, Vulnerability
from aegis.remediation.candidates import evaluate_candidates


def test_evaluate_candidates_filters_non_applicable() -> None:
    dep = Dependency(name="requests", specifier="==2.32.0")
    vuln = Vulnerability(
        id="VULN-999",
        summary="Not applicable to 2.32.0",
        affected_ranges=[
            {
                "type": "ECOSYSTEM",
                "events": [{"introduced": "0"}, {"fixed": "2.28.0"}],
            }
        ],
        fixed_versions=["2.28.1"],
    )

    finding = DependencyFinding(dependency=dep, vulnerabilities=[vuln])
    candidates = evaluate_candidates(finding)

    # Since 2.32.0 is outside the affected range (< 2.28.0), applicability is False,
    # so the fix candidate should be filtered out.
    assert len(candidates) == 0