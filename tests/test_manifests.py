import pytest

# python provides us "tmp_path" a temporary directory for tests
from aegis.discovery.manifests import discover_manifests


# when both path are given
def test_discovers_supported_manifests(tmp_path):
    requirements = tmp_path / "requirements.txt"
    pyproject = tmp_path / "pyproject.toml"

    requirements.write_text("requests==2.32\n", encoding="utf-8")
    pyproject.write_text("[project]\nname = 'smaple'\n", encoding="utf-8")

    result = discover_manifests(tmp_path)
    assert result == [requirements, pyproject]


# when only path of file is given
def test_only_requirementfile_exists(tmp_path):
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("requests==2.34.05\n", encoding="utf-8")

    result = discover_manifests(tmp_path)
    assert result == [requirements]


# when file is not present
def test_project_directory_doesnot_exist(tmp_path):
    project = tmp_path / "nonexistent_project"

    with pytest.raises(FileNotFoundError):
        discover_manifests(project)


# When we expect directory and a file is given
def test_not_a_directory(tmp_path):
    notes = tmp_path / "notes.txt"
    notes.write_text("hello world", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        discover_manifests(notes)


# when a valid project with no supported manifests is presented
def test_directory_exists_butno_supportedfiles(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("This is a place holder", encoding="utf-8")
    result = discover_manifests(tmp_path)
    assert result == []


# inspect project without modifying them
def test_discovery_does_not_modify_manifest(tmp_path):
    requirements = tmp_path / "requirements.txt"
    original_contents = "requests==2.31.0\n"
    requirements.write_text(original_contents, encoding="utf-8")

    discover_manifests(tmp_path)

    assert requirements.read_text(encoding="utf-8") == original_contents
