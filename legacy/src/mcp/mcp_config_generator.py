import json
import logging
from pathlib import Path
from typing import Dict, Any
from ..bot.workspace import get_python_workspace_root
from ..utils import read_json_file
logger = logging.getLogger(__name__)

class MCPConfigGenerator:

    def __init__(self, bot_name: str, bot_directory: Path, config_path: Path):
        self.bot_name = bot_name
        self.bot_directory = bot_directory
        self.config_path = config_path

    def generate_bot_config_file(self, behaviors: list) -> Path:
        config_path = self.bot_directory / 'bot_config.json'
        if config_path.exists():
            return config_path
        config_data = {'name': self.bot_name}
        config_path.write_text(json.dumps(config_data, indent=2), encoding='utf-8')
        return config_path

    def generate_cursor_mcp_config(self) -> Dict:
        server_path = str(self.bot_directory / 'src' / f'{self.bot_name}_mcp_server.py')
        repo_root = str(get_python_workspace_root())
        mcp_config = {'mcpServers': {f"{self.bot_name.replace('_', '-')}": {'command': 'python', 'args': [server_path], 'cwd': repo_root}}}
        return mcp_config

    def generate_workspace_rules_file(self, discover_behaviors_fn, load_trigger_info_fn) -> Path:
        rules_file = self._get_rules_file_path()
        behaviors = discover_behaviors_fn()
        bot_config = read_json_file(self.config_path)
        behavior_info = self._load_behavior_info(behaviors, load_trigger_info_fn)
        behavior_sections_str = self._build_behavior_sections(behaviors, behavior_info)
        rules_content = self._generate_rules_content(bot_config, behaviors, behavior_info, behavior_sections_str)
        rules_file.write_text(rules_content, encoding='utf-8')
        return rules_file

    def _get_rules_file_path(self) -> Path:
        repo_root = get_python_workspace_root()
        rules_dir = repo_root / '.cursor' / 'rules'
        rules_dir.mkdir(parents=True, exist_ok=True)
        bot_name_with_hyphens = self.bot_name.replace('_', '-')
        return rules_dir / f'mcp-{bot_name_with_hyphens}-awareness.mdc'

    def _load_behavior_info(self, behaviors: list, load_trigger_info_fn) -> dict:
        info = {'trigger_words': {}, 'descriptions': {}}
        for behavior in behaviors:
            result = load_trigger_info_fn(behavior)
            if result:
                info['descriptions'][behavior] = result['description']
                if result['trigger_words']:
                    info['trigger_words'][behavior] = result['trigger_words']
        return info

    def _build_behavior_sections(self, behaviors: list, behavior_info: dict) -> str:
        sections = []
        for behavior in behaviors:
            section = self._build_single_behavior_section(behavior, behavior_info)
            if section:
                sections.append(section)
        return '\n'.join(sections)

    def _build_single_behavior_section(self, behavior: str, behavior_info: dict) -> str:
        trigger_words = behavior_info['trigger_words'].get(behavior, [])
        if not trigger_words:
            return ''
        behavior_display_name = behavior.replace('_', ' ').title()
        trigger_words_str = ', '.join(trigger_words)
        behavior_desc = behavior_info['descriptions'].get(behavior, '')
        if behavior_desc:
            return f'### {behavior_display_name} Behavior\n\n**When user is trying to:** {behavior_desc}  \n**as indicated by Trigger words:** {trigger_words_str}\n\n**Then check for:** `{self.bot_name}_{behavior}_<action>` tool\n\n**Example:** "{trigger_words[0]}" -> use `{self.bot_name}_{behavior}_clarify`\n\n'
        else:
            return f'### {behavior_display_name} Behavior\n**Trigger words:** {trigger_words_str}\n**Tool pattern:** `{self.bot_name}_{behavior}_<action>`\n**Example:** "{trigger_words[0]}" -> use `{self.bot_name}_{behavior}_clarify`\n\n'

    def _generate_rules_content(self, bot_config: dict, behaviors: list, behavior_info: dict, behavior_sections_str: str) -> str:
        bot_goal = bot_config.get('goal', '')
        bot_description = bot_config.get('description', '')
        goal_line = f'\n**Bot Goal:** {bot_goal}\n' if bot_goal else ''
        desc_line = f'**Bot Description:** {bot_description}\n' if bot_description else ''
        critical_rule = self._build_critical_rule(bot_goal)
        example_trigger = self._get_example_trigger(behaviors, behavior_info)
        example_behavior = behaviors[0] if behaviors else 'behavior'
        return f'# MCP Tool Awareness\n\n## Bot: {self.bot_name}\n\n## Priority: Check MCP Tools First\n\n{critical_rule}\n\n## Behaviors and Trigger Words\n\n{behavior_sections_str}\n\n## Error Handling\n\n**CRITICAL:** If a registered tool is broken or returns an error:\n\n1. **DO NOT automatically attempt a workaround**\n2. **Inform user of the exact error details** (include full error message, tool name, parameters used)\n3. **Ask user:** "The tool returned an error. Should I attempt to repair the tool, or proceed manually?"\n4. **Wait for user decision** before taking any action\n\n## Workflow Pattern\n\nWhen you recognize a trigger word:\n\n1. **Check if MCP tools are available** (ask mode vs agent mode)\n2. **If in ask mode:** Inform user to switch to agent mode for MCP tool access\n3. **If in agent mode:** Look for matching MCP tool and invoke it\n4. **If tool returns error:** Follow error handling above (do NOT workaround)\n5. **If no matching tool found:** Fall back to manual operations with explanation\n\n## Example Usage\n\n**User says:** "{example_trigger}"\n\n**AI should:**\n1. Recognize trigger word from behavior section above\n2. Check: Am I in agent mode?\n3. Check: Is `{self.bot_name}_{example_behavior}_clarify` available?\n4. If yes -> Invoke the tool\n5. If no -> Explain and ask how to proceed\n\n**DO NOT** immediately start reading files manually without checking for tools first.\n'

    def _build_critical_rule(self, bot_goal: str) -> str:
        if bot_goal:
            return f'**CRITICAL RULE:** When user is trying to {bot_goal.lower()}, ALWAYS check for and use MCP {self.bot_name} tools FIRST before falling back to manual file operations.'
        return f'**CRITICAL RULE:** When user mentions workflow operations with trigger words, ALWAYS check for and use MCP {self.bot_name} tools FIRST before falling back to manual file operations.'

    def _get_example_trigger(self, behaviors: list, behavior_info: dict) -> str:
        if behaviors and behavior_info['trigger_words']:
            return behavior_info['trigger_words'].get(behaviors[0], [behaviors[0]])[0]
        return 'trigger word'