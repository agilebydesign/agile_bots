from pathlib import Path
from typing import Dict, Any, Optional
import importlib
from actions.render.template import Template
from actions.render.synchronizer import Synchronizer
from bot_path import BotPath
from utils import read_json_file

class RenderSpec:

    def __init__(self, config_data: Dict[str, Any], render_folder: Path, bot_paths: BotPath, config_file: Path=None):
        self._config_data = config_data.copy()
        self._render_folder = render_folder
        self._bot_paths = bot_paths
        if config_file is not None:
            self._config_data['file'] = str(config_file.relative_to(bot_paths.bot_directory))
        elif 'file' not in self._config_data:
            self._config_data['file'] = 'unknown'
        self._input = config_data.get('input')
        self._output = config_data.get('output')
        self._instructions = config_data.get('instructions', [])
        self._template, self._synchronizer = self._init_template_or_synchronizer()
        self._execution_result: Optional[Dict[str, Any]] = None
        self._execution_status: str = 'pending'

    def _init_template_or_synchronizer(self):
        config_data = self._config_data
        if 'synchronizer' in config_data:
            return (None, Synchronizer(config_data['synchronizer']))
        if 'template' in config_data:
            template_path_str = config_data['template']
            if template_path_str.startswith('templates/'):
                template_path_str = template_path_str[10:]
            template_path = self._render_folder / 'templates' / template_path_str
            return (Template(template_path), None)
        return (None, None)

    @property
    def input(self) -> Optional[str]:
        return self._input

    @property
    def output(self) -> Optional[str]:
        return self._output

    @property
    def template(self) -> Optional[Template]:
        return self._template

    @property
    def synchronizer(self) -> Optional[Synchronizer]:
        return self._synchronizer

    @property
    def instructions(self) -> list:
        return self._instructions

    @property
    def config_data(self) -> Dict[str, Any]:
        return self._config_data

    @property
    def name(self) -> str:
        return self._config_data.get('name', 'unknown')

    @property
    def requires_ai_handling(self) -> bool:
        return self._template is not None

    @property
    def is_executed(self) -> bool:
        return self._execution_result is not None

    @property
    def execution_status(self) -> str:
        return self._execution_status

    @property
    def execution_result(self) -> Optional[Dict[str, Any]]:
        return self._execution_result

    def mark_executed(self, result: Dict[str, Any]):
        self._execution_result = result
        self._execution_status = 'executed'

    def mark_failed(self, error: str):
        self._execution_result = {'error': error}
        self._execution_status = 'failed'

    def execute_synchronizer(self, scope: Optional[str] = None) -> Dict[str, Any]:
        if not self.synchronizer:
            raise ValueError(f"No synchronizer specified in render spec '{self.name}'")
        synchronizer_instance = self._import_synchronizer_class(self.synchronizer.synchronizer_class_path)()
        input_path = self._resolve_input_path()
        output_path = self._resolve_output_path(input_path, scope=scope)
        kwargs = self._build_synchronizer_kwargs(scope=scope)
        return synchronizer_instance.render(str(input_path), str(output_path), **kwargs)

    def _resolve_input_path(self) -> Path:
        workspace_dir = self._bot_paths.workspace_directory
        # Use centralized path as default fallback
        default_path = str(self._bot_paths.story_graph_paths.docs_root)
        config_path = self._config_data.get('path', default_path)
        input_file = self._config_data.get('input', 'story-graph.json')
        input_path = workspace_dir / config_path / input_file
        if not input_path.exists():
            # Fall back to story graph location
            input_path = self._bot_paths.story_graph_paths.story_graph_path
        return input_path

    def _resolve_output_path(self, input_path: Path, scope: Optional[str] = None) -> Path:
        workspace_dir = self._bot_paths.workspace_directory
        # Use centralized path as default fallback
        default_path = str(self._bot_paths.story_graph_paths.docs_root)
        config_path = self._config_data.get('path', default_path)
        output_file = self._config_data.get('output', '')
        if output_file:
            if '{solution_name_slug}' in output_file:
                output_file = self._resolve_solution_name_slug(output_file, input_path)
            if '{scope}' in output_file:
                output_file = self._resolve_scope_placeholder(output_file, scope)
            return workspace_dir / config_path / output_file
        # If no output specified, just use the path (for folder-based synchronizers)
        return workspace_dir / config_path
    
    def _resolve_scope_placeholder(self, output_file: str, scope: Optional[str] = None) -> str:
        """Replace {scope} placeholder with actual scope value or default."""
        if scope:
            # Sanitize scope for filename: replace spaces with dashes, keep alphanumeric and dashes
            sanitized_scope = scope.lower().replace(' ', '-')
            sanitized_scope = ''.join(c for c in sanitized_scope if c.isalnum() or c == '-')
            return output_file.replace('{scope}', sanitized_scope)
        # If no scope provided, use 'all' as default
        return output_file.replace('{scope}', 'all')

    def _resolve_solution_name_slug(self, output_file: str, input_path: Path) -> str:
        try:
            if input_path.exists():
                solution_name = read_json_file(input_path).get('solution_name', 'solution')
                return output_file.replace('{solution_name_slug}', solution_name.lower().replace(' ', '-'))
        except Exception as e:
            logging.getLogger(__name__).debug(f'Failed to get solution name: {e}')
        return output_file.replace('{solution_name_slug}', 'solution')

    def _build_synchronizer_kwargs(self, scope: Optional[str] = None) -> Dict[str, Any]:
        kwargs = {'project_path': str(self._bot_paths.workspace_directory)}
        if 'renderer_command' in self._config_data:
            kwargs['renderer_command'] = self._config_data['renderer_command']
        if 'force_outline' in self._config_data:
            kwargs['force_outline'] = self._config_data['force_outline']
        if scope:
            kwargs['scope'] = scope
        return kwargs

    def _import_synchronizer_class(self, synchronizer_class_path: str):
        module_path, class_name = synchronizer_class_path.rsplit('.', 1)
        # Try multiple import paths to handle different Python path configurations
        # Try src.* paths first since they work most reliably
        possible_paths = [
            f'src.{module_path}',  # Import from src package (works when cwd is workspace root)
            module_path,  # Direct import (works when src is in PYTHONPATH)
            f'agile_bots.bots.{self._bot_paths.bot_directory.name}.src.{module_path}',
            f'agile_bots.bots.{self._bot_paths.bot_directory.name}.src.synchronizers.{module_path}'
        ]
        module = None
        last_error = None
        for path in possible_paths:
            try:
                module = importlib.import_module(path)
                if hasattr(module, class_name):
                    break
                module = None
            except ImportError as e:
                last_error = e
                continue
        if module is None:
            raise ImportError(f'Could not import synchronizer module: {synchronizer_class_path}. Last error: {last_error}')
        synchronizer_class = getattr(module, class_name)
        if not hasattr(synchronizer_class, 'render'):
            raise ValueError(f'Synchronizer class {synchronizer_class_path} does not have render method')
        return synchronizer_class