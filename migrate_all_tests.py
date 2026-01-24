"""
Automated Test Migration Script
Migrates all test files according to the test-reorganization-plan.md
"""
import os
import re
import shutil
from pathlib import Path


def update_imports(content):
    """Update import statements to use new helpers location"""
    content = content.replace('from domain.bot_test_helper import BotTestHelper', 
                             'from helpers.bot_test_helper import BotTestHelper')
    content = content.replace('from CLI.helpers import', 'from helpers import')
    content = content.replace('from domain.helpers', 'from helpers')
    return content


def create_merged_file(domain_file, cli_file, output_file, title, subepic):
    """Merge domain and CLI test files into one"""
    print(f"\nMerging: {title}")
    print(f"  Domain: {domain_file}")
    print(f"  CLI: {cli_file}")
    print(f"  Output: {output_file}")
    
    domain_content = ""
    cli_content = ""
    
    # Read domain file if it exists
    if domain_file and os.path.exists(domain_file):
        with open(domain_file, 'r', encoding='utf-8') as f:
            domain_content = f.read()
        domain_content = update_imports(domain_content)
        # Extract test classes (remove imports and docstrings at top)
        domain_content = re.sub(r'^.*?(?=class Test)', '', domain_content, flags=re.DOTALL)
    
    # Read CLI file if it exists
    if cli_file and os.path.exists(cli_file):
        with open(cli_file, 'r', encoding='utf-8') as f:
            cli_content = f.read()
        cli_content = update_imports(cli_content)
        # Extract test classes
        cli_content = re.sub(r'^.*?(?=class Test)', '', cli_content, flags=re.DOTALL)
    
    # Create header
    header = f'''"""
{title}

SubEpic: {subepic}
Parent Epic: Invoke Bot

Combines domain logic tests with CLI-specific display tests.
Uses parameterized tests across TTY, Pipe, and JSON channels for CLI tests.
"""
import re
import pytest
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


# ============================================================================
# DOMAIN TESTS - Core Domain Logic
# ============================================================================

'''
    
    cli_section = '''

# ============================================================================
# CLI TESTS - CLI-Specific Display and Commands
# ============================================================================

'''
    
    # Write merged file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)
        if domain_content:
            f.write(domain_content)
        if cli_content:
            f.write(cli_section + cli_content)
    
    print(f"  ✓ Created: {output_file}")


# Simple merges (1-to-1 mapping)
simple_merges = [
    # Already completed:
    # - test_get_help_using_cli.py ✓
    # - test_edit_story_nodes.py ✓
]

print("=" * 80)
print("TEST MIGRATION - Simple Merges")
print("=" * 80)

# Note: test_get_help_using_cli.py and test_edit_story_nodes.py already done

print("\n✓ Simple merges completed: test_get_help_using_cli.py, test_edit_story_nodes.py")

print("\n" + "=" * 80)
print("MIGRATION COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Complex files need manual splitting (see test-reorganization-plan.md)")
print("2. Update pytest.ini configuration")
print("3. Run tests to verify migrations")
print("4. Delete old files after verification")
