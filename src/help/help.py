
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CoreCommands:
    
    @property
    def navigation_pattern(self) -> str:
        return "echo '[behavior.][action.]operation' | python repl_main.py"
    
    @property
    def short_navigation_pattern(self) -> str:
        return "echo '[behavior][.action]' | python repl_main.py"
    
    @property
    def description_full(self) -> str:
        return "navigate and perform operation"
    
    @property
    def description_short(self) -> str:
        return "navigate to behavior/action"

@dataclass
class OtherCommands:
    
    @property
    def commands(self) -> List[tuple[str, str]]:
        return [
            ('status', 'Show full workflow hierarchy'),
            ('back', 'Go back to previous action'),
            ('current', 'Re-execute current operation'),
            ('next', 'Advance to next action'),
            ('path [dir]', 'Show/set working directory'),
            ('scope [filter]', 'Set scope filter (see Scope Command Details)'),
            ('scope all', 'Clear scope filter'),
            ('help', 'Show this help'),
            ('exit', 'Exit CLI'),
        ]

@dataclass
class CommandExamples:
    
    @property
    def examples(self) -> List[tuple[str, str]]:
        return [
            ('.', 'Execute current behavior.action.operation'),
            ('shape', 'Jump to behavior and execute first action.operation'),
            ('build', 'Jump to action and execute first operation'),
            ('submit scope="s1"', 'Jump to operation with params and execute'),
            ('shape.build', 'Jump to behavior.action and execute first operation'),
            ('shape.build.submit', 'Jump to behavior.action.operation and execute'),
        ]

@dataclass
class CommandsHelp:
    
    def __init__(self):
        self.core = CoreCommands()
        self.other = OtherCommands()
        self.examples = CommandExamples()

@dataclass
class ScopeHelp:
    
    @property
    def important_rules(self) -> List[str]:
        return [
            "IMPORTANT: You can only have ONE scope type at a time (story OR files, never both).",
            "Setting a new scope REPLACES any previous scope.",
            "",
            "When passing file/folder paths to scope, you MUST provide the COMPLETE",
            "folder structure. Use ABSOLUTE paths or FULL relative paths from the work path.",
        ]
    
    @property
    def usage_patterns(self) -> List[tuple[str, str]]:
        return [
            ('scope', 'Show current scope'),
            ('scope all', 'Clear scope filter'),
            ('scope "Story Name"', 'Filter by story (replaces file scope)'),
            ('scope "file:C:/path/to/src/**/*.py"', 'Filter by files (replaces story scope)'),
        ]
    
    @property
    def correct_examples(self) -> List[tuple[str, str]]:
        return [
            ('scope "Enter Password, Authenticate User"', 'Story scope'),
            ('scope "file:C:/dev/augmented-teams/agile_bots/src/**/*.py"', 'File scope with glob'),
        ]
    
    @property
    def incorrect_examples(self) -> List[tuple[str, str]]:
        return [
            ('scope src', 'partial path - missing parent directories'),
            ('scope repl_cli', 'folder name only - incomplete structure'),
            ('scope ..\\src', 'relative navigation - use complete paths'),
        ]

@dataclass
class OperationsHelp:
    
    @property
    def operations(self) -> List[tuple[str, str]]:
        return [
            ('instructions', '[context, scope, or action-specific params]'),
            ('submit', '[scope, decisions, assumptions, or action-specific params]'),
            ('confirm', ''),
        ]

@dataclass
class ComponentsHelp:
    
    def __init__(self, behaviors_names: Optional[List[str]] = None, actions_list: Optional[List] = None):
        self._behaviors_names = behaviors_names or []
        self._actions_list = actions_list or []
        self.operations = OperationsHelp()
    
    @property
    def behaviors(self) -> str:
        return " | ".join(self._behaviors_names)
    
    @property
    def actions(self) -> List[tuple[str, str]]:
        result = []
        for action in self._actions_list:
            result.append((action.action_name, action.description))
        return result

class Help:
    
    def __init__(self, bot=None):
        self.bot = bot
        self.commands = CommandsHelp()
        self.scope = ScopeHelp()
        
        if bot:
            behaviors_names = bot.behaviors.names if hasattr(bot, 'behaviors') else []
            actions_list = []
            if hasattr(bot, 'behaviors'):
                for behavior in bot.behaviors:
                    for action in behavior.actions:
                        if not any(a.action_name == action.action_name for a in actions_list):
                            actions_list.append(action)
            self.components = ComponentsHelp(behaviors_names, actions_list)
        else:
            self.components = ComponentsHelp()
    
    @property
    def available_commands(self) -> List[str]:
        return ['status', 'back', 'current', 'next', 'path', 'scope', 'help', 'exit']
