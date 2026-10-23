from aegis.parsing.pyproject import parse_pyproject


def test_parses_pep621_and_optional_dependencies(tmp_path):
    path = tmp_path / "pyproject.toml"

    path.write_text(
        (
            "[project]\n"
            'name = "demo"\n'
            'dependencies = ["requests>=2.0", "flask==3.0"]\n'
            "[project.optional-dependencies]\n"
            'test = ["pytest>=8"]\n'
        ),
        encoding="utf-8",
    )

    dependencies, issues = parse_pyproject(path)

    assert [dependency.name for dependency in dependencies] == [
        "requests",
        "flask",
        "pytest",
    ]
    assert not issues


def test_reports_invalid_pyproject_dependency(tmp_path):
    path = tmp_path / "pyproject.toml"

    path.write_text(
        '[project]\nname="demo"\ndependencies=["not a dependency"]\n',
        encoding="utf-8",
    )

    dependencies, issues = parse_pyproject(path)

    assert not dependencies
    assert issues[0].code == "PYPROJECT_REQUIREMENT"
