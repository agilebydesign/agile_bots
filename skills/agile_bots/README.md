# agile_bots skill — deploy (Cursor, global only)

Install this skill in **`%USERPROFILE%\.cursor\skills\`**, same as your other personal skills—not under the repo’s **`.cursor/`** tree.

## Setup

1. **Build** (after editing `content/*.md`):

   ```powershell
   cd <path-to>\agile_bots\skills\agile_bots
   python scripts\build.py
   ```

2. **Junction** the global skills folder to this skill directory (adjust the target path to your clone):

   ```powershell
   $skills = "$env:USERPROFILE\.cursor\skills"
   $target = "C:\dev\agile_bots\skills\agile_bots"   # your clone
   if (-not (Test-Path $skills)) { New-Item -ItemType Directory -Path $skills -Force }
   if (Test-Path "$skills\agile_bots") { cmd /c "rmdir `"$skills\agile_bots`"" }   # replace existing junction
   New-Item -ItemType Junction -Path "$skills\agile_bots" -Target $target
   ```

3. **Reload** Cursor.

## Layout (source repo)

| File | Role |
|------|------|
| `SKILL.md` | Skill entry (frontmatter + body) |
| `content/*.md` | Reference bundled into `AGENTS.md` |
| `scripts/build.py` | Writes `AGENTS.md` = `SKILL.md` + sorted `content/*.md` |

Do not install under **`~/.cursor/skills-cursor/`** (reserved for Cursor).
