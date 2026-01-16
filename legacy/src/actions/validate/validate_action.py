from typing import Dict, Any, List, Type
import logging
from ..action import Action
from ..action_context import ActionContext, ValidateActionContext
from ..rules.rules import Rules
from .validation_executor import ValidationExecutor
from ...utils import read_json_file
from ...scanners.scanner_execution_error import ScannerExecutionError

logger = logging.getLogger(__name__)

class ValidateRulesAction(Action):
    context_class: Type[ActionContext] = ValidateActionContext

    def __init__(self, behavior=None, action_config=None):
        super().__init__(behavior=behavior, action_config=action_config)
        self._rules = Rules(behavior=self.behavior, bot_paths=self.behavior.bot_paths)
        self._executor = ValidationExecutor(self.behavior, self._rules)

    @property
    def action_name(self) -> str:
        return 'validate'

    @action_name.setter
    def action_name(self, value: str):
        raise AttributeError('action_name is read-only for ValidateRulesAction')

    @property
    def rules(self) -> Rules:
        return self._rules

    def _prepare_instructions(self, instructions, context: ValidateActionContext):
        """Prepare validation instructions with rules and validation data."""
        # Get rules with file paths for AI to read
        rules_text = self._format_rules_with_file_paths()
        
        # Get story graph schema path
        schema_path = self.behavior.bot_paths.workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        
        # Get scope description
        scope_text = self._format_scope_description(context)
        
        # Run scanners and get formatted results
        scanner_output = self._run_scanners_and_format_results(context)
        
        # Build replacement data
        replacements = {
            'rules': rules_text if rules_text else 'No rules defined',
            'scanner_output': scanner_output,
            'schema': f'**Schema:** Story graph at `{schema_path}`',
            'description': f'Validate **{self.behavior.name}** artifacts against rules. Scanner results shown above.',
            'scope': scope_text
        }
        
        # Replace placeholders in base instructions (both {{}} and {} formats)
        base_instructions = instructions.get('base_instructions', [])
        new_instructions = []
        for line in base_instructions:
            if isinstance(line, str):
                # Replace {{placeholder}} format
                for key, value in replacements.items():
                    placeholder = '{{' + key + '}}'
                    if placeholder in line:
                        line = line.replace(placeholder, value)
                # Replace {placeholder} format
                for key, value in replacements.items():
                    placeholder = '{' + key + '}'
                    if placeholder in line:
                        line = line.replace(placeholder, value)
            new_instructions.append(line)
        
        instructions._data['base_instructions'] = new_instructions
        
        # Add knowledge graph config and template paths for reference (same as build action)
        kg_dir = self.behavior.bot_paths.bot_directory / 'behaviors' / self.behavior.name / 'content' / 'knowledge_graph'
        
        # Find config file
        config_files = list(kg_dir.glob('*.json')) if kg_dir.exists() else []
        config_file = next((f for f in config_files if 'config' in f.name.lower() or f.name.endswith('-outline.json')), None)
        if config_file:
            instructions._data['config_path'] = str(config_file.resolve())
        
        # Find template file  
        template_files = list(kg_dir.glob('*template*.json')) if kg_dir.exists() else []
        template_file = template_files[0] if template_files else None
        if template_file:
            instructions._data['template_path'] = str(template_file.resolve())
        
        # Add structured rules data for display panel (same format as build action)
        rules_data = self.inject_behavior_specific_rules()
        all_rules = rules_data.get('validation_rules', [])
        if all_rules:
            # Convert to absolute file paths (same format as build action)
            rule_files = []
            bots_dir = self.behavior.bot_paths.python_workspace_root / 'agile_bot' / 'bots'
            for rule in all_rules:
                rule_file = rule.get('rule_file', '')
                if rule_file:
                    # Convert relative path to absolute
                    rule_path = str(bots_dir / rule_file)
                    rule_files.append(rule_path)
            instructions._data['rules'] = rule_files

    def _run_scanners_and_format_results(self, context: ValidateActionContext) -> str:
        """Run validation scanners and format results for display in instructions."""
        logger.info('Running scanners for instructions display...')
        
        try:
            # Execute validation synchronously
            result = self._executor.execute_synchronous(context)
            
            # Get the report path from the result
            instructions_dict = result.get('instructions', {})
            report_link = instructions_dict.get('report_link', '')
            
            # Read the generated validation report file
            if report_link:
                # Extract path from markdown link format [text](path)
                import re
                match = re.search(r'\[.*?\]\((.*?)\)', report_link)
                if match:
                    report_path = match.group(1)
                    # Convert to absolute path
                    from pathlib import Path
                    report_file = Path(report_path)
                    if not report_file.is_absolute():
                        report_file = self.behavior.bot_paths.workspace_directory / report_path
                    
                    if report_file.exists():
                        # Read and return the report content
                        report_content = report_file.read_text(encoding='utf-8')
                        return f'**Scanner Results:**\n\n{report_content}\n\n**Full Report:** {report_link}'
            
            # Fallback: check violation summary
            violation_summary = self._rules.violation_summary if hasattr(self._rules, 'violation_summary') else []
            if violation_summary:
                return '\n'.join(['**Scanner Violations Found:**', ''] + violation_summary)
            
            return '✅ **No scanner violations detected.**\n\nAll automated rule scanners passed successfully.'
            
        except Exception as e:
            logger.error(f'Error running scanners: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return f'Error running scanners: {e}\n\nPlease review the validation report file in docs/stories/reports/'
    
    def _format_scope_description(self, context: ValidateActionContext) -> str:
        """Format scope description for validation instructions."""
        if context.scope:
            scope_type = context.scope.type.value  # ScopeType enum
            scope_value = context.scope.value
            
            if scope_type == 'epic':
                return f"epic(s): {', '.join(scope_value)}"
            elif scope_type == 'story':
                return f"story/stories: {', '.join(scope_value)}"
            elif scope_type == 'files':
                return f"file(s): {', '.join(scope_value)}"
            else:
                return "all epics, sub-epics, stories, and domain concepts in the knowledge graph"
        else:
            return "all epics, sub-epics, stories, and domain concepts in the knowledge graph"

    def _format_rules_with_file_paths(self) -> str:
        """Format rules with file paths for AI to read and analyze."""
        rules_data = self.inject_behavior_specific_rules()
        all_rules = rules_data.get('validation_rules', [])
        
        if not all_rules:
            return 'No validation rules found.'
        
        # Sort by priority (lower number = higher priority)
        all_rules = sorted(all_rules, key=lambda r: r.get('rule_content', {}).get('priority', 99))
        
        lines = []
        lines.append("**Rules to validate against (read each file for full DO/DON'T examples):**")
        lines.append("")
        
        for rule in all_rules:
            rule_file = rule.get('rule_file', 'unknown')
            rule_content = rule.get('rule_content', {})
            
            # Extract rule info
            name = rule_content.get('name', rule_file.split('/')[-1].replace('.json', '').replace('_', ' ').title())
            description = rule_content.get('description', 'No description')
            priority = rule_content.get('priority', 99)
            has_scanner = 'scanner' in rule_content or 'scanners' in rule_content
            
            # Format rule entry with file path
            scanner_status = '[Scanner]' if has_scanner else '[Manual Check]'
            lines.append(f"### Rule: {name} (Priority {priority}) {scanner_status}")
            lines.append(f"**File:** `{rule_file}`")
            lines.append(f"**Description:** {description}")
            
            # Add DO section
            do_section = rule_content.get('do', {})
            do_desc = do_section.get('description', '')
            if do_desc:
                lines.append(f"**DO:** {do_desc}")
            
            # Add DON'T section
            dont_section = rule_content.get('dont', {})
            dont_desc = dont_section.get('description', '')
            if dont_desc:
                lines.append(f"**DON'T:** {dont_desc}")
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def _do_confirm(self, context: ValidateActionContext) -> Dict[str, Any]:
        """Run validation scanners and generate reports."""
        logger.info('=== Starting validation ===')
        logger.info(f'Behavior: {self.behavior.name}')
        logger.info(f'Context: scope={context.scope}, skip_cross_file={context.skip_cross_file}')
        
        result = self._executor.execute_synchronous(context)
        
        return {
            'message': 'Validation completed',
            'validation_result': result
        }
    
    def do_execute(self, context: ValidateActionContext) -> Dict[str, Any]:
        """Legacy method for backwards compatibility."""
        logger.info('=== Starting validation ===')
        logger.info(f'Behavior: {self.behavior.name}')
        logger.info(f'Context: scope={context.scope}, skip_cross_file={context.skip_cross_file}')
        return self._executor.execute_synchronous(context)

    def inject_behavior_specific_rules(self) -> Dict[str, Any]:
        all_rules = []
        bot_dir = self.behavior.bot_paths.bot_directory
        behavior_rules_dir = bot_dir / 'behaviors' / self.behavior.name / 'rules'
        for rule_file in behavior_rules_dir.glob('*.json'):
            rule_data = read_json_file(rule_file)
            all_rules.append({'rule_file': f'{bot_dir.name}/behaviors/{self.behavior.name}/rules/{rule_file.name}', 'rule_content': rule_data})
        return {'validation_rules': all_rules}

    def get_action_instructions(self) -> List[str]:
        action_instructions = []
        base_actions_path = self.base_actions_dir
        config_path = base_actions_path / 'validate' / 'action_config.json'
        config = read_json_file(config_path)
        action_instructions = config.get('instructions', [])
        return action_instructions

    def inject_next_action_instructions(self):
        return ''

    def finalize_and_transition(self, next_action: str=None):

        class ActionResult:

            def __init__(self, next_action):
                self.next_action = next_action
        return ActionResult(next_action=next_action)