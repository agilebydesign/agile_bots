"""Scanner for detecting useless or redundant comments in JavaScript."""

from typing import List, Dict, Any
from pathlib import Path
import re
from scanners.code.javascript.js_code_scanner import JSCodeScanner
from scanners.resources.violation import Violation
from scanners.resources.scan_context import FileScanContext


class UselessCommentsScanner(JSCodeScanner):
    """Detects comments that don't add value to the code."""
    
    USELESS_PATTERNS = [
        # Comments that just repeat the code
        (r'//\s*function\s+\w+', 'Comment just repeats function declaration'),
        (r'//\s*const\s+\w+', 'Comment just repeats const declaration'),
        (r'//\s*let\s+\w+', 'Comment just repeats let declaration'),
        (r'//\s*var\s+\w+', 'Comment just repeats var declaration'),
        (r'//\s*return\s*$', 'Comment just says "return"'),
        (r'//\s*end\s+of\s+\w+', 'Obvious end-of-block comment'),
        (r'//\s*TODO:\s*$', 'Empty TODO comment'),
        (r'//\s*FIXME:\s*$', 'Empty FIXME comment'),
    ]
    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        violations = []
        
        if not context.exists or not str(context.file_path).endswith('.js'):
            return violations
        
        parsed = self._parse_js_file(context.file_path)
        if not parsed:
            return violations
        
        content, ast, lines = parsed
        
        # Check inline comments
        for line_num, line in enumerate(lines, start=1):
            # Find // comments
            comment_match = re.search(r'//\s*(.+)', line)
            if comment_match:
                comment_text = comment_match.group(1).strip()
                
                # Skip copyright/license comments
                if any(keyword in comment_text.lower() for keyword in ['copyright', 'license', 'spdx']):
                    continue
                
                # ALL non-license comments are violations per the rule
                violation = self._create_violation(
                    file_path=context.file_path,
                    line_number=line_num,
                    message=f"Delete comment - code must be self-explanatory: {comment_text[:50]}",
                    details={'comment': comment_text}
                )
                violations.append(violation)
        
        # Check AST comments (block comments /** ... */ from esprima)
        ast_comments = ast.get('comments', [])
        for comment in ast_comments:
            line = comment.get('loc', {}).get('start', {}).get('line', 0)
            value = comment.get('value', '').strip()
            
            # Skip copyright/license comments
            if any(keyword in value.lower() for keyword in ['copyright', 'license', 'spdx']):
                continue
            
            # ALL non-license block comments are violations per the rule
            comment_preview = value[:50].replace('\n', ' ')
            violation = self._create_violation(
                file_path=context.file_path,
                line_number=line,
                message=f"Delete block comment - code must be self-explanatory: {comment_preview}",
                details={'comment': value, 'comment_type': 'block'}
            )
            violations.append(violation)
        
        return violations
