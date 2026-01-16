"""Scanner that detects direct config access when object model should be used."""
import re
from pathlib import Path
from typing import List, Dict, Any
from .code_scanner import CodeScanner
from .violation import Violation


class PreferObjectModelOverConfigScanner(CodeScanner):
    
    def __init__(self, rule_obj=None):
        super().__init__()
        self.rule_name = "prefer_object_model_over_config"
        self.rule_obj = rule_obj
        
        # Patterns that indicate direct config access from OUTSIDE the class
        # Only flag when accessing _config on objects other than self
        self.config_access_patterns = [
            (r'(?<!self)\._config\[', 'Direct access to _config dictionary'),
            (r'(?<!self)\._config\.get\(', 'Using .get() on _config attribute'),
            (r"hasattr\([^,]+,\s*['\"]_config['\"]", 'Checking for _config attribute existence'),
        ]
        
        # Pattern for reading config files
        self.config_file_pattern = r'read_json_file\([^)]*(?:action_config|behavior_config|bot_config)\.json[^)]*\)'
        
        # Exceptions - locations where config access is acceptable
        self.exception_patterns = [
            r'def __init__\(',  # Constructor
            r'class.*\(.*Config.*\)',  # Config-related classes
            r'def.*load.*config',  # Config loading methods
            r'def.*_load_.*_config',  # Private config loading methods
            r'# scanner ignore',  # Explicit ignore comment
        ]
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Dict[str, Any] = None) -> List[Violation]:
        violations = []
        
        # Use self.rule_obj directly - let code fail if not set
        if not self.rule_obj:
            return violations
        
        # Store file_path for creating violations
        self.current_file_path = file_path
        
        # Read the file content
        if not file_path.exists():
            return violations
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return violations
        
        lines = content.split('\n')
        
        if self._is_exception_file(file_path):
            return violations
        
        for line_num, line in enumerate(lines, start=1):
            # Skip if line has explicit ignore comment
            if '# scanner ignore' in line or '# noqa' in line:
                continue
            
            if self._is_in_exception_context(lines, line_num):
                continue
            
            for pattern, description in self.config_access_patterns:
                if re.search(pattern, line):
                    violations.append(self._create_violation(
                        line_num,
                        f"{description}. Use object properties instead of accessing _config directly."
                    ))
            
            if re.search(self.config_file_pattern, line):
                # Only flag if it looks like we're reading config when an object might exist
                if self._looks_like_object_exists_context(lines, line_num):
                    violations.append(self._create_violation(
                        line_num,
                        "Reading config file directly when object model may exist. Use object properties instead."
                    ))
        
        return violations
    
    def _is_exception_file(self, file_path: Path) -> bool:
        file_str = str(file_path).lower()
        exception_paths = [
            'config',
            'loader',
            'factory',
            'migration',
            'setup',
            'generator',
            '__init__.py',
        ]
        return any(exc in file_str for exc in exception_paths)
    
    def _is_in_exception_context(self, lines: List[str], current_line: int) -> bool:
        # Look backwards to find the current function/method definition
        # We need to check if we're INSIDE an exception function, not just if one exists nearby
        current_indent = len(lines[current_line - 1]) - len(lines[current_line - 1].lstrip())
        
        # Look backwards to find the function definition at same or lower indentation
        for i in range(current_line - 2, max(0, current_line - 50), -1):
            line = lines[i]
            line_indent = len(line) - len(line.lstrip())
            
            # Found a function/method definition at same or lower indentation
            if line_indent <= current_indent and ('def ' in line):
                for pattern in self.exception_patterns:
                    if re.search(pattern, line):
                        return True
                # Found the enclosing function, and it's not an exception
                return False
        
        return False
    
    def _looks_like_object_exists_context(self, lines: List[str], current_line: int) -> bool:
        # Look at surrounding lines for object access patterns
        start = max(0, current_line - 5)
        end = min(len(lines), current_line + 5)
        context = '\n'.join(lines[start:end])
        
        # Patterns that suggest object model exists
        object_patterns = [
            r'\.find_by_name\(',
            r'\.behaviors\.',
            r'\.actions\.',
            r'for \w+ in \w+\.behaviors',
            r'for \w+ in \w+\.actions',
            r'behavior\s*=',
            r'action\s*=',
        ]
        
        return any(re.search(pattern, context) for pattern in object_patterns)
    
    def _create_violation(self, line_num: int, message: str) -> Violation:
        return Violation(
            rule=self.rule_obj,
            violation_message=message,
            location=str(self.current_file_path),
            line_number=line_num,
            severity='error'
        )

