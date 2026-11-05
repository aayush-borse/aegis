"""End-to-end integration tests for AEGIS workflow."""

from pathlib import Path

from aegis.analysis.engine import analyze_project
from aegis.reporting.exporters import export_sarif, export_sbom
from aegis.reporting.writers import write_json, write_markdown
from aegis.verification.sandbox import create_workspace


def test_end_to_end_workflow(tmp_path: Path) -> None:
    # 1. Setup sample project
    reqs = tmp_path / "requirements.txt"
    reqs.write_text("requests==2.31.0\n", encoding="utf-8")

    # 2. Run offline analysis to test engine + parser integration
    report = analyze_project(tmp_path, check_vulnerabilities=False)
    assert report.complete is True
    assert len(report.dependencies) == 1

    # 3. Test report writers
    json_rep = tmp_path / "reports" / "scan.json"
    md_rep = tmp_path / "reports" / "scan.md"
    write_json(report, json_rep)
    write_markdown(report, md_rep)
    assert json_rep.exists()
    assert md_rep.exists()

    # 4. Test SBOM and SARIF exporters
    sbom_rep = tmp_path / "reports" / "sbom.json"
    sarif_rep = tmp_path / "reports" / "sarif.json"
    export_sbom(report, sbom_rep)
    export_sarif(report, sarif_rep)
    assert sbom_rep.exists()
    assert sarif_rep.exists()

    # 5. Test workspace preparation sandbox copy
    workspace = create_workspace(tmp_path, tmp_path / "workspace_copy")
    assert workspace.path.exists()
    assert (workspace.path / "requirements.txt").exists()