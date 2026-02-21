import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import json
from datetime import datetime
from behaviors import Behaviors, Behavior
from bot_path import BotPath
from scope.scope import Scope
from help import Help
from navigation import NavigationResult
from exit_result import ExitResult
from utils import read_json_file
from story_graph import StoryMap

logger = logging.getLogger(__name__)
__all__ = ['Bot', 'BotResult', 'Behavior']

DEFAULT_ACTION_DONE_TIMEOUT_SECONDS = 3600.0
DEFAULT_ACTION_DONE_POLL_INTERVAL_SECONDS = 2.0

class BotResult:

    def __init__(self, status: str, behavior: str, action: str, data: Dict[str, Any]=None):
        self.status = status
        self.behavior = behavior
        self.action = action
        self.data = data or {}
        self.executed_instructions_from = f'{behavior}/{action}'

class Bot:
    _active_bot_instance: Optional['Bot'] = None
    _active_bot_name: Optional[str] = None

    def __init__(self, bot_name: str, bot_directory: Path, config_path: Path, workspace_path: Path=None):
        self.name = bot_name
        self.bot_name = bot_name
        self.config_path = Path(config_path)
        
        Bot._active_bot_instance = self
        Bot._active_bot_name = bot_name
        


        self.bot_paths = BotPath(workspace_path=workspace_path, bot_directory=bot_directory)
        bot_config_path = self.bot_paths.bot_directory / 'bot_config.json'
        if not bot_config_path.exists():
            raise FileNotFoundError(f'Bot config not found at {bot_config_path}')
        self._config = read_json_file(bot_config_path)
        allowed_behaviors = self._config.get('behaviors')
        self.behaviors = Behaviors(bot_name, self.bot_paths, allowed_behaviors=allowed_behaviors)
        self.behaviors._bot_instance = self
        for behavior in self.behaviors:
            behavior.bot = self
            behavior.bot_name = self.bot_name
        
        self._scope = Scope(self.bot_paths.workspace_directory, self.bot_paths)
        self._scope.load()
        
        self._story_graph = None
        self._story_graph_file_mtime = None

    @property
    def base_actions_path(self) -> Path:
        return self.bot_paths.base_actions_directory

    @property
    def description(self) -> str:
        return self._config.get('description', '')

    @property
    def goal(self) -> str:
        return self._config.get('goal', '')

    @property
    def instructions(self) -> List[str]:
        return self._config.get('instructions', [])

    @property
    def mcp(self) -> Dict[str, Any]:
        return self._config.get('mcp', {})

    @property
    def trigger_words(self) -> List[str]:
        return self._config.get('trigger_words', [])

    @property
    def working_area(self) -> Optional[str]:
        return self._config.get('WORKING_AREA')
    
    @property
    def bot_directory(self) -> Path:
        return self.bot_paths.bot_directory
    
    @property
    def workspace_directory(self) -> Path:
        return self.bot_paths.workspace_directory

    @property
    def story_map(self) -> StoryMap:
        """Lazy-load and return the story map from workspace.
        
        Returns:
            StoryMap: The loaded story map with Epic/SubEpic/Story hierarchy
            
        Raises:
            FileNotFoundError: If story-graph.json doesn't exist in workspace
        """
        story_graph_path = self.bot_paths.story_graph_paths.story_graph_path
        

        if self._story_graph is not None and story_graph_path.exists():
            try:
                current_mtime = story_graph_path.stat().st_mtime

                if self._story_graph_file_mtime is None or current_mtime > self._story_graph_file_mtime:
                    self._story_graph = None
                    self._story_graph_file_mtime = None
            except (OSError, ValueError) as e:
                logger.debug(f"Could not read story graph mtime for cache invalidation: {e}")
        
        if self._story_graph is None:
            if not story_graph_path.exists():
                raise FileNotFoundError(
                    f'Story graph not found at {story_graph_path}. '
                    f'Please create a story-graph.json file in the docs/story directory.'
                )
            
            with open(story_graph_path, 'r', encoding='utf-8') as f:
                story_graph_data = json.load(f)
            
            self._story_graph = StoryMap(story_graph_data, bot=self)

            try:
                self._story_graph_file_mtime = story_graph_path.stat().st_mtime
            except (OSError, ValueError) as e:
                import time
                logger.debug(f"Could not get story graph mtime, using current time: {e}")
                self._story_graph_file_mtime = time.time()
        
        return self._story_graph
    
    def reload_story_graph(self) -> dict:
        """Clear the cached story graph to force reload on next access.
        
        Returns:
            dict: Status message indicating the cache was cleared
        """
        self._story_graph = None
        self._story_graph_file_mtime = None
        return {'status': 'success', 'message': 'Story graph cache cleared'}

    def generate_context_package(self) -> dict:
        """Generate .mdc rule files from active bot behaviors to workspace .cursor/rules/.

        Returns:
            dict: Result with created_files and summary
        """
        from synchronizers.context_package.rule_file_generator import RuleFileGenerator
        bot = self.active_bot
        generator = RuleFileGenerator(
            bot_directory=bot.bot_directory,
            workspace_directory=bot.workspace_directory
        )
        return generator.generate()



    @property
    def story_graph(self) -> StoryMap:


        return self.story_map

    @property
    def progress_path(self) -> str:
        if self.behaviors.current:
            behavior = self.behaviors.current
            if behavior.actions.current_action_name:
                return f"{behavior.name}.{behavior.actions.current_action_name}"
            else:
                return behavior.name
        return "idle"
    
    @property
    def stage_name(self) -> str:
        if not self.behaviors.current:
            return "Idle"
        elif not self.behaviors.current.actions.current_action_name:
            return "Ready"
        else:
            return "In Progress"
    
    @property
    def commands(self) -> 'Help':
        return self.help()
    
    @property
    def current_behavior_name(self) -> str:
        return self.behaviors.current.name if self.behaviors.current else None
    
    @property
    def current_action_name(self) -> str:
        if self.behaviors.current and self.behaviors.current.actions.current_action_name:
            return self.behaviors.current.actions.current_action_name
        return None
    
    @property
    def bots(self) -> List[str]:
        registered_bots = []
        
        bots_parent_dir = self.bot_paths.bot_directory.parent
        if not (bots_parent_dir.exists() and bots_parent_dir.is_dir()):
            return []
        
        for bot_dir in bots_parent_dir.iterdir():
            if not bot_dir.is_dir():
                continue
            
            bot_config = bot_dir / 'bot_config.json'
            if bot_config.exists():
                registered_bots.append(bot_dir.name)
        
        return sorted(registered_bots)
    
    @property
    def active_bot(self) -> 'Bot':
        return Bot._active_bot_instance if Bot._active_bot_instance else self
    
    @active_bot.setter
    def active_bot(self, bot_name: str):
        registered_bots = self.bots
        
        if bot_name not in registered_bots:
            raise ValueError(
                f"Bot '{bot_name}' not found. Available bots: {', '.join(registered_bots)}"
            )
        
        if bot_name == Bot._active_bot_name:
            return
        
        bots_parent_dir = self.bot_paths.bot_directory.parent
        new_bot_dir = bots_parent_dir / bot_name
        new_config_path = new_bot_dir / 'bot_config.json'
        
        if not new_config_path.exists():
            raise FileNotFoundError(f"Bot config not found at {new_config_path}")
        
        Bot(
            bot_name=bot_name,
            bot_directory=new_bot_dir,
            config_path=new_config_path
        )

    def help(self, topic: Optional[str] = None):
        from help.help import Help
        
        return Help(bot=self)
    
    def exit(self) -> Dict[str, Any]:
        return {
            'status': 'exit',
            'message': 'Exiting bot session. Goodbye!'
        }
    
    
    def current(self) -> Dict[str, Any]:
        if not self.behaviors.current:
            return {
                'status': 'error',
                'message': 'No current behavior'
            }
        
        behavior = self.behaviors.current
        if not behavior.actions.current:
            return {
                'status': 'error',
                'message': 'No current action'
            }
        
        action = behavior.actions.current
        
        try:
            from actions.action_context import ActionContext
            context = action.context_class() if hasattr(action, 'context_class') else ActionContext()
            instructions = action.get_instructions(context)
            
            return instructions
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error getting instructions: {str(e)}'
            }
    
    def _clear_scope_and_return_result(self, message: str):
        self._scope.clear()
        self._scope.save()
        from scope.scope_command_result import ScopeCommandResult
        return ScopeCommandResult(
            status='success',
            message=message,
            scope=self._scope
        )
    
    def _normalize_scope_filter(self, scope_filter: str) -> str:
        scope_filter_lower = scope_filter.lower().strip()
        if scope_filter_lower.startswith('set '):
            scope_filter = scope_filter[4:].strip()
        
        scope_filter = scope_filter.strip()
        if (scope_filter.startswith('"') and scope_filter.endswith('"')) or \
           (scope_filter.startswith("'") and scope_filter.endswith("'")):
            scope_filter = scope_filter[1:-1]
        
        return scope_filter.strip()
    
    def _determine_scope_type(self, prefix: str):
        from scope.scope import ScopeType
        
        if prefix in ('file', 'files'):
            return ScopeType.FILES
        elif prefix in ('story', 'epic', 'subepic'):
            return ScopeType.STORY
        elif prefix == 'increment':
            return ScopeType.INCREMENT
        else:
            return ScopeType.STORY
    
    def _looks_like_file_path(self, values: list) -> bool:
        import os
        return any(os.path.isabs(v) or '\\' in v or '/' in v for v in values)
    
    def _parse_delimited_scope(self, scope_filter: str):
        delimiter = '=' if '=' in scope_filter else ':'
        prefix, value_part = scope_filter.split(delimiter, 1)
        
        prefix = prefix.strip().lower()
        value_part = value_part.strip()
        scope_values = [v.strip() for v in value_part.split(',') if v.strip()]
        
        scope_type = self._determine_scope_type(prefix)
        if prefix in ('story', 'epic'):
            prefix = prefix
        elif prefix not in ('file', 'files', 'increment'):
            prefix = 'story'
        
        return scope_type, prefix, scope_values
    
    def _parse_spaced_scope(self, scope_filter: str):
        parts = scope_filter.split(None, 1)
        potential_prefix = parts[0].lower()
        
        if potential_prefix in ('story', 'epic', 'subepic', 'increment', 'file', 'files'):
            prefix = potential_prefix
            value_part = parts[1] if len(parts) > 1 else ''
            scope_values = [v.strip() for v in value_part.split(',') if v.strip()]
            scope_type = self._determine_scope_type(prefix)
            return scope_type, prefix, scope_values
        

        scope_values = [v.strip() for v in scope_filter.split(',') if v.strip()]
        if self._looks_like_file_path(scope_values):
            return self._determine_scope_type('files'), 'files', scope_values
        else:
            return self._determine_scope_type('story'), 'story', scope_values
    
    def _parse_undelimited_scope(self, scope_filter: str):
        scope_values = [v.strip() for v in scope_filter.split(',') if v.strip()]
        
        if self._looks_like_file_path(scope_values):
            return self._determine_scope_type('files'), 'files', scope_values
        else:
            return self._determine_scope_type('story'), 'story', scope_values
    
    def scope(self, scope_filter: Optional[str] = None):
        from scope.scope import ScopeType
        
        if scope_filter is None:
            return self._scope
        
        scope_filter = self._normalize_scope_filter(scope_filter)
        scope_filter_lower = scope_filter.lower()
        

        if scope_filter_lower == 'clear':
            return self._clear_scope_and_return_result('Scope cleared')
        
        if scope_filter_lower == 'all':
            return self._clear_scope_and_return_result('Scope cleared (set to all)')
        
        if scope_filter_lower == 'showall':
            self._scope.filter(ScopeType.SHOW_ALL, [])
            self._scope.save()
            from scope.scope_command_result import ScopeCommandResult
            return ScopeCommandResult(
                status='success',
                message='Scope set to show all',
                scope=self._scope
            )
        

        if scope_filter_lower.startswith('include_level='):
            level = scope_filter.split('=', 1)[1].strip().lower()
            valid_levels = ['stories', 'domain_concepts', 'acceptance', 'scenarios', 'examples', 'tests', 'code']
            if level in valid_levels:
                self._scope.include_level = level
                self._scope.save()
                from scope.scope_command_result import ScopeCommandResult
                return ScopeCommandResult(
                    status='success',
                    message=f'Include level set to {level}',
                    scope=self._scope
                )
            return ScopeCommandResult(
                status='error',
                message=f"Invalid include_level '{level}'. Valid: {', '.join(valid_levels)}",
                scope=self._scope
            )
        

        if '=' in scope_filter or ':' in scope_filter:
            scope_type, prefix, scope_values = self._parse_delimited_scope(scope_filter)
        elif ' ' in scope_filter:
            scope_type, prefix, scope_values = self._parse_spaced_scope(scope_filter)
        else:
            scope_type, prefix, scope_values = self._parse_undelimited_scope(scope_filter)
        
        self._scope.filter(scope_type, scope_values)
        self._scope.save()
        
        from scope.scope_command_result import ScopeCommandResult
        return ScopeCommandResult(
            status='success',
            message=f'Scope set to {prefix}: {", ".join(scope_values)}',
            scope=self._scope
        )
    
    def workspace(self, directory: Optional[str] = None) -> Dict[str, Any]:
        return self.path(directory)
    
    def path(self, directory: Optional[str] = None) -> Dict[str, Any]:
        if directory is None:
            current_path = self.bot_paths.workspace_directory
            return {
                'status': 'success',
                'path': str(current_path),
                'message': f'Current working directory: {current_path}'
            }
        
        new_path = Path(directory)
        if not new_path.is_absolute():
            new_path = self.bot_paths.workspace_directory / new_path
        
        if not new_path.exists():
            return {
                'status': 'error',
                'message': f'Directory does not exist: {new_path}'
            }
        
        self.bot_paths.update_workspace_directory(new_path, persist=True)
        
        self._scope = Scope(self.bot_paths.workspace_directory, self.bot_paths)
        self._scope.load()
        
        return {
            'status': 'success',
            'path': str(new_path),
            'message': f'Working directory set to: {new_path}'
        }

    def _navigate_and_save(self, behavior, action_name: str, message_prefix: str = "Moved to") -> Dict[str, Any]:
        behavior.actions.navigate_to(action_name)
        self.behaviors.save_state()
        return {
            'status': 'success',
            'message': f'{message_prefix} {behavior.name}.{action_name}',
            'behavior': behavior.name,
            'action': action_name
        }
    
    def next(self) -> Dict[str, Any]:
        if not self.behaviors.current:
            return {
                'status': 'error',
                'message': 'No behavior is currently active. Use a behavior.action command to start.'
            }
        
        behavior = self.behaviors.current
        current_action = behavior.actions.current_action_name
        
        if not current_action:
            if behavior.action_names:
                first_action = behavior.action_names[0]
                return self._navigate_and_save(behavior, first_action)
            else:
                return {
                    'status': 'error',
                    'message': f'Behavior {behavior.name} has no actions'
                }
        
        action_names = behavior.action_names
        try:
            current_index = action_names.index(current_action)
            if current_index < len(action_names) - 1:
                next_action = action_names[current_index + 1]
                return self._navigate_and_save(behavior, next_action)
            else:
                advance_result = self.behaviors.advance()
                return advance_result
        except ValueError:
            return {
                'status': 'error',
                'message': f'Current action {current_action} not found in behavior'
            }
    
    def back(self) -> Dict[str, Any]:
        if not self.behaviors.current:
            return {
                'status': 'error',
                'message': 'No behavior is currently active'
            }
        
        behavior = self.behaviors.current
        current_action = behavior.actions.current_action_name
        
        if not current_action:
            return {
                'status': 'error',
                'message': 'No current action to go back from'
            }
        
        action_names = behavior.action_names
        try:
            current_index = action_names.index(current_action)
            if current_index > 0:
                prev_action = action_names[current_index - 1]
                return self._navigate_and_save(behavior, prev_action, "Moved back to")
            else:
                return {
                    'status': 'info',
                    'message': f'Already at first action in {behavior.name}',
                    'behavior': behavior.name,
                    'action': current_action
                }
        except ValueError:
            return {
                'status': 'error',
                'message': f'Current action {current_action} not found in behavior'
            }
    
    def execute(self, behavior_name: str, action_name: Optional[str] = None, params: Optional[Dict[str, Any]] = None, include_scope: bool = False) -> Any:
        behavior = self.behaviors.find_by_name(behavior_name)
        if not behavior:
            return {
                'status': 'error',
                'message': f'Behavior not found: {behavior_name}',
                'available_behaviors': [b.name for b in self.behaviors]
            }
        
        self.behaviors.navigate_to(behavior_name)
        
        if action_name:
            try:
                behavior.actions.navigate_to(action_name)
            except ValueError:
                return {
                    'status': 'error',
                    'message': f'Action not found: {action_name}',
                    'available_actions': behavior.action_names
                }
        else:
            if not behavior.actions.current_action_name:
                if behavior.action_names:
                    behavior.actions.navigate_to(behavior.action_names[0])
                else:
                    return {
                        'status': 'error',
                        'message': f'Behavior {behavior_name} has no actions'
                    }
        
        action = behavior.actions.current
        if not action:
            return {
                'status': 'error',
                'message': f'No current action in {behavior_name}'
            }
        
        self.behaviors.save_state()
        
        behavior_execute = self.get_behavior_execute(behavior_name)
        if behavior_execute == 'skip':
            return {'status': 'skipped', 'message': f'Behavior {behavior_name} has execute set to skip', 'actions_run': [], 'actions_skipped': behavior.action_names}
        
        try:
            from actions.action_context import ActionContext, ScopeActionContext
            context = action.context_class() if hasattr(action, 'context_class') else ActionContext()
            
            if params:

                if 'scope' in params and isinstance(params['scope'], dict):
                    from scope.scope import Scope, ScopeType
                    scope_dict = params.pop('scope')
                    try:
                        from utils.scope_debug_log import log
                        log(f"[BOT] execute RECEIVED scope in params: scope_dict={scope_dict}", self.workspace_directory)
                    except Exception as e:
                        logger.debug(f"Scope debug log skipped: {e}")
                    scope = Scope(self.workspace_directory, self.bot_paths)
                    scope_type = ScopeType(scope_dict.get('type', 'all'))
                    scope_value = scope_dict.get('value', [])
                    if not isinstance(scope_value, list):
                        scope_value = [scope_value]
                    scope.filter(scope_type, scope_value)
                    setattr(context, 'scope', scope)
                    setattr(context, '_scope_from_params', True)
                    try:
                        from utils.scope_debug_log import log
                        log(f"[BOT] execute SET context.scope type={scope_type} value={scope_value}", self.workspace_directory)
                    except Exception as e:
                        logger.debug(f"Scope debug log skipped: {e}")
                

                for key, value in params.items():
                    setattr(context, key, value)
            elif hasattr(context, 'scope'):

                try:
                    from utils.scope_debug_log import log
                    log(f"[BOT] execute NO scope in params - using bot._scope (params had scope? no)", self.workspace_directory)
                except Exception as e:
                    logger.debug(f"Scope debug log skipped: {e}")
                self._scope.load()
                if self._scope.value or self._scope.type.value == 'showAll':
                    setattr(context, 'scope', self._scope)
                    include_scope = True
            
            execution_mode = self.get_execution_mode(behavior_name, action.action_name)
            current_action_name = action.action_name
            action_names = behavior.action_names


            if execution_mode == 'combine_next':
                pass
            if execution_mode == 'skip':
                try:
                    idx = action_names.index(current_action_name)
                    while idx + 1 < len(action_names):
                        idx += 1
                        next_name = action_names[idx]
                        if self.get_execution_mode(behavior_name, next_name) != 'skip':
                            behavior.actions.navigate_to(next_name)
                            self.behaviors.save_state()
                            action = behavior.actions.current
                            current_action_name = action.action_name
                            context = action.context_class() if hasattr(action, 'context_class') else ActionContext()
                            if params:
                                if 'scope' in params and isinstance(params.get('scope'), dict):
                                    from scope.scope import Scope, ScopeType
                                    scope_dict = params.pop('scope', {})
                                    scope = Scope(self.workspace_directory, self.bot_paths)
                                    scope_type = ScopeType(scope_dict.get('type', 'all'))
                                    scope_value = scope_dict.get('value', [])
                                    if not isinstance(scope_value, list):
                                        scope_value = [scope_value]
                                    scope.filter(scope_type, scope_value)
                                    setattr(context, 'scope', scope)
                                for key, value in params.items():
                                    setattr(context, key, value)
                            elif hasattr(context, 'scope'):
                                self._scope.load()
                                if self._scope.value or self._scope.type.value == 'showAll':
                                    setattr(context, 'scope', self._scope)
                                    include_scope = True
                            execution_mode = self.get_execution_mode(behavior_name, current_action_name)
                            break
                except (ValueError, IndexError) as e:
                    logger.debug(f"Skip navigation failed: {e}")



            instructions = action.get_instructions(context, include_scope=include_scope)
            return instructions
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error executing {behavior_name}.{action.action_name}: {str(e)}'
            }
    
    def _append_next_action_instructions_if_combine_next(
        self,
        behavior,
        behavior_name: str,
        current_action_name: str,
        action,
        instructions,
        context=None,
        include_scope: bool = False,
    ) -> Optional[str]:
        """Combine with next: run current then run the next one too. Returns last appended action name, or None.
        Mental model: Go to first action. If it's not skip, do it. If it's combine_next, go to next action. Repeat.
        When combining: scope, clarification, context files, behavior instructions shown only once (in first action).
        Subsequent actions use action-only content. Combining text added at top and between actions."""
        if self.get_execution_mode(behavior_name, current_action_name) != 'combine_next':
            return None
        action_names = behavior.action_names
        try:
            idx = action_names.index(current_action_name)
        except ValueError:
            return None
        last_appended: Optional[str] = None
        first_append = True
        while idx + 1 < len(action_names):
            next_action_name = action_names[idx + 1]
            next_mode = self.get_execution_mode(behavior_name, next_action_name)
            if next_mode == 'skip':
                idx += 1
                continue

            current_mode = self.get_execution_mode(behavior_name, action_names[idx])
            if current_mode != 'combine_next':
                break
            next_action = behavior.actions.find_by_name(next_action_name)
            if not next_action:
                break
            if first_append:
                instructions._display_content.insert(0, '')
                instructions._display_content.insert(0, '**Combined instructions:** The following combines multiple actions. Perform them one after another.')
                first_append = False
            next_instructions = next_action.get_instructions(None, include_scope=False)
            next_intro = '**Next:** Perform the following action.'
            if next_action_name == 'validate':
                next_intro += ' Fix any errors found in the Violation.'
            instructions.add_display('', '---', f'## Next action: {next_action_name}', next_intro, '')
            from instructions.markdown_instructions import MarkdownInstructions
            action_only_md = MarkdownInstructions(next_instructions, include_scope=False, action_only=True)
            action_only_lines = action_only_md.serialize().split('\n')
            for line in action_only_lines:
                instructions.add_display(line)
            last_appended = next_action_name
            idx += 1
        return last_appended

    def _append_next_behavior_instructions_if_combine_with_next(
        self,
        current_behavior,
        instructions,
        first_append: bool,
    ) -> None:
        """When behavior has combine_with_next, append the next behavior's non-skip actions. Recurses if next also has combine_with_next."""
        behavior = current_behavior
        while True:
            if self.get_behavior_execute(behavior.name) != 'combine_with_next':
                break
            next_behavior = self.behaviors.next_after(behavior)
            if not next_behavior:
                break
            if self.get_behavior_execute(next_behavior.name) == 'skip':
                break
            if first_append:
                instructions._display_content.insert(0, '')
                instructions._display_content.insert(0, '**Combined instructions:** The following combines multiple actions. Perform them one after another.')
                first_append = False
            for action_name in next_behavior.action_names:
                if self.get_execution_mode(next_behavior.name, action_name) == 'skip':
                    continue
                next_action = next_behavior.actions.find_by_name(action_name)
                if not next_action:
                    continue
                next_instructions = next_action.get_instructions(None, include_scope=False)
                next_intro = '**Next:** Perform the following action.'
                if action_name == 'validate':
                    next_intro += ' Fix any errors found in the Violation.'
                instructions.add_display('', '---', f'## Next action: {next_behavior.name}.{action_name}', next_intro, '')
                from instructions.markdown_instructions import MarkdownInstructions
                action_only_md = MarkdownInstructions(next_instructions, include_scope=False, action_only=True)
                for line in action_only_md.serialize().split('\n'):
                    instructions.add_display(line)
            behavior = next_behavior

    ACTION_IS_DONE_FILENAME = 'action_is_done.json'

    def _action_is_done_path(self) -> Path:
        return self.workspace_directory / self.ACTION_IS_DONE_FILENAME

    def set_action_is_done(self, value: bool) -> None:


        path = self._action_is_done_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({'action_is_done': value}, indent=2), encoding='utf-8')

    def get_action_is_done(self) -> bool:


        path = self._action_is_done_path()
        if not path.exists():
            return False
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return data.get('action_is_done', False)
        except (json.JSONDecodeError, OSError):
            return False

    def wait_until_action_done(self, timeout_seconds: float = DEFAULT_ACTION_DONE_TIMEOUT_SECONDS, poll_interval: float = DEFAULT_ACTION_DONE_POLL_INTERVAL_SECONDS) -> bool:


        import time
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if self.get_action_is_done():
                return True
            time.sleep(poll_interval)
        return False

    def get_execution_mode(self, behavior_name: str, action_name: str) -> str:


        path = self.workspace_directory / 'execution_settings.json'
        if not path.exists():
            return 'manual'
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            key = f"{self.bot_name}.{behavior_name}.{action_name}"
            mode = data.get(key, 'manual')
            return 'combine_next' if mode == 'auto' else mode
        except (json.JSONDecodeError, OSError):
            return 'manual'

    def set_action_execution(self, behavior_name: str, action_name: str, mode: str) -> Dict[str, Any]:


        path = self.workspace_directory / 'execution_settings.json'
        data = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError) as e:
                logger.debug(f"Could not load execution_settings.json, starting fresh: {e}")
        key = f"{self.bot_name}.{behavior_name}.{action_name}"
        data[key] = 'combine_next' if mode == 'auto' else mode
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return {'status': 'success', 'message': f'{behavior_name}.{action_name} set to {mode}', 'key': key}

    def _behavior_execute_key(self, behavior_name: str) -> str:
        return f"{self.bot_name}._behavior.{behavior_name}"

    def get_behavior_execute(self, behavior_name: str) -> str:
        path = self.workspace_directory / 'execution_settings.json'
        if not path.exists():
            return 'manual'
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            key = self._behavior_execute_key(behavior_name)
            mode = data.get(key, 'manual')
            return 'combine_with_next' if mode == 'auto' else mode
        except (json.JSONDecodeError, OSError):
            return 'manual'

    def set_behavior_execute(self, behavior_name: str, mode: str) -> Dict[str, Any]:
        if mode not in ('combine_with_next', 'skip', 'manual'):
            raise ValueError(f"Invalid behavior execution mode: {mode}. Use combine_with_next, skip, or manual.")
        path = self.workspace_directory / 'execution_settings.json'
        data = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError) as e:
                logger.debug(f"Could not load execution_settings.json, starting fresh: {e}")
        key = self._behavior_execute_key(behavior_name)
        data[key] = 'combine_with_next' if mode == 'auto' else mode
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return {'status': 'success', 'message': f'{behavior_name} set to {mode}', 'key': key}

    def get_execution_settings(self) -> Dict[str, str]:


        path = self.workspace_directory / 'execution_settings.json'
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            prefix = f"{self.bot_name}."
            result = {}
            for key, mode in data.items():
                if isinstance(mode, str) and key.startswith(prefix):
                    result[key[len(prefix):]] = 'combine_next' if mode == 'auto' else mode
            return result
        except (json.JSONDecodeError, OSError):
            return {}

    def _bot_workspace_path(self) -> Path:
        return self.bot_paths.story_graph_paths.bot_workspace_config_path

    def _load_special_instructions(self) -> Dict[str, str]:
        path = self._bot_workspace_path()
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            return dict(data.get('special_instructions', {}))
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_special_instructions(self, si_data: Dict[str, str]) -> None:
        path = self._bot_workspace_path()
        data = {}
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError):
                pass
        data['special_instructions'] = si_data
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def get_special_instructions_settings(self) -> Dict[str, str]:
        result = {}
        for behavior in self.behaviors:
            text = self.get_behavior_special_instructions(behavior.name)
            if text:
                result[behavior.name] = text
            for action in behavior.actions:
                text = self.get_action_special_instructions(behavior.name, action.action_name)
                if text:
                    result[f"{behavior.name}.{action.action_name}"] = text
        return result

    def set_behavior_special_instructions(self, behavior_name: str, instruction_text: str) -> Dict[str, Any]:
        behavior = self.behaviors.find_by_name(behavior_name)
        if not behavior:
            return {'status': 'error', 'message': f'Behavior {behavior_name} not found'}
        si_data = self._load_special_instructions()
        si_data[behavior_name] = instruction_text
        self._save_special_instructions(si_data)
        return {'status': 'success', 'message': f'Stored special instructions for {behavior_name}'}

    def set_action_special_instructions(self, behavior_name: str, action_name: str, instruction_text: str) -> Dict[str, Any]:
        behavior = self.behaviors.find_by_name(behavior_name)
        if not behavior:
            return {'status': 'error', 'message': f'Behavior {behavior_name} not found'}
        action = behavior.actions.find_by_name(action_name)
        if not action:
            return {'status': 'error', 'message': f'Action {action_name} not found in {behavior_name}'}
        si_data = self._load_special_instructions()
        key = f"{behavior_name}.{action_name}"
        si_data[key] = instruction_text
        self._save_special_instructions(si_data)
        return {'status': 'success', 'message': f'Stored special instructions for {behavior_name}.{action_name}'}

    def get_behavior_special_instructions(self, behavior_name: str) -> Optional[str]:
        si_data = self._load_special_instructions()
        return si_data.get(behavior_name) or None

    def get_action_special_instructions(self, behavior_name: str, action_name: str) -> Optional[str]:
        si_data = self._load_special_instructions()
        return si_data.get(f"{behavior_name}.{action_name}") or None

    def _collect_special_instructions_for_prompt(self, behavior_name: str, action_name: str) -> List[str]:
        lines = []
        behavior_instruction = self.get_behavior_special_instructions(behavior_name)
        if behavior_instruction:
            lines.append(f"**Special Instructions (behavior {behavior_name}):** {behavior_instruction}")
        action_instruction = self.get_action_special_instructions(behavior_name, action_name)
        if action_instruction:
            lines.append(f"**Special Instructions ({behavior_name}.{action_name}):** {action_instruction}")
        return lines

    def save(self, answers: Optional[Dict[str, str]] = None,
             evidence_provided: Optional[Dict[str, str]] = None,
             decisions: Optional[Dict[str, str]] = None,
             assumptions: Optional[List[str]] = None) -> Dict[str, Any]:
        from actions.clarify.requirements_clarifications import RequirementsClarifications
        from actions.clarify.required_context import RequiredContext
        from actions.strategy.strategy_decision import StrategyDecision
        from actions.strategy.strategy import Strategy
        
        current_behavior = self.behaviors.current
        if not current_behavior:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        try:
            saved_items = []
            
            if answers or evidence_provided:
                required_context = RequiredContext(current_behavior.folder)
                clarifications = RequirementsClarifications(
                    behavior_name=current_behavior.name,
                    bot_paths=current_behavior.bot_paths,
                    required_context=required_context,
                    key_questions_answered=answers or {},
                    evidence_provided=evidence_provided or {},
                    context=None
                )
                clarifications.save()
                if answers:
                    saved_items.append('answers')
                if evidence_provided:
                    saved_items.append('evidence')
            
            if decisions or assumptions:
                strategy = Strategy(current_behavior.folder)
                strategy_decision = StrategyDecision(
                    behavior_name=current_behavior.name,
                    bot_paths=current_behavior.bot_paths,
                    strategy=strategy,
                    decisions_made=decisions or {},
                    assumptions_made=assumptions or []
                )
                strategy_decision.save()
                if decisions:
                    saved_items.append('decisions')
                if assumptions:
                    saved_items.append('assumptions')
            
            if not saved_items:
                return {
                    'status': 'error',
                    'message': 'No data provided to save'
                }
            
            return {
                'status': 'success',
                'message': f"Saved {', '.join(saved_items)} for {current_behavior.name}",
                'behavior': current_behavior.name,
                'saved': saved_items
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error saving: {str(e)}'
            }
    
    def submit_behavior_rules(self, behavior_name: str) -> Dict[str, Any]:
        saved_behavior = self.behaviors.current.name if self.behaviors.current else None
        saved_action = self.behaviors.current.actions.current_action_name if self.behaviors.current else None
        
        try:
            behavior = self.behaviors.find_by_name(behavior_name)
            if not behavior:
                return {
                    'status': 'error',
                    'message': f'Behavior not found: {behavior_name}'
                }
            
            self.behaviors.navigate_to(behavior_name)
            

            submit_result = behavior.submitRules()
            
            if saved_behavior and saved_action:
                try:
                    self.execute(saved_behavior, saved_action)
                except Exception as e:
                    logger.warning(f'Failed to restore saved behavior/action state: {str(e)}')
            
            return submit_result
            
        except Exception as e:
            logger.error(f'Error in submit_behavior_rules: {str(e)}', exc_info=True)
            return {
                'status': 'error',
                'message': f'Error getting rules for {behavior_name}: {str(e)}'
            }
    
    def submit_instructions(self, instructions, behavior_name: str = None, action_name: str = None) -> Dict[str, Any]:
        display_content = instructions.display_content
        if not display_content:
            return {
                'status': 'error',
                'message': 'No instructions available to submit'
            }
        
        if isinstance(display_content, list):
            content_str = '\n'.join(display_content)
        else:
            content_str = str(display_content)
        

        if 'pytest' in sys.modules or os.environ.get('PYTEST_CURRENT_TEST'):
            return {
                'status': 'success',
                'message': 'Instructions generated (test mode - clipboard/GUI skipped)',
                'clipboard_status': 'skipped',
                'cursor_status': 'skipped',
                'instructions': content_str
            }
        
        clipboard_status = 'failed'
        cursor_status = 'not_attempted'
        
        try:
            import pyperclip
            import pyautogui
            import time
            import platform

            pyperclip.copy(content_str)
            clipboard_status = 'success'
            time.sleep(0.2)

            cursor = (os.environ.get('IDE') or '').lower() == 'cursor'
            mac = platform.system().lower() == 'darwin'            


            if (cursor == True):
                if (mac == True):
                    pyautogui.hotkey('command', 'l')
                else:
                    pyautogui.hotkey('ctrl', 'l')

            else:
                if (mac == True):
                    pyautogui.hotkey('ctrl', 'command', 'i')
                else:
                    pyautogui.hotkey('ctrl', 'alt', 'i')
            time.sleep(0.3)


            if (mac == True):
                pyautogui.hotkey('command', 'v')
            else:
                pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            
            cursor_status = 'opened'
            
        except ImportError as e:
            clipboard_status = 'failed'
            cursor_status = f'failed: pyautogui/pyperclip not installed - {str(e)}'
        except Exception as e:
            cursor_status = f'failed: {str(e)}'
        
        if not behavior_name:
            behavior_name = getattr(instructions, 'behavior_name', 
                                   self.behaviors.current.name if self.behaviors.current else 'unknown')
        if not action_name:
            action_name = getattr(instructions, 'action_name', 'unknown')
        
        return {
            'status': 'success',
            'message': f'Instructions submitted for {behavior_name}.{action_name}',
            'behavior': behavior_name,
            'action': action_name,
            'timestamp': datetime.now().isoformat(),
            'clipboard_status': clipboard_status,
            'cursor_status': cursor_status,
            'instructions_length': len(content_str),
            'instructions': content_str
        }
    
    def submit_current_action(self, scope: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:


        current_behavior = self.behaviors.current
        if not current_behavior:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        current_action_name = current_behavior.actions.current_action_name
        if not current_action_name:
            return {
                'status': 'error',
                'message': 'No current action set'
            }

        # Advance past skip actions to the first non-skip action (same as execute flow)
        if self.get_execution_mode(current_behavior.name, current_action_name) == 'skip':
            for action_name in current_behavior.action_names:
                if self.get_execution_mode(current_behavior.name, action_name) != 'skip':
                    current_action_name = action_name
                    current_behavior.actions.navigate_to(current_action_name)
                    break
            else:
                return {
                    'status': 'error',
                    'message': f'All actions in {current_behavior.name} are set to skip'
                }
        
        try:
            action = current_behavior.actions.find_by_name(current_action_name)
            if not action:
                return {
                    'status': 'error',
                    'message': f'Action {current_action_name} not found'
                }
            

            from actions.action_context import ActionContext
            context = action.context_class() if hasattr(action, 'context_class') else ActionContext()
            if scope and isinstance(scope, dict):
                from scope.scope import Scope, ScopeType
                scope_type = ScopeType(scope.get('type', 'all'))
                scope_value = scope.get('value', [])
                if not isinstance(scope_value, list):
                    scope_value = [scope_value]
                s = Scope(self.workspace_directory, self.bot_paths)
                s.filter(scope_type, scope_value)
                setattr(context, 'scope', s)
                setattr(context, '_scope_from_params', True)
            elif hasattr(context, 'scope'):
                self._scope.load()
                if self._scope.value or self._scope.type.value == 'showAll':
                    setattr(context, 'scope', self._scope)
            

            instructions = action.get_instructions(context, include_scope=True)

            special_lines = self._collect_special_instructions_for_prompt(current_behavior.name, current_action_name)
            if special_lines:
                instructions.prepend_display("", "---", "")
                for line in reversed(special_lines):
                    instructions.prepend_display(line)

            last_appended = self._append_next_action_instructions_if_combine_next(
                current_behavior, current_behavior.name, current_action_name, action, instructions,
                context=None, include_scope=True
            )
            self._append_next_behavior_instructions_if_combine_with_next(
                current_behavior, instructions, first_append=(last_appended is None)
            )
            result = self.submit_instructions(instructions, current_behavior.name, current_action_name)
            if last_appended:
                action_names = current_behavior.action_names
                try:
                    next_idx = action_names.index(last_appended) + 1
                    if next_idx < len(action_names):
                        current_behavior.actions.navigate_to(action_names[next_idx])
                    else:
                        current_behavior.actions.navigate_to(last_appended)
                    self.behaviors.save_state()
                except ValueError as e:
                    logger.debug(f"Could not advance to next action after last_appended: {e}")
            return result
            
        except Exception as e:
            logger.error(f'Error in submit_current_action: {str(e)}', exc_info=True)
            return {
                'status': 'error',
                'message': f'Error submitting instructions: {str(e)}'
            }
    

    def tree(self) -> str:
        lines = []
        behaviors_list = list(self.behaviors)
        
        for i, behavior in enumerate(behaviors_list):
            is_last_behavior = (i == len(behaviors_list) - 1)
            behavior_prefix = "Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬" if is_last_behavior else "Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬"
            is_current_behavior = (self.behaviors.current and behavior.name == self.behaviors.current.name)
            behavior_marker = "➤ " if is_current_behavior else ""
            lines.append(f"{behavior_prefix} {behavior_marker}{behavior.name}")
            
            action_names = behavior.action_names
            for j, action in enumerate(action_names):
                is_last_action = (j == len(action_names) - 1)
                action_prefix = "    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬" if is_last_behavior else "Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬" if is_last_action else "Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬"
                if not is_last_behavior and not is_last_action:
                    action_prefix = "Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬"
                is_current_action = (is_current_behavior and 
                                   behavior.actions.current_action_name == action)
                action_marker = "➤ " if is_current_action else ""
                lines.append(f"{action_prefix} {action_marker}{action}")
        
        return "\n".join(lines)
    
    def pos(self) -> Dict[str, Any]:
        if not self.behaviors.current:
            return {
                'status': 'error',
                'message': 'No behavior is currently active'
            }
        
        behavior = self.behaviors.current
        action = behavior.actions.current_action_name
        
        if not action:
            return {
                'status': 'error',
                'message': f'No action is currently active in {behavior.name}'
            }
        
        return {
            'status': 'success',
            'behavior': behavior.name,
            'action': action,
            'position': f'{behavior.name}.{action}'
        }

    def __getattr__(self, name: str):



        if name == 'story_map':

            return type(self).story_map.fget(self)
        if name == 'story_graph':

            return type(self).story_map.fget(self)
        
        behavior = self.behaviors.find_by_name(name)
        if behavior:

            self.behaviors.navigate_to(name)
            return behavior
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
