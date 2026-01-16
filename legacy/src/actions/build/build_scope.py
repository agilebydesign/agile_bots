from typing import Dict, Any, Optional, TYPE_CHECKING
from ...bot.bot_paths import BotPaths
from ..action_scope import ActionScope

if TYPE_CHECKING:
    from ..action_context import ScopeActionContext

class BuildScope(ActionScope):

    def __init__(self, parameters: Dict[str, Any], bot_paths: Optional[BotPaths]=None):
        super().__init__(parameters, bot_paths)
        if not self._scope_config or not any((key in self._scope_config for key in ['story_names', 'increment_priorities', 'epic_names', 'increment_names', 'all'])):
            self._scope_config['all'] = True
    
    @classmethod
    def from_context(cls, context: 'ScopeActionContext', bot_paths: Optional[BotPaths] = None) -> 'BuildScope':
        from agile_bot.bots.base_bot.src.actions.action_context import Scope
        
        # Convert typed context to parameters dict for now
        # TODO: Refactor ActionScope to work directly with Scope
        params = {}
        if context.scope:
            params['scope'] = context.scope.to_dict()
        
        return cls(params, bot_paths)