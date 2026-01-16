import dataclasses
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ActionDescription:
    name: str
    description: str


@dataclass
class CommandExample:
    pattern: str
    description: str


class StageCollection:
    def __init__(self, stages: List[List[str]]):
        self._stages = stages
    
    def format_as_lines(self) -> List[str]:
        result = []
        for stage in self._stages:
            result.extend(stage)
        return result


class ParameterCollection:
    def __init__(self, parameters: List[str]):
        self._parameters = parameters
    
    def format_as_lines(self) -> List[str]:
        if not self._parameters:
            return []
        result = ["Context Parameters (when confirming):"]
        result.extend([f"  --{param} <value>" for param in self._parameters])
        result.append("")
        return result


class ActionNameCollection:
    def __init__(self, action_names: List[str], behavior_name: str):
        self._action_names = action_names
        self._behavior_name = behavior_name
    
    def format_as_lines(self) -> List[str]:
        result = [f"Available Actions for behavior: {self._behavior_name}"]
        result.extend([f"  {name}" for name in self._action_names])
        return result


class ActionDescriptionCollection:
    def __init__(self, descriptions: List[ActionDescription]):
        self._descriptions = descriptions
    
    def format_as_lines(self) -> List[str]:
        return [f"      {action.name:12} - {action.description}" for action in self._descriptions]


class CommandExampleCollection:
    def __init__(self, examples: List[CommandExample]):
        self._examples = examples
    
    def format_as_lines(self) -> List[str]:
        return [f"    {example.pattern:45} -> {example.description}" for example in self._examples]


class OtherCommandCollection:
    def __init__(self, commands: List[CommandExample]):
        self._commands = commands
    
    def format_as_lines(self) -> List[str]:
        return [f"    {cmd.pattern:45} - {cmd.description}" for cmd in self._commands]


class ActionHelp:
    def __init__(self, action, action_name: str):
        self.action = action
        self.action_name = action_name
    
    @property
    def help_text(self) -> str:
        lines = [
            f"## {self.action_name}",
            "",
            "Hierarchy: behavior → action → stage",
            "",
            "Usage:",
            f"  {self.action_name} [instructions|confirm|submit]",
            "",
            "Action Stages (two steps):",
            "",
        ]
        
        # Delegate to collection class
        stage_collection = StageCollection(self._stages)
        lines.extend(stage_collection.format_as_lines())
        
        lines.extend([
            "Note: Calling action name without stage cycles through: instructions → confirm",
            "      Use 'submit' to send instructions directly to Cursor chat (Windows only)",
            "",
        ])
        
        # Delegate to collection class
        param_collection = ParameterCollection(self._context_parameters)
        lines.extend(param_collection.format_as_lines())
        
        return "\n".join(lines)
    
    @property
    def _stages(self) -> List[List[str]]:
        return [
            [
                "  1. instructions",
                "     Request: Get instructions for the action",
                "     Response: Shows instructions, questions to answer, evidence to provide",
                f"     Example: {self.action_name} instructions  (or just: {self.action_name})",
                "",
            ],
            [
                "  2. confirm",
                "     Request: Process work, mark complete and advance to next action",
                "     Response: Saves any data, then auto-executes next action and shows its instructions",
                f"     Example: {self.action_name} confirm  (or call {self.action_name} again to cycle)",
                "",
            ],
        ]
    
    @property
    def _context_parameters(self) -> List[str]:
        if dataclasses.is_dataclass(self.action.context_class):
            return [f.name for f in dataclasses.fields(self.action.context_class)]
        return []


class BehaviorHelp:
    def __init__(self, behavior):
        self.behavior = behavior
    
    @property
    def name(self) -> str:
        return self.behavior.name
    
    @property
    def action_names(self) -> List[str]:
        return [a.action_name for a in self.behavior.actions]
    
    @property
    def actions_list(self) -> str:
        # Delegate to collection class
        collection = ActionNameCollection(self.action_names, self.name)
        return "\n".join(collection.format_as_lines())
    
    def action(self, action_name: str) -> Optional[ActionHelp]:
        for action in self.behavior.actions._actions:
            if action.action_name == action_name:
                return ActionHelp(action, action_name)
        return None


class HeadlessModeHelp:
    def __init__(self):
        from agile_bot.bots.base_bot.src.repl_cli.headless.headless_config import HeadlessConfig
        try:
            self._config = HeadlessConfig.load()
        except Exception:
            self._config = None
    
    @property
    def is_configured(self) -> bool:
        return self._config is not None and self._config.is_configured
    
    def format_as_lines(self) -> List[str]:
        lines = [
            "",
            "  Headless Mode:",
        ]
        
        if self.is_configured:
            lines.extend([
                "    Status: Available (API key configured)",
                "",
                "    Usage:",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless \"Your instruction\"",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build \"context message\"",
                "",
                "    Commands:",
                "      headless \"text\"                    Execute pass-through instruction",
                "      headless shape                      Execute entire behavior",
                "      headless shape.build                Execute single action",
                "      headless shape.build.confirm        Execute single operation",
                "      headless shape.build \"message\"      Execute action with context message",
                "",
                "    Options:",
                "      --context file.md    Context file to include",
                "      --timeout N          API timeout in seconds (default: 600, use 30 for tests)",
                "",
                "    Examples:",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless \"Create hello world function\"",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build --timeout 30",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless shape.build \"Focus on error handling\"",
                "      python agile_bot/bots/base_bot/src/repl_cli/repl_main.py headless \"Build feature\" --context context.md",
            ])
        else:
            lines.extend([
                "    Status: Unavailable (API key not configured)",
                "",
                "    To configure headless mode:",
                "      1. Create file: agile_bot/secrets/cursor_api_key.txt",
                "      2. Add your Cursor API key to the file",
                "      3. Restart the REPL",
            ])
        
        return lines


class REPLHelp:
    def __init__(self, bot, session=None):
        self.bot = bot
        self.session = session
        self._headless_help = HeadlessModeHelp()
    
    @property
    def behavior_names(self) -> List[str]:
        if not self.bot or not self.bot.behaviors:
            return []
        return [b.name for b in self.bot.behaviors]
    
    @property
    def action_descriptions(self) -> List[ActionDescription]:
        return [
            ActionDescription("clarify", "Gather context and answer key questions"),
            ActionDescription("strategy", "Plan the approach for this behavior"),
            ActionDescription("build", "Execute the main work of this behavior"),
            ActionDescription("validate", "Verify work meets requirements"),
            ActionDescription("render", "Generate final outputs and artifacts"),
        ]
    
    @property
    def command_examples(self) -> List[CommandExample]:
        return [
            CommandExample("echo '.' | python repl_main.py", "Execute current behavior.action.operation"),
            CommandExample("echo 'shape' | python repl_main.py", "Jump to behavior and execute first action.operation"),
            CommandExample("echo 'build' | python repl_main.py", "Jump to action and execute first operation"),
            CommandExample("echo 'confirm scope=\"s1\"' | python repl_main.py", "Jump to operation with params and execute"),
            CommandExample("echo 'shape.build' | python repl_main.py", "Jump to behavior.action and execute first operation"),
            CommandExample("echo 'shape.build.confirm' | python repl_main.py", "Jump to behavior.action.operation and execute"),
            CommandExample("python repl_main.py headless shape", "Execute behavior in headless mode (unattended)"),
        ]
    
    @property
    def other_commands(self) -> List[CommandExample]:
        return [
            CommandExample("echo 'status' | python repl_main.py", "Show full workflow hierarchy"),
            CommandExample("echo 'back' | python repl_main.py", "Go back to previous action"),
            CommandExample("echo 'current' | python repl_main.py", "Re-execute current operation"),
            CommandExample("echo 'next' | python repl_main.py", "Advance to next action"),
            CommandExample("echo 'path [dir]' | python repl_main.py", "Show/set working directory"),
            CommandExample("echo 'scope C:\\full\\path' | python repl_main.py", "Set scope to COMPLETE folder path"),
            CommandExample("echo 'scope all' | python repl_main.py", "Clear scope filter"),
            CommandExample("echo 'scope showAll' | python repl_main.py", "Show entire story graph"),
            CommandExample("echo 'headless \"message\"' | python repl_main.py", "Execute message in headless mode"),
            CommandExample("echo 'help' | python repl_main.py", "Show this help"),
            CommandExample("echo 'exit' | python repl_main.py", "Exit CLI"),
        ]
    
    @property
    def main_help(self) -> str:
        behaviors_list = " | ".join(self.behavior_names)
        
        lines = [
            "Core Commands:",
            "  echo '[behavior.][action.]operation' | python repl_main.py  - navigate and perform operation",
            "  echo '[behavior][.action]' | python repl_main.py           - navigate to behavior/action",
            "",
            "  Available Components:",
            f"    behaviors   -> {behaviors_list}",
            "",
            "    actions:"
        ]
        
        # Show actions with their parameter hints
        if self.session and self.session.has_current_behavior:
            behavior = self.session.current_behavior
            for action in behavior.actions._actions:
                action_name = action.action_name
                action_desc = next((a.description for a in self.action_descriptions if a.name == action_name), "")
                
                instructions_hint = self.session._get_instructions_params_hint(action)
                confirm_hint = self.session._get_confirm_params_hint(action)
                
                # Combine hints
                hints = []
                if instructions_hint:
                    hints.append(instructions_hint)
                if confirm_hint:
                    hints.append(confirm_hint)
                
                params_line = " | ".join(hints) if hints else ""
                
                lines.append(f"      {action_name:12} - {action_desc}")
                if params_line:
                    lines.append(f"                     {params_line}")
        else:
            # Fallback if no current behavior - delegate to collection class
            desc_collection = ActionDescriptionCollection(self.action_descriptions)
            lines.extend(desc_collection.format_as_lines())
        
        lines.append("")
        lines.append("    operations:")
        
        # Show operations with parameter hints if we have a current action
        if self.session and self.session.has_current_action:
            action_obj = self.session.current_action
            instructions_hint = self.session._get_instructions_params_hint(action_obj)
            confirm_hint = self.session._get_confirm_params_hint(action_obj)
            
            if instructions_hint:
                lines.append(f"      instructions  {instructions_hint}")
            else:
                lines.append(f"      instructions")
            
            if confirm_hint:
                lines.append(f"      confirm       {confirm_hint}")
            else:
                lines.append(f"      confirm")
        else:
            lines.append(f"      instructions  [context, scope, or action-specific params]")
            lines.append(f"      confirm       [scope, decisions, assumptions, or action-specific params]")
            lines.append(f"      submit        Submit instructions directly to Cursor chat (Windows only)")
        
        lines.extend([
            "",
            "  Examples:"
        ])
        
        # Delegate to collection class
        example_collection = CommandExampleCollection(self.command_examples)
        lines.extend(example_collection.format_as_lines())
        
        lines.append("")
        lines.append("  Other Commands:")
        
        # Delegate to collection class
        other_cmd_collection = OtherCommandCollection(self.other_commands)
        lines.extend(other_cmd_collection.format_as_lines())
        
        lines.extend([
            "",
            "  Scope Command Details:",
            "    IMPORTANT: You can only have ONE scope type at a time (story OR files, never both).",
            "    Setting a new scope REPLACES any previous scope.",
            "",
            "    When passing file/folder paths to scope, you MUST provide the COMPLETE",
            "    folder structure. Use ABSOLUTE paths or FULL relative paths from the work path.",
            "",
            "    Usage (pick ONE - each replaces the previous scope):",
            "      echo 'scope' | python repl_main.py                           - Show current scope",
            "      echo 'scope all' | python repl_main.py                       - Clear scope filter",
            "      echo 'scope showAll' | python repl_main.py                   - Show entire story graph (no filtering)",
            "      echo 'scope \"Story Name\"' | python repl_main.py              - Filter by story (replaces file scope)",
            '      echo \'scope "file:C:/path/to/src/**/*.py"\' | python repl_main.py - Filter by files (replaces story scope)',
            "",
            "    Examples (CORRECT - each sets a SINGLE scope type):",
            '      scope "Enter Password, Authenticate User"                                        - Story scope',
            '      scope "file:C:/dev/augmented-teams/agile_bot/bots/base_bot/src/**/*.py"          - File scope with glob',
            "",
            "    Examples (INCORRECT - DO NOT USE):",
            "      scope src              [X] partial path - missing parent directories",
            "      scope repl_cli         [X] folder name only - incomplete structure",
            "      scope ..\\src           [X] relative navigation - use complete paths",
        ])
        
        # Add headless mode section
        lines.extend(self._headless_help.format_as_lines())
        
        return "\n".join(lines)
    
    def behavior_help(self, behavior_name: str) -> Optional[BehaviorHelp]:
        behavior = self.bot.behaviors.find_by_name(behavior_name)
        if not behavior:
            return None
        return BehaviorHelp(behavior)
    
    def action_help(self, behavior_name: str, action_name: str) -> Optional[ActionHelp]:
        bh = self.behavior_help(behavior_name)
        if not bh:
            return None
        return bh.action(action_name)
