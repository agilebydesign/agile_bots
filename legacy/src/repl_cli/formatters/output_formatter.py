"""
Minimal OutputFormatter for display helpers (icons, separators).

This is ONLY for display utilities in TTY output.
"""


class OutputFormatter:
    """Minimal formatter for display helpers only."""
    
    def bot_icon(self) -> str:
        """Return bot icon."""
        return "[*]"
    
    def workspace_icon(self) -> str:
        """Return workspace icon."""
        return "[W]"
    
    def scope_icon(self) -> str:
        """Return scope icon."""
        return "[S]"
    
    def position_icon(self) -> str:
        """Return position icon."""
        return "[P]"
    
    def file_icon(self) -> str:
        """Return file icon."""
        return "[F]"
    
    def section_separator(self) -> str:
        """Return section separator."""
        return "=" * 80
    
    def subsection_separator(self) -> str:
        """Return subsection separator."""
        return "-" * 80
    
    def status_marker(self, is_current: bool, is_completed: bool) -> str:
        """Return status marker based on state."""
        if is_current:
            return "[*]"  # Current
        elif is_completed:
            return "[OK]"  # Completed
        else:
            return "[ ]"  # Pending
