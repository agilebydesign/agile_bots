"""Extract text from a PDF into Markdown so it can be searched/summarized.

Usage (from repo root):
  python tools/pdf_extract.py --input "path/to/file.pdf" --out "path/to/file.md"

If you don't have a PDF extraction library installed:
  python -m pip install pypdf

Notes:
- This does NOT create a venv; it uses whatever `python` you run.
- Some PDFs are scanned images; for those you'll need OCR (e.g., Tesseract).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExtractResult:
    pages: int
    chars: int


def extract_with_pypdf(pdf_path: Path) -> list[str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: pypdf. Install with: python -m pip install pypdf"
        ) from exc

    reader = PdfReader(str(pdf_path))
    texts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        # Normalize Windows newlines and trim trailing spaces
        text = "\n".join(line.rstrip() for line in text.splitlines()).strip("\n")
        texts.append(text)
    return texts


def to_markdown(pages: list[str], title: str) -> str:
    out: list[str] = [f"# {title}", ""]
    for i, page_text in enumerate(pages, start=1):
        out.append(f"## Page {i}")
        out.append("")
        if page_text.strip():
            out.append(page_text)
        else:
            out.append("(No extractable text on this page — possibly scanned image.)")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def run(input_path: Path, out_path: Path) -> ExtractResult:
    pages = extract_with_pypdf(input_path)
    md = to_markdown(pages, title=input_path.stem)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    chars = sum(len(p) for p in pages)
    return ExtractResult(pages=len(pages), chars=chars)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract PDF text to Markdown")
    parser.add_argument("--input", required=True, help="Path to input PDF")
    parser.add_argument(
        "--out",
        required=True,
        help="Path to output Markdown (.md)",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    if not input_path.exists():
        raise SystemExit(f"Input PDF not found: {input_path}")

    result = run(input_path, out_path)
    print(f"Wrote: {out_path} (pages={result.pages}, extracted_chars={result.chars})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
