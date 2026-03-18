from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_key_project_files_exist():
    expected = [
        ROOT / "main.py",
        ROOT / "README.md",
        ROOT / "pyproject.toml",
        ROOT / "pytest.ini",
        ROOT / "Makefile",
        ROOT / "package.json",
    ]
    for path in expected:
        assert path.exists(), f"Missing expected file: {path.name}"


def test_ci_workflow_exists():
    workflow = ROOT / ".github" / "workflows" / "ci.yml"
    assert workflow.exists(), "CI workflow file should exist"
