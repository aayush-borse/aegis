"""Tests for SBOM and SARIF export generation."""

from datetime import datetime, timezone
from pathlib import Path

from aegis.models import AnalysisReport, Dependency
from aegis.reporting.exporters import export_sarif, export_sbom


def test_exporters_generation(tmp_path: Path) -> None:
    report = AnalysisReport(
        project=str(tmp_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
        dependencies=[
            Dependency(
                name="requests",
                specifier="==2.31.0",
                source="requirements.txt",
            )
        ],
    )

    sbom_path = tmp_path / "sbom.json"
    sarif_path = tmp_path / "sarif.json"

    export_sbom(report, sbom_path)
    export_sarif(report, sarif_path)

    assert sbom_path.exists()
    assert sarif_path.exists()
    assert "CycloneDX" in sbom_path.read_text(encoding="utf-8")
    assert "sarif-schema" in sarif_path.read_text(encoding="utf-8")