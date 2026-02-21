"""Scope debug logging - writes to logs/scope_debug.log for tracing scope flow."""
from pathlib import Path
from datetime import datetime


def _log_path(workspace_dir=None):
    """Get path to scope debug log file."""
    if workspace_dir and str(workspace_dir).strip():
        base = Path(workspace_dir)
    else:
        base = Path(__file__).parent.parent.parent
    log_dir = base / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir / "scope_debug.log"


def log(message: str, workspace_dir=None):
    """Append a line to scope_debug.log."""
    try:
        log_file = _log_path(workspace_dir)
        ts = datetime.now().isoformat()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception as e:
        pass  # Don't fail on log write
