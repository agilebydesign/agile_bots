import json
import logging
from pathlib import Path
from typing import Dict, Any, List, TYPE_CHECKING, NamedTuple
from ..utils import read_json_file
if TYPE_CHECKING:
    from ..bot.behavior import Behavior
    from ..bot.behaviors import Behaviors
logger = logging.getLogger(__name__)


class CurrentBehaviorContext(NamedTuple):
    name: str
    icon: str
    actions: List[str]
    current_action: str
    completed: List[str]


class BehaviorActionStatusBuilder:

    def __init__(self, behavior: 'Behavior'):
        self.behavior = behavior

    def get_behavior_action_status_breadcrumbs(self) -> list:
        if not self.behavior or not self.behavior.bot:
            return self._get_default_breadcrumbs()
        try:
            workspace_dir = self.behavior.bot_paths.workspace_directory
        except (AttributeError, ValueError, Exception):
            return self._get_default_breadcrumbs()
        try:
            behaviors = self.behavior.bot.behaviors
            current_behavior = behaviors.current
            completed_actions, _ = self._load_state_file(workspace_dir / 'behavior_action_state.json')
            categorization = self._categorize_behaviors(behaviors, current_behavior, completed_actions)
            lines = self._build_behavior_action_table(workspace_dir, categorization)
            lines.extend(self._build_behavior_action_progress(behaviors.names, categorization))
            return lines
        except Exception as e:
            logger.debug(f'Failed to generate behavior/action progress breadcrumbs: {e}')
            return self._get_default_breadcrumbs()

    def _load_state_file(self, state_file: Path) -> tuple:
        if not state_file.exists():
            return ([], None)
        state_data = json.loads(state_file.read_text(encoding='utf-8'))
        completed_actions = state_data.get('completed_actions', [])
        current_action_path = state_data.get('current_action', '')
        current_action_from_state = None
        if current_action_path:
            parts = current_action_path.split('.')
            if len(parts) >= 3:
                current_action_from_state = parts[2]
        return (completed_actions, current_action_from_state)

    def _categorize_behaviors(self, behaviors, current_behavior, completed_actions):
        all_behaviors = behaviors.names
        current_behavior_name = current_behavior.name
        completed_behaviors = []
        remaining_behaviors = []
        current_action_name = None
        remaining_actions_in_current = []
        current_behavior_actions = []
        current_behavior_completed = []
        for behavior_name in all_behaviors:
            behavior_obj = behaviors.find_by_name(behavior_name)
            if not behavior_obj:
                continue
            behavior_actions = behavior_obj.actions.names
            completed_for_behavior = self._get_completed_actions_for_behavior(self.behavior.bot, behavior_obj, completed_actions)
            if behavior_name == current_behavior_name:
                current_action = current_behavior.actions.current
                current_action_name = current_action.action_name if current_action else None
                current_behavior_actions = behavior_actions
                current_behavior_completed = completed_for_behavior
                if current_action_name and current_action_name in behavior_actions:
                    idx = behavior_actions.index(current_action_name)
                    remaining_actions_in_current = behavior_actions[idx + 1:]
            elif len(completed_for_behavior) == len(behavior_actions) and behavior_actions:
                completed_behaviors.append(behavior_name)
            else:
                remaining_behaviors.append({'name': behavior_name, 'actions': behavior_actions, 'completed': completed_for_behavior})
        return {'completed_behaviors': completed_behaviors, 'remaining_behaviors': remaining_behaviors, 'current_behavior_name': current_behavior_name, 'current_action_name': current_action_name, 'remaining_actions_in_current': remaining_actions_in_current, 'current_behavior_actions': current_behavior_actions, 'current_behavior_completed': current_behavior_completed}

    def _get_completed_actions_for_behavior(self, bot, behavior_obj, completed_actions):
        behavior_prefix = f'{bot.name}.{behavior_obj.name}.'
        return [action.get('action_state', '').split('.')[-1] for action in completed_actions if action.get('action_state', '').startswith(behavior_prefix)]

    def _build_behavior_action_table(self, workspace_dir, categorization):
        lines = ['',
                 '## Behavior/Action Status',
                 '',
                 '| Setting | Value |',
                 '|---------|-------|',
                 f'| **Working Directory** | {workspace_dir} |',
                 f'| **Bot Path** | {self.behavior.bot_paths.bot_directory} |']
        current_behavior_name = categorization['current_behavior_name']
        current_action_name = categorization['current_action_name']
        if current_behavior_name and current_action_name:
            lines.append(f'| **Current State** | {current_behavior_name}.{current_action_name} |')
        next_step = self._build_next_step_row(self.behavior.bot.behaviors)
        if next_step:
            lines.append(next_step)
        return lines

    def _build_next_step_row(self, behaviors) -> str:
        next_step_cmd = behaviors.next_step_command()
        if next_step_cmd:
            return f'| **Next step** | `{next_step_cmd}` |'
        return ''

    def _build_behavior_action_progress(self, all_behaviors, categorization):
        lines = ['', '## Behavior/Action Progress', '']
        DONE, CURRENT, PENDING = ('✓', '➤', '☐')
        completed_behaviors = categorization['completed_behaviors']
        current_behavior_name = categorization['current_behavior_name']
        ordered_behaviors = self._get_ordered_behaviors(all_behaviors)
        for behavior_name in ordered_behaviors:
            if behavior_name in completed_behaviors:
                lines.append(f'### {DONE} **{behavior_name}**')
            elif behavior_name == current_behavior_name:
                ctx = CurrentBehaviorContext(
                    name=behavior_name,
                    icon=CURRENT,
                    actions=categorization['current_behavior_actions'],
                    current_action=categorization['current_action_name'],
                    completed=categorization['current_behavior_completed']
                )
                lines.extend(self._build_current_behavior_section(ctx))
            else:
                lines.append(f'### {PENDING} **{behavior_name}**')
        lines.append('')
        return lines

    def _build_current_behavior_section(self, ctx: CurrentBehaviorContext):
        lines = [f'### {ctx.icon} **{ctx.name}**']
        for action_name in ctx.actions:
            lines.append(self._format_action_line(action_name, ctx.current_action, ctx.completed))
        return lines

    def _format_action_line(self, action_name: str, current_action_name: str, completed_actions: list) -> str:
        DONE, CURRENT, PENDING = ('✓', '➤', '☐')
        if action_name == current_action_name:
            return f'  - {CURRENT} **{action_name}**'
        if action_name in completed_actions:
            return f'  - {DONE} {action_name}'
        return f'  - {PENDING} {action_name}'

    def _get_ordered_behaviors(self, all_behaviors: list) -> list:
        if not self.behavior or not self.behavior.bot:
            return all_behaviors
        try:
            bot_directory = self.behavior.bot_paths.bot_directory
            behaviors_with_order = [(self._get_behavior_order(bot_directory, name), name) for name in all_behaviors]
            behaviors_with_order.sort(key=lambda x: x[0])
            return [name for _, name in behaviors_with_order]
        except Exception:
            return all_behaviors

    def _get_behavior_order(self, bot_directory: Path, behavior_name: str) -> int:
        behavior_json_path = bot_directory / 'behaviors' / behavior_name / 'behavior.json'
        if not behavior_json_path.exists():
            return 999
        try:
            config = read_json_file(behavior_json_path)
            return config.get('order', 999)
        except Exception:
            logger.debug(f'Failed to read behavior order for {behavior_name}')
            return 999

    def _get_default_breadcrumbs(self) -> list:
        PENDING = '☐'
        lines = ['## Behavior/Action Status', '']
        if self.behavior and self.behavior.bot:
            try:
                bot_dir = self.behavior.bot_paths.bot_directory
                lines.append(f'**Bot Directory:** {bot_dir}')
                lines.append('')
            except Exception as e:
                logger.debug(f'Failed to get bot directory for breadcrumbs: {e}')
                raise
            try:
                all_behaviors = self.behavior.bot.behaviors.names
                ordered_behaviors = self._get_ordered_behaviors(all_behaviors)
                lines.append('## Behavior/Action Progress')
                lines.append('')
                for behavior_name in ordered_behaviors:
                    lines.append(f'### {PENDING} **{behavior_name}**')
                lines.append('')
                lines.append('*(No workspace configured - run from a project directory)*')
            except Exception:
                lines.append('*(No behavior/action state available)*')
        else:
            lines.append('*(No behavior/action state available)*')
        return lines
