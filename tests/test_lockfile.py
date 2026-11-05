"""Tests for pinned lockfile parsing."""

from pathlib import Path

from aegis.parsing.lockfile import lockfile_to_dependencies, parse_lockfile


def test_parse_lockfile(tmp_path: Path) -> None:
    lock = tmp_path / "requirements.lock"
    lock.write_text(
        "requests==2.31.0\nurllib3==1.26.15 # via requests\n",
        encoding="utf-8",
    )

    result = parse_lockfile(lock)
    assert len(result.requirements) == 2
    assert not result.issues

    deps, issues = lockfile_to_dependencies(result)
    assert len(deps) == 2
    assert deps[0].name == "requests"
    assert deps[0].specifier == "==2.31.0"
    assert deps[0].direct is False
    assert lock.exists()