"""Scanner for detecting code duplication (DRY principle)."""

from typing import List, Dict, Any, Optional, Tuple, Set
from pathlib import Path
import ast
from datetime import datetime
import logging
from .code_scanner import CodeScanner
from .violation import Violation
import hashlib
from difflib import SequenceMatcher
import json

logger = logging.getLogger(__name__)

# Timeout for individual file scans (seconds)
FILE_SCAN_TIMEOUT = 60  # 60 seconds per file max


def _safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Convert arguments to ASCII-safe strings
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Replace problematic Unicode characters with ASCII equivalents
                safe_str = arg.encode('ascii', errors='replace').decode('ascii')
                safe_args.append(safe_str)
            else:
                safe_args.append(str(arg))
        print(*safe_args, **kwargs)


class DuplicationScanner(CodeScanner):
    
    SCANNER_VERSION = "1.0"
    
    def _get_cache_dir(self, file_path: Optional[Path] = None) -> Path:
        if file_path:
            current = file_path.parent
            while current and current.parent != current:
                if (current / '.git').exists() or (current / 'pyproject.toml').exists() or (current / 'setup.py').exists():
                    cache_dir = current / '.cache' / 'duplication_blocks'
                    break
                current = current.parent
            else:
                import tempfile
                cache_dir = Path(tempfile.gettempdir()) / 'agile_bot_cache' / 'duplication_blocks'
        else:
            import tempfile
            cache_dir = Path(tempfile.gettempdir()) / 'agile_bot_cache' / 'duplication_blocks'
        
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    def _get_file_cache_key(self, file_path: Path) -> Optional[str]:
        try:
            mtime = file_path.stat().st_mtime
            file_size = file_path.stat().st_size
            key_data = f"{file_path}:{mtime}:{file_size}:{self.SCANNER_VERSION}"
            return hashlib.md5(key_data.encode()).hexdigest()
        except Exception:
            return None
    
    def _load_blocks_from_cache(self, file_path: Path) -> Optional[List[Dict]]:
        cache_key = self._get_file_cache_key(file_path)
        if not cache_key:
            return None
        
        cache_file = self._get_cache_dir(file_path) / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                return cached_data.get('blocks', [])
        except Exception as e:
            logger.debug(f"Cache read failed for {file_path}: {e}")
            return None
    
    def _save_blocks_to_cache(self, file_path: Path, blocks: List[Dict]):
        cache_key = self._get_file_cache_key(file_path)
        if not cache_key:
            return
        
        cache_file = self._get_cache_dir(file_path) / f"{cache_key}.json"
        
        try:
            serializable_blocks = []
            for block in blocks:
                serializable_block = {k: v for k, v in block.items() if k not in ('ast_nodes', 'file_path', 'lines')}
                serializable_blocks.append(serializable_block)
            
            cache_data = {
                'file_path': str(file_path),
                'cached_at': datetime.now().isoformat(),
                'blocks': serializable_blocks
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            logger.debug(f"Cache write failed for {file_path}: {e}")
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, knowledge_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        _safe_print(f"[DuplicationScanner.scan_code_file] Called for: {file_path}")
        
        if not file_path.exists():
            _safe_print(f"[DuplicationScanner.scan_code_file] File does not exist: {file_path}")
            return violations
        
        # Track time for timeout detection
        file_start_time = datetime.now()
        
        try:
            file_size = file_path.stat().st_size
            if file_size > 500_000:  # Skip files larger than 500KB
                _safe_print(f"Skipping large file ({file_size/1024:.1f}KB): {file_path}")
                return violations
        except Exception as e:
            _safe_print(f"Could not check file size for {file_path}: {e}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            lines = content.split('\n')
            
            functions = []
            
            def extract_functions_from_node(node: ast.AST, parent_class: str = None):
                if isinstance(node, ast.ClassDef):
                    # Found a class - extract its methods
                    for child in node.body:
                        extract_functions_from_node(child, node.name)
                elif isinstance(node, ast.FunctionDef):
                    # Found a function - extract it with class context
                    func_body = ast.unparse(node.body) if hasattr(ast, 'unparse') else str(node.body)
                    functions.append((node.name, func_body, node.lineno, node, parent_class))
            
            for node in tree.body:
                extract_functions_from_node(node, None)
            
            func_violations = self._check_duplicate_functions(functions, file_path, rule_obj, lines)
            violations.extend(func_violations)
            
            elapsed = (datetime.now() - file_start_time).total_seconds()
            if elapsed > FILE_SCAN_TIMEOUT:
                _safe_print(f"TIMEOUT: File scan exceeded {FILE_SCAN_TIMEOUT}s: {file_path} (stopping early)")
                return violations
            
            block_violations = self._check_duplicate_code_blocks(functions, lines, file_path, rule_obj)
            violations.extend(block_violations)
            
            file_elapsed = (datetime.now() - file_start_time).total_seconds()
            if file_elapsed > FILE_SCAN_TIMEOUT:
                _safe_print(f"VERY SLOW scan: {file_path} took {file_elapsed:.1f}s (exceeded {FILE_SCAN_TIMEOUT}s threshold)")
            elif file_elapsed > 10:
                _safe_print(f"Slow scan: {file_path} took {file_elapsed:.1f}s")
            
            # Log detailed information if violations found
            if violations:
                _safe_print(f"[DUPLICATION SCANNER] Found {len(violations)} violations in {file_path}")
                _safe_print(f"[DUPLICATION SCANNER] Violations: {[v.get('violation_message', '')[:100] for v in violations]}")
                self._log_violation_details(file_path, violations, lines)
            else:
                _safe_print(f"[DUPLICATION SCANNER] No violations found in {file_path}")
            
            return violations
        
        except (SyntaxError, UnicodeDecodeError) as e:
            # Skip files with syntax errors - these are expected and not scanner errors
            _safe_print(f"Skipping file with syntax/encoding error: {file_path}: {e}")
            return violations
        except Exception as e:
            # Unexpected errors should bubble up - log and re-raise
            file_elapsed = (datetime.now() - file_start_time).total_seconds()
            import traceback
            _safe_print(f"Unexpected error scanning {file_path} after {file_elapsed:.1f}s: {e}")
            traceback.print_exc()
            raise  # Re-raise to let validation framework handle it
    
    def _check_duplicate_functions(self, functions: List[tuple], file_path: Path, rule_obj: Any, lines: List[str] = None) -> List[Dict[str, Any]]:
        violations = []
        
        # Group functions by body hash
        body_hashes = {}
        for func_tuple in functions:
            func_name, func_body, line_num, node, class_name = func_tuple
            body_hash = hashlib.md5(func_body.encode()).hexdigest()
            if body_hash not in body_hashes:
                body_hashes[body_hash] = []
            body_hashes[body_hash].append((func_name, line_num, node, class_name))
        
        # Find duplicates
        for body_hash, func_list in body_hashes.items():
            if len(func_list) > 1:
                # Multiple functions with same body - check if this is legitimate duplication
                func_names = [f[0] for f in func_list]
                func_nodes = [f[2] for f in func_list]
                class_names = [f[3] for f in func_list]
                line_numbers = [f[1] for f in func_list]
                
                # Skip if these are interface methods in different classes (legitimate duplication)
                if self._are_interface_methods(func_names, class_names, func_nodes):
                    continue
                
                # Skip if these are simple property getters (legitimate boilerplate)
                if all(self._is_simple_property(node) for node in func_nodes):
                    continue
                
                # Skip if these are all simple delegation/wrapper methods (legitimate design pattern)
                # This catches cases like format_directive, format_header, format_workflow_status_header
                # which are intentional wrappers that delegate to other methods
                if all(self._is_simple_delegation(node) for node in func_nodes):
                    continue
                
                # Multiple functions with same body
                # No code snippet for duplicate function violations
                violation = Violation(
                    rule=rule_obj,
                    violation_message=f'Duplicate code detected: functions {", ".join(func_names)} have identical bodies - extract to shared function',
                    location=str(file_path),
                    line_number=line_numbers[0],
                    severity='error'
                ).to_dict()
                violations.append(violation)
        
        return violations
    
    def _are_interface_methods(self, func_names: List[str], class_names: List[Any], func_nodes: List[ast.FunctionDef]) -> bool:
        if all(name.startswith('__') and name.endswith('__') for name in func_names):
            # If they're in different classes, they're interface implementations
            unique_classes = set(c for c in class_names if c is not None)
            if len(unique_classes) > 1:
                return True
            # If same class, check if it's a simple property getter pattern
            if len(func_names) == 1 and func_names[0] == '__str__':
                # __str__ that just returns self.name is a common pattern
                return True
        
        # This is common for interface implementations (e.g., children property in node classes)
        if all(self._is_simple_property_getter(node) for node in func_nodes):
            # If they're in different classes, they're interface implementations
            unique_classes = set(c for c in class_names if c is not None)
            if len(unique_classes) > 1:
                return True
        
        # This suggests interface implementation
        if len(set(func_names)) == 1:  # All have same name
            unique_classes = set(c for c in class_names if c is not None)
            if len(unique_classes) > 1:
                # Same method name in different classes - likely interface
                if all(self._is_simple_delegation(node) for node in func_nodes):
                    return True
        
        return False
    
    def _is_simple_delegation(self, func_node: ast.FunctionDef) -> bool:
        if self._is_simple_property_getter(func_node):
            return True
        
        # Check if it's a simple method that just returns self.attr.method() or self.attr[item]
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        if len(executable_body) == 1:
            stmt = executable_body[0]
            if isinstance(stmt, ast.Return) and stmt.value:
                if isinstance(stmt.value, (ast.Call, ast.Subscript)):
                    # Method call or subscript - check if it's on self.attribute
                    if isinstance(stmt.value, ast.Call):
                        if isinstance(stmt.value.func, ast.Attribute):
                            if isinstance(stmt.value.func.value, ast.Name) and stmt.value.func.value.id == 'self':
                                return True  # self.method() - simple wrapper
                            elif isinstance(stmt.value.func.value, ast.Attribute):
                                if isinstance(stmt.value.func.value.value, ast.Name) and stmt.value.func.value.value.id == 'self':
                                    return True  # self.attr.method()
                            # Also check for static/class method calls: ClassName.method() or ClassName.attr.method()
                            elif isinstance(stmt.value.func.value, ast.Name):
                                # Static method call: ClassName.method() - legitimate delegation
                                return True
                    elif isinstance(stmt.value, ast.Subscript):
                        if isinstance(stmt.value.value, ast.Attribute):
                            if isinstance(stmt.value.value.value, ast.Name) and stmt.value.value.value.id == 'self':
                                return True  # self.attr[key]
                # Also check self.attr directly
                elif isinstance(stmt.value, ast.Attribute):
                    if isinstance(stmt.value.value, ast.Name) and stmt.value.value.id == 'self':
                        return True  # self.attr
        
        return False
    
    def _is_simple_property_getter(self, func_node: ast.FunctionDef) -> bool:
        is_property = False
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                is_property = True
                break
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ('setter', 'deleter'):
                    # Setter/deleter, check if it's simple
                    pass
                elif hasattr(decorator, 'value') and isinstance(decorator.value, ast.Name):
                    if decorator.value.id == 'property':
                        is_property = True
                        break
        
        if not is_property:
            # (not decorated but simple return)
            if len(func_node.body) <= 2:  # docstring + return
                for stmt in func_node.body:
                    if isinstance(stmt, ast.Return):
                        if isinstance(stmt.value, ast.Attribute):
                            if isinstance(stmt.value.value, ast.Name) and stmt.value.value.id == 'self':
                                return True
        
        # For properties, check if body is just return self._attribute
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        if len(executable_body) == 1:
            stmt = executable_body[0]
            if isinstance(stmt, ast.Return):
                if isinstance(stmt.value, ast.Attribute):
                    if isinstance(stmt.value.value, ast.Name) and stmt.value.value.id == 'self':
                        return True
                # Also check for simple expressions like self._children
                if isinstance(stmt.value, ast.Name):
                    # Returning a name (could be self.name or similar)
                    return True
        
        return False
    
    def _check_duplicate_code_blocks(self, functions: List[tuple], lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        all_blocks = []
        for func_tuple in functions:
            func_name, func_body, func_line, func_node, _ = func_tuple
            blocks = self._extract_code_blocks(func_node, func_line, func_name)
            all_blocks.extend(blocks)
        
        # Use similarity checking to find duplicate blocks
        SIMILARITY_THRESHOLD = 0.90  # Increased to 90% to reduce false positives
        
        # Debug: track comparison attempts
        comparison_count = 0
        similarity_scores = []
        
        # Track duplicate pairs and build groups using union-find approach
        duplicate_pairs = []  # List of (block1_idx, block2_idx, similarity) tuples
        reported_block_indices = set()  # Track which blocks have been reported
        
        _safe_print(f"[DuplicationScanner] Extracted {len(all_blocks)} blocks from {len(functions)} functions")
        
        # Compare all blocks pairwise
        compared_pairs = set()
        for i, block1 in enumerate(all_blocks):
            for j, block2 in enumerate(all_blocks[i+1:], start=i+1):
                # Skip if same block
                if i == j:
                    continue
                
                # Skip if already compared
                pair_key = tuple(sorted([i, j]))
                if pair_key in compared_pairs:
                    continue
                compared_pairs.add(pair_key)
                
                # Skip if blocks overlap significantly (same function, overlapping line ranges)
                # This prevents comparing overlapping blocks from the same function
                if (block1['func_name'] == block2['func_name'] and 
                    not (block1['end_line'] < block2['start_line'] or block2['end_line'] < block1['start_line'])):
                    continue
                
                # Calculate AST-level similarity (more accurate than string comparison)
                try:
                    ast_similarity = self._compare_ast_blocks(block1['ast_nodes'], block2['ast_nodes'])
                except Exception as e:
                    _safe_print(f"Error comparing AST blocks: {e}")
                    ast_similarity = 0.0
                
                # Also check normalized structure similarity
                try:
                    normalized_similarity = SequenceMatcher(None, block1['normalized'], block2['normalized']).ratio()
                except Exception as e:
                    _safe_print(f"Error comparing normalized blocks: {e}")
                    normalized_similarity = 0.0
                
                try:
                    preview1_normalized = ' '.join(block1['preview'].split())
                    preview2_normalized = ' '.join(block2['preview'].split())
                    content_similarity = SequenceMatcher(None, preview1_normalized, preview2_normalized).ratio()
                except Exception as e:
                    _safe_print(f"Error comparing content blocks: {e}")
                    content_similarity = 0.0
                
                # Use AST similarity as primary indicator (it ignores variable names)
                # Content similarity is secondary - lower threshold since variable names differ
                # If AST similarity is high (>= 85%), accept even with lower content similarity (>= 50%)
                # Otherwise require both to be reasonably high
                max_similarity = 0.0
                if ast_similarity >= 0.85 and content_similarity >= 0.50:
                    max_similarity = max(ast_similarity, content_similarity)
                elif ast_similarity >= 0.80 and content_similarity >= 0.70:
                    max_similarity = max(ast_similarity, content_similarity)
                elif max(ast_similarity, content_similarity) >= 0.90 and min(ast_similarity, content_similarity) >= 0.60:
                    max_similarity = max(ast_similarity, content_similarity)
                elif ast_similarity >= SIMILARITY_THRESHOLD:
                    # If AST similarity alone meets threshold, use it (AST is more reliable for structural duplication)
                    max_similarity = ast_similarity
                else:
                    # If both aren't reasonably high, skip this comparison
                    similarity_scores.append((ast_similarity, content_similarity, max(ast_similarity, content_similarity)))
                    continue
                
                similarity_scores.append((ast_similarity, content_similarity, max_similarity))
                
                if max_similarity >= SIMILARITY_THRESHOLD:
                    # Similar blocks found - check if they should be reported
                    # Skip if EITHER block is an interface method - interface implementations are legitimate, not duplication
                    if self._is_interface_method(block1['func_name']) or self._is_interface_method(block2['func_name']):
                        continue
                    
                    # Skip if EITHER block is mostly helper calls - that's intended reuse, not duplication
                    if self._is_mostly_helper_calls(block1['ast_nodes']) or self._is_mostly_helper_calls(block2['ast_nodes']):
                        continue
                    
                    # Skip if BOTH functions are helper functions - helper functions are meant to encapsulate patterns
                    # Finding similar patterns in helpers is expected, not duplication
                    if self._is_helper_function(block1['func_name']) and self._is_helper_function(block2['func_name']):
                        continue
                    
                    # Skip if blocks operate on different domain entities - legitimate separate implementations
                    # This prevents flagging similar CRUD operations on different entities as duplication
                    if self._operates_on_different_domains(block1, block2):
                        continue
                    
                    # Skip if blocks are structurally similar but call different methods
                    # This catches cases like lines.extend(builder.method1()) vs lines.extend(builder.method2())
                    # which are legitimate structural patterns, not duplication
                    if self._calls_different_methods(block1['ast_nodes'], block2['ast_nodes']):
                        continue
                    
                    # Only report if blocks are in different functions or far apart in same function
                    should_report = False
                    
                    if block1['func_name'] != block2['func_name']:
                        # Different functions - report as potential duplication
                        should_report = True
                    elif abs(block1['start_line'] - block2['start_line']) > 10:
                        # Same function but far apart - report as potential duplication
                        should_report = True
                    
                    if should_report:
                        duplicate_pairs.append((i, j, max_similarity))
                        _safe_print(f"[DuplicationScanner] Found duplicate pair: block {i} (line {block1['start_line']}) vs block {j} (line {block2['start_line']}), similarity={max_similarity:.2f}")
        
        _safe_print(f"[DuplicationScanner] Compared {comparison_count} block pairs")
        _safe_print(f"[DuplicationScanner] Found {len(duplicate_pairs)} duplicate pairs (threshold: {SIMILARITY_THRESHOLD})")
        if similarity_scores:
            top_scores = sorted(similarity_scores, key=lambda x: x[2], reverse=True)[:10]
            _safe_print(f"[DuplicationScanner] Top similarity scores: {[(f'{a:.2f}', f'{c:.2f}', f'{m:.2f}') for a, c, m in top_scores]}")
        
        # Map each block to its group representative
        group_repr = list(range(len(all_blocks)))  # Initially each block is its own representative
        
        def find(x):
            if group_repr[x] != x:
                group_repr[x] = find(group_repr[x])  # Path compression
            return group_repr[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                group_repr[root_y] = root_x  # Union by making root_x the parent
        
        # Union all duplicate pairs
        for i, j, _ in duplicate_pairs:
            union(i, j)
        
        # Group blocks by their representative
        groups = {}
        for idx in range(len(all_blocks)):
            root = find(idx)
            if root not in groups:
                groups[root] = []
            groups[root].append(idx)
        
        # Merge groups that represent the same duplication (same function pairs with overlapping ranges)
        # This prevents reporting the same duplication multiple times with different block boundaries
        merged_groups = {}
        group_keys = list(groups.keys())
        
        for i, root_idx in enumerate(group_keys):
            if root_idx in merged_groups:
                continue  # Already merged into another group
            
            group_blocks = [all_blocks[idx] for idx in groups[root_idx]]
            func_pairs = set()
            for block in group_blocks:
                func_pairs.add(block['func_name'])
            
            merged_with = root_idx
            for j, other_root_idx in enumerate(group_keys[i+1:], start=i+1):
                if other_root_idx in merged_groups:
                    continue
                
                other_blocks = [all_blocks[idx] for idx in groups[other_root_idx]]
                other_func_pairs = set()
                for block in other_blocks:
                    other_func_pairs.add(block['func_name'])
                
                # If they share function pairs, check for overlapping ranges
                if func_pairs == other_func_pairs:
                    overlaps = False
                    for block1 in group_blocks:
                        for block2 in other_blocks:
                            if (block1['func_name'] == block2['func_name'] and
                                not (block1['end_line'] < block2['start_line'] or 
                                     block2['end_line'] < block1['start_line'])):
                                overlaps = True
                                break
                        if overlaps:
                            break
                    
                    if overlaps:
                        # Merge into the first group
                        groups[merged_with].extend(groups[other_root_idx])
                        merged_groups[other_root_idx] = merged_with
            
            merged_groups[root_idx] = merged_with
        
        # Consolidate groups after merging
        final_groups = {}
        for root_idx, block_indices in groups.items():
            merged_root = merged_groups.get(root_idx, root_idx)
            if merged_root not in final_groups:
                final_groups[merged_root] = []
            final_groups[merged_root].extend(block_indices)
        
        for root_idx in final_groups:
            final_groups[root_idx] = list(set(final_groups[root_idx]))
        
        _safe_print(f"[DuplicationScanner] Built {len(final_groups)} duplicate groups")
        
        # Report each duplicate group once
        for root_idx, block_indices in final_groups.items():
            # Skip groups with only one block (no duplicates)
            if len(block_indices) < 2:
                _safe_print(f"[DuplicationScanner] Skipping group {root_idx}: only {len(block_indices)} block(s)")
                continue
            
            # Skip if all blocks in this group have already been reported
            if all(idx in reported_block_indices for idx in block_indices):
                continue
            
            group_blocks = [all_blocks[idx] for idx in sorted(block_indices)]
            
            # Filter out overlapping blocks from the same function
            # Keep only the largest non-overlapping blocks per function
            filtered_blocks = []
            blocks_by_func = {}
            
            # Group blocks by function
            for block in group_blocks:
                func_name = block['func_name']
                if func_name not in blocks_by_func:
                    blocks_by_func[func_name] = []
                blocks_by_func[func_name].append(block)
            
            # For each function, keep only non-overlapping blocks (prefer larger blocks)
            for func_name, func_blocks in blocks_by_func.items():
                # Sort by size (largest first), then by start line
                func_blocks.sort(key=lambda b: (b['end_line'] - b['start_line'], -b['start_line']), reverse=True)
                
                non_overlapping = []
                for block in func_blocks:
                    overlaps = False
                    for selected in non_overlapping:
                        if not (block['end_line'] < selected['start_line'] or selected['end_line'] < block['start_line']):
                            overlaps = True
                            break
                    if not overlaps:
                        non_overlapping.append(block)
                
                filtered_blocks.extend(non_overlapping)
            
            # Skip if filtering removed all blocks
            if len(filtered_blocks) < 2:
                _safe_print(f"[DuplicationScanner] Skipping group {root_idx}: filtering reduced to {len(filtered_blocks)} block(s)")
                continue
            
            _safe_print(f"[DuplicationScanner] Reporting duplicate group: {len(filtered_blocks)} blocks")
            
            # Use the first block as the primary one for reporting
            primary_block = filtered_blocks[0]
            
            previews = []
            for block in filtered_blocks:
                location = f"{block['func_name']}:{block['start_line']}-{block['end_line']}"
                preview = block['preview'][:200] + '...' if len(block['preview']) > 200 else block['preview']
                previews.append(f"Location ({location}):\n```python\n{preview}\n```")
            
            violation_message = (
                f'Duplicate code blocks detected ({len(filtered_blocks)} locations) - extract to helper function.\n\n' +
                '\n\n'.join(previews)
            )
            
            # No code snippet for duplicate block violations (previews already included in message)
            violation = Violation(
                rule=rule_obj,
                violation_message=violation_message,
                location=str(file_path),
                line_number=primary_block['start_line'],
                severity='error'
            ).to_dict()
            violations.append(violation)
            
            # Mark all blocks in this group as reported
            reported_block_indices.update(block_indices)
        
        _safe_print(f"[DuplicationScanner._check_duplicate_code_blocks] Returning {len(violations)} violations")
        return violations
    
    def _extract_code_blocks(self, func_node: ast.FunctionDef, func_start_line: int, func_name: str) -> List[Dict[str, Any]]:
        blocks = []
        MIN_NODES = 5  # Minimum AST nodes for a meaningful subtree
        MAX_NODES = 80  # Maximum nodes to avoid overly large blocks
        MIN_LINES = 5  # Minimum lines of code
        MAX_LINES = 20  # Maximum lines (goldilocks zone)
        
        # Skip blocks in test methods - test structure similarity is expected, not duplication
        if func_name.startswith('test_'):
            return blocks
        
        # Skip interface methods - these are legitimate interface implementations, not duplication
        # Interface methods like __getitem__, __contains__, items, keys are required by protocols
        # and should be implemented consistently across classes, not flagged as duplication
        if self._is_interface_method(func_name):
            return blocks
        
        # Skip simple property methods (getters/setters) - these are legitimate boilerplate
        if self._is_simple_property(func_node):
            return blocks
        
        # Skip simple constructors that only set instance variables - legitimate boilerplate
        if self._is_simple_constructor(func_node):
            return blocks
        
        # These are nodes with bodies: functions, loops, conditionals, try blocks, etc.
        subtrees = self._extract_subtrees_from_function(func_node, MIN_NODES, MAX_NODES)
        
        for subtree in subtrees:
            start_line = subtree.lineno if hasattr(subtree, 'lineno') else func_start_line
            end_line = subtree.end_lineno if hasattr(subtree, 'end_lineno') and subtree.end_lineno else start_line
            
            total_lines = end_line - start_line + 1
            if total_lines < MIN_LINES or total_lines > MAX_LINES:
                continue
            
            if not hasattr(subtree, 'body') or not isinstance(subtree.body, list):
                continue
            
            block_statements = [stmt for stmt in subtree.body if not self._is_docstring_or_comment(stmt, func_node)]
            
            if not block_statements:
                continue
            
            # Skip if block contains only docstrings or comments
            if all(self._is_docstring_or_comment(s, func_node) for s in block_statements):
                continue
            
            # Skip if block is just sequences of helper function calls
            if self._is_only_helper_calls(block_statements):
                continue
            
            # Skip if block is mostly helper calls with minimal actual implementation
            if self._is_mostly_helper_calls(block_statements):
                continue
            
            # Skip if block is mostly assertions - test assertions are expected to be similar
            if self._is_mostly_assertions(block_statements):
                continue
            
            # Skip if block follows test pattern (helper calls + assertions) - that's legitimate test structure
            if self._is_test_pattern(block_statements):
                continue
            
            # Skip if block is a list-building pattern (sequences of lines.extend()/append() calls)
            # This is a legitimate pattern for building output lists, not duplication
            if self._is_list_building_pattern(block_statements):
                continue
            
            # Skip blocks with fewer than 3 actual code statements (one-liners and trivial blocks)
            actual_code_count = self._count_actual_code_statements(block_statements)
            if actual_code_count < 3:
                continue
            
            # Normalize block (remove variable names, keep structure)
            normalized = self._normalize_block(block_statements)
            if not normalized:
                continue
            
            preview = self._get_block_preview(block_statements)
            
            blocks.append({
                'hash': hashlib.md5(normalized.encode()).hexdigest(),
                'start_line': start_line,
                'end_line': end_line,
                'func_name': func_name,
                'preview': preview,
                'normalized': normalized,
                'ast_nodes': block_statements  # Store AST nodes for comparison
            })
        
        # Also extract sequences of statements from the function body itself
        # This catches patterns that aren't wrapped in control structures
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        
        # Extract sequences of 5-10 consecutive statements (sliding window for non-control patterns)
        for block_size in range(5, min(11, len(executable_body) + 1)):
            for i in range(len(executable_body) - block_size + 1):
                block_statements = executable_body[i:i+block_size]
                
                # Skip if this is already covered by a subtree
                # (e.g., if all statements are part of a single if/for block)
                if self._is_contained_in_subtree(block_statements, subtrees):
                    continue
                
                # Apply same filters as subtrees
                if all(self._is_docstring_or_comment(s, func_node) for s in block_statements):
                    continue
                if self._is_only_helper_calls(block_statements):
                    continue
                if self._is_mostly_helper_calls(block_statements):
                    continue
                if self._is_mostly_assertions(block_statements):
                    continue
                if self._is_test_pattern(block_statements):
                    continue
                
                # Skip blocks with fewer than 3 actual code statements (one-liners and trivial blocks)
                actual_code_count = self._count_actual_code_statements(block_statements)
                if actual_code_count < 3:
                    continue
                
                start_line = block_statements[0].lineno if hasattr(block_statements[0], 'lineno') else func_start_line
                end_line = block_statements[-1].end_lineno if hasattr(block_statements[-1], 'end_lineno') else (
                    block_statements[-1].lineno if hasattr(block_statements[-1], 'lineno') else start_line
                )
                
                total_lines = end_line - start_line + 1
                if total_lines < MIN_LINES or total_lines > MAX_LINES:
                    continue
                
                normalized = self._normalize_block(block_statements)
                if not normalized:
                    continue
                
                preview = self._get_block_preview(block_statements)
                
                blocks.append({
                    'hash': hashlib.md5(normalized.encode()).hexdigest(),
                    'start_line': start_line,
                    'end_line': end_line,
                    'func_name': func_name,
                    'preview': preview,
                    'normalized': normalized,
                    'ast_nodes': block_statements
                })
        
        return blocks
    
    def _extract_subtrees_from_function(self, func_node: ast.FunctionDef, min_nodes: int, max_nodes: int) -> List[ast.AST]:
        subtrees = []
        
        # Control structures that represent semantic units
        control_structures = (ast.If, ast.For, ast.While, ast.Try, ast.With, 
                             ast.AsyncFor, ast.AsyncWith)
        
        def extract_from_node(node):
            if isinstance(node, control_structures):
                # Count nodes in this subtree
                num_nodes = len(list(ast.walk(node)))
                if min_nodes <= num_nodes <= max_nodes:
                    subtrees.append(node)
            
            if hasattr(node, 'body') and isinstance(node.body, list):
                for child in node.body:
                    extract_from_node(child)
            
            if hasattr(node, 'orelse') and isinstance(node.orelse, list):
                for child in node.orelse:
                    extract_from_node(child)
            
            if hasattr(node, 'handlers') and isinstance(node.handlers, list):
                for handler in node.handlers:
                    if hasattr(handler, 'body') and isinstance(handler.body, list):
                        for child in handler.body:
                            extract_from_node(child)
            
            if hasattr(node, 'finalbody') and isinstance(node.finalbody, list):
                for child in node.finalbody:
                    extract_from_node(child)
        
        # Start extracting from function body
        for stmt in func_node.body:
            extract_from_node(stmt)
        
        return subtrees
    
    def _is_contained_in_subtree(self, block_statements: List[ast.stmt], subtrees: List[ast.AST]) -> bool:
        if not block_statements or not subtrees:
            return False
        
        block_start = block_statements[0].lineno if hasattr(block_statements[0], 'lineno') else 0
        block_end = block_statements[-1].end_lineno if hasattr(block_statements[-1], 'end_lineno') else block_start
        
        for subtree in subtrees:
            subtree_start = subtree.lineno if hasattr(subtree, 'lineno') else 0
            subtree_end = subtree.end_lineno if hasattr(subtree, 'end_lineno') else subtree_start
            
            if subtree_start <= block_start and block_end <= subtree_end:
                return True
        
        return False
    
    def _get_statement_end_line(self, stmt: ast.stmt) -> int:
        if hasattr(stmt, 'end_lineno') and stmt.end_lineno:
            return stmt.end_lineno
        
        # For control structures, find the end of their body
        if isinstance(stmt, ast.If):
            end_line = stmt.lineno
            if stmt.body:
                end_line = max(end_line, self._get_body_end_line(stmt.body))
            if stmt.orelse:
                end_line = max(end_line, self._get_body_end_line(stmt.orelse))
            return end_line
        elif isinstance(stmt, (ast.For, ast.While, ast.AsyncFor)):
            end_line = stmt.lineno
            if stmt.body:
                end_line = max(end_line, self._get_body_end_line(stmt.body))
            if stmt.orelse:
                end_line = max(end_line, self._get_body_end_line(stmt.orelse))
            return end_line
        elif isinstance(stmt, ast.Try):
            end_line = stmt.lineno
            if stmt.body:
                end_line = max(end_line, self._get_body_end_line(stmt.body))
            if stmt.orelse:
                end_line = max(end_line, self._get_body_end_line(stmt.orelse))
            if stmt.finalbody:
                end_line = max(end_line, self._get_body_end_line(stmt.finalbody))
            for handler in stmt.handlers:
                if handler.body:
                    end_line = max(end_line, self._get_body_end_line(handler.body))
            return end_line
        elif isinstance(stmt, (ast.With, ast.AsyncWith)):
            end_line = stmt.lineno
            if stmt.body:
                end_line = max(end_line, self._get_body_end_line(stmt.body))
            return end_line
        
        # Default: use lineno if end_lineno not available
        return stmt.lineno if hasattr(stmt, 'lineno') else 0
    
    def _get_body_end_line(self, body: List[ast.stmt]) -> int:
        if not body:
            return 0
        end_line = 0
        for stmt in body:
            stmt_end = self._get_statement_end_line(stmt)
            end_line = max(end_line, stmt_end)
        return end_line
    
    def _is_docstring_or_comment(self, stmt: ast.stmt, func_node: ast.FunctionDef = None) -> bool:
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            if isinstance(stmt.value.value, str):
                # If we have the function node, check if this is the first statement (docstrings are always first)
                if func_node and func_node.body and func_node.body[0] is stmt:
                    return True
                # Also check for common docstring patterns (Args:, Returns:, etc.)
                value_str = stmt.value.value.strip()
                if any(pattern in value_str for pattern in ['Args:', 'Returns:', 'Raises:', 'Yields:', 'Note:', 'Example:']):
                    return True
                if '\n' in value_str:
                    return True
        if isinstance(stmt, ast.Pass):
            return True
        return False
    
    def _is_mostly_helper_calls(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        helper_count = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
            
            is_helper = False
            
            if isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call):
                    func_name = self._get_function_name(stmt.value.func)
                    if func_name:
                        is_helper = any(func_name.startswith(pattern) for pattern in [
                            'given_', 'when_', 'then_',
                            'create_', 'build_', 'make_', 'generate_',
                            'verify_', 'assert_', 'check_', 'ensure_',
                            'setup_', 'bootstrap_', 'initialize_',
                            'get_', 'load_', 'fetch_'
                        ])
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = self._get_function_name(stmt.value.func)
                if func_name:
                    is_helper = any(func_name.startswith(pattern) for pattern in [
                        'given_', 'when_', 'then_',
                        'create_', 'build_', 'make_', 'generate_',
                        'verify_', 'assert_', 'check_', 'ensure_',
                        'setup_', 'bootstrap_', 'initialize_',
                        'get_', 'load_', 'fetch_'
                    ])
            elif isinstance(stmt, ast.Assert):
                # Assertions are verification, not duplication
                is_helper = True
            
            if is_helper:
                helper_count += 1
        
        if total_count == 0:
            return True  # All docstrings/comments
        
        # If >= 60% are helper calls, consider it mostly helpers
        return (helper_count / total_count) >= 0.6
    
    def _is_only_helper_calls(self, statements: List[ast.stmt]) -> bool:
        helper_patterns = [
            'given_', 'when_', 'then_',
            'create_', 'build_', 'make_', 'generate_',
            'verify_', 'assert_', 'check_', 'ensure_',
            'setup_', 'bootstrap_', 'initialize_',
            'get_', 'load_', 'fetch_'
        ]
        
        for stmt in statements:
            if isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call):
                    func_name = self._get_function_name(stmt.value.func)
                    if func_name:
                        if not self._check_helper_pattern_match(func_name, helper_patterns):
                            # Not a helper call - this is actual implementation
                            return False
                else:
                    # Assignment but not from function call - could be duplication
                    return False
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # Expression statement with function call (no assignment)
                func_name = self._get_function_name(stmt.value.func)
                if func_name:
                    if not self._check_helper_pattern_match(func_name, helper_patterns):
                        return False
            elif isinstance(stmt, ast.Assert):
                # Assertions are fine - they're verification, not duplication
                continue
            else:
                # Other statement types - could be duplication
                return False
        
        # All statements are helper calls - not duplication
        return True
    
    def _check_helper_pattern_match(self, func_name: str, helper_patterns: List[str]) -> bool:
        return any(func_name.startswith(pattern) for pattern in helper_patterns)
    
    def _get_function_name(self, func_node: ast.expr) -> Optional[str]:
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            # Method call or module.function
            return func_node.attr
        return None
    
    def _is_helper_function(self, func_name: str) -> bool:
        helper_patterns = [
            'given_', 'when_', 'then_',
            'create_', 'build_', 'make_', 'generate_',
            'verify_', 'assert_', 'check_', 'ensure_',
            'setup_', 'bootstrap_', 'initialize_',
            'get_', 'load_', 'fetch_'
        ]
        return any(func_name.startswith(pattern) for pattern in helper_patterns)
    
    def _is_interface_method(self, func_name: str) -> bool:
        # Magic methods (dunder methods) - these are interface requirements
        if func_name.startswith('__') and func_name.endswith('__'):
            return True
        
        # Common protocol/interface method names
        interface_methods = {
            'items', 'keys', 'values',  # dict-like interface
            'children', 'steps',  # node/tree interface
            'default_test_method',  # test interface
            'get', 'set', 'has',  # common accessor patterns
        }
        if func_name in interface_methods:
            return True
        
        # Property-like methods that are part of interfaces
        if func_name in ['items', 'keys', 'values', 'children', 'steps']:
            return True
        
        return False
    
    def _count_actual_code_statements(self, statements: List[ast.stmt]) -> int:
        count = 0
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            if isinstance(stmt, ast.Pass):
                continue
            
            # Count simple executable statements
            if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign, 
                                 ast.Expr, ast.Return, ast.Raise, ast.Assert,
                                 ast.Delete, ast.Import, ast.ImportFrom,
                                 ast.Global, ast.Nonlocal)):
                count += 1
            
            # For control structures, count their body statements recursively
            elif isinstance(stmt, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                if hasattr(stmt, 'body'):
                    count += self._count_actual_code_statements(stmt.body)
                if hasattr(stmt, 'orelse') and stmt.orelse:
                    count += self._count_actual_code_statements(stmt.orelse)
                if hasattr(stmt, 'handlers'):  # Try blocks
                    for handler in stmt.handlers:
                        count += self._count_actual_code_statements(handler.body)
                if hasattr(stmt, 'finalbody') and stmt.finalbody:
                    count += self._count_actual_code_statements(stmt.finalbody)
            
            elif isinstance(stmt, (ast.AsyncFor, ast.AsyncWith)):
                if hasattr(stmt, 'body'):
                    count += self._count_actual_code_statements(stmt.body)
        
        return count
    
    def _is_mostly_assertions(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        assertion_count = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
            if isinstance(stmt, ast.Assert):
                assertion_count += 1
        
        if total_count == 0:
            return False
        
        return (assertion_count / total_count) >= 0.6
    
    def _is_test_pattern(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        # Count helper calls and assertions
        helper_count = 0
        assertion_count = 0
        other_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            if isinstance(stmt, ast.Assert):
                assertion_count += 1
            elif isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                func_name = self._get_function_name(stmt.value.func)
                if func_name and self._is_helper_function(func_name):
                    helper_count += 1
                else:
                    other_count += 1
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = self._get_function_name(stmt.value.func)
                if func_name and self._is_helper_function(func_name):
                    helper_count += 1
                else:
                    other_count += 1
            else:
                other_count += 1
        
        total = helper_count + assertion_count + other_count
        if total == 0:
            return False
        
        # If it's mostly helper calls + assertions with minimal other code, it's a test pattern
        test_pattern_ratio = (helper_count + assertion_count) / total
        return test_pattern_ratio >= 0.75 and other_count <= 1
    
    def _is_list_building_pattern(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        list_building_count = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
            
            is_list_building = False
            
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    method_name = stmt.value.func.attr
                    if method_name in ('extend', 'append'):
                        is_list_building = True
            
            if is_list_building:
                list_building_count += 1
        
        if total_count == 0:
            return False
        
        # If >= 75% are list-building calls, it's a list-building pattern
        return (list_building_count / total_count) >= 0.75
    
    def _is_simple_property(self, func_node: ast.FunctionDef) -> bool:
        if not func_node.decorator_list:
            return False
        
        has_property_decorator = False
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                has_property_decorator = True
                break
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ('setter', 'deleter'):
                    has_property_decorator = True
                    break
        
        if not has_property_decorator:
            return False
        
        # Simple properties are usually just return self._field or self._field = value
        # Count actual statements (excluding docstrings)
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        
        # If <= 2 executable statements, it's likely a simple property
        if len(executable_body) <= 2:
            return True
        
        return False
    
    def _is_simple_constructor(self, func_node: ast.FunctionDef) -> bool:
        if func_node.name != '__init__':
            return False
        
        # Count statements that are just assignments to self
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        
        self_assignments = 0
        other_statements = 0
        
        for stmt in executable_body:
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                if isinstance(stmt, ast.Assign):
                    targets = stmt.targets
                else:
                    targets = [stmt.target]
                
                all_self_attrs = True
                for target in targets:
                    if not (isinstance(target, ast.Attribute) and 
                           isinstance(target.value, ast.Name) and 
                           target.value.id == 'self'):
                        all_self_attrs = False
                        break
                
                if all_self_attrs:
                    self_assignments += 1
                else:
                    other_statements += 1
            else:
                other_statements += 1
        
        # If >= 80% are just self assignments, it's a simple constructor
        total = self_assignments + other_statements
        if total > 0 and (self_assignments / total) >= 0.8:
            return True
        
        return False
    
    def _extract_domain_entities(self, block: Dict[str, Any]) -> Set[str]:
        func_name = block['func_name'].lower()
        entities = set()
        
        # Common domain entity patterns
        # This could be improved with AST analysis of variable names
        common_entities = ['user', 'product', 'order', 'item', 'account', 'payment', 
                          'customer', 'invoice', 'report', 'task', 'project', 'story',
                          'feature', 'epic', 'sprint', 'team', 'workflow', 'action',
                          'rule', 'validation', 'scanner', 'violation', 'document',
                          'file', 'path', 'config', 'context', 'state', 'node']
        
        for entity in common_entities:
            if entity in func_name:
                entities.add(entity)
        
        return entities
    
    def _operates_on_different_domains(self, block1: Dict[str, Any], block2: Dict[str, Any]) -> bool:
        domain_patterns1 = self._extract_domain_entities(block1)
        domain_patterns2 = self._extract_domain_entities(block2)
        
        # If they have different domain entities and function names are similar,
        # they're likely legitimate separate implementations
        if domain_patterns1 and domain_patterns2:
            if domain_patterns1 != domain_patterns2:
                # If so, this is likely legitimate - each domain needs its own handlers
                func1 = block1['func_name']
                func2 = block2['func_name']
                if abs(len(func1) - len(func2)) <= 3:  # Similar length names
                    # Extract common prefixes (CRUD operations: create, read, update, delete, get, set)
                    crud_ops = ['create', 'read', 'get', 'update', 'delete', 'remove', 
                               'save', 'load', 'fetch', 'set', 'find', 'search']
                    func1_lower = func1.lower()
                    func2_lower = func2.lower()
                    
                    for op in crud_ops:
                        if func1_lower.startswith(op) and func2_lower.startswith(op):
                            return True  # Same CRUD operation on different domains = legitimate
        
        return False
    
    def _calls_different_methods(self, block1_nodes: List[ast.stmt], block2_nodes: List[ast.stmt]) -> bool:
        calls1 = self._extract_method_calls(block1_nodes)
        calls2 = self._extract_method_calls(block2_nodes)
        
        if not calls1 or not calls2:
            return False
        
        # If blocks have same number of calls but different method names, they're likely
        # structural patterns calling different methods (not duplication)
        if len(calls1) == len(calls2) and len(calls1) >= 2:
            method_names1 = {call for call in calls1}
            method_names2 = {call for call in calls2}
            
            # If more than 50% of method names are different, it's likely a structural pattern
            if method_names1 != method_names2:
                # Count how many calls are the same vs different
                same_calls = len(method_names1 & method_names2)
                total_unique = len(method_names1 | method_names2)
                if total_unique > 0:
                    similarity_ratio = same_calls / total_unique
                    # If less than 50% of method names match, they're calling different methods
                    if similarity_ratio < 0.5:
                        return True
        
        return False
    
    def _extract_method_calls(self, nodes: List[ast.stmt]) -> List[str]:
        method_calls = []
        
        for node in nodes:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Attribute):
                    # Method call: obj.method()
                    method_calls.append(call.func.attr)
                elif isinstance(call.func, ast.Name):
                    # Function call: func()
                    method_calls.append(call.func.id)
            elif isinstance(node, ast.Assign):
                # Assignment with call: result = obj.method()
                if isinstance(node.value, ast.Call):
                    call = node.value
                    if isinstance(call.func, ast.Attribute):
                        method_calls.append(call.func.attr)
                    elif isinstance(call.func, ast.Name):
                        method_calls.append(call.func.id)
        
        return method_calls
        
        return False
    
    def _normalize_block(self, statements: List[ast.stmt]) -> Optional[str]:
        try:
            normalized_parts = []
            for stmt in statements:
                stmt_type = type(stmt).__name__
                
                # Skip docstrings and comments
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                    if isinstance(stmt.value.value, str) and stmt.value.value.strip().startswith('"""'):
                        continue
                
                # Normalize assignment: var = value -> ASSIGN
                if isinstance(stmt, ast.Assign):
                    normalized_parts.append(f"ASSIGN({len(stmt.targets)}_targets)")
                
                # Normalize function call: func() -> CALL
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    normalized_parts.append("CALL")
                
                # Normalize assert: assert x -> ASSERT
                elif isinstance(stmt, ast.Assert):
                    normalized_parts.append("ASSERT")
                
                # Normalize for loop: for x in y -> FOR_LOOP
                elif isinstance(stmt, ast.For):
                    normalized_parts.append("FOR_LOOP")
                
                # Normalize with statement: with x -> WITH
                elif isinstance(stmt, ast.With):
                    normalized_parts.append("WITH")
                
                # Keep other statement types
                else:
                    normalized_parts.append(stmt_type)
            
            return "|".join(normalized_parts) if normalized_parts else None
        except Exception as e:
            # Log error but return None - this is a helper method, exception will bubble up if critical
            _safe_print(f"Error normalizing block: {e}")
            return None
    
    def _get_block_preview(self, statements: List[ast.stmt]) -> str:
        try:
            if hasattr(ast, 'unparse'):
                preview_lines = []
                for stmt in statements:
                    # Skip docstrings when generating preview
                    if self._is_docstring_or_comment(stmt):
                        continue
                    preview_lines.append(ast.unparse(stmt))
                return "\n".join(preview_lines)
            else:
                return str(statements)
        except Exception as e:
            # Log error but return fallback - this is a helper method, exception will bubble up if critical
            _safe_print(f"Error generating block preview: {e}")
            return str(statements)
    
    def _compare_ast_blocks(self, block1: List[ast.stmt], block2: List[ast.stmt]) -> float:
        if len(block1) == 0 and len(block2) == 0:
            return 1.0
        if len(block1) == 0 or len(block2) == 0:
            return 0.0
        
        if len(block1) != len(block2):
            # Different lengths - use longest common subsequence approach
            return self._compare_ast_structures(block1, block2)
        
        # Same length - compare node by node with weighted similarity
        similarities = []
        for node1, node2 in zip(block1, block2):
            similarity = self._compare_ast_nodes_deep(node1, node2)
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _compare_ast_structures(self, block1: List[ast.stmt], block2: List[ast.stmt]) -> float:
        if not block1 or not block2:
            return 0.0
        
        similarities = []
        for node1 in block1:
            best_match = 0.0
            for node2 in block2:
                similarity = self._compare_ast_nodes_deep(node1, node2)
                best_match = max(best_match, similarity)
            similarities.append(best_match)
        
        # Average similarity, weighted by block lengths
        if similarities:
            avg_similarity = sum(similarities) / len(similarities)
            length_ratio = min(len(block1), len(block2)) / max(len(block1), len(block2))
            return avg_similarity * length_ratio
        
        return 0.0
    
    def _get_ast_signature(self, block: List[ast.stmt]) -> str:
        signatures = []
        for node in block:
            sig = self._get_node_signature(node)
            signatures.append(sig)
        return "|".join(signatures)
    
    def _get_node_signature(self, node: ast.AST) -> str:
        node_type = type(node).__name__
        
        if isinstance(node, ast.Assign):
            return f"ASSIGN({len(node.targets)}_targets)"
        elif isinstance(node, ast.AugAssign):
            return f"AUGASSIGN({type(node.op).__name__})"
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return "CALL"
        elif isinstance(node, ast.Assert):
            return "ASSERT"
        elif isinstance(node, ast.Return):
            return "RETURN"
        elif isinstance(node, ast.If):
            return "IF"
        elif isinstance(node, ast.For):
            return "FOR"
        elif isinstance(node, ast.While):
            return "WHILE"
        elif isinstance(node, ast.With):
            return "WITH"
        elif isinstance(node, ast.Try):
            return "TRY"
        elif isinstance(node, ast.Raise):
            return "RAISE"
        else:
            return node_type
    
    def _compare_ast_nodes_deep(self, node1: ast.AST, node2: ast.AST) -> float:
        if type(node1) != type(node2):
            return 0.0
        
        # Compare based on node type
        if isinstance(node1, ast.Assign):
            return self._compare_assign_nodes(node1, node2)
        elif isinstance(node1, ast.AugAssign):
            return self._compare_augassign_nodes(node1, node2)
        elif isinstance(node1, ast.Expr) and isinstance(node1.value, ast.Call):
            # Both are Expr nodes with Call values
            if isinstance(node2, ast.Expr) and isinstance(node2.value, ast.Call):
                return self._compare_call_nodes(node1.value, node2.value)
            return 0.0
        elif isinstance(node1, ast.Assert):
            return self._compare_assert_nodes(node1, node2)
        elif isinstance(node1, ast.Return):
            return self._compare_return_nodes(node1, node2)
        elif isinstance(node1, ast.If):
            return self._compare_if_nodes(node1, node2)
        elif isinstance(node1, ast.For):
            return self._compare_for_nodes(node1, node2)
        elif isinstance(node1, ast.While):
            return self._compare_while_nodes(node1, node2)
        elif isinstance(node1, ast.With):
            return self._compare_with_nodes(node1, node2)
        elif isinstance(node1, ast.Try):
            return self._compare_try_nodes(node1, node2)
        elif isinstance(node1, ast.Raise):
            return self._compare_raise_nodes(node1, node2)
        else:
            # Generic comparison - same type means high similarity
            return 0.8  # Not perfect match but structurally similar
    
    def _compare_assign_nodes(self, node1: ast.Assign, node2: ast.Assign) -> float:
        # Compare number of targets
        if len(node1.targets) != len(node2.targets):
            return 0.5  # Partial match
        
        # Compare value structure (ignore actual values)
        value_sim = self._compare_expr_structure(node1.value, node2.value)
        return 0.7 + 0.3 * value_sim  # Base similarity + value structure bonus
    
    def _compare_augassign_nodes(self, node1: ast.AugAssign, node2: ast.AugAssign) -> float:
        if type(node1.op) != type(node2.op):
            return 0.5
        return 0.9  # Same operation type = very similar
    
    def _compare_call_nodes(self, node1: ast.Call, node2: ast.Call) -> float:
        arg_count1 = len(node1.args) + len(node1.keywords)
        arg_count2 = len(node2.args) + len(node2.keywords)
        
        if arg_count1 != arg_count2:
            return 0.6  # Partial match - different arg counts
        
        # Compare function structure (ignore function name)
        func_sim = self._compare_expr_structure(node1.func, node2.func)
        
        arg_sims = []
        for a1, a2 in zip(node1.args, node2.args):
            arg_sims.append(self._compare_expr_structure(a1, a2))
        
        avg_arg_sim = sum(arg_sims) / len(arg_sims) if arg_sims else 1.0
        
        return 0.5 + 0.3 * func_sim + 0.2 * avg_arg_sim
    
    def _compare_assert_nodes(self, node1: ast.Assert, node2: ast.Assert) -> float:
        test_sim = self._compare_expr_structure(node1.test, node2.test)
        return 0.8 + 0.2 * test_sim
    
    def _compare_return_nodes(self, node1: ast.Return, node2: ast.Return) -> float:
        if node1.value is None and node2.value is None:
            return 1.0
        if node1.value is None or node2.value is None:
            return 0.5
        return 0.7 + 0.3 * self._compare_expr_structure(node1.value, node2.value)
    
    def _compare_if_nodes(self, node1: ast.If, node2: ast.If) -> float:
        test_sim = self._compare_expr_structure(node1.test, node2.test)
        body_sim = self._compare_ast_structures(node1.body, node2.body)
        orelse_sim = self._compare_ast_structures(node1.orelse, node2.orelse)
        return 0.3 * test_sim + 0.5 * body_sim + 0.2 * orelse_sim
    
    def _compare_for_nodes(self, node1: ast.For, node2: ast.For) -> float:
        body_sim = self._compare_ast_structures(node1.body, node2.body)
        orelse_sim = self._compare_ast_structures(node1.orelse, node2.orelse)
        return 0.8 * body_sim + 0.2 * orelse_sim
    
    def _compare_while_nodes(self, node1: ast.While, node2: ast.While) -> float:
        test_sim = self._compare_expr_structure(node1.test, node2.test)
        body_sim = self._compare_ast_structures(node1.body, node2.body)
        return 0.3 * test_sim + 0.7 * body_sim
    
    def _compare_with_nodes(self, node1: ast.With, node2: ast.With) -> float:
        if len(node1.items) != len(node2.items):
            return 0.5
        body_sim = self._compare_ast_structures(node1.body, node2.body)
        return 0.7 + 0.3 * body_sim
    
    def _compare_try_nodes(self, node1: ast.Try, node2: ast.Try) -> float:
        body_sim = self._compare_ast_structures(node1.body, node2.body)
        handlers_sim = 1.0 if len(node1.handlers) == len(node2.handlers) else 0.5
        orelse_sim = self._compare_ast_structures(node1.orelse, node2.orelse)
        finalbody_sim = self._compare_ast_structures(node1.finalbody, node2.finalbody)
        return 0.4 * body_sim + 0.2 * handlers_sim + 0.2 * orelse_sim + 0.2 * finalbody_sim
    
    def _compare_raise_nodes(self, node1: ast.Raise, node2: ast.Raise) -> float:
        if node1.exc is None and node2.exc is None:
            return 1.0
        if node1.exc is None or node2.exc is None:
            return 0.5
        return 0.7 + 0.3 * self._compare_expr_structure(node1.exc, node2.exc)
    
    def _compare_expr_structure(self, expr1: ast.expr, expr2: ast.expr) -> float:
        if type(expr1) != type(expr2):
            return 0.0
        
        if isinstance(expr1, ast.Call):
            return self._compare_call_nodes(expr1, expr2)
        elif isinstance(expr1, ast.Attribute):
            # Compare attribute access structure (ignore attribute name)
            return 0.8 + 0.2 * self._compare_expr_structure(expr1.value, expr2.value)
        elif isinstance(expr1, ast.Name):
            # Names are different but structure is same
            return 0.9
        elif isinstance(expr1, ast.Constant):
            # Constants - compare types only
            if type(expr1.value) == type(expr2.value):
                return 0.8
            return 0.5
        elif isinstance(expr1, ast.BinOp):
            if type(expr1.op) == type(expr2.op):
                left_sim = self._compare_expr_structure(expr1.left, expr2.left)
                right_sim = self._compare_expr_structure(expr1.right, expr2.right)
                return 0.5 + 0.25 * left_sim + 0.25 * right_sim
            return 0.3
        elif isinstance(expr1, ast.UnaryOp):
            if type(expr1.op) == type(expr2.op):
                return 0.7 + 0.3 * self._compare_expr_structure(expr1.operand, expr2.operand)
            return 0.3
        elif isinstance(expr1, ast.Compare):
            if len(expr1.ops) == len(expr2.ops) and len(expr1.comparators) == len(expr2.comparators):
                left_sim = self._compare_expr_structure(expr1.left, expr2.left)
                return 0.6 + 0.4 * left_sim
            return 0.4
        else:
            # Generic expression - same type means some similarity
            return 0.7
    
    def _log_violation_details(self, file_path: Path, violations: List[Dict[str, Any]], lines: List[str]) -> None:
        if not violations:
            return
        
        # Log detailed violation information
        # Note: This can be verbose, but provides valuable debugging info
        
        _safe_print(f"\n[{file_path}] Found {len(violations)} duplication violation(s):")
        
        for idx, violation in enumerate(violations, 1):
            line_num = violation.get('line_number', '?')
            msg = violation.get('violation_message', '')
            
            _safe_print(f"\n  Violation {idx} (line {line_num}):")
            
            # Format: "Duplicate code blocks detected (N locations)...\n\nLocation (func:start-end):\ncode..."
            if 'Location (' in msg:
                # Split by "Location (" to get each location block
                parts = msg.split('Location (')
                locations_found = []
                
                for part in parts[1:]:  # Skip first part (header)
                    if '):' in part:
                        location_part = part.split('):')[0]
                        
                        try:
                            func_name, line_range = location_part.split(':')
                            start_line, end_line = line_range.split('-')
                            locations_found.append((func_name, int(start_line), int(end_line)))
                        except ValueError:
                            logger.debug(f'Could not parse location: {location_part}')
                
                # Log all duplicate locations with actual code
                for loc_idx, (func_name, start_line, end_line) in enumerate(locations_found, 1):
                    _safe_print(f"\n    Location {loc_idx}: {func_name}() at lines {start_line}-{end_line}")
                    
                    if start_line is not None and end_line is not None and lines:
                        # Convert to 0-based indexing and ensure valid range
                        start_idx = max(0, start_line - 1)
                        end_idx = min(len(lines), end_line)
                        
                        if start_idx < len(lines) and end_idx > start_idx:
                            code_block = lines[start_idx:end_idx]
                            _safe_print(f"    {'-' * 70}")
                            for line_num, code_line in enumerate(code_block, start=start_line):
                                # Show line numbers and code
                                _safe_print(f"    {line_num:4d} | {code_line}")
                            _safe_print(f"    {'-' * 70}")
                        else:
                            _safe_print(f"    (Could not extract code: invalid line range)")
                    else:
                        _safe_print(f"    (Could not extract code: invalid location)")
            else:
                # For duplicate functions or other violations, log the message
                _safe_print(f"    {msg[:300]}...")
        
        _safe_print("")  # Blank line after violations
    
    def _filter_files_by_package_proximity(
        self,
        changed_files: List[Path],
        all_files: List[Path],
        max_parent_levels: int = 3,
        max_files: int = 20
    ) -> List[Path]:
        """Filter all_files to only include files in nearby packages.
        
        Priority:
        1. Same package (immediate siblings)
        2. Parent package
        3. Parent's parent package (up to max_parent_levels)
        
        Stops adding files once max_files limit is reached.
        
        Args:
            changed_files: Files that were changed (to determine package context)
            all_files: All files available for comparison
            max_parent_levels: Maximum number of parent levels to traverse (default: 3)
            max_files: Maximum number of files to include in comparison (default: 20)
        
        Returns:
            Filtered list of files in nearby packages (up to max_files)
        """
        if not changed_files:
            return all_files[:max_files] if len(all_files) > max_files else all_files
        
        nearby_files = []
        seen_files = set()
        
        for changed_file in changed_files:
            if len(nearby_files) >= max_files:
                break
            
            changed_dir = changed_file.parent
            
            # Level 0: Same package (immediate siblings) - highest priority
            for file in all_files:
                if len(nearby_files) >= max_files:
                    break
                if file not in seen_files and file.parent == changed_dir:
                    nearby_files.append(file)
                    seen_files.add(file)
            
            # Level 1-N: Parent packages - lower priority
            current_dir = changed_dir
            for level in range(1, max_parent_levels + 1):
                if len(nearby_files) >= max_files:
                    break
                
                current_dir = current_dir.parent
                if not current_dir or current_dir == current_dir.parent:
                    break
                
                for file in all_files:
                    if len(nearby_files) >= max_files:
                        break
                    
                    if file in seen_files:
                        continue
                    
                    # Include files in this parent package
                    if file.parent == current_dir:
                        nearby_files.append(file)
                        seen_files.add(file)
                    # Include files in sibling packages at this level
                    elif file.parent.parent == current_dir:
                        nearby_files.append(file)
                        seen_files.add(file)
        
        if len(nearby_files) < len(all_files):
            _safe_print(f"[CROSS-FILE] Filtered to {len(nearby_files)} nearby files (from {len(all_files)} total, max: {max_files}) based on package proximity")
        
        return nearby_files
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: int = 20
    ) -> List[Dict[str, Any]]:
        violations = []
        
        # If all_* not provided, fall back to regular behavior
        if all_test_files is None:
            all_test_files = test_files
        if all_code_files is None:
            all_code_files = code_files
        
        # Combine changed files (to scan)
        changed_files = []
        if code_files:
            changed_files.extend(code_files)
        if test_files:
            changed_files.extend(test_files)
        
        # Combine all files (for reference)
        all_files = []
        if all_code_files:
            all_files.extend(all_code_files)
        if all_test_files:
            all_files.extend(all_test_files)
        
        if not changed_files or not all_files:
            return violations
        
        # Filter all_files to only include files in nearby packages
        all_files = self._filter_files_by_package_proximity(changed_files, all_files, max_files=max_cross_file_comparisons)
        
        if len(changed_files) < len(all_files):
            _safe_print(f"\n[CROSS-FILE] Incremental scan: Checking {len(changed_files)} changed file(s) against {len(all_files)} total files...")
        else:
            _safe_print(f"\n[CROSS-FILE] Full scan: Scanning {len(all_files)} files for cross-file duplication...")
        import sys
        
        def write_status(msg: str):
            if status_writer and hasattr(status_writer, 'write_cross_file_progress'):
                try:
                    status_writer.write_cross_file_progress(msg)
                except Exception as e:
                    logger.debug(f'Could not write to status file: {type(e).__name__}: {e}')
        
        write_status(f"\n## Cross-File Duplication Analysis")
        write_status(f"Scanning {len(changed_files)} changed file(s) against {len(all_files)} total files...")
        
        # Extract blocks from changed files (files to check for duplication)
        changed_blocks = []
        # Extract blocks from all files (reference set for comparison)
        all_blocks = []
        
        # First, extract blocks from changed files
        _safe_print(f"[CROSS-FILE] Extracting blocks from {len(changed_files)} changed file(s)...")
        for file_idx, file_path in enumerate(changed_files):
            if file_idx % 10 == 0:
                _safe_print(f"[CROSS-FILE] Changed files: {file_idx}/{len(changed_files)} - {file_path.name}")
                sys.stdout.flush()
            if not file_path.exists():
                continue
            
            try:
                file_size = file_path.stat().st_size
                if file_size > 500_000:  # Skip files larger than 500KB
                    _safe_print(f"Skipping large file ({file_size/1024:.1f}KB): {file_path}")
                    continue
            except Exception as e:
                logger.debug(f'Error checking file size for {file_path}: {type(e).__name__}: {e}')
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                lines = content.split('\n')
                
                functions = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_body = ast.unparse(node.body) if hasattr(ast, 'unparse') else str(node.body)
                        functions.append((node.name, func_body, node.lineno, node))
                
                for func_tuple in functions:
                    if len(func_tuple) == 5:
                        func_name, func_body, func_line, func_node, _ = func_tuple
                    else:
                        func_name, func_body, func_line, func_node = func_tuple
                    blocks = self._extract_code_blocks(func_node, func_line, func_name)
                    for block in blocks:
                        block['file_path'] = file_path
                        block['lines'] = lines
                        changed_blocks.append(block)
                        
            except (SyntaxError, UnicodeDecodeError) as e:
                logger.debug(f'Skipping file {file_path} due to {type(e).__name__}: {e}')
                continue
            except Exception as e:
                _safe_print(f"Error processing {file_path} for cross-file scan: {e}")
                continue
        
        # Second, extract blocks from all files (reference set)
        _safe_print(f"\n[CROSS-FILE] Extracting blocks from {len(all_files)} reference file(s)...")
        cache_hits = 0
        cache_misses = 0
        
        for file_idx, file_path in enumerate(all_files):
            if file_idx % 10 == 0:
                _safe_print(f"[CROSS-FILE] Reference files: {file_idx}/{len(all_files)} - {file_path.name} (cache: {cache_hits} hits, {cache_misses} misses)")
                sys.stdout.flush()
            
            if not file_path.exists():
                continue
            
            # Try to load from cache first
            cached_blocks = self._load_blocks_from_cache(file_path)
            if cached_blocks is not None:
                cache_hits += 1
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = content.split('\n')
                    for block in cached_blocks:
                        block['file_path'] = file_path
                        block['lines'] = lines
                        all_blocks.append(block)
                except Exception as e:
                    logger.debug(f'Error rehydrating cached blocks for {file_path}: {e}')
                continue
            
            cache_misses += 1
            
            # Not in cache - extract blocks normally
            try:
                file_size = file_path.stat().st_size
                if file_size > 500_000:  # Skip files larger than 500KB
                    _safe_print(f"Skipping large file ({file_size/1024:.1f}KB): {file_path}")
                    continue
            except Exception as e:
                logger.debug(f'Error checking file size for {file_path}: {type(e).__name__}: {e}')
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                lines = content.split('\n')
                
                functions = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_body = ast.unparse(node.body) if hasattr(ast, 'unparse') else str(node.body)
                        functions.append((node.name, func_body, node.lineno, node))
                
                file_blocks = []
                for func_tuple in functions:
                    if len(func_tuple) == 5:
                        func_name, func_body, func_line, func_node, _ = func_tuple
                    else:
                        func_name, func_body, func_line, func_node = func_tuple
                    blocks = self._extract_code_blocks(func_node, func_line, func_name)
                    for block in blocks:
                        block['file_path'] = file_path
                        block['lines'] = lines
                        all_blocks.append(block)
                        file_blocks.append(block)
                
                # Save to cache for next time
                self._save_blocks_to_cache(file_path, file_blocks)
                        
            except (SyntaxError, UnicodeDecodeError) as e:
                logger.debug(f'Skipping file {file_path} due to {type(e).__name__}: {e}')
                continue
            except Exception as e:
                _safe_print(f"Error processing {file_path} for cross-file scan: {e}")
                continue
        
        _safe_print(f"[CROSS-FILE] Cache statistics: {cache_hits} hits, {cache_misses} misses ({cache_hits/(cache_hits+cache_misses)*100:.1f}% hit rate)" if (cache_hits + cache_misses) > 0 else "[CROSS-FILE] No files processed")
        
        _safe_print(f"\n[CROSS-FILE] Extracted {len(changed_blocks)} blocks from changed files, {len(all_blocks)} blocks from all files")
        write_status(f"Extracted {len(changed_blocks)} changed blocks, {len(all_blocks)} reference blocks")
        
        # Compare changed blocks against all blocks (including changed blocks)
        SIMILARITY_THRESHOLD = 0.90
        compared_pairs = set()
        total_comparisons = len(changed_blocks) * len(all_blocks)
        comparison_count = 0
        last_progress = 0
        
        _safe_print(f"[CROSS-FILE] Starting {total_comparisons:,} pairwise comparisons (changed vs all)...")
        write_status(f"Starting {total_comparisons:,} pairwise comparisons...")
        
        start_time = datetime.now()
        last_report_time = start_time
        REPORT_INTERVAL_SECONDS = 10  # Report at least every 10 seconds
        REPORT_INTERVAL_COMPARISONS = 50000  # Or every 50K comparisons
        last_comparison_report = 0
        
        # Compare each changed block against all blocks
        for i, block1 in enumerate(changed_blocks):
            for j, block2 in enumerate(all_blocks):
                # Skip if same file (within-file duplication already checked in scan_file)
                if block1['file_path'] == block2['file_path']:
                    continue
                
                # Skip comparing a block against itself
                if (block1['file_path'] == block2['file_path'] and 
                    block1['start_line'] == block2['start_line'] and
                    block1['func_name'] == block2['func_name']):
                    continue
                
                comparison_count += 1
                
                # Report progress: every 5%, every 50K comparisons, or every 10 seconds
                now = datetime.now()
                elapsed_since_report = (now - last_report_time).total_seconds()
                progress_pct = (comparison_count * 100) // total_comparisons if total_comparisons > 0 else 0
                
                should_report = (
                    progress_pct >= last_progress + 5 or  # Every 5%
                    comparison_count >= last_comparison_report + REPORT_INTERVAL_COMPARISONS or  # Every 50K comparisons
                    elapsed_since_report >= REPORT_INTERVAL_SECONDS  # Every 10 seconds
                )
                
                if should_report:
                    elapsed_total = (now - start_time).total_seconds()
                    rate = comparison_count / max(1, elapsed_total)
                    remaining = total_comparisons - comparison_count
                    eta_seconds = int(remaining / max(1, rate))
                    progress_msg = f"Comparing: {progress_pct}% ({comparison_count:,}/{total_comparisons:,}) - {len(violations)} violations - ETA: {eta_seconds}s"
                    _safe_print(f"[CROSS-FILE] {progress_msg}")
                    write_status(progress_msg + "  ")  # Add 2 trailing spaces for markdown line break
                    last_progress = progress_pct
                    last_report_time = now
                    last_comparison_report = comparison_count
                
                # Calculate similarity
                # Check if both blocks have ast_nodes (cached blocks don't have them)
                if 'ast_nodes' in block1 and 'ast_nodes' in block2:
                    ast_similarity = self._compare_ast_blocks(block1['ast_nodes'], block2['ast_nodes'])
                else:
                    ast_similarity = 0.0  # No AST comparison if nodes not available
                
                normalized_similarity = SequenceMatcher(None, block1['normalized'], block2['normalized']).ratio()
                
                preview1_normalized = ' '.join(block1['preview'].split())
                preview2_normalized = ' '.join(block2['preview'].split())
                content_similarity = SequenceMatcher(None, preview1_normalized, preview2_normalized).ratio()
                
                # Use AST similarity as primary indicator (if available)
                if ast_similarity >= SIMILARITY_THRESHOLD or (normalized_similarity >= SIMILARITY_THRESHOLD and content_similarity >= 0.85):
                    # Found duplicate across files
                    file1 = block1['file_path']
                    file2 = block2['file_path']
                    func1 = block1['func_name']
                    func2 = block2['func_name']
                    start1 = block1['start_line']
                    end1 = block1['end_line']
                    start2 = block2['start_line']
                    end2 = block2['end_line']
                    
                    preview1 = block1['preview']
                    preview2 = block2['preview']
                    
                    # Truncate previews if too long
                    if len(preview1) > 300:
                        preview1 = preview1[:300] + '...'
                    if len(preview2) > 300:
                        preview2 = preview2[:300] + '...'
                    
                    location1 = f"{file1.name}:{func1} (lines {start1}-{end1})"
                    location2 = f"{file2.name}:{func2} (lines {start2}-{end2})"
                    
                    violation_message = (
                        f'Duplicate code detected across files - extract to shared function.\n\n'
                        f'Location 1 ({location1}):\n```python\n{preview1}\n```\n\n'
                        f'Location 2 ({location2}):\n```python\n{preview2}\n```'
                    )
                    
                    # No code snippet for cross-file duplication violations (previews already included in message)
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=violation_message,
                        location=str(file1),
                        line_number=start1,
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
                    
                    if len(violations) % 10 == 0:
                        write_status(f"Found {len(violations)} violations so far...")
                        sys.stdout.flush()
        
        complete_msg = f"Complete: {comparison_count} comparisons, {len(violations)} violations"
        _safe_print(f"\n[CROSS-FILE] {complete_msg}")
        write_status(complete_msg)
        write_status("")
        return violations

