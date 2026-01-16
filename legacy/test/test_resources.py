"""Scanner Resources Tests

Tests for resource-oriented domain model classes following pytest BDD orchestrator pattern.
"""

import pytest
from pathlib import Path
from agile_bot.bots.base_bot.src.scanners.resources import Scope, File, Block, Line, Scan, Violation
from agile_bot.bots.base_bot.src.scanners.resources.block_extractor import BlockExtractor

# ============================================================================
# HELPER FUNCTIONS - Reusable operations (under 20 lines each)
# ============================================================================

def create_test_file(tmp_path: Path, filename: str, content: str) -> Path:
    """Helper: Create test file with content."""
    test_file = tmp_path / filename
    test_file.write_text(content)
    return test_file

def create_scope_with_files(tmp_path: Path, files: list) -> Scope:
    """Helper: Create scope with test files."""
    file_paths = [create_test_file(tmp_path, name, content) for name, content in files]
    return Scope(file_paths)

def create_rule(tmp_path: Path, name: str = 'test_rule', scanner_path: str = None):
    """Helper: Create rule object for tests."""
    from agile_bot.bots.base_bot.src.actions.rules.rule import Rule
    rule_file = tmp_path / f'{name}.json'
    rule_content = {
        'name': name,
        'description': f'Test rule: {name}',
        'scanner': scanner_path or 'agile_bot.bots.base_bot.src.scanners.test_scanner.TestScanner'
    }
    rule_file.write_text('{}')  # Create empty file
    return Rule(rule_file, behavior_name='code', bot_name='base_bot', rule_content=rule_content)

def verify_file_has_lines(file: File, expected_count: int):
    """Helper: Verify file has expected number of lines."""
    assert len(file.lines) == expected_count

def verify_block_has_content(block: Block, expected_content: str):
    """Helper: Verify block has expected content."""
    assert expected_content in block.content

# ============================================================================
# FIXTURES - Test setup
# ============================================================================

@pytest.fixture
def workspace_root(tmp_path):
    """Fixture: Temporary workspace directory."""
    workspace = tmp_path / 'workspace'
    workspace.mkdir(exist_ok=True)
    return workspace

# ============================================================================
# STORY: Line Resource
# ============================================================================

class TestLineResource:
    """Story: Line Resource - Tests line resource behavior."""
    
    def test_line_has_file_number_and_content(self, workspace_root):
        """
        SCENARIO: Line has file, number, and content
        GIVEN: File exists
        WHEN: Line is created with number and content
        THEN: Line has file, number, and content
        """
        # Given: File exists
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        file = scope.files[0]
        
        # When: Line is created
        line = Line(file, 1, 'def test(): pass')
        
        # Then: Line has properties
        assert line.file == file
        assert line.number == 1
        assert line.content == 'def test(): pass'
    
    def test_line_extracts_number_from_ast_node(self, workspace_root):
        """
        SCENARIO: Line extracts number from AST node
        GIVEN: AST node exists
        WHEN: Line extracts from AST node
        THEN: Line number is returned
        """
        import ast
        # Given: File and line exist
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        file = scope.files[0]
        line = Line(file, 1, 'def test(): pass')
        
        # When: Extract from AST node
        node = ast.parse('def test(): pass').body[0]
        line_num = line.extract_from_ast_node(node)
        
        # Then: Line number returned
        assert line_num == 1
    
    def test_line_extracts_number_from_position(self, workspace_root):
        """
        SCENARIO: Line extracts number from file position
        GIVEN: File with content exists
        WHEN: Line extracts from position
        THEN: Correct line number is returned
        """
        # Given: File with content
        scope = Scope([create_test_file(workspace_root, 'test.py', 'line1\nline2\nline3')])
        file = scope.files[0]
        line = Line(file, 1, 'line1')
        
        # When: Extract from position
        line1_num = line.extract_from_position(0)
        line2_num = line.extract_from_position(6)
        
        # Then: Correct line numbers returned
        assert line1_num == 1
        assert line2_num == 2

# ============================================================================
# STORY: File Resource
# ============================================================================

class TestFileResource:
    """Story: File Resource - Tests file resource behavior."""
    
    def test_file_has_path_and_scope(self, workspace_root):
        """
        SCENARIO: File has path and scope
        GIVEN: Scope with file path exists
        WHEN: File is created
        THEN: File has path and scope
        """
        # Given: Scope with file
        test_file = create_test_file(workspace_root, 'test.py', 'def test(): pass')
        scope = Scope([test_file])
        
        # When: File is accessed
        file = scope.files[0]
        
        # Then: File has path and scope
        assert file.path == test_file
        assert file.scope == scope
    
    def test_file_parses_python_file_safely(self, workspace_root):
        """
        SCENARIO: File parses Python file safely
        GIVEN: Valid Python file exists
        WHEN: File parses safely
        THEN: File parsing succeeds
        """
        # Given: Valid Python file
        test_file = create_test_file(workspace_root, 'test.py', 'def test(): pass')
        scope = Scope([test_file])
        file = scope.files[0]
        
        # When: Parse safely
        result = file.parse_safely()
        
        # Then: Parsing succeeded
        assert result is True
        assert file.parse_python_file() is not None
    
    def test_file_identifies_test_files(self, workspace_root):
        """
        SCENARIO: File identifies test files
        GIVEN: Test file exists
        WHEN: File checks if test file
        THEN: File identifies as test file
        """
        # Given: Test file
        test_file = create_test_file(workspace_root, 'test_test.py', 'def test(): pass')
        scope = Scope([test_file])
        file = scope.files[0]
        
        # When: Check if test file
        is_test = file.is_test_file()
        
        # Then: Identified as test file
        assert is_test is True
    
    def test_file_extracts_blocks(self, workspace_root):
        """
        SCENARIO: File extracts blocks
        GIVEN: Python file with functions and classes exists
        WHEN: File extracts blocks
        THEN: Blocks are extracted
        """
        # Given: File with code blocks
        test_file = create_test_file(workspace_root, 'test.py', 'def test(): pass\nclass Test: pass')
        scope = Scope([test_file])
        file = scope.files[0]
        file.parse_safely()
        
        # When: Extract blocks
        blocks = file.blocks
        
        # Then: Blocks extracted
        assert len(blocks) >= 1

# ============================================================================
# STORY: Block Resource
# ============================================================================

class TestBlockResource:
    """Story: Block Resource - Tests block resource behavior."""
    
    def test_block_has_content_and_file(self, workspace_root):
        """
        SCENARIO: Block has content and references file
        GIVEN: File exists
        WHEN: Block is created
        THEN: Block has content and file reference
        """
        # Given: File exists
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        file = scope.files[0]
        
        # When: Block is created
        block = Block(file, 'def test(): pass', 1, 2)
        
        # Then: Block has properties
        assert block.content == 'def test(): pass'
        assert block.file == file
        assert block.start_line == 1
        assert block.end_line == 2
    
    def test_block_has_violations(self, workspace_root):
        """
        SCENARIO: Block has violations
        GIVEN: Block exists
        WHEN: Violation is created for block
        THEN: Block contains violation
        """
        # Given: Block exists
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        file = scope.files[0]
        block = Block(file, 'def test(): pass', 1, 2)
        rule = create_rule(workspace_root, 'test_rule')
        scan = Scan(scope, rule)
        
        # When: Violation is created
        violation = Violation.create_from_rule_and_context(rule, block, scan, 'Test violation')
        
        # Then: Block has violation
        assert len(block.violations) == 1
        assert violation in block.violations
    
    def test_block_normalizes_content(self, workspace_root):
        """
        SCENARIO: Block normalizes content
        GIVEN: Block with whitespace exists
        WHEN: Block normalizes content
        THEN: Content is normalized
        """
        # Given: Block with whitespace
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        file = scope.files[0]
        block = Block(file, '  def test(): pass  \r\n', 1, 2)
        
        # When: Normalize content
        normalized = block.normalize_content()
        
        # Then: Content normalized
        assert '\r' not in normalized
        assert normalized.strip() == 'def test(): pass'

# ============================================================================
# STORY: Scope Resource
# ============================================================================

class TestScopeResource:
    """Story: Scope Resource - Tests scope resource behavior."""
    
    def test_scope_contains_files(self, workspace_root):
        """
        SCENARIO: Scope contains files
        GIVEN: Multiple file paths exist
        WHEN: Scope is created
        THEN: Scope contains all files
        """
        # Given: Multiple files
        file1 = create_test_file(workspace_root, 'file1.py', 'def test1(): pass')
        file2 = create_test_file(workspace_root, 'file2.py', 'def test2(): pass')
        
        # When: Scope is created
        scope = Scope([file1, file2])
        
        # Then: Scope contains files
        assert len(scope.files) == 2
        assert scope.files[0].path == file1
        assert scope.files[1].path == file2
    
    def test_scope_aggregates_blocks_from_files(self, workspace_root):
        """
        SCENARIO: Scope aggregates blocks from files
        GIVEN: File with blocks exists
        WHEN: Scope aggregates blocks
        THEN: Scope contains blocks from all files
        """
        # Given: File with blocks
        test_file = create_test_file(workspace_root, 'test.py', 'def test(): pass')
        scope = Scope([test_file])
        scope.files[0].parse_safely()
        
        # When: Access blocks
        blocks = scope.blocks
        
        # Then: Blocks aggregated
        assert len(blocks) >= 1

# ============================================================================
# STORY: Scan Resource
# ============================================================================

class TestScanResource:
    """Story: Scan Resource - Tests scan resource behavior."""
    
    def test_scan_created_for_scope_and_rule(self, workspace_root):
        """
        SCENARIO: Scan created for scope and rule
        GIVEN: Scope and rule exist
        WHEN: Scan is created
        THEN: Scan has scope and rule
        """
        # Given: Scope and rule
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        rule = create_rule(workspace_root, 'test_rule')
        
        # When: Scan is created
        scan = Scan(scope, rule)
        
        # Then: Scan has scope and rule
        assert scan.scope == scope
        assert scan.rule == rule
        assert len(scan.violations) == 0
    
    def test_scan_collects_violations(self, workspace_root):
        """
        SCENARIO: Scan collects violations
        GIVEN: Scan and block exist
        WHEN: Violation is created
        THEN: Scan contains violation
        """
        # Given: Scan and block
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        rule = create_rule(workspace_root, 'test_rule')
        scan = Scan(scope, rule)
        file = scope.files[0]
        block = Block(file, 'def test(): pass', 1, 2)
        
        # When: Violation is created
        violation = Violation.create_from_rule_and_context(rule, block, scan, 'Test violation')
        
        # Then: Scan contains violation
        assert len(scan.violations) == 1
        assert violation in scan.violations

# ============================================================================
# STORY: Violation Resource
# ============================================================================

class TestViolationResource:
    """Story: Violation Resource - Tests violation resource behavior."""
    
    def test_violation_references_rule_block_and_scan(self, workspace_root):
        """
        SCENARIO: Violation references rule, block, and scan
        GIVEN: Rule, block, and scan exist
        WHEN: Violation is created
        THEN: Violation references all resources
        """
        # Given: Rule, block, and scan
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        rule = create_rule(workspace_root, 'test_rule')
        scan = Scan(scope, rule)
        file = scope.files[0]
        block = Block(file, 'def test(): pass', 1, 2)
        
        # When: Violation is created
        violation = Violation.create_from_rule_and_context(
            rule, block, scan, 'Test violation', line_number=1
        )
        
        # Then: Violation references resources
        assert violation.rule == rule
        assert violation.block == block
        assert violation.scan == scan
        assert violation.violation_message == 'Test violation'
        assert violation.line_number == 1
    
    def test_violation_converts_to_dictionary(self, workspace_root):
        """
        SCENARIO: Violation converts to dictionary
        GIVEN: Violation exists
        WHEN: Violation converts to dictionary
        THEN: Dictionary contains violation data
        """
        # Given: Violation
        scope = Scope([create_test_file(workspace_root, 'test.py', 'def test(): pass')])
        rule = create_rule(workspace_root, 'test_rule')
        scan = Scan(scope, rule)
        file = scope.files[0]
        block = Block(file, 'def test(): pass', 1, 2)
        violation = Violation.create_from_rule_and_context(
            rule, block, scan, 'Test violation', line_number=1
        )
        
        # When: Convert to dictionary
        result = violation.to_dict()
        
        # Then: Dictionary contains data
        assert result['rule'] == 'test_rule'
        # Rule file may include #embedded suffix for embedded rules
        assert result['rule_file'] in ['test_rule.json', 'test_rule.json#embedded']
        assert result['violation_message'] == 'Test violation'
        assert result['line_number'] == 1
        assert result['severity'] == 'error'

# ============================================================================
# STORY: BlockExtractor Helper
# ============================================================================

class TestBlockExtractorHelper:
    """Story: BlockExtractor Helper - Tests block extractor behavior."""
    
    def test_block_extractor_extracts_blocks_from_file(self, workspace_root):
        """
        SCENARIO: BlockExtractor extracts blocks from file
        GIVEN: Python file with functions and classes exists
        WHEN: BlockExtractor extracts blocks
        THEN: Blocks are extracted
        """
        # Given: File with code blocks
        test_file = create_test_file(workspace_root, 'test.py', 'def test(): pass\nclass Test: pass')
        scope = Scope([test_file])
        file = scope.files[0]
        file.parse_safely()
        
        # When: Extract blocks
        extractor = BlockExtractor()
        blocks = extractor.extract_blocks_from_file(file)
        
        # Then: Blocks extracted
        assert len(blocks) >= 2
        assert all(isinstance(block, Block) for block in blocks)
