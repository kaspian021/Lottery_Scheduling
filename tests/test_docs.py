from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_markdown_local_links_and_images_resolve():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_docs.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_exercise_has_required_structure():
    folders = sorted((ROOT / "exercises").glob("exercise_*"))
    assert len(folders) == 8
    for folder in folders:
        for relative in (
            "README.md", "src/run.py", "tests", "docs/README.md",
            "docs/figures/architecture.svg", "docs/figures/flowchart.svg",
            "docs/figures/results.png", "docs/reports/report_fa.md",
            "docs/reports/report_en.md", "outputs/results.json",
        ):
            assert (folder / relative).exists(), f"{folder.name}/{relative}"
