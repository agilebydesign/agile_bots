from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from ....actions.action import Action
    from ...repl_session import REPLSession

from .cli_action import CLIAction
from ....actions.action_context import ScopeActionContext, Scope


class RenderCLIAction(CLIAction):
    
    def _parse_args_to_context(self, args: str) -> ScopeActionContext:
        if not args or args.strip() == "":
            return ScopeActionContext()
        
        try:
            args_dict = json.loads(args)
            
            scope_data = args_dict.get('scope')
            scope = Scope.from_dict(scope_data) if scope_data else None
            
            return ScopeActionContext(scope=scope)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return ScopeActionContext()

