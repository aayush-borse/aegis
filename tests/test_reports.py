import json

from aegis.models import AnalysisReport, Dependency
from aegis.reporting.writers import write_json, write_markdown


def test_report_writers(tmp_path):
    report = AnalysisReport(
        project="demo",
        generated_at="now",
        dependencies=[Dependency(name="requests", specifier=">=2")],
    )
    jp = write_json(report, tmp_path / "nested" / "report.json")
    mp = write_markdown(report, tmp_path / "nested" / "report.md")
    assert json.loads(jp.read_text())["dependencies"][0]["name"] == "requests"
    assert "AEGIS Dependency Analysis" in mp.read_text()
