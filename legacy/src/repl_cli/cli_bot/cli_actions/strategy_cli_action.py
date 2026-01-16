from __future__ import annotations
from typing import TYPE_CHECKING, List
import json

if TYPE_CHECKING:
    from ....actions.action import Action
    from ...repl_session import REPLSession

from .cli_action import CLIAction
from ....actions.action_context import StrategyActionContext


class StrategyCLIAction(CLIAction):
    
    def _parse_args_to_context(self, args: str) -> StrategyActionContext:
        if not args or args.strip() == "":
            return StrategyActionContext()
        
        try:
            args_dict = json.loads(args)
            
            assumptions = args_dict.get('assumptions')
            
            context = StrategyActionContext(assumptions=assumptions)
            
            for key, value in args_dict.items():
                if key != 'assumptions':
                    setattr(context, key, value)
            
            return context
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return StrategyActionContext()

