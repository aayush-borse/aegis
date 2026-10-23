from aegis.models import Vulnerability
from aegis.vulnerability.advisories import group_advisories


def test_groups_records_sharing_an_alias():
    first = Vulnerability(
        id="GHSA-example",
        summary="First record",
        aliases=["CVE-2026-12345"],
        fixed_versions=["2.0.0"],
    )
    second = Vulnerability(
        id="PYSEC-example",
        summary="Second record",
        aliases=["CVE-2026-12345"],
        fixed_versions=["2.1.0"],
    )

    groups = group_advisories([first, second])

    assert len(groups) == 1
    assert len(groups[0].records) == 2
    assert "CVE-2026-12345" in groups[0].identifiers
    assert groups[0].fixed_versions == ["2.0.0", "2.1.0"]


def test_unrelated_records_remain_separate():
    first = Vulnerability(id="OSV-A", summary="First")
    second = Vulnerability(id="OSV-B", summary="Second")

    groups = group_advisories([first, second])

    assert len(groups) == 2


def test_transitively_linked_records_form_one_group():
    first = Vulnerability(
        id="OSV-A",
        summary="First",
        aliases=["CVE-2026-12345"],
    )
    second = Vulnerability(
        id="OSV-B",
        summary="Second",
        aliases=["CVE-2026-12345", "CVE-2026-67890"],
    )
    third = Vulnerability(
        id="OSV-C",
        summary="Third",
        aliases=["CVE-2026-67890"],
    )

    groups = group_advisories([first, second, third])

    assert len(groups) == 1
    assert len(groups[0].records) == 3


def test_empty_input_returns_no_groups():
    assert group_advisories([]) == []


def test_original_records_are_preserved():
    original = Vulnerability(
        id="OSV-A",
        summary="Original summary",
        aliases=["CVE-2026-12345"],
        references=["https://example.com/advisory"],
    )

    groups = group_advisories([original])

    assert groups[0].records[0] is original
    assert original.summary == "Original summary"
    assert original.references == ["https://example.com/advisory"]
