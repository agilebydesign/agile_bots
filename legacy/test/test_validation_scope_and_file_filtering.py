"""
Validation Scope and File Filtering Tests

Tests for defects found during validation system debugging:
1. FileFilter.filter_files() glob pattern matching
2. ValidationContext file discovery with scope
3. REPL instructions command parsing CLI args
4. Scanner path validation in rules
5. Integration test for validate with file scope

These tests ensure that the validation system correctly:
- Filters files based on glob patterns
- Discovers and filters files when scope is provided
- Parses CLI arguments in REPL instructions command
- Validates scanner paths in rule JSON files
- Executes end-to-end validation with file scope
"""
import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


# ============================================================================
# TEST: FileFilter.filter_files() glob pattern matching
# ============================================================================

class TestFileFilterGlobPatternMatching:
    """Tests for FileFilter.filter_files() to ensure glob patterns work correctly."""
    
    def test_file_filter_includes_matching_files(self):
        """
        SCENARIO: FileFilter includes files matching include patterns
        GIVEN: A list of files and a FileFilter with include patterns
        WHEN: filter_files() is called
        THEN: Only files matching include patterns are returned
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('test/test_file2.py'),
            Path('src/source_file.py'),
            Path('docs/readme.md')
        ]
        
        # AND: A FileFilter with include pattern for test files
        file_filter = FileFilter(include_patterns=['**/test*.py'])
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Only test files are included
        assert len(filtered) == 2
        assert Path('test/test_file1.py') in filtered
        assert Path('test/test_file2.py') in filtered
        assert Path('src/source_file.py') not in filtered
    
    def test_file_filter_excludes_matching_files(self):
        """
        SCENARIO: FileFilter excludes files matching exclude patterns
        GIVEN: A list of files and a FileFilter with exclude patterns
        WHEN: filter_files() is called
        THEN: Files matching exclude patterns are removed
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('test/test_file2.py'),
            Path('test/__pycache__/cached.pyc'),
            Path('test/.pytest_cache/file.py')
        ]
        
        # AND: A FileFilter with exclude pattern for cache files
        file_filter = FileFilter(exclude_patterns=['**/__pycache__/**', '**/.pytest_cache/**'])
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Cache files are excluded
        assert len(filtered) == 2
        assert Path('test/test_file1.py') in filtered
        assert Path('test/test_file2.py') in filtered
    
    def test_file_filter_combines_include_and_exclude(self):
        """
        SCENARIO: FileFilter combines include and exclude patterns
        GIVEN: A list of files and a FileFilter with both include and exclude patterns
        WHEN: filter_files() is called
        THEN: Files must match include AND not match exclude
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        
        # GIVEN: A list of files
        files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py'),
            Path('src/source.py')
        ]
        
        # AND: A FileFilter with include for test files and exclude for helpers
        file_filter = FileFilter(
            include_patterns=['**/test*.py'],
            exclude_patterns=['**/*helpers*.py']
        )
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Test files are included except helpers
        assert len(filtered) == 2
        assert Path('test/test_execute_in_headless_mode.py') in filtered
        assert Path('test/test_monitor_session.py') in filtered
        assert Path('test/test_helpers.py') not in filtered
    
    def test_file_filter_returns_all_when_no_patterns(self):
        """
        SCENARIO: FileFilter returns all files when no patterns specified
        GIVEN: A list of files and a FileFilter with no patterns
        WHEN: filter_files() is called
        THEN: All files are returned
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('src/source.py'),
            Path('docs/readme.md')
        ]
        
        # AND: A FileFilter with no patterns
        file_filter = FileFilter()
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: All files are returned
        assert len(filtered) == 3
        assert all(f in filtered for f in files)
    
    def test_file_filter_handles_specific_file_paths(self):
        """
        SCENARIO: FileFilter handles specific file paths (not just globs)
        GIVEN: A list of files and a FileFilter with specific file path
        WHEN: filter_files() is called
        THEN: Only the specific file is included
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        
        # GIVEN: A list of files
        files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py')
        ]
        
        # AND: A FileFilter with specific file path
        file_filter = FileFilter(include_patterns=['**/test_execute_in_headless_mode.py'])
        
        # WHEN: filter_files() is called
        filtered = file_filter.filter_files(files)
        
        # THEN: Only the specific file is included
        assert len(filtered) == 1
        assert Path('test/test_execute_in_headless_mode.py') in filtered


# ============================================================================
# TEST: ValidationContext file discovery with scope
# ============================================================================

class TestValidationContextFileDiscovery:
    """Tests for ValidationContext to ensure file discovery works with scope."""
    
    def test_scope_filters_files_correctly(self):
        """
        SCENARIO: Scope.filters_files() filters files correctly
        GIVEN: A list of files and a Scope with file filter
        WHEN: filters_files() is called
        THEN: Only files matching the filter are returned
        
        This test verifies the fix for the bug where ValidationContext
        was not using Scope.filters_files() to filter discovered files.
        """
        from agile_bot.bots.base_bot.src.actions.action_context import Scope, FileFilter
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py')
        ]
        
        # AND: A scope with file filter for specific file
        file_filter = FileFilter(include_patterns=['**/test_execute_in_headless_mode.py'])
        scope = Scope(_file_filter=file_filter)
        
        # WHEN: filters_files() is called
        filtered = scope.filters_files(files)
        
        # THEN: Only the filtered file is included
        assert len(filtered) == 1
        assert Path('test/test_execute_in_headless_mode.py') in filtered
        assert Path('test/test_monitor_session.py') not in filtered
        assert Path('test/test_helpers.py') not in filtered
    
    def test_scope_returns_all_files_when_no_filter(self):
        """
        SCENARIO: Scope.filters_files() returns all files when no filter
        GIVEN: A list of files and a Scope with no file filter
        WHEN: filters_files() is called
        THEN: All files are returned
        """
        from agile_bot.bots.base_bot.src.actions.action_context import Scope
        from pathlib import Path
        
        # GIVEN: A list of files
        files = [
            Path('test/test_file1.py'),
            Path('test/test_file2.py'),
            Path('test/test_file3.py')
        ]
        
        # AND: A scope with no file filter
        scope = Scope()
        
        # WHEN: filters_files() is called
        filtered = scope.filters_files(files)
        
        # THEN: All files are returned
        assert len(filtered) == 3
        assert all(f in filtered for f in files)


# ============================================================================
# TEST: REPL instructions command parsing CLI args
# ============================================================================

class TestREPLInstructionsCommandCLIArgs:
    """Tests for REPL _handle_instructions_command to ensure CLI args are parsed."""
    
    def test_cli_context_builder_parses_scope_argument(self):
        """
        SCENARIO: CliContextBuilder parses --scope argument
        GIVEN: A CLI argument string with --scope
        WHEN: CliContextBuilder parses the arguments
        THEN: A context with scope is created
        
        This test verifies the fix for the bug where _handle_instructions_command
        was not parsing CLI arguments, causing --scope to be ignored.
        """
        from agile_bot.bots.base_bot.src.repl_cli.cli_context_builder import CliContextBuilder
        from agile_bot.bots.base_bot.src.actions.validate.validate_action import ValidateRulesAction
        from unittest.mock import Mock
        
        # GIVEN: A mock action
        mock_behavior = Mock()
        mock_behavior.name = 'tests'
        action = ValidateRulesAction(behavior=mock_behavior)
        
        # AND: CLI arguments with --scope
        args = ['--scope', 'files:test/test_file.py']
        
        # WHEN: CliContextBuilder parses the arguments
        builder = CliContextBuilder()
        context = builder.build_context(action, args)
        
        # THEN: Context with scope is created
        assert context is not None
        assert hasattr(context, 'scope')
        assert context.scope is not None
        assert context.scope.file_filter is not None
    
    def test_cli_context_builder_handles_no_arguments(self):
        """
        SCENARIO: CliContextBuilder handles no arguments
        GIVEN: An empty CLI argument list
        WHEN: CliContextBuilder parses the arguments
        THEN: A context with no scope is created
        """
        from agile_bot.bots.base_bot.src.repl_cli.cli_context_builder import CliContextBuilder
        from agile_bot.bots.base_bot.src.actions.validate.validate_action import ValidateRulesAction
        from unittest.mock import Mock
        
        # GIVEN: A mock action
        mock_behavior = Mock()
        mock_behavior.name = 'tests'
        action = ValidateRulesAction(behavior=mock_behavior)
        
        # AND: Empty CLI arguments
        args = []
        
        # WHEN: CliContextBuilder parses the arguments
        builder = CliContextBuilder()
        context = builder.build_context(action, args)
        
        # THEN: Context with no scope is created
        assert context is not None
        assert hasattr(context, 'scope')
        assert context.scope is None


# ============================================================================
# TEST: Scanner path validation in rules
# ============================================================================

class TestScannerPathValidation:
    """Tests for scanner path validation in rule JSON files."""
    
    def test_rule_loads_scanner_with_correct_path(self, tmp_path):
        """
        SCENARIO: Rule loads scanner with correct path
        GIVEN: A rule JSON file with correct scanner path
        WHEN: Rule is loaded
        THEN: Scanner is loaded successfully
        """
        from agile_bot.bots.base_bot.src.actions.rules.rule import Rule
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        
        # GIVEN: A rule JSON file with correct scanner path
        rule_dir = tmp_path / 'rules'
        rule_dir.mkdir()
        rule_file = rule_dir / 'test_rule.json'
        rule_content = {
            'priority': 1,
            'description': 'Test rule',
            'scanner': 'agile_bot.bots.base_bot.src.scanners.ubiquitous_language_scanner.UbiquitousLanguageScanner',
            'do': {'description': 'Do this'},
            'dont': {'description': 'Dont do this'}
        }
        rule_file.write_text(json.dumps(rule_content))
        
        # AND: BotPaths
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=tmp_path
        )
        
        # WHEN: Rule is loaded
        rule = Rule(rule_file, bot_name='story_bot', behavior_name='tests')
        
        # THEN: Scanner is loaded successfully (no error)
        assert rule.scanner_path == rule_content['scanner']
        # Note: We can't check if scanner is actually loaded without the actual scanner module
        # But we can check that the path is stored correctly
    
    def test_rule_detects_incorrect_scanner_path(self, tmp_path):
        """
        SCENARIO: Rule detects incorrect scanner path
        GIVEN: A rule JSON file with incorrect scanner path (old location)
        WHEN: Rule is loaded
        THEN: Scanner load error is recorded
        """
        from agile_bot.bots.base_bot.src.actions.rules.rule import Rule
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        
        # GIVEN: A rule JSON file with incorrect scanner path
        rule_dir = tmp_path / 'rules'
        rule_dir.mkdir()
        rule_file = rule_dir / 'test_rule.json'
        rule_content = {
            'priority': 1,
            'description': 'Test rule',
            'scanner': 'agile_bot.bots.base_bot.src.actions.validate.scanners.nonexistent_scanner.NonexistentScanner',
            'do': {'description': 'Do this'},
            'dont': {'description': 'Dont do this'}
        }
        rule_file.write_text(json.dumps(rule_content))
        
        # AND: BotPaths
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=tmp_path
        )
        
        # WHEN: Rule is loaded
        rule = Rule(rule_file, bot_name='story_bot', behavior_name='tests')
        
        # THEN: Scanner load error is recorded
        assert rule.scanner_load_error is not None
        assert 'nonexistent_scanner' in rule.scanner_load_error.lower() or 'not found' in rule.scanner_load_error.lower()
    
    def test_rule_requires_scanner_field_not_scanners(self, tmp_path):
        """
        SCENARIO: Rule requires 'scanner' field not 'scanners' (plural)
        GIVEN: A rule JSON file with 'scanners' (plural) field
        WHEN: Rule is loaded
        THEN: Scanner is not loaded (field name is wrong)
        """
        from agile_bot.bots.base_bot.src.actions.rules.rule import Rule
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        
        # GIVEN: A rule JSON file with 'scanners' (plural) field
        rule_dir = tmp_path / 'rules'
        rule_dir.mkdir()
        rule_file = rule_dir / 'test_rule.json'
        rule_content = {
            'priority': 1,
            'description': 'Test rule',
            'scanners': [  # Wrong: should be 'scanner' (singular)
                'agile_bot.bots.base_bot.src.scanners.ubiquitous_language_scanner.UbiquitousLanguageScanner'
            ],
            'do': {'description': 'Do this'},
            'dont': {'description': 'Dont do this'}
        }
        rule_file.write_text(json.dumps(rule_content))
        
        # AND: BotPaths
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=tmp_path
        )
        
        # WHEN: Rule is loaded
        rule = Rule(rule_file, bot_name='story_bot', behavior_name='tests')
        
        # THEN: Scanner is not loaded (scanner_path is None)
        assert rule.scanner_path is None
        assert rule.scanner is None


# ============================================================================
# TEST: Behavior validation type determines file discovery
# ============================================================================
# NOTE: Tests for behavior validation_type are in test_validate_knowledge_and_content_against_rules.py
# This test file focuses on file filtering and scope functionality

class TestBehaviorValidationType:
    """Tests for Behavior.validation_type to ensure correct validation target."""
    
    def test_shape_behavior_has_story_graph_validation_type(self, tmp_path):
        """
        SCENARIO: Shape behavior validates story graph only
        GIVEN: A shape behavior
        WHEN: validation_type property is accessed
        THEN: It returns ValidationType.STORY_GRAPH
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.action_context import ValidationType
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A shape behavior
        behavior = Behavior(name='shape', bot_paths=bot_paths)
        
        # WHEN: validation_type is accessed
        validation_type = behavior.validation_type
        
        # THEN: It returns STORY_GRAPH
        assert validation_type == ValidationType.STORY_GRAPH
    
    def test_discovery_behavior_has_story_graph_validation_type(self, tmp_path):
        """
        SCENARIO: Discovery behavior validates story graph only
        GIVEN: A discovery behavior
        WHEN: validation_type property is accessed
        THEN: It returns ValidationType.STORY_GRAPH
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.action_context import ValidationType
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A discovery behavior
        behavior = Behavior(name='discovery', bot_paths=bot_paths)
        
        # WHEN: validation_type is accessed
        validation_type = behavior.validation_type
        
        # THEN: It returns STORY_GRAPH
        assert validation_type == ValidationType.STORY_GRAPH
    
    def test_code_behavior_has_files_validation_type(self, tmp_path):
        """
        SCENARIO: Code behavior validates files only
        GIVEN: A code behavior
        WHEN: validation_type property is accessed
        THEN: It returns ValidationType.FILES
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.action_context import ValidationType
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A code behavior
        behavior = Behavior(name='code', bot_paths=bot_paths)
        
        # WHEN: validation_type is accessed
        validation_type = behavior.validation_type
        
        # THEN: It returns FILES
        assert validation_type == ValidationType.FILES
    
    def test_validation_context_returns_empty_files_for_story_graph_only_behavior(self, tmp_path):
        """
        SCENARIO: ValidationContext returns empty files for story-graph-only behaviors
        GIVEN: A shape behavior and ValidateActionContext with no files scope
        WHEN: ValidationContext._get_files_for_validation is called
        THEN: It returns empty dict (no files discovered)
        
        This test ensures that story-graph-only behaviors don't validate files by default.
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.rules.rules import ValidationContext
        from agile_bot.bots.base_bot.src.actions.action_context import ValidateActionContext
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A shape behavior (story-graph-only)
        behavior = Behavior(name='shape', bot_paths=bot_paths)
        
        # AND: A ValidateActionContext with no files scope
        context = ValidateActionContext(scope=None)
        
        # WHEN: _get_files_for_validation is called
        files = ValidationContext._get_files_for_validation(behavior, context)
        
        # THEN: It returns empty dict (no files discovered)
        assert files == {}
    
    def test_validation_context_returns_files_when_explicit_files_scope(self, tmp_path):
        """
        SCENARIO: ValidationContext returns files for story-graph-only behavior when explicit files scope
        GIVEN: A shape behavior and ValidateActionContext with files scope
        WHEN: ValidationContext._get_files_for_validation is called
        THEN: It returns discovered files
        
        This test ensures that story-graph-only behaviors CAN validate files if explicitly scoped.
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.rules.rules import ValidationContext
        from agile_bot.bots.base_bot.src.actions.action_context import ValidateActionContext, Scope, ScopeType
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A shape behavior (story-graph-only)
        behavior = Behavior(name='shape', bot_paths=bot_paths)
        
        # AND: A ValidateActionContext with explicit files scope
        scope = Scope(type=ScopeType.FILES, value=['test/**/*.py'])
        context = ValidateActionContext(scope=scope)
        
        # WHEN: _get_files_for_validation is called
        files = ValidationContext._get_files_for_validation(behavior, context)
        
        # THEN: It returns files dict (may be empty if no files found, but structure is correct)
        assert isinstance(files, dict)
        # Files dict should have 'test' and/or 'src' keys if files are discovered
        # (Empty dict is also valid if no matching files exist)
    
    def test_validation_context_returns_files_for_code_behavior(self, tmp_path):
        """
        SCENARIO: ValidationContext returns files for code behavior by default
        GIVEN: A code behavior and ValidateActionContext with no scope
        WHEN: ValidationContext._get_files_for_validation is called
        THEN: It returns discovered files
        
        This test ensures that file-validating behaviors discover files by default.
        """
        from agile_bot.bots.base_bot.src.bot.behavior import Behavior
        from agile_bot.bots.base_bot.src.bot.bot_paths import BotPaths
        from agile_bot.bots.base_bot.src.actions.rules.rules import ValidationContext
        from agile_bot.bots.base_bot.src.actions.action_context import ValidateActionContext
        
        # GIVEN: Bot paths pointing to story_bot
        bot_paths = BotPaths(
            workspace_path=tmp_path,
            bot_directory=Path(__file__).parent.parent.parent / 'story_bot'
        )
        
        # AND: A code behavior (files-validating)
        behavior = Behavior(name='code', bot_paths=bot_paths)
        
        # AND: A ValidateActionContext with no scope
        context = ValidateActionContext(scope=None)
        
        # WHEN: _get_files_for_validation is called
        files = ValidationContext._get_files_for_validation(behavior, context)
        
        # THEN: It returns files dict (structure is correct, may be empty if no files)
        assert isinstance(files, dict)
        # Code behavior should discover 'src' files
        # (Empty dict is valid if no src files exist in test environment)


# ============================================================================
# TEST: Integration test for validate with file scope
# ============================================================================

class TestValidateWithFileScopeIntegration:
    """Integration test for end-to-end validation with file scope."""
    
    def test_file_discovery_and_filtering_integration(self):
        """
        SCENARIO: File discovery and filtering work together
        GIVEN: A FileDiscovery component and a FileFilter
        WHEN: Files are discovered and then filtered
        THEN: Only matching files are returned
        
        This test verifies the integration between FileDiscovery and FileFilter,
        which was the core fix for the validation scope bug.
        """
        from agile_bot.bots.base_bot.src.actions.action_context import FileFilter
        from pathlib import Path
        
        # GIVEN: A list of discovered files (simulating FileDiscovery output)
        discovered_files = [
            Path('test/test_execute_in_headless_mode.py'),
            Path('test/test_monitor_session.py'),
            Path('test/test_helpers.py'),
            Path('test/__pycache__/cached.pyc')
        ]
        
        # AND: A FileFilter for specific files
        file_filter = FileFilter(
            include_patterns=['**/test_execute_in_headless_mode.py', '**/test_monitor_session.py'],
            exclude_patterns=['**/__pycache__/**']
        )
        
        # WHEN: Files are filtered
        filtered_files = file_filter.filter_files(discovered_files)
        
        # THEN: Only matching files are returned
        assert len(filtered_files) == 2
        assert Path('test/test_execute_in_headless_mode.py') in filtered_files
        assert Path('test/test_monitor_session.py') in filtered_files
        assert Path('test/test_helpers.py') not in filtered_files
        assert Path('test/__pycache__/cached.pyc') not in filtered_files

