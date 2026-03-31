# No Local Imports

A pre-commit hook and CLI tool that checks your `pyproject.toml` for local path dependencies in `[tool.uv.sources]` — because it's easy to forget to remove them before committing.

## What it does

When developing with [uv](https://docs.astral.sh/uv/), you might temporarily point a dependency to a local path:

```toml
[tool.uv.sources]
my-lib = { path = "../my-lib" }
```

This is useful during development but should not be committed. `no-local-imports` catches these before they make it into your repo.

## Installation

### As a pre-commit hook (recommended)

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kjaymiller/no-local-imports
    rev: v0.1.0  # use the latest tag
    hooks:
      - id: no-local-imports
```

Then install the hook:

```bash
pre-commit install
```

The hook runs automatically on commits that modify `pyproject.toml`.

### As a CLI tool

Install with pip or uv:

```bash
pip install no-local-imports
# or
uv pip install no-local-imports
```

## Usage

### CLI

Run against the default `pyproject.toml` in the current directory:

```bash
no-local-imports
```

Or specify a path:

```bash
no-local-imports path/to/pyproject.toml
```

If local path sources are found, the tool exits with an error:

```
Local path sources found in [tool.uv.sources]: my-lib, other-lib
```

If no local path sources are found, the tool exits silently with code 0.

### Pre-commit

Once configured, the hook runs automatically when `pyproject.toml` is staged for commit. If local path sources are detected, the commit is blocked until they are removed.
