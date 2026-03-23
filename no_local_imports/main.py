import sys

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def check_for_local_sources(pyproject_path: str = "pyproject.toml") -> list[str]:
    """Return a list of source names that use a local path."""
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    sources = data.get("tool", {}).get("uv", {}).get("sources", {})
    return [
        name
        for name, config in sources.items()
        if isinstance(config, dict) and "path" in config
    ]


def main() -> None:
    pyproject_path = sys.argv[1] if len(sys.argv) > 1 else "pyproject.toml"
    local_sources = check_for_local_sources(pyproject_path)

    if local_sources:
        raise SystemExit(
            f"Local path sources found in [tool.uv.sources]: {', '.join(local_sources)}"
        )


if __name__ == "__main__":
    main()
