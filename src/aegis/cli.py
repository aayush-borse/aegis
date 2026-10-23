"""Command-line interface for AEGIS."""

import argparse
import sys
from pathlib import Path

from aegis import __version__
from aegis.analysis.engine import analyze_project
from aegis.reporting.writers import write_json, write_markdown
from aegis.verification.sandbox import create_workspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegis",
        description=(
            "Evidence-driven Python dependency investigation and remediation support."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"AEGIS {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser(
        "scan",
        help="Discover manifests, parse dependencies, and query OSV.dev",
    )
    scan.add_argument(
        "project",
        type=Path,
        help="Project directory to inspect (read-only)",
    )
    scan.add_argument(
        "--offline",
        action="store_true",
        help="Skip online vulnerability queries",
    )
    scan.add_argument(
        "--timeout",
        type=float,
        default=12.0,
        help="OSV request timeout in seconds (default: 12)",
    )
    scan.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        default=Path("aegis-report.json"),
        help="JSON report path",
    )
    scan.add_argument(
        "--markdown",
        dest="markdown_path",
        type=Path,
        default=Path("aegis-report.md"),
        help="Markdown report path",
    )
    scan.add_argument(
        "--fail-on-vulnerability",
        action="store_true",
        help="Exit with code 1 if any OSV records are returned",
    )

    prep = sub.add_parser(
        "prepare-workspace",
        help=(
            "Copy a project into an isolated workspace; "
            "does not execute code or install packages"
        ),
    )
    prep.add_argument("project", type=Path)
    prep.add_argument(
        "--destination",
        type=Path,
        help="Optional new destination path; it must not already exist",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.command == "prepare-workspace":
            workspace = create_workspace(args.project, args.destination)
            print(f"Workspace created: {workspace.path}")
            print("No code was executed and no packages were installed.")
            return 0

        if args.timeout <= 0:
            print(
                "Error: --timeout must be greater than zero.",
                file=sys.stderr,
            )
            return 2

        report = analyze_project(
            args.project,
            check_vulnerabilities=not args.offline,
            timeout=args.timeout,
        )

        write_json(report, args.json_path)
        write_markdown(report, args.markdown_path)

        vulns = sum(len(f.vulnerabilities) for f in report.findings)

        print(f"AEGIS analysis {'complete' if report.complete else 'incomplete'}")
        print(
            f"Manifests: {len(report.manifests)} | "
            f"Dependencies: {len(report.dependencies)} | "
            f"OSV records: {vulns} | "
            f"Issues: {len(report.issues)}"
        )
        print(f"JSON report: {args.json_path.resolve()}")
        print(f"Markdown report: {args.markdown_path.resolve()}")

        if not report.complete:
            print(
                "Review report issues; one or more checks were incomplete.",
                file=sys.stderr,
            )

        if args.fail_on_vulnerability and vulns:
            return 1

        return 0 if report.complete else 2

    except (
        FileNotFoundError,
        NotADirectoryError,
        PermissionError,
        OSError,
        ValueError,
    ) as exc:
        print(f"AEGIS error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
