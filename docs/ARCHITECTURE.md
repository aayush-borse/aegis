# AEGIS Architecture

## Current implementation

AEGIS is a Python modular monolith. Its static analysis path is:

1. `discovery`: locate supported root-level `requirements.txt` and `pyproject.toml` manifests.
2. `parsing`: parse PEP 508 requirements and PEP 621 `[project]` declarations. Unsupported syntax is reported as an issue.
3. `analysis`: orchestrate parsing, preserve source locations, and optionally query OSV.dev.
4. `vulnerability`: use OSV.dev's public query API for PyPI package names.
5. `remediation`: expose fixed versions observed in vulnerability records, constrained by declared specifiers where possible.
6. `reporting`: emit JSON and Markdown reports.
7. `verification`: create a disposable project copy for later verification; this component deliberately does not execute code or install packages.

## Trust boundaries

Project files are read, not changed, by `scan`. Online vulnerability data is external evidence and can be unavailable or incomplete. A query returning no records is not a guarantee of safety. The scanner does not resolve a full environment or prove runtime reachability. Remediation suggestions are candidates, not automatic edits. The workspace helper copies files but does not constitute a hardened sandbox for executing untrusted code.

## Current limitations

- Root-level manifests only; no recursive discovery.
- `requirements.txt` parser handles PEP 508 declarations, blank lines, full-line comments, and simple line continuations. Pip options, nested `-r` files, editable installs, VCS references, and index configuration are reported as unsupported.
- `pyproject.toml` support currently reads PEP 621 `project.dependencies` and optional dependencies. Poetry/PDM-specific formats and lockfiles are not yet resolved.
- OSV lookup is package-level except for a single exact `==` pin. Applicability is not fully evaluated against all version ranges.
- Fixed versions from OSV are not proof of compatibility. Candidate filtering by declared specifier can exclude the appropriate fix if a manifest constraint itself must be changed.
- Verification execution, lockfile updates, transitive dependency resolution, SBOM output, and AI assistance are future work.
