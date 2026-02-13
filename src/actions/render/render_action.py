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
        
        # Collect synchronizer specs that need to be executed by the AI
        sync_specs = [spec for spec in render_specs if spec.synchronizer and not spec.is_executed]
        if sync_specs:
            behavior_name = self.behavior.name
            sync_names = [spec.name or spec.output for spec in sync_specs]
            instructions._data['synchronizer_specs'] = [spec.config_data for spec in sync_specs]
            instructions._data['base_instructions'].append(
                f"IMPORTANT: After completing all template-based rendering, you MUST execute "
                f"the synchronizer-based render specs by running: {behavior_name}.render.renderAll\n"
                f"This will render the following outputs: {', '.join(sync_names)}"
            )
    
    def do_execute(self, context: ScopeActionContext = None):
        render_instructions = self._config_loader.load_render_instructions()
        render_specs = self._render_specs
        # NOTE: _execute_synchronizers removed — diagrams are only rendered
        # via the explicit "Render Diagram" button (renderDiagram method).
        
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

    def saveDiagramLayout(self) -> Dict[str, Any]:
        """Extract and save positional data from current diagram files.
        CLI: <behavior>.render.saveDiagramLayout
        """
        from synchronizers.story_io.story_io_synchronizer import DrawIOSynchronizer
        sync = DrawIOSynchronizer()
        results = []

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            if not diagram_path.exists():
                continue
            result = sync.save_layout(diagram_path)
            results.append({'diagram': spec.output, **result})

        saved_count = sum(1 for r in results if r.get('status') == 'success')
        return {
            'status': 'success',
            'message': 'Saved layout for ' + str(saved_count) + ' diagram(s)',
            'results': results
        }

    def clearLayout(self) -> Dict[str, Any]:
        """Delete layout files for all DrawIO diagrams so next render starts fresh.
        CLI: <behavior>.render.clearLayout
        """
        workspace_dir = self.behavior.bot_paths.workspace_directory
        results = []

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            layout_path = diagram_path.parent / f"{diagram_path.stem}-layout.json"
            if layout_path.exists():
                layout_path.unlink()
                results.append({'diagram': spec.output, 'status': 'cleared'})
            else:
                results.append({'diagram': spec.output, 'status': 'no_layout'})

        cleared_count = sum(1 for r in results if r['status'] == 'cleared')
        return {
            'status': 'success',
            'message': f'Cleared layout for {cleared_count} diagram(s)',
            'results': results
        }

    def renderAll(self) -> Dict[str, Any]:
        """Execute all synchronizer-based render specs.
        CLI: <behavior>.render.renderAll
        """
        sync_specs = [spec for spec in self._render_specs if spec.synchronizer]
        if not sync_specs:
            return {'status': 'success', 'message': 'No synchronizer specs to execute', 'results': []}

        self._execute_synchronizers(sync_specs)

        results = []
        for spec in sync_specs:
            results.append({
                'name': spec.name,
                'output': spec.output,
                'status': spec.execution_status,
            })

        rendered_count = sum(1 for r in results if r['status'] == 'executed')
        return {
            'status': 'success',
            'message': f'Rendered {rendered_count} spec(s)',
            'results': results
        }

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
        from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
        from synchronizers.story_io.story_io_synchronizer import DrawIOSynchronizer
        from story_graph.nodes import StoryMap

        story_graph_path = self.behavior.bot_paths.story_graph_paths.story_graph_path
        results = []
        sync = DrawIOSynchronizer()

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            if not diagram_path.exists():
                continue

            sync.save_layout(diagram_path)

            try:
                drawio_map = DrawIOStoryMap.load(diagram_path)
                graph_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
                original_map = StoryMap(graph_data)

                # Write extracted JSON (the diagram's current structure)
                extracted_path = diagram_path.parent / f"{diagram_path.stem}-extracted.json"
                drawio_map.save_as_json(extracted_path)

                report = drawio_map.generate_update_report(original_map)
                update_report_path = diagram_path.parent / f"{diagram_path.stem}-update-report.json"
                report.save(update_report_path)

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
        from synchronizers.story_io.update_report import UpdateReport

        story_graph_path = self.behavior.bot_paths.story_graph_paths.story_graph_path
        results = []

        for spec, diagram_path in self._get_drawio_specs_with_paths():
            update_report_path = diagram_path.parent / f"{diagram_path.stem}-update-report.json"

            if not update_report_path.exists():
                continue

            try:
                report_data = json.loads(update_report_path.read_text(encoding='utf-8'))
                report = UpdateReport.from_dict(report_data)

                if not report.has_changes:
                    results.append({'diagram': spec.output, 'status': 'no_changes'})
                    continue

                graph_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
                changed = False

                for rename in report.renames:
                    if self._apply_rename(graph_data, rename.original_name, rename.extracted_name):
                        changed = True

                for new_epic in report.new_epics:
                    if self._apply_new_epic(graph_data, new_epic.name):
                        changed = True

                for new_sub_epic in report.new_sub_epics:
                    if self._apply_new_sub_epic(graph_data, new_sub_epic.name, new_sub_epic.parent):
                        changed = True

                for new_story in report.new_stories:
                    if self._apply_new_story(graph_data, new_story.name, new_story.parent):
                        changed = True

                # Apply story moves BEFORE removes to preserve story data.
                # If a sub-epic is removed but its stories were moved to
                # another sub-epic, the move must happen first or the
                # stories are lost when the sub-epic is deleted.
                for move in report.moved_stories:
                    if self._apply_move_story(graph_data, move.name,
                                               move.from_parent, move.to_parent):
                        changed = True

                for removed in report.removed_epics:
                    if self._apply_remove_epic(graph_data, removed.name):
                        changed = True

                for removed in report.removed_sub_epics:
                    if self._apply_remove_sub_epic(graph_data, removed.name, removed.parent):
                        changed = True

                for removed in report.removed_stories:
                    if self._apply_remove_story(graph_data, removed.name, removed.parent):
                        changed = True

                # Apply increment changes (stories added/removed from increments)
                for inc_change in report.increment_changes:
                    if self._apply_increment_change(graph_data, inc_change):
                        changed = True

                # Apply increment moves (story moved from one increment to another)
                for inc_move in report.increment_moves:
                    if self._apply_increment_move(graph_data, inc_move):
                        changed = True

                # Remove increments that are no longer in the diagram
                for inc_name in report.removed_increments:
                    if self._apply_remove_increment(graph_data, inc_name):
                        changed = True

                # Update increment priorities to match diagram order
                if report.increment_order:
                    if self._apply_increment_order(graph_data, report.increment_order):
                        changed = True

                if changed:
                    story_graph_path.write_text(
                        json.dumps(graph_data, indent=2, ensure_ascii=False), encoding='utf-8')

                update_report_path.unlink()

                results.append({
                    'diagram': spec.output,
                    'status': 'success',
                    'changes_applied': changed
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

    def _apply_rename(self, graph_data: dict, old_name: str, new_name: str) -> bool:
        for epic in graph_data.get('epics', []):
            if self._rename_in_node(epic, old_name, new_name):
                return True
        return False

    def _rename_in_node(self, node: dict, old_name: str, new_name: str) -> bool:
        for se in node.get('sub_epics', []):
            if se.get('name') == old_name:
                se['name'] = new_name
                return True
            if self._rename_in_node(se, old_name, new_name):
                return True
        for sg in node.get('story_groups', []):
            for story in sg.get('stories', []):
                if story.get('name') == old_name:
                    story['name'] = new_name
                    return True
        return False

    def _apply_new_story(self, graph_data: dict, story_name: str, parent_name: str) -> bool:
        for epic in graph_data.get('epics', []):
            if self._add_story_to_parent(epic, story_name, parent_name):
                return True
        return False

    def _add_story_to_parent(self, node: dict, story_name: str, parent_name: str) -> bool:
        if node.get('name') == parent_name:
            groups = node.get('story_groups', [])
            if not groups:
                groups = [{'type': 'and', 'connector': None, 'stories': []}]
                node['story_groups'] = groups
            stories = groups[0].get('stories', [])
            order = max((s.get('sequential_order') or 0 for s in stories), default=0) + 1
            stories.append({'name': story_name, 'sequential_order': order, 'story_type': 'user'})
            return True
        for se in node.get('sub_epics', []):
            if self._add_story_to_parent(se, story_name, parent_name):
                return True
        return False

    def _apply_remove_story(self, graph_data: dict, story_name: str, parent_name: str) -> bool:
        for epic in graph_data.get('epics', []):
            if self._remove_story_from_node(epic, story_name):
                return True
        return False

    def _remove_story_from_node(self, node: dict, story_name: str) -> bool:
        for sg in node.get('story_groups', []):
            stories = sg.get('stories', [])
            for i, story in enumerate(stories):
                if story.get('name') == story_name:
                    stories.pop(i)
                    return True
        for se in node.get('sub_epics', []):
            if self._remove_story_from_node(se, story_name):
                return True
        return False

    def _apply_new_epic(self, graph_data: dict, epic_name: str) -> bool:
        epics = graph_data.get('epics', [])
        # Don't add if already exists
        if any(e.get('name') == epic_name for e in epics):
            return False
        order = max((e.get('sequential_order') or 0 for e in epics), default=0) + 1
        epics.append({
            'name': epic_name,
            'sequential_order': order,
            'sub_epics': []
        })
        return True

    def _apply_new_sub_epic(self, graph_data: dict, sub_epic_name: str, parent_name: str) -> bool:
        for epic in graph_data.get('epics', []):
            if self._add_sub_epic_to_parent(epic, sub_epic_name, parent_name):
                return True
        return False

    def _add_sub_epic_to_parent(self, node: dict, sub_epic_name: str, parent_name: str) -> bool:
        if node.get('name') == parent_name:
            sub_epics = node.get('sub_epics', [])
            # Don't add if already exists
            if any(se.get('name') == sub_epic_name for se in sub_epics):
                return False
            order = max((se.get('sequential_order') or 0 for se in sub_epics), default=0) + 1
            sub_epics.append({
                'name': sub_epic_name,
                'sequential_order': order,
                'sub_epics': [],
                'story_groups': []
            })
            node['sub_epics'] = sub_epics
            return True
        for se in node.get('sub_epics', []):
            if self._add_sub_epic_to_parent(se, sub_epic_name, parent_name):
                return True
        return False

    def _apply_remove_epic(self, graph_data: dict, epic_name: str) -> bool:
        epics = graph_data.get('epics', [])
        for i, epic in enumerate(epics):
            if epic.get('name') == epic_name:
                epics.pop(i)
                return True
        return False

    def _apply_remove_sub_epic(self, graph_data: dict, sub_epic_name: str, parent_name: str) -> bool:
        for epic in graph_data.get('epics', []):
            if self._remove_sub_epic_from_node(epic, sub_epic_name):
                return True
        return False

    def _remove_sub_epic_from_node(self, node: dict, sub_epic_name: str) -> bool:
        sub_epics = node.get('sub_epics', [])
        for i, se in enumerate(sub_epics):
            if se.get('name') == sub_epic_name:
                sub_epics.pop(i)
                return True
            if self._remove_sub_epic_from_node(se, sub_epic_name):
                return True
        return False

    def _apply_move_story(self, graph_data: dict, story_name: str,
                          from_parent: str, to_parent: str) -> bool:
        """Move a story from one sub-epic to another, preserving all data.

        Extracts the full story dict from the old parent and inserts it
        into the new parent, keeping scenarios, acceptance criteria, etc.
        """
        # Step 1: Extract (remove) the story data from its current location
        story_data = None
        for epic in graph_data.get('epics', []):
            story_data = self._extract_story_from_node(epic, story_name, from_parent)
            if story_data:
                break

        if story_data is None:
            # Fallback: search anywhere if from_parent didn't match
            for epic in graph_data.get('epics', []):
                story_data = self._extract_story_from_node(epic, story_name)
                if story_data:
                    break

        if story_data is None:
            return False

        # Step 2: Insert the story into the new parent
        for epic in graph_data.get('epics', []):
            if self._insert_story_into_parent(epic, story_data, to_parent):
                return True

        # If we couldn't find the target parent, put the story back
        # where it came from to avoid data loss
        for epic in graph_data.get('epics', []):
            if self._insert_story_into_parent(epic, story_data, from_parent):
                return False
        return False

    def _extract_story_from_node(self, node: dict, story_name: str,
                                  parent_name: str = None) -> Optional[dict]:
        """Remove and return a story dict from the tree.

        If parent_name is given, only extract from that specific parent.
        """
        if parent_name is None or node.get('name') == parent_name:
            for sg in node.get('story_groups', []):
                stories = sg.get('stories', [])
                for i, story in enumerate(stories):
                    if story.get('name') == story_name:
                        return stories.pop(i)
        for se in node.get('sub_epics', []):
            result = self._extract_story_from_node(se, story_name, parent_name)
            if result:
                return result
        return None

    def _insert_story_into_parent(self, node: dict, story_data: dict,
                                   parent_name: str) -> bool:
        """Insert a story dict under the named parent."""
        if node.get('name') == parent_name:
            groups = node.get('story_groups', [])
            if not groups:
                groups = [{'type': 'and', 'connector': None, 'stories': []}]
                node['story_groups'] = groups
            stories = groups[0].get('stories', [])
            # Don't insert if it already exists (safety check)
            if not any(s.get('name') == story_data.get('name') for s in stories):
                stories.append(story_data)
            return True
        for se in node.get('sub_epics', []):
            if self._insert_story_into_parent(se, story_data, parent_name):
                return True
        return False

    def _apply_increment_change(self, graph_data: dict, change) -> bool:
        """Apply an IncrementChange to the story graph's increments section.

        Adds/removes stories from the named increment.  If the increment
        does not exist yet, it is created.
        """
        increments = graph_data.setdefault('increments', [])

        # Find the increment by name
        target = None
        for inc in increments:
            if inc.get('name') == change.name:
                target = inc
                break

        if target is None and change.added:
            # Increment mentioned in diagram but not in graph → create it
            target = {'name': change.name, 'priority': len(increments) + 1, 'stories': []}
            increments.append(target)

        if target is None:
            return False

        modified = False
        stories = target.get('stories', [])

        # Normalise: stories can be plain strings or dicts with 'name'
        def _story_name(s):
            return s.get('name', '') if isinstance(s, dict) else str(s)

        # Remove stories
        for name in change.removed:
            for i, s in enumerate(stories):
                if _story_name(s) == name:
                    stories.pop(i)
                    modified = True
                    break

        # Add stories (as plain strings, matching the existing format)
        existing_names = {_story_name(s) for s in stories}
        for name in change.added:
            if name not in existing_names:
                stories.append(name)
                modified = True

        target['stories'] = stories
        return modified

    def _apply_increment_move(self, graph_data: dict, move) -> bool:
        """Move a story from one increment to another.

        Removes the story from *from_increment* and adds it to *to_increment*.
        Creates the target increment if it does not exist.
        """
        increments = graph_data.get('increments', [])

        def _story_name(s):
            return s.get('name', '') if isinstance(s, dict) else str(s)

        modified = False

        # Remove from source increment (if specified)
        if move.from_increment:
            for inc in increments:
                if inc.get('name') == move.from_increment:
                    stories = inc.get('stories', [])
                    for i, s in enumerate(stories):
                        if _story_name(s) == move.story:
                            stories.pop(i)
                            modified = True
                            break
                    break

        # Add to target increment
        if move.to_increment:
            target = None
            for inc in increments:
                if inc.get('name') == move.to_increment:
                    target = inc
                    break
            if target is None:
                target = {'name': move.to_increment,
                          'priority': len(increments) + 1, 'stories': []}
                increments.append(target)

            stories = target.get('stories', [])
            existing = {_story_name(s) for s in stories}
            if move.story not in existing:
                stories.append(move.story)
                target['stories'] = stories
                modified = True

        return modified

    def _apply_remove_increment(self, graph_data: dict, inc_name: str) -> bool:
        """Remove an entire increment from the story graph."""
        increments = graph_data.get('increments', [])
        for i, inc in enumerate(increments):
            if inc.get('name') == inc_name:
                increments.pop(i)
                return True
        return False

    def _apply_increment_order(self, graph_data: dict,
                                order: list) -> bool:
        """Update increment priorities to match the diagram order.

        *order* is a list of ``{'name': ..., 'priority': ...}`` dicts from
        the diagram (top-to-bottom).  Any increments not in this list keep
        their existing priority but are pushed after the ordered ones.
        """
        increments = graph_data.get('increments', [])
        if not increments:
            return False

        order_map = {entry['name']: entry['priority'] for entry in order}
        modified = False

        for inc in increments:
            name = inc.get('name', '')
            if name in order_map:
                new_priority = order_map[name]
                if inc.get('priority') != new_priority:
                    inc['priority'] = new_priority
                    modified = True

        # Sort increments by priority so the JSON is ordered correctly
        if modified:
            increments.sort(key=lambda inc: inc.get('priority', 9999))

        return modified

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