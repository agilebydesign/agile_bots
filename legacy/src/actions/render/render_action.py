from pathlib import Path
from typing import Dict, Any, List, Optional, Type
import json
import importlib
import logging
from ...utils import read_json_file
from ..action import Action
from ..action_context import ActionContext, ScopeActionContext
from .render_spec import RenderSpec
from .render_config_loader import RenderConfigLoader
from .render_instruction_builder import RenderInstructionBuilder
from ...bot.merged_instructions import MergedInstructions
logger = logging.getLogger(__name__)

class RenderOutputAction(Action):
    context_class: Type[ActionContext] = ScopeActionContext

    def __init__(self, behavior=None, action_config=None):
        super().__init__(behavior=behavior, action_config=action_config)
        self._config_loader = RenderConfigLoader(self.behavior)
        self._instruction_formatter = RenderInstructionBuilder()
        self._render_specs: List[RenderSpec] = self._config_loader.load_render_specs()

    @property
    def action_name(self) -> str:
        return 'render'

    @action_name.setter
    def action_name(self, value: str):
        raise AttributeError('action_name is read-only for RenderOutputAction')

    def _execute_synchronizers(self, render_specs: List['RenderSpec']) -> None:
        """Execute synchronizers for all render specs."""
        for spec in render_specs:
            if spec.synchronizer:
                try:
                    result = spec.execute_synchronizer()
                    spec.mark_executed(result)
                    logger.info(f"Executed synchronizer for {spec.name}: {result.get('output_path', 'N/A')}")
                except Exception as e:
                    logger.error(f'Failed to execute synchronizer for {spec.name}: {e}')
                    spec.mark_failed(str(e))
    
    def _prepare_instructions(self, instructions, context: ScopeActionContext):
        """Prepare render instructions with render specs and templates."""
        render_instructions = self._config_loader.load_render_instructions()
        render_specs = self._render_specs
        
        # Execute synchronizers during preparation
        self._execute_synchronizers(render_specs)
        
        # Merge and inject render data
        merged_instructions = MergedInstructions(
            base_instructions=instructions.get('base_instructions', []),
            render_instructions=render_instructions
        ).merge()
        self._instruction_formatter.inject_render_data(merged_instructions, render_instructions, render_specs)
        
        # Store render specs for later use
        executed_specs = [spec for spec in render_specs if spec.is_executed]
        template_specs = [spec for spec in render_specs if spec.requires_ai_handling and (not spec.is_executed)]
        
        # Update instructions with properly formatted data from merged_instructions dict
        instructions._data['base_instructions'] = merged_instructions.get('base_instructions', [])
        instructions.set('render_instructions', merged_instructions.get('render_instructions', {}))
        instructions.set('render_configs', merged_instructions.get('render_configs', []))
        instructions.set('executed_configs', merged_instructions.get('executed_configs', []))
        if 'workspace_path' in merged_instructions:
            instructions.set('workspace_path', merged_instructions['workspace_path'])
        instructions.set('executed_specs', [spec.config_data for spec in executed_specs])
        instructions.set('template_specs', [spec.config_data for spec in template_specs])
        
        # Add render config file paths for display panel (similar to build action's config/template paths)
        render_config_paths = []
        render_template_paths = []
        render_output_paths = []
        
        bot_dir = self.behavior.bot_paths.bot_directory
        workspace_dir = self.behavior.bot_paths.workspace_directory
        
        for spec in render_specs:
            # Add the render config file path (stored as relative path in config_data['file'])
            if 'file' in spec.config_data:
                config_file_rel = spec.config_data['file']
                config_file_abs = bot_dir / config_file_rel
                if config_file_abs.exists():
                    render_config_paths.append(str(config_file_abs.resolve()))
            
            # Add template file path if using template
            if spec.template and hasattr(spec.template, 'template_path'):
                template_path = spec.template.template_path
                if template_path:
                    render_template_paths.append(str(template_path.resolve()))
            
            # Add output file path (drawio, md, txt, etc.)
            if spec.output:
                # Get the path prefix
                path_prefix = spec.config_data.get('path', 'docs/stories')
                output_file_abs = workspace_dir / path_prefix / spec.output
                render_output_paths.append(str(output_file_abs.resolve()))
        
        # Store as separate arrays like build action does
        if render_config_paths:
            instructions._data['render_config_paths'] = render_config_paths
        if render_template_paths:
            instructions._data['render_template_paths'] = render_template_paths
        if render_output_paths:
            instructions._data['render_output_paths'] = render_output_paths
    
    def _do_confirm(self, context: ScopeActionContext) -> Dict[str, Any]:
        """Render actions execute synchronizers during preparation."""
        return {
            'message': 'Render instructions provided to AI - documents will be rendered by AI'
        }
    
    def do_execute(self, context: ScopeActionContext) -> Dict[str, Any]:
        """Legacy method for backwards compatibility."""
        render_instructions = self._config_loader.load_render_instructions()
        render_specs = self._render_specs
        self._execute_synchronizers(render_specs)
        instructions = MergedInstructions(base_instructions=self.instructions.get('base_instructions', []) if isinstance(self.instructions, dict) else self.instructions['base_instructions'], render_instructions=render_instructions).merge()
        self._instruction_formatter.inject_render_data(instructions, render_instructions, render_specs)
        executed_specs = [spec for spec in render_specs if spec.is_executed]
        template_specs = [spec for spec in render_specs if spec.requires_ai_handling and (not spec.is_executed)]
        return {'instructions': instructions, 'executed_specs': [spec.config_data for spec in executed_specs], 'template_specs': [spec.config_data for spec in template_specs]}

    @property
    def render_specs(self) -> List[RenderSpec]:
        return self._render_specs

    @property
    def templates(self) -> List:
        templates = []
        for spec in self._render_specs:
            if spec.template:
                templates.append(spec.template)
        return templates

    @property
    def synchronizers(self) -> List:
        synchronizers = []
        for spec in self._render_specs:
            if spec.synchronizer:
                synchronizers.append(spec.synchronizer)
        return synchronizers

    def inject_next_action_instructions(self):
        return 'Proceed to validate action'