# dotlinkdoctor

A lightweight Python CLI that scans a dotfile tree for broken symlinks and reports them as plain text or JSON. It ignores dotted directories such as `.config` and `.dotfiles` by default, so you can audit `~/` without noise.

## Why

Broken symlinks accumulate in homedir dotfile setups when source files move and links are left behind. `dotlinkdoctor` is a small, portable scanner that can run anywhere Python 3.10+ is installed.

## Features

- Scan paths with mixed files and symlinks
- Report broken symlinks with source and target paths
- Stop descending into common dotfile directories (`.config`, `.dotfiles`, and any parent `.../.` segment)
- Plain text or JSON output via `--output`
- No mandatory dependencies beyond the Python standard library
- Optional `typer`-powered CLI

## Installation

From source:

```bash
python -m pip install .[cli]
```

For CLI usage without installation, `typer` must be installed:

```bash
python -m pip install typer
```

## Usage

```bash
# show broken symlinks under your home directory
dotlinkdoctor scan ~/

# JSON output
dotlinkdoctor scan ~/ --output json

# show version
dotlinkdoctor version
```

## Project structure

```text
src/dotlinkdoctor/
  main.py     # CLI entry point
  scanner.py  # symlink discovery and filtering
  version.py  # package version
tests/
  test_scanner.py
pyproject.toml
README.md
```

## Requirements

- Python 3.10+
- Optional: `typer>=0.9` for CLI mode
- Optional dev tools: `pytest`, `ruff`

## Tags

`dotfiles`, `symlinks`, `python`, `cli`, `lint`
