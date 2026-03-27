"""
Story bot CLI entry point: forces this repository's ``src`` onto ``sys.path``
before loading ``cli.cli_main``.

Use this when ``PYTHONPATH`` (or another checkout) points at a different
``agile_bots`` tree, which would make ``python -m cli.cli_main`` load the wrong
``cli`` package and fail commands such as ``*.render.renderAll``.
"""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    src = root / "src"
    if not src.is_dir():
        print(f"ERROR: expected src at {src}", file=sys.stderr)
        sys.exit(1)
    # This repo first so ``import cli`` resolves here, not another checkout.
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(src))
    try:
        os.chdir(root)
    except OSError:
        pass
    runpy.run_module("cli.cli_main", run_name="__main__")


if __name__ == "__main__":
    main()
