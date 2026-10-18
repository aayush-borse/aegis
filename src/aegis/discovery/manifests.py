"""Discover supported dependency manifests in a project directory."""

from pathlib import Path

SUPPORTED_MANIFESTS = (
    "requirements.txt",
    "pyproject.toml",
)


def discover_manifests(project: str | Path) -> list[Path]:
    project = Path(project)

    if not project.exists():
        raise FileNotFoundError(f"Project directory not found: {project}")
    if not project.is_dir():
        raise NotADirectoryError(f"Project is not a directory: {project}")

    found = []
    for name in SUPPORTED_MANIFESTS:
        manifest = project / name

        if manifest.is_file():
            found.append(manifest)

    return found
