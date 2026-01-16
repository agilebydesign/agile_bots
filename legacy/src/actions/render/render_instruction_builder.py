from pathlib import Path
from typing import Dict, Any, List, TYPE_CHECKING
if TYPE_CHECKING:
    from agile_bot.bots.base_bot.src.actions.render.render_spec import RenderSpec

class RenderInstructionBuilder:

    def inject_render_data(self, instructions: Dict[str, Any], render_instructions: Dict[str, Any], render_specs: List['RenderSpec']) -> None:
        base_instructions_list = instructions.get('base_instructions', []).copy()
        working_dir = self._inject_workspace_info(base_instructions_list, render_specs)
        executed_specs = [spec for spec in render_specs if spec.is_executed]
        template_specs = [spec for spec in render_specs if spec.requires_ai_handling and (not spec.is_executed)]
        
        # If no template specs require AI handling, clear the template-related instructions
        if not template_specs:
            base_instructions_list = []
        
        self._add_spec_instructions(base_instructions_list, executed_specs, template_specs)
        # Process action_config.json placeholders with ALL render_specs (for {{#for_each_render_config}} loops)
        self.inject_render_template_variables(base_instructions_list, render_instructions, template_specs, all_render_specs=render_specs)
        self._update_instructions_dict(instructions, base_instructions_list, render_instructions, template_specs, executed_specs, render_specs, working_dir)

    def _inject_workspace_info(self, base_instructions_list: List[str], render_specs: List['RenderSpec']) -> Path:
        if not render_specs:
            return None
        bot_paths = render_specs[0]._bot_paths
        working_dir = bot_paths.workspace_directory
        # Workspace path info removed - not needed in instructions
        return working_dir

    def _add_spec_instructions(self, base_instructions_list: List[str], executed_specs: List['RenderSpec'], template_specs: List['RenderSpec']) -> None:
        if executed_specs:
            # Find the end of context sources section (after the blank line following context sources)
            # Context sources typically look like:
            # [0]: "**Look for context in the following locations:**"
            # [1]: "- in this message and chat history"
            # [2]: "- in `{workspace}/docs/context/`"
            # [3]: "- generated files in `{workspace}/docs/stories/`"
            # [4]: "  clarification.json, planning.json"
            # [5]: ""  <- blank line
            # We want to insert AFTER this blank line
            insert_position = 1  # Default to position 1 if we can't find the pattern
            for i, line in enumerate(base_instructions_list):
                # Look for the blank line after context sources (after lines starting with "-" or spaces)
                if i > 0 and line == "" and i > 1:
                    # Found a blank line, check if previous lines were context sources
                    prev_line = base_instructions_list[i-1]
                    if prev_line.strip().startswith('-') or (prev_line.startswith('  ') and prev_line.strip()):
                        # This is the blank line after context sources
                        insert_position = i + 1
                        break
            
            # Split the multiline string into separate lines and insert them
            synchronizer_lines = self.format_executed_synchronizers(executed_specs).split('\n')
            for line in reversed(synchronizer_lines):
                base_instructions_list.insert(insert_position, line)

    def _update_instructions_dict(self, instructions: Dict[str, Any], base_instructions_list: List[str], render_instructions: Dict[str, Any], template_specs: List['RenderSpec'], executed_specs: List['RenderSpec'], render_specs: List['RenderSpec'], working_dir: Path) -> None:
        instructions['base_instructions'] = base_instructions_list
        instructions['render_instructions'] = render_instructions
        instructions['render_configs'] = [spec.config_data for spec in template_specs]
        instructions['executed_configs'] = [spec.config_data for spec in executed_specs]
        if render_specs and working_dir and (working_dir != render_specs[0]._bot_paths.bot_directory):
            instructions['workspace_path'] = str(working_dir)

    def inject_render_template_variables(self, instructions_list: List[str], render_instructions: Dict[str, Any], render_specs: List['RenderSpec'], all_render_specs: List['RenderSpec'] = None) -> None:
        """Inject render template variables and process for-each loops.
        
        Args:
            instructions_list: List of instruction strings to process
            render_instructions: Render instructions dict from instructions.json
            render_specs: Template specs that require AI handling
            all_render_specs: All render specs (for {{#for_each_render_config}} loops). Defaults to render_specs if not provided.
        """
        if all_render_specs is None:
            all_render_specs = render_specs
            
        render_instructions_text = '\n'.join(render_instructions.get('instructions', []))
        render_configs_text = self.format_render_configs(render_specs)
        
        # First, process for-each loops with ALL render specs
        processed_list = self._process_for_each_loops(instructions_list, all_render_specs)
        
        # Then process simple placeholders
        new_instructions = []
        for line in processed_list:
            if '{{render_instructions}}' in line:
                instructions_lines = render_instructions_text.split('\n')
                new_instructions.extend(instructions_lines)
            elif '{{render_configs}}' in line:
                configs_lines = render_configs_text.split('\n')
                new_instructions.extend(configs_lines)
            else:
                new_instructions.append(line)
        instructions_list[:] = new_instructions

    def format_render_configs(self, render_specs: List['RenderSpec']) -> str:
        formatted_parts = []
        for i, spec in enumerate(render_specs, 1):
            self._format_single_spec(spec, i, formatted_parts)
        return '\n'.join(formatted_parts)

    def _format_single_spec(self, spec: 'RenderSpec', index: int, formatted_parts: list):
        config_name = spec.name
        
        # Build the simplified instruction line
        workspace = spec._bot_paths.workspace_directory if hasattr(spec, '_bot_paths') else None
        path_prefix = spec.config_data.get('path', 'docs/stories')
        
        # Get full paths
        if workspace:
            output_path = workspace / path_prefix / spec.output if spec.output else 'N/A'
            input_path = workspace / path_prefix / spec.input if spec.input else 'N/A'
        else:
            output_path = spec.output if spec.output else 'N/A'
            input_path = spec.input if spec.input else 'N/A'
        
        # Get template path
        if spec.template and hasattr(spec.template, 'template_path'):
            template_path = spec.template.template_path
        else:
            template_path = spec.config_data.get('template', 'N/A')
        
        # Create single instruction line
        formatted_parts.append(f'{index}. {config_name} > manually generate {output_path} by taking {input_path} and transform using {template_path}')
        formatted_parts.append('')

    def format_executed_synchronizers(self, executed_specs: List['RenderSpec']) -> str:
        parts = ['**Synchronizers Already Executed:**', '', 'The following render configurations have been automatically executed via synchronizers:', '']
        for i, spec in enumerate(executed_specs, 1):
            self._format_executed_spec(spec, i, parts)
        parts.extend(['These outputs have been generated and do not require further action.', ''])
        return '\n'.join(parts)

    def _format_executed_spec(self, spec: 'RenderSpec', index: int, parts: list) -> None:
        if spec.execution_status == 'executed':
            result = spec.execution_result
            output_path = result.get('output_path', 'N/A') if result else 'N/A'
            parts.append(f'{index}. **{spec.name}** - EXECUTED')
            parts.append(f'   - Output generated at: {output_path}')
            if spec.synchronizer:
                parts.append(f'   - Synchronizer: {spec.synchronizer.synchronizer_class_path}')
        else:
            error = spec.execution_result.get('error', 'Unknown error') if spec.execution_result else 'Unknown error'
            parts.append(f'{index}. **{spec.name}** - FAILED')
            parts.append(f'   - Error: {error}')
        parts.append('')
    
    def _process_for_each_loops(self, instructions_list: List[str], render_specs: List['RenderSpec']) -> List[str]:
        """Process {{#for_each_render_config}}...{{/for_each_render_config}} loops."""
        new_instructions = []
        i = 0
        while i < len(instructions_list):
            line = instructions_list[i]
            
            if '{{#for_each_render_config}}' in line:
                # Find the end of the loop
                loop_start = i + 1
                loop_end = None
                for j in range(loop_start, len(instructions_list)):
                    if '{{/for_each_render_config}}' in instructions_list[j]:
                        loop_end = j
                        break
                
                if loop_end is None:
                    # Malformed loop, skip the marker
                    new_instructions.append(line)
                    i += 1
                    continue
                
                # Extract the template lines
                template_lines = instructions_list[loop_start:loop_end]
                
                # Generate instructions for each render spec
                for spec in render_specs:
                    expanded_lines = self._expand_template_for_spec(template_lines, spec)
                    new_instructions.extend(expanded_lines)
                
                # Skip past the loop
                i = loop_end + 1
            else:
                new_instructions.append(line)
                i += 1
        
        return new_instructions
    
    def _expand_template_for_spec(self, template_lines: List[str], spec: 'RenderSpec') -> List[str]:
        """Expand template lines with render_config placeholders replaced."""
        # Handle instructions - can be string or list
        instructions = spec.config_data.get('instructions', 'No instructions provided')
        if isinstance(instructions, list):
            instructions = '\n'.join(instructions)
        
        replacements = {
            '{render_config.name}': spec.name,
            '{render_config.instructions}': instructions,
            '{render_config.synchronizer}': spec.synchronizer.synchronizer_class_path if spec.synchronizer else 'N/A',
            '{render_config.template}': spec.config_data.get('template', 'N/A'),
            '{render_config.input}': spec.input or 'N/A',
            '{render_config.output}': spec.output or 'N/A',
            '{render_config.path}': spec.config_data.get('path', 'N/A')
        }
        
        expanded_lines = []
        for line in template_lines:
            expanded_line = line
            for placeholder, value in replacements.items():
                # For instructions, if it's multiline, we need to handle it specially
                if placeholder == '{render_config.instructions}' and '\n' in value:
                    # Replace the placeholder with first line, then insert remaining lines
                    lines = value.split('\n')
                    expanded_line = expanded_line.replace(placeholder, lines[0])
                    expanded_lines.append(expanded_line)
                    # Add remaining lines (if the original line only had the placeholder)
                    if line.strip() == placeholder:
                        for additional_line in lines[1:]:
                            expanded_lines.append(additional_line)
                    break
                else:
                    expanded_line = expanded_line.replace(placeholder, str(value))
            else:
                # No multiline instructions handling needed
                expanded_lines.append(expanded_line)
        
        return expanded_lines