"""Validate local Markdown links and embedded image paths in the repository."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    markdown = sorted(ROOT.rglob("*.md"))
    for source in markdown:
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{source.relative_to(ROOT)}: not valid UTF-8")
            continue
        for target in LINK.findall(content):
            target = target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            candidate = (source.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing target: {target}")
    if errors:
        print("Broken Markdown links:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"Checked {len(markdown)} Markdown files: all local links and image paths resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
