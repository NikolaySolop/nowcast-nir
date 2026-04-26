"""Smoke tests for the initial project skeleton."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_expected_top_level_files_exist() -> None:
    """Verify the basic project files exist."""

    expected_files = [
        ".env.example",
        "Dockerfile",
        "README.md",
        "docker-compose.yml",
        "pyproject.toml",
    ]

    for relative_path in expected_files:
        assert (PROJECT_ROOT / relative_path).is_file()


def test_expected_source_modules_exist() -> None:
    """Verify the agreed source modules exist."""

    expected_modules = [
        "config",
        "ingestion",
        "storage",
    ]

    for module_name in expected_modules:
        assert (PROJECT_ROOT / "src" / module_name).is_dir()
