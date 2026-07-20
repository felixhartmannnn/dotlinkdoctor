"""Core scanner for finding broken symlinks in dotfile trees."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List


@dataclass(frozen=True)
class SymlinkIssue:
    path: str
    target: str
    kind: str


@dataclass(frozen=True)
class _SymlinkEntry:
    path: Path
    target: Path
    exists: bool
    dangling: bool


def is_dotfile_root(path: Path) -> bool:
    """Best-effort heuristic for a dotfile directory that should not descend."""
    candidates = {".config", ".dotfiles", ".files"}
    if path.name in candidates:
        return True
    if any(p.name.startswith(".") for p in path.parents if p != path.parent):
        return True
    return False


def iter_symlinks(root: Path) -> Iterator[_SymlinkEntry]:
    root = root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Root not found or not a directory: {root}")

    for dirpath, dirnames, filenames in os.walk(root):
        rp = Path(dirpath)
        if is_dotfile_root(rp):
            dirnames[:] = []
            continue

        for name in list(filenames) + list(dirnames):
            candidate = rp / name
            try:
                if not candidate.is_symlink():
                    continue
            except OSError:
                continue

            target_str = os.readlink(candidate)
            target = Path(target_str)

            if os.path.isabs(target_str):
                resolved = target
                exists = resolved.exists()
            else:
                resolved = (candidate.parent / target).resolve()
                exists = resolved.exists()

            dangling = not exists

            yield _SymlinkEntry(
                path=candidate,
                target=target,
                exists=exists,
                dangling=dangling,
            )


def scan(root: Path, follow_links: bool = False) -> List[SymlinkIssue]:
    del follow_links
    found: List[SymlinkIssue] = []
    for entry in iter_symlinks(root):
        if entry.dangling:
            found.append(
                SymlinkIssue(
                    path=str(entry.path),
                    target=str(entry.target),
                    kind="broken",
                )
            )
    return found
