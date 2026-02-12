from pathlib import Path
from typing import Dict, Any, List, Optional, Type
import json
import importlib
import logging
from utils import read_json_file
from actions.action import Action
from actions.action_context import ActionContext, ScopeActionContext
from actions.render.render_spec import RenderSpec
from actions.render.render_config_loader import RenderConfigLoader
from actions.render.render_instruction_builder import RenderInstructionBuilder
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

    def _execute_synchronizers(self, render_specs: List['RenderSpec'], context: ScopeActionContext = None) -> None:
        # Extract scope value from context if available
        scope_value = None
        if context and context.scope and context.scope.value:
            # Use first scope value for filename placeholder
            scope_value = context.scope.value[0] if context.scope.value else None
        
        for spec in render_specs:
            if spec.synchronizer:
                try:
                    result = spec.execute_synchronizer(scope=scope_value)
                    spec.mark_executed(result)
                    logger.info(f"Executed synchronizer for {spec.name}: {result.get('output_path', 'N/A')}")
                except Exception as e:
                    logger.error(f'Failed to execute synchronizer for {spec.name}: {e}')
                    spec.mark_failed(str(e))
    
    def _prepare_instructions(self, instructions, context: ScopeActionContext):
        render_instructions = self._config_loader.load_render_instructions()
        render_specs = self._render_specs
        
        self._execute_synchronizers(render_specs, context=context)
        
        merged_data = {
            'base_instructions': instructions.get('base_instructions', []),
            'render_instructions': render_instructions
        }
        self._instruction_formatter.inject_render_data(merged_data, render_instructions, render_specs)
        
        executed_specs = [spec for spec in render_specs if spec.is_executed]
        template_specs = [spec for spec in render_specs if spec.requires_ai_handling and (not spec.is_executed)]
        
        instructions._data['base_instructions'] = merged_data.get('base_instructions', [])
        instructions.set('render_instructions', merged_data.get('render_instructions', {}))
        instructions.set('render_configs', merged_data.get('render_configs', []))
        instructions.set('executed_configs', merged_data.get('executed_configs', []))
        if 'workspace_path' in merged_data:
            instructions.set('workspace_path', merged_data['workspace_path'])
        instructions.set('executed_specs', [spec.config_data for spec in executed_specs])
        instructions.set('template_specs', [spec.config_data for spec in template_specs])
        
        render_config_paths = []
        render_template_paths = []
        render_output_paths = []
        
        bot_dir = self.behavior.bot_paths.bot_directory
        workspace_dir = self.behavior.bot_paths.workspace_directory
        
        for spec in render_specs:
            if 'file' in spec.config_data:
                config_file_rel = spec.config_data['file']
                config_file_abs = bot_dir / config_file_rel
                if config_file_abs.exists():
                    render_config_paths.append(str(config_file_abs.resolve()))
            
            if spec.template and hasattr(spec.template, 'template_path'):
                template_path = spec.template.template_path
                if template_path:
                    render_template_paths.append(str(template_path.resolve()))
            
            if spec.output:
                # Use centralized path as default fallback
                default_path = str(self.behavior.bot_paths.story_graph_paths.docs_root)
                path_prefix = spec.config_data.get('path', default_path)
                output_file_abs = workspace_dir / path_prefix / spec.output
                render_output_paths.append(str(output_file_abs.resolve()))
        
        if render_config_paths:
            instructions._data['render_config_paths'] = render_config_paths
        if render_template_paths:
            instructions._data['render_template_paths'] = render_template_paths
        if render_output_paths:
            instructions._data['render_output_paths'] = render_output_paths
        
        diagrams = self._collect_diagram_data(render_specs, workspace_dir)
        if diagrams:
            instructions._data['diagrams'] = diagrams
    
    def do_execute(self, context: ScopeActionContext = None):
        render_instructions = self._config_loader.load_render_instructions()
        render_specs = self._render_specs
        self._execute_synchronizers(render_specs, context=context)
        
        instructions = self.get_instructions(context)
        
        merged_data = {
            'base_instructions': instructions.get('base_instructions', []),
            'render_instructions': render_instructions
        }
        self._instruction_formatter.inject_render_data(merged_data, render_instructions, render_specs)
        
        instructions._data['base_instructions'] = merged_data.get('base_instructions', [])
        if 'render_instructions' in merged_data:
            instructions.set('render_instructions', merged_data['render_instructions'])
        
        executed_specs = [spec for spec in render_specs if spec.is_executed]
        template_specs = [spec for spec in render_specs if spec.requires_ai_handling and (not spec.is_executed)]
        if executed_specs:
            instructions.set('executed_specs', [spec.config_data for spec in executed_specs])
        if template_specs:
            instructions.set('template_specs', [spec.config_data for spec in template_specs])
        
        return instructions

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

    def _get_drawio_specs_with_paths(self) -> list:
        """Get drawio render specs paired with their resolved diagram paths."""
        workspace_dir = self.behavior.bot_paths.workspace_directory
        result = []
        for spec in self._render_specs:
            if not spec.output or not spec.output.endswith('.drawio'):
                continue
            default_path = str(self.behavior.bot_paths.story_graph_paths.docs_root)
            path_prefix = spec.config_data.get('path', default_path)
            diagram_path = workspace_dir / path_prefix / spec.output
            result.append((spec, diagram_path))
        return result

    def renderDiagram(self) -> Dict[str, Any]:
        """Re-render all DrawIO diagrams from story graph.
        CLI: <behavior>.render.renderDiagram
        """
        drawio_specs = self._get_drawio_specs_with_paths()
        if not drawio_specs:
            return {'status': 'error', 'message': 'No DrawIO render specs configured'}

        specs_only = [spec for spec, _ in drawio_specs]
        self._execute_synchronizers(specs_only)

        results = []
        for spec, diagram_path in drawio_specs:
            results.append({
                'diagram': spec.output,
                'status': spec.execution_status,
                'path': str(diagram_path)
            })

        rendered_count = sum(1 for r in results if r['status'] == 'executed')
        return {
            'status': 'success',
            'message': f'Rendered {rendered_count} diagram(s)',
            'results': results
        }

    def generateReport(self) -> Dict[str, Any]:
        """Extract from DrawIO diagrams and generate update reports.
        CLI: <behavior>.render.generateReport
        """
        from synchronizers.story_io.story_map_drawio_synchronizer import (
            synchronize_story_graph_from_drawio_outline,
            synchronize_story_graph_from_drawio_increments,
            generate_merge_report
        )
        import shutil

        story_graph_path = self.behavior.bot_paths.story_graph_paths.story_graph_path
        results = []

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            if not diagram_path.exists():
                continue

            extracted_path = diagram_path.parent / f"{diagram_path.stem}-extracted.json"

            try:
                if 'increment' in diagram_path.stem:
                    synchronize_story_graph_from_drawio_increments(
                        drawio_path=diagram_path,
                        output_path=extracted_path,
                        original_path=story_graph_path
                    )
                else:
                    synchronize_story_graph_from_drawio_outline(
                        drawio_path=diagram_path,
                        output_path=extracted_path,
                        original_path=story_graph_path
                    )

                merge_report_path = extracted_path.parent / f"{extracted_path.stem}-merge-report.json"
                update_report_path = diagram_path.parent / f"{diagram_path.stem}-update-report.json"

                if merge_report_path.exists():
                    shutil.copy2(str(merge_report_path), str(update_report_path))
                elif story_graph_path.exists():
                    generate_merge_report(extracted_path, story_graph_path, update_report_path)

                results.append({
                    'diagram': spec.output,
                    'status': 'success',
                    'report_path': str(update_report_path)
                })
            except Exception as e:
                logger.error(f'Failed to generate report for {spec.output}: {e}')
                results.append({
                    'diagram': spec.output,
                    'status': 'error',
                    'message': str(e)
                })

        return {
            'status': 'success',
            'message': f'Generated {len(results)} report(s)',
            'results': results
        }

    def updateFromDiagram(self) -> Dict[str, Any]:
        """Apply update reports to merge diagram changes into story graph.
        CLI: <behavior>.render.updateFromDiagram
        """
        from synchronizers.story_io.story_map_drawio_synchronizer import merge_story_graphs

        story_graph_path = self.behavior.bot_paths.story_graph_paths.story_graph_path
        results = []

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            extracted_path = diagram_path.parent / f"{diagram_path.stem}-extracted.json"
            update_report_path = diagram_path.parent / f"{diagram_path.stem}-update-report.json"

            if not extracted_path.exists() or not update_report_path.exists():
                continue

            try:
                result = merge_story_graphs(
                    extracted_path=extracted_path,
                    original_path=story_graph_path,
                    report_path=update_report_path,
                    output_path=story_graph_path
                )
                results.append({
                    'diagram': spec.output,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                logger.error(f'Failed to update from {spec.output}: {e}')
                results.append({
                    'diagram': spec.output,
                    'status': 'error',
                    'message': str(e)
                })

        if not results:
            return {
                'status': 'error',
                'message': 'No diagrams with reports found. Run generateReport first.'
            }

        return {
            'status': 'success',
            'message': f'Updated story graph from {len(results)} diagram(s)',
            'results': results
        }

    def _collect_diagram_data(self, render_specs: List['RenderSpec'], workspace_dir: Path) -> List[Dict[str, Any]]:
        diagrams = []
        for spec in render_specs:
            if not spec.output:
                continue
            output_name = spec.output
            if not output_name.endswith('.drawio'):
                continue
            default_path = str(self.behavior.bot_paths.story_graph_paths.docs_root)
            path_prefix = spec.config_data.get('path', default_path)
            diagram_path = workspace_dir / path_prefix / output_name
            layout_path = diagram_path.with_suffix('.drawio').with_name(
                diagram_path.stem + '-layout.json')
            update_report_path = diagram_path.with_suffix('.drawio').with_name(
                diagram_path.stem + '-update-report.json')
            # Also check for merge report (written by synchronizer)
            extracted_stem = diagram_path.stem + '-extracted'
            merge_report_path = diagram_path.parent / (extracted_stem + '-merge-report.json')
            # Prefer update-report (written by generate_diagram_report), fall back to merge-report
            report_path = None
            if update_report_path.exists():
                report_path = str(update_report_path.resolve())
            elif merge_report_path.exists():
                report_path = str(merge_report_path.resolve())
            last_sync_time = None
            if layout_path.exists():
                last_sync_time = layout_path.stat().st_mtime
            file_modified_time = None
            if diagram_path.exists():
                file_modified_time = diagram_path.stat().st_mtime
            diagrams.append({
                'file_path': str(diagram_path.resolve()),
                'exists': diagram_path.exists(),
                'last_sync_time': last_sync_time,
                'file_modified_time': file_modified_time,
                'report_path': report_path
            })
        return diagrams

    def inject_next_action_instructions(self):
        return 'Proceed to validate action'