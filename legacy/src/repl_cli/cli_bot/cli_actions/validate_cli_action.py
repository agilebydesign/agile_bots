from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from ....actions.action import Action
    from ...repl_session import REPLSession

from .cli_action import CLIAction
from ....actions.action_context import ValidateActionContext, Scope


class ValidateCLIAction(CLIAction):
    
    def _parse_args_to_context(self, args: str) -> ValidateActionContext:
        if not args or args.strip() == "":
            return ValidateActionContext()
        
        try:
            args_dict = json.loads(args)
            
            scope_data = args_dict.get('scope')
            scope = Scope.from_dict(scope_data) if scope_data else None
            
            background = args_dict.get('background')
            skip_cross_file = args_dict.get('skip_cross_file', False)
            all_files = args_dict.get('all_files', False)
            force_full = args_dict.get('force_full', False)
            
            return ValidateActionContext(
                scope=scope,
                background=background,
                skip_cross_file=skip_cross_file,
                all_files=all_files,
                force_full=force_full
            )
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return ValidateActionContext()

