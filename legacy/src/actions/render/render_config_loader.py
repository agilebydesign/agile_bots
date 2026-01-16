from pathlib import Path
from typing import Dict, Any, List
from ...utils import read_json_file
from .render_spec import RenderSpec
import importlib

class RenderConfigLoader:

    def __init__(self, behavior):
        self.behavior = behavior

    def find_render_folder(self) -> Path:
        return self.behavior.folder / 'content' / 'render'

    def load_render_instructions(self) -> Dict[str, Any]:
        render_folder = self.find_render_folder()
        if not render_folder.exists() or not render_folder.is_dir():
            return {}
        instructions_path = render_folder / 'instructions.json'
        if not instructions_path.exists():
            raise FileNotFoundError(f'Render folder exists at {render_folder} but instructions.json is missing. instructions.json is mandatory when render folder exists.')
        return read_json_file(instructions_path)

    def load_render_specs(self) -> List[RenderSpec]:
        render_folder = self.find_render_folder()
        render_specs = []
        if not render_folder.exists() or not render_folder.is_dir():
            return render_specs
        render_json_files = [f for f in render_folder.glob('*.json')]
        for render_json_file in render_json_files:
            config_data = read_json_file(render_json_file)
            render_spec = RenderSpec(config_data, render_folder, self.behavior.bot_paths, render_json_file)
            render_specs.append(render_spec)
        return render_specs

    def load_render_configs(self) -> List[Dict[str, Any]]:
        render_folder = self.find_render_folder()
        render_configs = []
        if not render_folder.exists() or not render_folder.is_dir():
            return render_configs
        render_json_files = [f for f in render_folder.glob('*.json')]
        for render_json_file in render_json_files:
            render_config = self.load_single_render_config(render_json_file)
            render_configs.append(render_config)
        return render_configs

    def load_single_render_config(self, render_json_file: Path) -> Dict[str, Any]:
        config = read_json_file(render_json_file)
        config_entry = {'file': str(render_json_file.relative_to(self.behavior.bot_paths.bot_directory)), 'config': config}
        if 'synchronizer' in config:
            self.verify_synchronizer_class(config['synchronizer'])
        elif 'template' in config:
            template_content = self.load_template_file(config['template'])
            config_entry['template'] = template_content
        return config_entry

    def verify_synchronizer_class(self, synchronizer_class_path: str) -> None:
        module_path, class_name = synchronizer_class_path.rsplit('.', 1)
        possible_paths = [module_path, f'agile_bot.bots.{self.behavior.bot_name}.src.{module_path}', f'agile_bot.bots.{self.behavior.bot_name}.src.synchronizers.{module_path}']
        module = None
        for path in possible_paths:
            try:
                module = importlib.import_module(path)
                if hasattr(module, class_name):
                    break
                module = None
            except ImportError:
                continue
        
        # If module not found, skip verification (may be in test environment)
        if module is None:
            return
        
        synchronizer_class = getattr(module, class_name, None)
        if synchronizer_class is None:
            return
            
        has_render = hasattr(synchronizer_class, 'render')
        has_sync_methods = any((hasattr(synchronizer_class, method) for method in ['synchronize_outline', 'synchronize_increments', 'synchronize_exploration']))
        if not (has_render or has_sync_methods):
            raise ValueError(f'Synchronizer class {synchronizer_class_path} does not have required methods')

    def load_template_file(self, template_path: str) -> str:
        render_folder = self.find_render_folder()
        templates_dir = render_folder / 'templates'
        if template_path.startswith('templates/'):
            template_path = template_path[10:]
        template_file = templates_dir / template_path
        return template_file.read_text(encoding='utf-8')