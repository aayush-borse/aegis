"""Tests for vulnerability applicability evaluation."""

from aegis.models import Vulnerability
from aegis.vulnerability.applicability import is_vulnerability_applicable


def test_vulnerability_applicability_in_range() -> None:
    vuln = Vulnerability(
        id="TEST-001",
        summary="Test vuln",
        affected_ranges=[
            {
                "type": "ECOSYSTEM",
                "events": [{"introduced": "0"}, {"fixed": "2.31.0"}],
            }
        ],
    )

    # Version 2.30.0 is within introduced="0", fixed="2.31.0"
    assert is_vulnerability_applicable(vuln, "2.30.0") is True

    # Version 2.31.0 is fixed / outside range
    assert is_vulnerability_applicable(vuln, "2.31.0") is False