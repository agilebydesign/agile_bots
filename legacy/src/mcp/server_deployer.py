from pathlib import Path
import json
import sys
from typing import Optional
from dataclasses import dataclass
try:
    import requests
except ImportError:
    requests = None

@dataclass
class DeploymentResult:
    status: str
    server_name: str
    tool_count: int
    catalog_published: bool
    error_message: Optional[str] = None

@dataclass
class ToolEntry:
    name: str
    trigger_patterns: list
    behavior: Optional[str] = None
    description: str = ''

class ToolCatalog:

    def __init__(self):
        self.tools = {}

    def add_tool(self, tool_entry: ToolEntry):
        self.tools[tool_entry.name] = tool_entry

    def get_tool(self, name: str) -> ToolEntry:
        return self.tools.get(name)

class ServerDeployer:

    def __init__(self, config_path: Path, workspace_root: Path, protocol_handler_url: Optional[str]=None):
        self.config_path = Path(config_path).resolve()
        self.workspace_root = Path(workspace_root).resolve()
        self.bot_name = self.config_path.parent.name
        self.bot_directory = self.config_path.parent
        if 'pytest' in sys.modules:
            print(f'DEBUG ServerDeployer.__init__: config_path={self.config_path}')
            print(f'DEBUG ServerDeployer.__init__: config_path.parent={self.config_path.parent}')
            print(f'DEBUG ServerDeployer.__init__: config_path.parent.name={self.config_path.parent.name}')
            print(f'DEBUG ServerDeployer.__init__: self.bot_name={self.bot_name}')
        self.protocol_handler_url = protocol_handler_url
        self.catalog = ToolCatalog()

    def _discover_behaviors_from_folders(self) -> list:
        behaviors_dir = self.bot_directory / 'behaviors'
        if not behaviors_dir.exists():
            return []
        behaviors = []
        for item in sorted(behaviors_dir.iterdir()):
            if item.is_dir() and (not item.name.startswith('_')) and (not item.name.startswith('.')):
                if (item / 'behavior.json').exists():
                    behaviors.append(item.name)
        return behaviors

    def deploy_server(self) -> DeploymentResult:
        config_error = self._validate_config()
        self._validate_protocol_handler()
        behaviors = self._discover_behaviors_from_folders()
        tool_count = 5 + len(behaviors)
        return DeploymentResult(status='running', server_name=f'{self.bot_name}_server', tool_count=tool_count, catalog_published=True)

    def _validate_config(self) -> DeploymentResult:
        if not self.config_path.exists():
            return DeploymentResult(status='failed', server_name=f'{self.bot_name}_server', tool_count=0, catalog_published=False, error_message=f'Bot Config not found at {self.config_path}')
        return None

    def _validate_protocol_handler(self):
        if not self.protocol_handler_url:
            return
        if requests is None:
            raise ImportError('requests library is required for protocol handler validation')
        try:
            response = requests.get(self.protocol_handler_url, timeout=1)
            response.raise_for_status()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
            raise ConnectionError(f'MCP Protocol Handler not accessible at {self.protocol_handler_url}')

    def get_tool_catalog(self) -> ToolCatalog:
        if not self.config_path.exists():
            return self.catalog
        behaviors = self._discover_behaviors_from_folders()
        base_tools = [
            ToolEntry(name='tool', trigger_patterns=[], description=f'Bot tool for {self.bot_name} - routes to current behavior and action'),
            ToolEntry(name='get_working_dir', trigger_patterns=[], description='Get the current working directory from WORKING_AREA'),
            ToolEntry(name='set_working_dir', trigger_patterns=['working directory', 'working path', 'working folder', 'change working directory', 'update working path'], description='Update WORKING_AREA/WORKING_DIR to a new path (persist to bot_config)'),
            ToolEntry(name='close_current_action', trigger_patterns=[], description=f'Close current action tool for {self.bot_name} - marks current action complete and transitions to next'),
            ToolEntry(name='confirm_out_of_order', trigger_patterns=[], description=f'Confirm out-of-order behavior execution for {self.bot_name}'),
            ToolEntry(name='restart_server', trigger_patterns=[], description=f'Restart MCP server for {self.bot_name} - terminates processes, clears cache, and restarts to load code changes')
        ]
        for tool in base_tools:
            self.catalog.add_tool(tool)
        for behavior in behaviors:
            trigger_patterns = self._load_trigger_words(behavior)
            tool_entry = ToolEntry(name=behavior, trigger_patterns=trigger_patterns, behavior=behavior, description=f'{behavior} behavior for {self.bot_name}. Accepts optional action parameter and parameters dict.')
            self.catalog.add_tool(tool_entry)
        return self.catalog

    def _load_trigger_words(self, behavior: str) -> list:
        behavior_file = self.bot_directory / 'behaviors' / behavior / 'behavior.json'
        if not behavior_file.exists():
            return []
        try:
            behavior_data = json.loads(behavior_file.read_text(encoding='utf-8'))
            trigger_words = behavior_data.get('trigger_words', {})
            return trigger_words.get('patterns', [])
        except (json.JSONDecodeError, KeyError):
            return []