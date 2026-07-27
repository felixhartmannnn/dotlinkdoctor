# dotlinkdoctor

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]
[![License-MIT](https://img.shields.io/badge/License-MIT-green)]

A lightweight Python CLI that scans a dotfile tree for broken symlinks and reports them as plain text or JSON. It ignores dotted directories such as `.config` and `.dotfiles` by default, so you can audit `~/` without noise.

Checkout the repo: https://github.com/felixhartmannnn/dotlinkdoctor

## Description

Broken symlinks accumulate in homedir dotfile setups when source files move and links are left behind. `dotlinkdoctor` is a small, portable scanner that can run anywhere Python 3.10+ is installed.

## Features

- Scan paths with mixed files and symlinks
- Report broken symlinks with source and target paths
- Stop descending into common dotfile directories (`.config`, `.dotfiles`, and any parent `.../.` segment)
- Plain text or JSON output via `--output` / `-o`
- No mandatory dependencies beyond the Python standard library

## Installation

From source:

```bash
python -m pip install .
python -m pip install .[dev]
```

For CLI usage without installation, no extra dependencies are required beyond the standard library.

## Usage

```bash
dotlinkdoctor ~/

dotlinkdoctor ~/ --output json

python -m dotlinkdoctor ~/
```

## Requirements

- Python 3.10+
- Optional dev tools: `pytest`, `ruff`

## Project structure

```text
src/dotlinkdoctor/
  __main__.py   # `python -m dotlinkdoctor` support
  main.py       # CLI entry point
  scanner.py    # symlink discovery and filtering
  version.py    # package version
tests/
  test_scanner.py
pyproject.toml
README.md
```

## License

This project is licensed under the [MIT License](LICENSE).
