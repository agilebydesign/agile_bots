import re

# Read both files
with open('test/domain/test_edit_story_graph.py', 'r', encoding='utf-8') as f:
    domain_content = f.read()

with open('test/CLI/test_edit_story_graph_in_cli.py', 'r', encoding='utf-8') as f:
    cli_content = f.read()

# Update imports in domain content
domain_content = domain_content.replace('from domain.bot_test_helper import BotTestHelper', 'from helpers.bot_test_helper import BotTestHelper')

# Update imports in CLI content
cli_content = cli_content.replace('from CLI.helpers import', 'from helpers import')

# Create merged file header
header = '''"""
Test Edit Story Nodes

SubEpic: Edit Story Nodes
Parent Epic: Invoke Bot > Edit Story Map

Tests for editing story graph hierarchy including:
- Creating Epics at root level
- Creating child story nodes
- Deleting story nodes
- Updating story node names
- Moving story nodes between parents
- Executing actions scoped to story nodes

Combines domain logic tests with CLI-specific display tests.
Uses parameterized tests across TTY, Pipe, and JSON channels for CLI tests.
"""
import re
import pytest
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


# ============================================================================
# DOMAIN TESTS - Core Story Graph Editing Logic
# ============================================================================

'''

# Extract domain test classes (remove imports and comments at top)
domain_tests = re.sub(r'^.*?(?=class Test)', '', domain_content, flags=re.DOTALL)

# Extract CLI test classes (remove imports and comments at top)
cli_tests = re.sub(r'^.*?(?=# ===)', '', cli_content, flags=re.DOTALL)
cli_tests = '''
# ============================================================================
# CLI TESTS - Story Graph Editing via CLI Commands
# ============================================================================

''' + cli_tests

# Write merged file
with open('test/invoke_bot/test_edit_story_nodes.py', 'w', encoding='utf-8') as f:
    f.write(header + domain_tests + '\n\n' + cli_tests)

print('Successfully merged test_edit_story_nodes.py')
print(f'Domain content: {len(domain_tests)} chars')
print(f'CLI content: {len(cli_tests)} chars')
