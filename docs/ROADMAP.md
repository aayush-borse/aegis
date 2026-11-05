# Roadmap

## Implemented foundation
- Read-only discovery of root-level `requirements.txt` and `pyproject.toml`.
- Static dependency inventory with source provenance and parser issues.
- Optional OSV.dev lookups for PyPI package names.
- JSON and Markdown reports with explicit incomplete-analysis states.
- Fixed-version candidate extraction from OSV records.
- Temporary copy preparation for future verification.
- Automated tests, linting, formatting, and CI matrix.

## Next milestones
1. **Resolution correctness:** support lockfiles, PEP 508 marker evaluation, and robust pip requirements syntax; model direct versus transitive dependencies.
2. **Vulnerability applicability:** evaluate OSV affected ranges against resolved installed/locked versions and show evidence for each applicability decision.
3. **Remediation planning:** compute candidate constraint changes, account for dependency conflicts, and explain rejected candidates.
4. **Safe verification:** implement a configurable container-backed execution adapter with resource limits, no host credentials, network restrictions, and explicit user consent. Never treat a temporary directory alone as a security sandbox.
5. **Before/after evidence:** compare install results, test commands, exit codes, logs, and environment metadata; never infer that unrun checks passed.
6. **Broader ecosystems:** npm, Maven, Cargo, and other manifest/lockfile formats behind explicit ecosystem adapters.
7. **SBOM and integrations:** CycloneDX/SPDX output, CI annotations, SARIF, and machine-readable policy gates.
8. **AI-assisted analysis:** optional, auditable explanations and remediation hypotheses; deterministic checks remain authoritative.
9. **Project setup assistant:** inspect environment/setup failures and propose reproducible setup fixes, clearly separated from security remediation.
10. **Cloud/runtime compatibility assessment:** assess dependency and runtime compatibility during cloud migration as a separate workflow.
11. **Evaluation:** benchmark precision, recall, runtime, false positives, reproducibility, and remediation success against representative projects and existing tools.
