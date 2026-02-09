"""
Run a single JavaScript/TypeScript code scanner on a file and print violations as JSON.
Used by Node tests (e.g. test_javascript_scanners.js) to verify JS scanner behavior.
Usage: python run_js_scanner.py --file <path> --scanner <scanner_name>
  Scanner names: ascii_only, domain_language, import_placement
Output: JSON array of violation dicts to stdout; exit 0.
"""
import argparse
import json
import sys
from pathlib import Path

# Allow importing from repo src
repo_root = Path(__file__).resolve().parents[2]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def main():
    parser = argparse.ArgumentParser(description="Run a JS code scanner on a file")
    parser.add_argument("--file", required=True, type=Path, help="Path to .js or .ts file")
    parser.add_argument("--scanner", required=True, choices=["ascii_only", "domain_language", "import_placement"])
    args = parser.parse_args()
    file_path = args.file.resolve()
    if not file_path.exists():
        print(json.dumps([{"error": "file_not_found", "path": str(file_path)}]))
        sys.exit(1)
    from scanners.resources.scan_context import FileScanContext
    class Rule:
        name = "test_rule"
        rule_file = "test/rules/test.json"
    rule = Rule()
    if args.scanner == "ascii_only":
        from scanners.code.javascript.ascii_only_scanner import AsciiOnlyScanner
        scanner = AsciiOnlyScanner(rule)
    elif args.scanner == "domain_language":
        from scanners.code.javascript.domain_language_code_scanner import DomainLanguageCodeScanner
        scanner = DomainLanguageCodeScanner(rule)
    elif args.scanner == "import_placement":
        from scanners.code.javascript.import_placement_scanner import ImportPlacementScanner
        scanner = ImportPlacementScanner(rule)
    else:
        print(json.dumps([{"error": "unknown_scanner", "scanner": args.scanner}]))
        sys.exit(1)
    ctx = FileScanContext(story_graph={}, file_path=file_path)
    violations = scanner.scan_file_with_context(ctx)
    out = [v for v in (violations or [])]
    print(json.dumps(out, indent=0))


if __name__ == "__main__":
    main()
