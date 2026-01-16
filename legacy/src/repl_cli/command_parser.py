from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ParsedCommand:
    command_type: str
    behavior: Optional[str] = None
    action: Optional[str] = None
    operation: Optional[str] = None
    args: str = ""
    
    @property
    def is_dot_notation(self) -> bool:
        return self.command_type == "dot_notation"
    
    @property
    def is_workflow(self) -> bool:
        return self.command_type == "workflow"
    
    @property
    def is_meta(self) -> bool:
        return self.command_type == "meta"
    
    @property
    def is_operation(self) -> bool:
        return self.operation is not None


class CommandParser:
    
    WORKFLOW_COMMANDS = ['next', 'back', 'first', 'last']
    META_COMMANDS = ['status', 'help', 'exit', 'quit', 'scope']
    OPERATIONS = ['instructions', 'confirm']
    
    def parse_command(self, input_line: str) -> ParsedCommand:
        if not input_line or input_line.strip() == "":
            return ParsedCommand(command_type="empty")
        
        input_line = input_line.strip()
        
        if input_line in self.META_COMMANDS:
            return ParsedCommand(command_type="meta", operation=input_line)
        
        if input_line in self.WORKFLOW_COMMANDS:
            return ParsedCommand(command_type="workflow", operation=input_line)
        
        if '.' in input_line:
            return self._parse_dot_notation(input_line)
        
        if input_line in self.OPERATIONS:
            return ParsedCommand(command_type="operation", operation=input_line)
        
        parts = input_line.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.META_COMMANDS:
            return ParsedCommand(command_type="meta", operation=command, args=args)
        
        if command in self.OPERATIONS:
            return ParsedCommand(command_type="operation", operation=command, args=args)
        
        # Treat unrecognized single-word commands as potential behavior names (dot notation with just behavior)
        if not args:  # Single word, no arguments
            return ParsedCommand(command_type="dot_notation", behavior=command)
        
        return ParsedCommand(command_type="unknown", args=input_line)
    
    def _parse_dot_notation(self, input_line: str) -> ParsedCommand:
        parts = input_line.split('.')
        
        if len(parts) == 3:
            behavior, action, operation = parts
            return ParsedCommand(
                command_type="dot_notation",
                behavior=behavior,
                action=action,
                operation=operation
            )
        elif len(parts) == 2:
            behavior, action = parts
            return ParsedCommand(
                command_type="dot_notation",
                behavior=behavior,
                action=action
            )
        elif len(parts) == 1:
            behavior = parts[0]
            return ParsedCommand(
                command_type="dot_notation",
                behavior=behavior
            )
        
        return ParsedCommand(command_type="unknown", args=input_line)
    
    @staticmethod
    def extract_behavior(input_line: str) -> Optional[str]:
        if '.' not in input_line:
            return None
        parts = input_line.split('.')
        return parts[0] if parts else None
    
    @staticmethod
    def extract_action(input_line: str) -> Optional[str]:
        if '.' not in input_line:
            return None
        parts = input_line.split('.')
        return parts[1] if len(parts) > 1 else None
    
    @staticmethod
    def extract_operation(input_line: str) -> Optional[str]:
        if '.' not in input_line:
            return None
        parts = input_line.split('.')
        return parts[2] if len(parts) > 2 else None

