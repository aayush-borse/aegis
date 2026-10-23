"""Safe-by-default isolated verification workspace preparation.

This module never installs packages or executes project code. It creates a temporary
copy for a human or explicitly configured external verification process to use.
"""

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Workspace:
    path: Path
    original: Path
    temporary: bool = True


def create_workspace(
    project: str | Path, destination: str | Path | None = None
) -> Workspace:
    source = Path(project).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Project directory not found: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Project is not a directory: {source}")
    if destination is None:
        target = Path(tempfile.mkdtemp(prefix="aegis-verify-")) / source.name
    else:
        target = Path(destination).expanduser().resolve()
        if target.exists():
            raise FileExistsError(f"Destination already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)

    def ignore(directory: str, names: list[str]) -> set[str]:
        excluded = {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
            "node_modules",
            "dist",
            "build",
        }
        return {name for name in names if name in excluded or name.endswith(".pyc")}

    shutil.copytree(source, target, ignore=ignore, symlinks=False)
    return Workspace(path=target, original=source)
