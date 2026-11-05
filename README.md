<div align="center">

  <img src="assets/aegis-logo.png" alt="AEGIS logo" width="420" />

  <h1>AEGIS</h1>

  <h3>Autonomous Software Supply-Chain Intelligence &amp; Verified Remediation Engine</h3>

  <p><strong>Understand the risk. Investigate the fix. Verify the outcome.</strong></p>

  <p>
    An evidence-driven Python engine for dependency investigation,
    vulnerability intelligence and verified remediation.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Security-Supply%20Chain-critical?style=flat-square" alt="Supply Chain Security" />
    <img src="https://img.shields.io/badge/Vulnerability%20Data-OSV.dev-blue?style=flat-square" alt="OSV.dev" />
    <img src="https://img.shields.io/badge/Testing-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest" />
    <img src="https://img.shields.io/badge/Code%20Quality-Ruff-D7FF64?style=flat-square" alt="Ruff" />
    <img src="https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square" alt="Version 1.0.0" />
    <img src="https://img.shields.io/github/license/aayush-borse/aegis?style=flat-square" alt="License" />
  </p>

  <p>
    <a href="#overview">Overview</a> ·
    <a href="#features">Features</a> ·
    <a href="#architecture">Architecture</a> ·
    <a href="#getting-started">Installation</a> ·
    <a href="#usage">Usage</a> ·
    <a href="#roadmap">Roadmap</a>
  </p>

  <p>
    <a href="docs/ARCHITECTURE.md">
      <strong>Architecture</strong>
    </a>
    &nbsp; · &nbsp;
    <a href="docs/ROADMAP.md">
      <strong>Roadmap</strong>
    </a>
    &nbsp; · &nbsp;
    <a href="LICENSE">
      <strong>License</strong>
    </a>
  </p>

</div>

---

## Overview

Modern software applications depend on increasingly complex ecosystems of third-party packages and libraries.

These dependencies introduce security risks that can be difficult to identify, investigate and resolve reliably.

**AEGIS (Autonomous Software Supply-Chain Intelligence & Verified Remediation Engine)** is a modular Python system designed to make dependency investigation, vulnerability analysis and remediation more structured, transparent and evidence-driven.

AEGIS goes beyond identifying potentially vulnerable dependencies. Its underlying engine supports dependency and lockfile resolution, vulnerability intelligence, applicability analysis, remediation candidate generation, remediation execution, verification and security-data exports.

The broader engineering objective is to investigate how dependency vulnerabilities can be analyzed, potential fixes evaluated, and remediation outcomes verified through reproducible evidence.

### The central idea

Finding a vulnerable dependency is only the beginning.

A meaningful remediation workflow must investigate:

* Which dependency is involved?
* Where was it declared?
* How was its version resolved?
* What vulnerability information is available?
* Does the vulnerability apply to the resolved dependency version?
* Which remediation options are supported by the available evidence?
* What happened when a proposed change was applied?
* What verification was actually performed?
* What evidence supports the final conclusion?

AEGIS is designed around this distinction between **detecting a potential risk and establishing evidence that a remediation is acceptable.**

> **Security and maturity:** AEGIS provides dependency investigation and remediation capabilities, but it is not a guarantee that a project is secure. Vulnerability intelligence can be incomplete, and successful verification checks cannot prove the absence of all vulnerabilities or runtime defects. Findings and evidence should be reviewed before accepting changes.

## Features

| Capability | Description | Status |
|---|---|---|
| Manifest Discovery | Discovers and parses supported dependency manifests. | Implemented |
| Requirements Parsing | Parses dependency declarations and retains source information. | Implemented |
| PyProject Parsing | Processes supported Python project dependency declarations. | Implemented |
| Dependency Inventory | Builds structured dependency representations. | Implemented |
| Lockfile Resolution | Resolves dependency information using supported lockfiles. | Implemented |
| Vulnerability Intelligence | Retrieves vulnerability information from OSV.dev. | Implemented |
| Applicability Analysis | Evaluates vulnerability applicability against resolved dependency versions. | Implemented |
| Remediation Candidates | Generates reviewable dependency remediation candidates. | Implemented |
| Remediation Execution | Applies supported remediation proposals programmatically. | Implemented |
| Verification Engine | Integrates automated verification checks for proposed changes. | Implemented |
| Evidence Collection | Collects verification and analysis results for review. | Implemented |
| JSON Reporting | Generates structured analysis and remediation reports. | Implemented |
| Markdown Reporting | Generates human-readable reports. | Implemented |
| SBOM Export | Provides software component inventory export capabilities. | Implemented |
| SARIF Export | Provides structured security finding export capabilities. | Implemented |
| Automated Testing | pytest test suite covering implemented functionality. | Implemented |
| Code Quality | Ruff linting and formatting. | Configured |
| Automated CI | GitHub Actions workflow. | Configured |

## How AEGIS Works

The overall workflow follows a structured dependency investigation and remediation process.

```text
                  TARGET PYTHON PROJECT
                           |
                           v
                    PROJECT DISCOVERY
                           |
                           v
             MANIFEST AND LOCKFILE ANALYSIS
                           |
                           v
                   DEPENDENCY RESOLUTION
                           |
                           v
                VULNERABILITY INTELLIGENCE
                           |
                           v
                 APPLICABILITY ANALYSIS
                           |
                           v
                REMEDIATION CANDIDATES
                           |
                           v
                REMEDIATION EXECUTION
                           |
                           v
                  VERIFICATION ENGINE
                           |
                           v
                  EVIDENCE COLLECTION
                           |
                  +--------+--------+
                  |        |        |
                  v        v        v
                REPORTS   SBOM     SARIF
```

This diagram represents the broader capabilities of the AEGIS package. Not every stage is exposed as an independent CLI command.

Workspace preparation is available as a separate operation. It creates a separate project copy for controlled evaluation.

## Architecture

AEGIS follows a modular Python architecture with separate responsibilities for discovery, parsing, dependency analysis, vulnerability intelligence, remediation, verification, reporting and workspace preparation.

### Component Responsibilities

| Component | Responsibility |
|---|---|
| CLI | Exposes user-facing commands and configuration. |
| Discovery | Identifies supported dependency manifests. |
| Parsing | Converts dependency declarations into structured representations. |
| Analysis | Coordinates dependency analysis and resolution. |
| Vulnerability | Integrates vulnerability intelligence and applicability analysis. |
| Remediation | Generates and applies remediation proposals. |
| Verification | Runs verification checks and evaluates outcomes. |
| Models | Defines structured data exchanged between components. |
| Reporting | Generates JSON, Markdown, SBOM and SARIF outputs. |
| Workspace | Prepares separate project copies for evaluation. |

### Engineering Principles

**1. Source-aware analysis**

Dependency findings retain relevant source information, allowing developers to trace declarations back to project files and locations.

**2. Explicit limitations**

Unsupported declarations and incomplete checks should be surfaced as issues rather than silently ignored.

**3. Isolation**

Dependency changes can be evaluated in separate workspaces rather than directly modifying the original project.

**4. Evidence over assumptions**

Vulnerability records, remediation candidates and verification results are treated as evidence for review, not automatic proof of security or compatibility.

**5. Separation of concerns**

Discovery, parsing, vulnerability queries, remediation, verification and reporting remain separate components.

**6. Reproducibility**

Analysis results and verification evidence should be traceable and repeatable.

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Core application |
| Dependency parsing | packaging | Python dependency and version handling |
| Configuration parsing | tomllib / tomli | TOML processing |
| Vulnerability intelligence | OSV.dev | Public vulnerability information |
| CLI | Python argparse | Command-line interface |
| Data models | Python | Structured analysis results |
| Testing | pytest | Automated tests |
| Code quality | Ruff | Linting and formatting |
| Version control | Git | Source control |
| CI | GitHub Actions | Automated checks |

## Getting Started

### Requirements

* Python 3.10 or newer.
* Git.
* pip.
* Network access for live OSV.dev vulnerability queries.

Network access is optional when using offline mode.

### 1. Clone the repository

```bash
git clone https://github.com/aayush-borse/aegis.git
cd aegis
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install AEGIS

Install the package with its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

This installs the project in editable mode and makes the `aegis` CLI available in the activated environment.

### 5. Verify installation

```bash
aegis --help
```

Inspect the available commands and options.

## Usage

AEGIS currently exposes two primary CLI commands: `scan` and `prepare-workspace`.

Additional remediation, verification and export capabilities are available through the underlying Python package modules.

### 1. Run a dependency scan

Perform a project scan with online OSV.dev vulnerability queries:

```bash
aegis scan /path/to/project
```

**Windows example:**

```powershell
aegis scan "C:\path\to\project"
```

The scan command performs project discovery, manifest and lockfile analysis, dependency resolution, vulnerability querying, applicability checking and report generation.

### 2. Run an offline scan

Skip online vulnerability queries:

```bash
aegis scan ./sample-project --offline
```

### 3. Configure report output

Choose custom JSON and Markdown output paths:

```bash
aegis scan ./sample-project --timeout 20 --json reports/scan.json --markdown reports/scan.md
```

The timeout controls the configured OSV query timeout.

### 4. Use vulnerability findings as a CI gate

Return a non-zero exit code when vulnerability findings meet the configured condition:

```bash
aegis scan ./sample-project --fail-on-vulnerability
```

Review the generated report to understand the findings and their applicability evidence.

### 5. Prepare a separate workspace

Create a project copy:

```bash
aegis prepare-workspace ./sample-project
```

Choose a custom destination:

```bash
aegis prepare-workspace ./sample-project --destination ./tmp/aegis-copy
```

Workspace preparation is a separate operation from remediation execution and verification.

**Important:** A separate project copy should not automatically be treated as a hardened security sandbox. Review execution permissions and environmental isolation before running untrusted project code.

## Remediation and Verification

AEGIS includes programmatic capabilities for generating and applying remediation proposals.

The remediation workflow is designed to distinguish between:

* Identifying a vulnerable dependency.
* Determining whether vulnerability information applies to the resolved version.
* Generating a candidate remediation.
* Applying a supported change.
* Running verification checks.
* Collecting evidence for human review.

Remediation candidates are not equivalent to guaranteed fixes. Version constraints, compatibility, project behavior and verification outcomes must be considered before accepting a change.

Advanced remediation and verification functionality is implemented in the Python package modules. These capabilities are not currently exposed as separate CLI subcommands.

## Reports and Exports

AEGIS supports multiple output formats to make findings and remediation results easier to inspect and integrate into development workflows.

### JSON Report

A structured output containing relevant dependency analysis, vulnerability findings and remediation or verification information.

### Markdown Report

A human-readable report designed to make dependency investigation results easier to inspect and review.

### SBOM Export

Programmatic software component inventory export capabilities.

### SARIF Export

Programmatic structured security finding export capabilities for compatible analysis workflows.

JSON and Markdown reporting are available through the scan CLI options. SBOM and SARIF exports are provided through the reporting modules rather than standalone CLI commands.

## Development

### Run Tests

```bash
python -m pytest
```

### Check Code Quality

```bash
python -m ruff check .
```

### Check Formatting

```bash
python -m ruff format --check .
```

These commands help maintain consistent formatting, code quality and expected behavior as the project evolves.

## Project Structure

The repository uses a modular Python source layout.

```text
aegis/
│
├── .github/
│   └── workflows/
│
├── assets/
│   └── aegis-logo.png
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
│
├── src/
│   └── aegis/
│       ├── analysis/
│       ├── parsing/
│       ├── remediation/
│       ├── reporting/
│       ├── verification/
│       ├── vulnerability/
│       └── cli.py
│
├── tests/
│
├── pyproject.toml
├── README.md
└── LICENSE
```

*The diagram illustrates the major architectural areas. Consult the repository for the exact current file list.*

## Roadmap

With the core capabilities implemented, future development focuses on improving reliability, evaluation quality and integration.

### Dependency Intelligence

* [ ] Build representative dependency and vulnerability evaluation datasets.
* [ ] Measure vulnerability applicability accuracy.
* [ ] Evaluate false-positive and false-negative behavior.
* [ ] Improve diagnostic reporting for incomplete dependency analysis.

### Verified Remediation

* [ ] Evaluate remediation success across representative projects.
* [ ] Improve verification reliability and coverage.
* [ ] Expand compatibility assessment.
* [ ] Improve reproducibility of remediation results.

### Reporting and Integration

* [ ] Improve CI/CD integration workflows.
* [ ] Expand interoperability with security tooling.
* [ ] Improve report traceability and evidence presentation.

### Security and Usability

* [ ] Review workspace isolation and execution boundaries.
* [ ] Improve failure handling and operational diagnostics.
* [ ] Expand documentation and developer experience.

See the detailed project documents:

* [Architecture](docs/ARCHITECTURE.md)
* [Roadmap and future scope](docs/ROADMAP.md)

## Responsible Use

AEGIS is intended to assist with dependency investigation and remediation decisions, not to certify that a software project is secure.

* Only analyze projects you are authorized to inspect.
* Review external vulnerability records before making security decisions.
* Evaluate proposed dependency upgrades before accepting them.
* Treat incomplete analysis and missing vulnerability data as uncertainty, not proof of safety.
* Review verification evidence rather than relying only on a successful exit code.
* Do not execute untrusted projects in ordinary temporary directories and assume they are isolated.

## Contributing

Contributions, suggestions and discussions are welcome.

1. Fork the repository.
2. Create a focused feature branch.
3. Implement your changes.
4. Add or update tests.
5. Run pytest and Ruff checks.
6. Submit a pull request with a clear explanation.

Contributions should preserve the project's focus on explicit behavior, traceable evidence and safe dependency investigation.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

  <img src="assets/aegis-logo.png" alt="AEGIS logo" width="120" />

  <h3>AEGIS</h3>

  <p><strong>Understand the risk. Investigate the fix. Verify the outcome.</strong></p>

  <sub>Evidence-driven software supply-chain investigation.</sub>

</div>