"""CLI entry point for dotlinkdoctor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotlinkdoctor.scanner import scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan a dotfile tree for broken symlinks",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root path to scan",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="plain",
        choices=["plain", "json"],
        help="Output format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root_path = Path(args.root).expanduser().resolve()
    issues = scan(root_path)

    if args.output == "json":
        payload = [
            {"path": issue.path, "target": issue.target, "kind": issue.kind}
            for issue in issues
        ]
        json.dump(payload, sys.stdout)
        sys.stdout.write("\n")
    else:
        print(f"broken={len(issues)}")
        for issue in issues:
            print(f"BROKEN {issue.path} -> {issue.target}")

    return 1 if issues else 0


__all__ = ["main"]
