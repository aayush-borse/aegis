<p align="center"><img src="assets/aegis-logo.png" alt="AEGIS logo" width="520"></p>
<h1 align="center">AEGIS</h1>
<h3 align="center">Autonomous Software Supply-Chain Intelligence &amp; Verified Remediation Engine</h3>
<p align="center"><strong>Understand the risk. Investigate the fix. Verify the outcome.</strong></p>

AEGIS is an early-stage Python CLI for evidence-driven dependency investigation. It discovers supported Python manifests, builds a source-aware dependency inventory, optionally queries OSV.dev, and produces JSON and Markdown reports. It does not silently change project dependencies or execute target project code.

> **Security and maturity note:** This is a useful research/MVP tool, not a complete security scanner or a hardened remediation agent. A clean scan does not prove a project is secure. Network results may be incomplete, and runtime compatibility is not established by dependency metadata alone.

## Features

- Read-only discovery of root-level `requirements.txt` and `pyproject.toml`.
- PEP 508 requirement parsing with source and line provenance for requirements files.
- PEP 621 dependency parsing from `[project.dependencies]` and `[project.optional-dependencies]`.
- Unsupported declarations and partial analysis surfaced as issues.
- Optional OSV.dev vulnerability queries for PyPI packages.
- Conservative extraction of fixed-version candidates from OSV records.
- JSON and Markdown reports.
- Disposable project-copy preparation for future verification work; it does **not** execute code or install dependencies.
- pytest, Ruff, and GitHub Actions CI.

## Requirements

- Python 3.10+
- Network access for live OSV queries (optional; use `--offline` to skip them)

## Install

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

Run a read-only scan with online OSV queries:

```bash
aegis scan /path/to/project
```

Windows example:

```powershell
aegis scan "C:\path\to\project"
```

Skip online queries (deterministic, offline inventory):

```bash
aegis scan ./sample-project --offline
```

Choose output paths and timeout:

```bash
aegis scan ./sample-project --timeout 20 --json reports/scan.json --markdown reports/scan.md
```

Return exit code 1 if OSV records were returned (useful for simple CI gates):

```bash
aegis scan ./sample-project --fail-on-vulnerability
```

Prepare a disposable copy for a future/manual verification workflow:

```bash
aegis prepare-workspace ./sample-project
```

Or select a new destination (it must not already exist):

```bash
aegis prepare-workspace ./sample-project --destination ./tmp/aegis-copy
```

The workspace command only copies files and excludes common VCS, environment, and cache directories. It is **not** a secure sandbox for running untrusted code.

## Reports and exit codes

- `aegis-report.json`: structured report including dependencies, findings, source locations, and issues.
- `aegis-report.md`: human-readable report.
- `0`: static analysis completed without reported parsing/query issues (or offline inventory completed). Review report status fields to see which checks were actually run.
- `1`: `--fail-on-vulnerability` was requested and OSV returned one or more records.
- `2`: invalid input or analysis was incomplete. Review the report and issue list.

A vulnerability record is not automatically proof that the exact declared version is affected. Conversely, zero returned records is not proof of safety. In this initial version, package-level OSV queries are not a substitute for lockfile-aware resolution and full affected-range evaluation.

## Supported input and current limits

| Input | Current behavior |
|---|---|
| `requirements.txt` | PEP 508 declarations, blank lines, full-line comments, simple backslash continuations. Pip options, nested includes, editable/VCS installs, and index directives are reported as unsupported. |
| `pyproject.toml` | PEP 621 `project.dependencies` and `project.optional-dependencies`. Poetry/PDM-specific layouts and lockfiles are not resolved. |
| Vulnerability data | Public OSV.dev query API; requires network unless `--offline`. |
| Remediation | Reports fixed versions present in vulnerability data; does not modify manifests or guarantee compatibility. |
| Verification | Workspace-copy preparation only. No package installation, arbitrary command execution, or app test execution occurs. |

## Development

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Architecture and roadmap

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap and future scope](docs/ROADMAP.md)

Future milestones include lockfile-aware dependency resolution, version-range applicability analysis, container-isolated verification, before/after evidence, SBOM/SARIF outputs, additional ecosystems, optional auditable AI assistance, setup-failure diagnosis, and cloud/runtime compatibility assessment. These are planned, not claimed as implemented.

## Responsible use

Only analyze projects you are authorized to inspect. Review external vulnerability records and proposed upgrades before applying changes. Do not execute untrusted projects in an ordinary temporary directory and assume they are isolated.

## License

MIT. See [LICENSE](LICENSE).
