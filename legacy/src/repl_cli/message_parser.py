"""Utility functions for parsing messages and CLI arguments."""

import shlex
from typing import Tuple, List


def parse_message_and_cli_args(message_and_cli_args: str) -> Tuple[str, List[str]]:
    """Parse a string containing both message and CLI arguments.
    
    Separates the message part from CLI arguments (starting with --).
    
    Args:
        message_and_cli_args: String containing message and optional CLI args
        
    Returns:
        Tuple of (message_string, cli_args_list)
    """
    try:
        parsed = shlex.split(message_and_cli_args)
    except:
        parsed = [message_and_cli_args]
    
    message_parts = []
    cli_args_parts = []
    i = 0
    while i < len(parsed):
        if parsed[i].startswith('--'):
            cli_args_parts = parsed[i:]
            break
        else:
            message_parts.append(parsed[i])
            i += 1
    
    message = ' '.join(message_parts)
    return message, cli_args_parts
