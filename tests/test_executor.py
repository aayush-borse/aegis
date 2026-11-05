"""Tests for isolated remediation execution proposals."""

from pathlib import Path

from aegis.remediation.executor import apply_proposal_to_workspace, create_proposal


def test_remediation_proposal_execution(tmp_path: Path) -> None:
    manifest = tmp_path / "requirements.txt"
    manifest.write_text("requests==2.31.0\n", encoding="utf-8")

    proposal = create_proposal(
        manifest_path=manifest,
        package_name="requests",
        current_specifier="==2.31.0",
        target_version="2.32.0",
    )

    assert proposal.package_name == "requests"
    assert proposal.target_version == "2.32.0"

    success = apply_proposal_to_workspace(proposal, tmp_path)
    assert success is True
    assert proposal.applied is True

    updated_content = manifest.read_text(encoding="utf-8")
    assert "requests==2.32.0" in updated_content