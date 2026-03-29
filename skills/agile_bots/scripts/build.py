"""Build AGENTS.md from content/*.md for skills.sh / portable skill install."""
from pathlib import Path


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    content_dir = skill_dir / "content"
    skill_md = skill_dir / "SKILL.md"
    out_path = skill_dir / "AGENTS.md"

    parts = []
    if skill_md.exists():
        parts.append(skill_md.read_text(encoding="utf-8"))
    for f in sorted(content_dir.glob("*.md")):
        parts.append(f.read_text(encoding="utf-8"))

    out_path.write_text("\n\n---\n\n".join(parts), encoding="utf-8")
    print(f"Wrote {out_path}")
    return str(out_path)


if __name__ == "__main__":
    main()
