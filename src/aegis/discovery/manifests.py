"""Discover supported dependency manifests in a project directory."""

from pathlib import Path

SUPPORTED_MANIFESTS = (
    "requirements.txt",
    "pyproject.toml",
)


def discover_manifests(project: str | Path) -> list[Path]:
    project = Path(project)

    if not project.exists():
        raise FileNotFoundError(
            f"Project directory not found: {project}"
        )  # if path doesnt exist we dont continue with our operation
    if not project.is_dir():
        raise NotADirectoryError(
            f"Project is not a directory: {project}"
        )  # if path exists but it is not in directory

    found = []
    for name in SUPPORTED_MANIFESTS:
        manifest = project / name

        if manifest.is_file():
            found.append(manifest)

    return found
