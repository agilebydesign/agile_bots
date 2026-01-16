"""CLI Context Builder - builds typed ActionContext from CLI arguments.

This module bridges the CLI and actions by:
1. Looking up the action's context_class
2. Using the generated parser for that context class
3. Parsing CLI args and building a typed context object
"""

import argparse
import json
from typing import Type, List, Optional, Any
from pathlib import Path

from ..actions.action import Action
from ..actions.action_context import (
    ActionContext,
    Scope,
    ScopeType,
)


class CliContextBuilder:
    
    def build_context(self, action: Action, cli_args: List[str]) -> ActionContext:
        context_class = action.context_class
        
        parser = self.build_parser_from_context_class(context_class)
        
        parsed, remaining = parser.parse_known_args(cli_args)
        
        if remaining:
            for arg in remaining:
                if arg.startswith('--'):
                    raise ValueError(
                        f"Unrecognized argument '{arg}' for action '{action.action_name}'. "
                        f"Valid arguments: {self._get_valid_args(context_class)}"
                    )
        
        # Convert to typed context
        return self._build_context_from_parsed(context_class, parsed)
    
    def build_parser_from_context_class(self, context_class: Type[ActionContext]) -> argparse.ArgumentParser:
        import dataclasses
        
        parser = argparse.ArgumentParser(add_help=False)
        
        if not dataclasses.is_dataclass(context_class):
            return parser
        
        for field_info in dataclasses.fields(context_class):
            self._add_argument_for_field(parser, field_info)
        
        return parser
    
    def _add_argument_for_field(self, parser: argparse.ArgumentParser, field_info) -> None:
        name = field_info.name
        field_type = field_info.type
        cli_name = f'--{name.replace("_", "-")}'
        dest_name = name
        
        import dataclasses
        default = field_info.default if field_info.default is not dataclasses.MISSING else None
        
        if field_type == bool:
            parser.add_argument(cli_name, dest=dest_name, action='store_true', default=default or False)
            return
        
        if 'Optional[bool]' in str(field_type):
            parser.add_argument(cli_name, dest=dest_name, action='store_true', default=None)
            return
        
        if 'Scope' in str(field_type):
            parser.add_argument(cli_name, dest=dest_name, type=str, default=None)
            return
        
        if 'Dict' in str(field_type):
            parser.add_argument(cli_name, dest=dest_name, type=str, default=None)
            return
        
        if 'List' in str(field_type):
            parser.add_argument(cli_name, dest=dest_name, nargs='*', default=None)
            return
        
        parser.add_argument(cli_name, dest=dest_name, type=str, default=default)
    
    def _build_context_from_parsed(self, context_class: Type[ActionContext], parsed: argparse.Namespace) -> ActionContext:
        import dataclasses
        
        kwargs = {}
        
        for field_info in dataclasses.fields(context_class):
            field_name = field_info.name
            value = getattr(parsed, field_name, None)
            
            if 'Scope' in str(field_info.type) and isinstance(value, str):
                value = self._parse_scope_config(value)
            elif 'Dict' in str(field_info.type) and isinstance(value, str):
                value = self._parse_json_dict(value)
            
            if value is not None:
                kwargs[field_name] = value
        
        return context_class(**kwargs)
    
    def _parse_scope_config(self, scope_str: str) -> Optional[Scope]:
        """Parse scope from simplified format:
        Two types only:
        - Story graph: "Item 1, Item 2" (searches entire graph - epics, sub-epics, stories, scenarios, increments)
        - Files: "files:path/file.py, path/file2.py"
        """
        if not scope_str:
            return None
        
        # Check if it's files scope (only special type)
        if ':' in scope_str and not scope_str.startswith('{'):
            parts = scope_str.split(':', 1)
            if len(parts) == 2 and parts[0].strip().lower() in ('file', 'files'):
                scope_value_str = parts[1].strip()
                scope_values_raw = [v.strip() for v in scope_value_str.split(',') if v.strip()]
                return Scope(type=ScopeType.FILES, value=scope_values_raw)
        
        # Everything else searches the story graph
        if not scope_str.startswith('{'):
            scope_values_raw = [v.strip() for v in scope_str.split(',') if v.strip()]
            return Scope(type=ScopeType.STORY, value=scope_values_raw)
        
        # Fallback to old JSON format for backwards compatibility
        try:
            data = json.loads(scope_str.replace("'", '"'))
            return Scope.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None
    
    def _parse_json_dict(self, json_str: str) -> Optional[dict]:
        if not json_str:
            return None
        return json.loads(json_str.replace("'", '"'))
    
    def _get_valid_args(self, context_class: Type[ActionContext]) -> List[str]:
        import dataclasses
        
        if not dataclasses.is_dataclass(context_class):
            return []
        
        return [f'--{f.name.replace("_", "-")}' for f in dataclasses.fields(context_class)]





