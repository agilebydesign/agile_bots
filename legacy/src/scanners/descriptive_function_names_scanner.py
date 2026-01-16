"""Scanner for validating descriptive function names."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import ast
import re
from .test_scanner import TestScanner
from .violation import Violation
from .resources.ast_elements import Functions


class DescriptiveFunctionNamesScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        functions = Functions(tree)
        for function in functions.get_many_functions:
            if not function.node.name.startswith('test_'):
                violation = self._check_descriptive_name(function.node, file_path, rule_obj)
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _check_descriptive_name(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        func_name_lower = func_node.name.lower()
        func_name_original = func_node.name
        
        # Domain-specific terms that are acceptable (standard interface methods, common patterns)
        # These are well-known domain terms, not vague abbreviations
        acceptable_domain_terms = {
            'scan',  # Standard Scanner interface method
            'scan_test_file',  # TestScanner interface method
            'scan_cross_file',  # Scanner cross-file method
            'parse',  # Common parsing operation
            'render',  # Common rendering operation
            'build',  # Common build operation
            'load',  # Common loading operation
            'save',  # Common saving operation
            'read',  # Common reading operation
            'write',  # Common writing operation
            'get',  # Common getter pattern
            'set',  # Common setter pattern
            'has',  # Common predicate pattern
            'is',  # Common predicate pattern
            'can',  # Common predicate pattern
        }
        
        if func_name_lower in acceptable_domain_terms:
            return None
        
        # Read file content for snippet extraction
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            content = None
        
        # Vague/abbreviated names
        vague_names = ['setup', 'do', 'handle', 'process', 'run', 'main', 'helper', 'util', 'func']
        if func_name_lower in vague_names or len(func_name_lower) < 5:
            line_number = func_node.lineno if hasattr(func_node, 'lineno') else None
            if content:
                return self._create_violation_with_snippet(
                    rule_obj=rule_obj,
                    violation_message=f'Helper function "{func_node.name}" uses vague/abbreviated name - use descriptive name that reveals purpose',
                    file_path=file_path,
                    line_number=line_number,
                    severity='error',
                    content=content,
                    ast_node=func_node,
                    max_lines=3
                )
            else:
                return Violation(
                    rule=rule_obj,
                    violation_message=f'Helper function "{func_node.name}" uses vague/abbreviated name - use descriptive name that reveals purpose',
                    location=str(file_path),
                    line_number=line_number,
                    severity='error'
                ).to_dict()
        
        # Common acceptable abbreviations that should NOT be flagged
        acceptable_abbrevs = {
            'init', 'config', 'json', 'cli', 'mcp', 'dir', 'sync', 'var', 'obj', 
            'param', 'req', 'resp', 'url', 'api', 'http', 'html', 'xml', 'yaml',
            'id', 'db', 'sql', 'ui', 'ux', 'io', 'os', 'env', 'tmp', 'log'
        }
        
        # Split function name into words (by underscore) - use original case for acronym detection
        words_lower = func_name_lower.split('_')
        words_original = func_name_original.split('_')
        
        # Check for actual acronyms (all caps sequences) - these are usually acceptable if well-known
        # But flag if they're cryptic or unclear
        cryptic_acronyms = set()  # Track if we find truly cryptic ones
        
        for word_lower, word_original in zip(words_lower, words_original):
            if word_original.isupper() and len(word_original) >= 2:
                # Well-known acronyms are acceptable
                well_known_acronyms = {'mcp', 'json', 'cli', 'api', 'http', 'html', 'xml', 'yaml', 'sql', 'ui', 'ux', 'io', 'os', 'id', 'db'}
                if word_lower not in well_known_acronyms:
                    cryptic_acronyms.add(word_original)
            
            # Only flag if it's a standalone word (not part of a longer word)
            if len(word_lower) <= 3 and word_lower not in acceptable_abbrevs:
                cryptic_short = ['cfg', 'mgr', 'acct', 'addr', 'cnt', 'cntr', 'ctrl', 'def', 'doc', 'err', 'exc', 'fn', 'fnc', 'hdlr', 'idx', 'len', 'loc', 'max', 'min', 'num', 'opt', 'prm', 'ptr', 'ref', 'ret', 'src', 'str', 'tmp', 'val', 'wrt']
                if word_lower in cryptic_short:
                    cryptic_acronyms.add(word_lower)
        
        # Only flag if we found truly cryptic abbreviations or unknown acronyms
        if cryptic_acronyms:
            line_number = func_node.lineno if hasattr(func_node, 'lineno') else None
            if content:
                return self._create_violation_with_snippet(
                    rule_obj=rule_obj,
                    violation_message=f'Helper function "{func_node.name}" contains cryptic abbreviations or acronyms ({", ".join(cryptic_acronyms)}) - use full descriptive words',
                    file_path=file_path,
                    line_number=line_number,
                    severity='warning',
                    content=content,
                    ast_node=func_node,
                    max_lines=3
                )
            else:
                return Violation(
                    rule=rule_obj,
                    violation_message=f'Helper function "{func_node.name}" contains cryptic abbreviations or acronyms ({", ".join(cryptic_acronyms)}) - use full descriptive words',
                    location=str(file_path),
                    line_number=line_number,
                    severity='warning'
                ).to_dict()
        
        return None

