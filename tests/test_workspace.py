import pytest

from aegis.verification.sandbox import create_workspace


def test_workspace_copies_project_but_omits_git_and_venv(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "requirements.txt").write_text("requests>=2\n", encoding="utf-8")
    (project / ".git").mkdir()
    (project / ".venv").mkdir()
    workspace = create_workspace(project)
    assert (workspace.path / "requirements.txt").exists()
    assert not (workspace.path / ".git").exists()
    assert not (workspace.path / ".venv").exists()


def test_workspace_refuses_existing_destination(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    dest = tmp_path / "dest"
    dest.mkdir()
    with pytest.raises(FileExistsError):
        create_workspace(project, dest)
