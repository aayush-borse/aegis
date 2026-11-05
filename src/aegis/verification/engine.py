"""Verification engine for running checks against prepared workspaces."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VerificationResult:
    """Outcome of running verification checks on a workspace."""

    success: bool
    exit_code: int
    stdout: str
    stderr: str
    checks_run: list[str] = field(default_factory=list)


def verify_workspace(
    workspace_path: str | Path,
    command: list[str] | None = None,
    timeout: float = 30.0,
) -> VerificationResult:
    """Run a verification command (e.g., pytest) within the workspace directory.

    If no command is specified, defaults to running python -m pytest.
    """
    target = Path(workspace_path).resolve()

    if not target.is_dir():
        return VerificationResult(
            success=False,
            exit_code=2,
            stdout="",
            stderr=f"Workspace directory not found: {target}",
            checks_run=[],
        )

    run_cmd = command or [sys.executable, "-m", "pytest"]

    try:
        completed = subprocess.run(
            run_cmd,
            cwd=target,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return VerificationResult(
            success=completed.returncode == 0,
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            checks_run=[" ".join(run_cmd)],
        )
    except subprocess.TimeoutExpired as exc:
        return VerificationResult(
            success=False,
            exit_code=124,
            stdout=exc.stdout or "",
            stderr=f"Verification timed out after {timeout} seconds.",
            checks_run=[" ".join(run_cmd)],
        )
    except Exception as exc:
        return VerificationResult(
            success=False,
            exit_code=2,
            stdout="",
            stderr=str(exc),
            checks_run=[" ".join(run_cmd)],
        )