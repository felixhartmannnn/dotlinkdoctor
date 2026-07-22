"""Tests for dotlinkdoctor scanner."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dotlinkdoctor.scanner import scan


def test_broken_symlink_is_reported() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "dotfiles"
        root.mkdir()
        target = root / "missing.txt"
        (root / "link.txt").symlink_to(target)
        issues = scan(root)
        assert any(issue.kind == "broken" and "link.txt" in issue.path for issue in issues)
        target_path = Path(issues[0].target)
        assert "missing.txt" in str(target_path)


def test_ignore_dotfile_dirs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        sub = root / ".config"
        sub.mkdir()
        target = sub / "real.txt"
        target.write_text("x")
        (sub / "link.txt").symlink_to(target)
        issues = scan(root)
        assert all(".config" not in issue.path for issue in issues)


def test_empty_tree_returns_empty() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "dotfiles"
        root.mkdir()
        assert scan(root) == []
