from aegis.models import Dependency, DependencyFinding, Vulnerability
from aegis.remediation.candidates import (
    evaluate_candidates,
    suggest_fixed_versions,
)


def make_finding(specifier, vulnerabilities):
    return DependencyFinding(
        dependency=Dependency(
            name="requests",
            specifier=specifier,
            source="requirements.txt",
        ),
        vulnerabilities=vulnerabilities,
    )


def make_vulnerability(identifier, fixed_versions):
    return Vulnerability(
        id=identifier,
        summary="Test vulnerability",
        fixed_versions=fixed_versions,
    )


def test_suggest_fixed_versions_deduplicates_and_sorts():
    finding = make_finding(
        ">=2.0",
        [
            make_vulnerability("OSV-1", ["2.20.0", "2.31.0"]),
            make_vulnerability("OSV-2", ["2.20.0", "invalid-version"]),
        ],
    )

    assert suggest_fixed_versions(finding) == ["2.20.0", "2.31.0"]


def test_evaluate_candidates_tracks_fix_evidence():
    finding = make_finding(
        ">=2.0",
        [
            make_vulnerability("OSV-1", ["2.20.0"]),
            make_vulnerability("OSV-2", ["2.20.0", "2.31.0"]),
        ],
    )

    candidates = evaluate_candidates(finding)

    assert [candidate.version for candidate in candidates] == [
        "2.20.0",
        "2.31.0",
    ]
    assert candidates[0].fixes == ["OSV-1", "OSV-2"]
    assert candidates[1].fixes == ["OSV-2"]


def test_candidate_satisfying_constraint_is_marked_compatible():
    finding = make_finding(
        ">=2.20,<3.0",
        [make_vulnerability("OSV-1", ["2.20.0", "3.1.0"])],
    )

    candidates = evaluate_candidates(finding)

    assert candidates[0].version == "2.20.0"
    assert candidates[0].compatible_with_constraint is True

    assert candidates[1].version == "3.1.0"
    assert candidates[1].compatible_with_constraint is False


def test_exact_pin_blocks_different_candidate():
    finding = make_finding(
        "==2.19.0",
        [make_vulnerability("OSV-1", ["2.20.0"])],
    )

    candidates = evaluate_candidates(finding)

    assert len(candidates) == 1
    assert candidates[0].compatible_with_constraint is False


def test_invalid_constraint_is_reported_without_crashing():
    finding = make_finding(
        "not-a-valid-specifier",
        [make_vulnerability("OSV-1", ["2.20.0"])],
    )

    candidates = evaluate_candidates(finding)

    assert len(candidates) == 1
    assert candidates[0].compatible_with_constraint is None
    assert any("Could not evaluate" in reason for reason in candidates[0].reasons)


def test_commit_hash_is_not_a_version_candidate():
    finding = make_finding(
        ">=2.0",
        [
            make_vulnerability(
                "OSV-1",
                ["2.20.0", "c45d7c49ea75133e52ab22a8e9e13173938e36ff"],
            )
        ],
    )

    candidates = evaluate_candidates(finding)

    assert [candidate.version for candidate in candidates] == ["2.20.0"]


def test_no_vulnerability_records_returns_no_candidates():
    finding = make_finding(">=2.0", [])

    assert evaluate_candidates(finding) == []
    assert suggest_fixed_versions(finding) == []
