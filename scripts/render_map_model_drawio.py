#!/usr/bin/env python
"""Emit a native diagrams.net file from map-model-spec.json (same mxCell pipeline as story maps).

Requires PYTHONPATH to include agile_bots ``src`` (see bots/cli_execute.ps1), or run from repo
with:

    set PYTHONPATH=src
    python scripts/render_map_model_drawio.py --input path/to/map-model-spec.json

Default output: alongside input, ``map-model-class-diagram.drawio``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

AGILE_BOTS_DIR = Path(__file__).resolve().parent.parent
SRC = AGILE_BOTS_DIR / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synchronizers.story_io.map_model_spec_drawio import write_map_model_class_diagram  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="map-model-spec.json → .drawio (native mxGraph XML)")
    ap.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Path to map-model-spec.json",
    )
    ap.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write .drawio here (default: <input_dir>/map-model-class-diagram.drawio)",
    )
    args = ap.parse_args()
    inp = args.input.resolve()
    if not inp.is_file():
        print(f"Not found: {inp}", file=sys.stderr)
        return 1
    out = args.output
    if out is None:
        out = inp.parent / "map-model-class-diagram.drawio"
    else:
        out = out.resolve()
    write_map_model_class_diagram(inp, out)
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
