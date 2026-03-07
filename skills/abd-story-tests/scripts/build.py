"""Build AGENTS.md for abd-story-tests. Portable skill for skills.sh install."""
from pathlib import Path

_CONTENT_ORDER = ["core", "process", "output", "strategy", "validation", "script-invocation"]
_CONTENT_STEMS = {s.lower() for s in _CONTENT_ORDER}


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    content_dir = skill_dir / "content"
    rules_dir = skill_dir / "rules"
    out_path = skill_dir / "AGENTS.md"

    parts = []
    # Content in defined order
    for stem in _CONTENT_ORDER:
        f = content_dir / (stem + ".md")
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))
    # Remaining content/*.md alphabetically
    for f in sorted(content_dir.glob("*.md")):
        if f.stem.lower() not in _CONTENT_STEMS:
            parts.append(f.read_text(encoding="utf-8"))
    # Rules
    if rules_dir.exists():
        for f in sorted(rules_dir.glob("*.md")):
            parts.append(f.read_text(encoding="utf-8"))

    out_path.write_text("\n\n---\n\n".join(parts), encoding="utf-8")
    print(f"Wrote {out_path}")
    return str(out_path)


if __name__ == "__main__":
    main()
