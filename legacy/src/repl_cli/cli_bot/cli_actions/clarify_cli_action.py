from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
import json

if TYPE_CHECKING:
    from ....actions.action import Action
    from ...repl_session import REPLSession

from .cli_action import CLIAction
from ....actions.action_context import ClarifyActionContext


class ClarifyCLIAction(CLIAction):
    
    def _parse_args_to_context(self, args: str) -> ClarifyActionContext:
        if not args or args.strip() == "":
            return ClarifyActionContext()
        
        try:
            args_dict = json.loads(args)
            
            answers = args_dict.get('answers')
            evidence_provided = args_dict.get('evidence_provided')
            context = args_dict.get('context')
            
            return ClarifyActionContext(
                answers=answers,
                evidence_provided=evidence_provided,
                context=context
            )
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            return ClarifyActionContext()

