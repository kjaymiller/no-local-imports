import textwrap

import pytest

from no_local_imports.main import check_for_local_sources, main


@pytest.fixture()
def pyproject(tmp_path):
    """Helper that writes a pyproject.toml and returns its path."""

    def _write(content: str) -> str:
        p = tmp_path / "pyproject.toml"
        p.write_text(textwrap.dedent(content))
        return str(p)

    return _write


class TestCheckForLocalSources:
    def test_no_sources_section(self, pyproject):
        path = pyproject("""\
            [project]
            name = "myapp"
        """)
        assert check_for_local_sources(path) == []

    def test_empty_sources(self, pyproject):
        path = pyproject("""\
            [tool.uv.sources]
        """)
        assert check_for_local_sources(path) == []

    def test_remote_sources_only(self, pyproject):
        path = pyproject("""\
            [tool.uv.sources]
            httpx = {git = "https://github.com/encode/httpx"}
        """)
        assert check_for_local_sources(path) == []

    def test_single_local_source(self, pyproject):
        path = pyproject("""\
            [tool.uv.sources]
            mylib = {path = "../mylib"}
        """)
        assert check_for_local_sources(path) == ["mylib"]

    def test_multiple_local_sources(self, pyproject):
        path = pyproject("""\
            [tool.uv.sources]
            mylib = {path = "../mylib"}
            other = {path = "/abs/path/other"}
            remote = {git = "https://example.com/remote"}
        """)
        result = check_for_local_sources(path)
        assert sorted(result) == ["mylib", "other"]

    def test_mixed_sources(self, pyproject):
        path = pyproject("""\
            [tool.uv.sources]
            remote = {git = "https://example.com/repo"}
            local = {path = "../local"}
        """)
        assert check_for_local_sources(path) == ["local"]


class TestMain:
    def test_exits_zero_when_no_local_sources(self, pyproject, monkeypatch):
        path = pyproject("""\
            [tool.uv.sources]
            httpx = {git = "https://github.com/encode/httpx"}
        """)
        monkeypatch.setattr("sys.argv", ["no-local-imports", path])
        main()  # should not raise

    def test_exits_nonzero_when_local_sources(self, pyproject, monkeypatch):
        path = pyproject("""\
            [tool.uv.sources]
            mylib = {path = "../mylib"}
        """)
        monkeypatch.setattr("sys.argv", ["no-local-imports", path])
        with pytest.raises(SystemExit, match="mylib"):
            main()

    def test_defaults_to_pyproject_toml(self, monkeypatch, tmp_path):
        p = tmp_path / "pyproject.toml"
        p.write_text("[project]\nname = 'x'\n")
        monkeypatch.setattr("sys.argv", ["no-local-imports"])
        monkeypatch.chdir(tmp_path)
        main()  # should not raise
