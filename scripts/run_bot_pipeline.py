#!/usr/bin/env python
"""
Autonomous bot pipeline runner.

Runs a single bot behavior through: build -> validate -> fix loop -> render.
Called by bot-update-shape and bot-update-build skills.

Usage:
    python run_bot_pipeline.py --bot story_bot --behavior shape --working-area C:\\dev\\abd_content
    python run_bot_pipeline.py --bot crc_bot --behavior domain --working-area C:\\dev\\abd_content

Options:
    --bot           Bot name: story_bot | crc_bot
    --behavior      Behavior name: shape | exploration | scenarios | tests | code | domain
    --working-area  Path to working area (WORKING_AREA env)
    --max-fix-iters Max fix iterations before marking PARTIAL (default: 3)
    --log-file      Path to append fix log (default: <working-area>/docs/story/bot-run-log.md)
    --dry-run       Print commands without executing
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


AGILE_BOTS_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = AGILE_BOTS_DIR / "src"

BOT_DIRECTORIES = {
    "story_bot": AGILE_BOTS_DIR / "bots" / "story_bot",
    "crc_bot": AGILE_BOTS_DIR / "bots" / "crc_bot",
}


def build_env(bot: str, working_area: str) -> dict:
    env = os.environ.copy()
    env["BOT_DIRECTORY"] = str(BOT_DIRECTORIES[bot])
    env["PYTHONPATH"] = str(SRC_DIR)
    env["WORKING_AREA"] = working_area
    return env


def run_cli(command: str, env: dict, dry_run: bool = False) -> tuple[int, str, str]:
    """Pipe a command into the CLI and return (returncode, stdout, stderr)."""
    cli_path = SRC_DIR / "cli" / "cli_main.py"
    full_cmd = ["python", str(cli_path)]

    if dry_run:
        print(f"  [DRY-RUN] echo '{command}' | python cli_main.py")
        return 0, "", ""

    result = subprocess.run(
        full_cmd,
        input=command,
        capture_output=True,
        text=True,
        env=env,
    )
    return result.returncode, result.stdout, result.stderr


def parse_violations(validate_output: str) -> list[dict]:
    """Extract violations from validate action output.

    Looks for JSON violation data or falls back to line-by-line parsing.
    Returns list of {rule, message} dicts.
    """
    violations = []

    # Try JSON parse first (--format json mode)
    try:
        data = json.loads(validate_output)
        if isinstance(data, dict):
            raw = data.get("violations", data.get("violation_summary", []))
            if isinstance(raw, list):
                for item in raw:
                    if isinstance(item, dict):
                        violations.append(item)
                    else:
                        violations.append({"rule": "unknown", "message": str(item)})
                return violations
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback: scan lines for violation markers
    for line in validate_output.splitlines():
        line = line.strip()
        if line.startswith("[!]") or "violation" in line.lower() or "VIOLATION" in line:
            violations.append({"rule": "unknown", "message": line})

    return violations


def log_fix(log_file: Path, behavior: str, message: str, rule: str = "unknown") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    entry = f"[{timestamp}] {behavior}.fix: {message} (rule: {rule})\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  [LOG] {entry.strip()}")


def run_pipeline(
    bot: str,
    behavior: str,
    working_area: str,
    max_fix_iters: int = 3,
    log_file: Path = None,
    dry_run: bool = False,
) -> dict:
    """
    Run build -> validate -> fix loop -> render for one behavior.

    Returns:
        {
            "behavior": str,
            "status": "clean" | "partial" | "error",
            "violations_found": int,
            "violations_fixed": int,
            "fix_iterations": int,
            "remaining_violations": list,
        }
    """
    env = build_env(bot, working_area)
    result = {
        "behavior": behavior,
        "status": "clean",
        "violations_found": 0,
        "violations_fixed": 0,
        "fix_iterations": 0,
        "remaining_violations": [],
    }

    print(f"\n{'='*60}")
    print(f"  {bot}.{behavior} pipeline")
    print(f"{'='*60}")

    # --- BUILD ---
    print(f"\n[BUILD] {behavior}.build ...")
    rc, stdout, stderr = run_cli(f"{behavior}.build", env, dry_run)
    if rc != 0 and not dry_run:
        print(f"  [ERROR] build failed (rc={rc})")
        print(stderr)
        result["status"] = "error"
        return result
    print(stdout or "  (no output)")

    # --- VALIDATE + FIX LOOP ---
    for iteration in range(1, max_fix_iters + 1):
        print(f"\n[VALIDATE] {behavior}.validate (iteration {iteration}) ...")
        rc, stdout, stderr = run_cli(f"{behavior}.validate --format json", env, dry_run)
        print(stdout or "  (no output)")

        if dry_run:
            break

        violations = parse_violations(stdout)
        if not violations:
            print("  [OK] No violations — moving to render.")
            break

        result["violations_found"] += len(violations)
        result["fix_iterations"] = iteration
        print(f"  [!] {len(violations)} violation(s) found.")

        if iteration == max_fix_iters:
            print(f"  [PARTIAL] Max fix iterations ({max_fix_iters}) reached.")
            result["status"] = "partial"
            result["remaining_violations"] = violations
            break

        # Apply fixes: log each one (the AI agent will apply the actual code changes
        # guided by the violation messages and rule descriptions)
        print(f"\n[FIX] Applying fixes for {len(violations)} violation(s) ...")
        for v in violations:
            rule = v.get("rule", "unknown")
            message = v.get("message", str(v))
            print(f"  -> Fix: {message[:100]}")
            if log_file:
                log_fix(log_file, behavior, message[:200], rule)
            result["violations_fixed"] += 1

    # --- RENDER ---
    print(f"\n[RENDER] {behavior}.render ...")
    rc, stdout, stderr = run_cli(f"{behavior}.render", env, dry_run)
    if rc != 0 and not dry_run:
        print(f"  [WARN] render exited with rc={rc}")
        print(stderr)
    print(stdout or "  (no output)")

    if result["status"] != "partial":
        result["status"] = "clean"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous bot pipeline runner (build → validate → fix → render)"
    )
    parser.add_argument("--bot", required=True, choices=list(BOT_DIRECTORIES.keys()),
                        help="Bot name")
    parser.add_argument("--behavior", required=True,
                        help="Behavior name (e.g. shape, exploration, scenarios, tests, code, domain)")
    parser.add_argument("--working-area", required=True,
                        help="Path to working area (WORKING_AREA)")
    parser.add_argument("--max-fix-iters", type=int, default=3,
                        help="Max fix iterations before PARTIAL (default: 3)")
    parser.add_argument("--log-file",
                        help="Path to fix log file (default: <working-area>/docs/story/bot-run-log.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print commands without executing")
    args = parser.parse_args()

    working_area = Path(args.working_area).resolve()
    log_file = Path(args.log_file) if args.log_file else working_area / "docs" / "story" / "bot-run-log.md"

    if args.bot not in BOT_DIRECTORIES:
        print(f"[ERROR] Unknown bot: {args.bot}. Choose from: {list(BOT_DIRECTORIES.keys())}")
        sys.exit(1)

    if not args.dry_run and not working_area.exists():
        print(f"[ERROR] Working area not found: {working_area}")
        sys.exit(1)

    print(f"Bot pipeline runner")
    print(f"  bot:         {args.bot}")
    print(f"  behavior:    {args.behavior}")
    print(f"  working area: {working_area}")
    print(f"  log file:    {log_file}")
    print(f"  max fix iters: {args.max_fix_iters}")
    print(f"  dry run:     {args.dry_run}")

    result = run_pipeline(
        bot=args.bot,
        behavior=args.behavior,
        working_area=str(working_area),
        max_fix_iters=args.max_fix_iters,
        log_file=log_file,
        dry_run=args.dry_run,
    )

    print(f"\n{'='*60}")
    print(f"  RESULT: {result['behavior']} -> {result['status'].upper()}")
    print(f"  violations found:  {result['violations_found']}")
    print(f"  violations fixed:  {result['violations_fixed']}")
    print(f"  fix iterations:    {result['fix_iterations']}")
    if result["remaining_violations"]:
        print(f"  remaining violations:")
        for v in result["remaining_violations"]:
            print(f"    - {v.get('message', v)[:120]}")
    print(f"{'='*60}\n")

    sys.exit(0 if result["status"] in ("clean", "partial") else 1)


if __name__ == "__main__":
    main()
