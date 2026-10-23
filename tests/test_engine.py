from aegis.analysis.engine import analyze_project


def test_offline_analysis_is_read_only_and_collects_both_manifests(tmp_path):
    req = tmp_path / "requirements.txt"
    req.write_text("requests>=2.0\n", encoding="utf-8")
    pp = tmp_path / "pyproject.toml"
    pp.write_text(
        '[project]\nname="demo"\ndependencies=["flask>=3.0"]\n', encoding="utf-8"
    )
    before_req, before_pp = req.read_text(), pp.read_text()
    report = analyze_project(tmp_path, check_vulnerabilities=False)
    assert len(report.manifests) == 2
    assert {d.name for d in report.dependencies} == {"requests", "flask"}
    assert all(f.status == "not_checked" for f in report.findings)
    assert req.read_text() == before_req and pp.read_text() == before_pp


def test_missing_manifest_is_reported(tmp_path):
    report = analyze_project(tmp_path, check_vulnerabilities=False)
    assert any(issue.code == "NO_MANIFESTS" for issue in report.issues)
