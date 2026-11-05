"""Safe, auditable remediation proposal and execution preparation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RemediationProposal:
    """A proposed change to a dependency manifest."""

    manifest_path: Path
    package_name: str
    current_specifier: str
    target_version: str
    applied: bool = False
    evidence: list[str] = field(default_factory=list)


def create_proposal(
    manifest_path: str | Path,
    package_name: str,
    current_specifier: str,
    target_version: str,
) -> RemediationProposal:
    """Create a structured remediation proposal requiring human review."""
    return RemediationProposal(
        manifest_path=Path(manifest_path),
        package_name=package_name,
        current_specifier=current_specifier,
        target_version=target_version,
        evidence=[
            "Proposed upgrade generated from verified advisory fixed versions.",
            "Requires human review and compatibility testing before application.",
        ],
    )


def apply_proposal_to_workspace(
    proposal: RemediationProposal, workspace_path: str | Path
) -> bool:
    """Apply a remediation proposal to a copied workspace file safely.

    Performs a text-based replacement in the manifest copy for the package,
    preserving human review and ensuring original files remain untouched.
    """
    workspace = Path(workspace_path).resolve()
    target_manifest = workspace / proposal.manifest_path.name

    if not target_manifest.is_file():
        return False

    content = target_manifest.read_text(encoding="utf-8")
    lines = content.splitlines()
    updated_lines = []
    replaced = False

    for line in lines:
        # Basic matching for requirements.txt style declarations
        if line.strip().startswith(proposal.package_name):
            updated_lines.append(f"{proposal.package_name}=={proposal.target_version}")
            replaced = True
        else:
            updated_lines.append(line)

    if replaced:
        target_manifest.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
        proposal.applied = True
        return True

    return False