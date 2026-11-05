"""Tests for enhanced evidence and reporting output."""

from datetime import datetime, timezone
from pathlib import Path

from aegis.models import AnalysisReport, Dependency
from aegis.reporting.writers import write_json, write_markdown


def test_evidence_report_generation(tmp_path: Path) -> None:
    report = AnalysisReport(
        project=str(tmp_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
        manifests=[str(tmp_path / "requirements.txt")],
        dependencies=[
            Dependency(
                name="requests",
                specifier="==2.31.0",
                source="requirements.txt",
            )
        ],
    )

    json_path = tmp_path / "report.json"
    md_path = tmp_path / "report.md"

    write_json(report, json_path)
    write_markdown(report, md_path)

    assert json_path.exists()
    assert md_path.exists()
    assert "Audit & Verification Evidence" in md_path.read_text(
        encoding="utf-8"
    )