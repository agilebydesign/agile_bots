"""Base class for CLI domain wrapper objects."""
from .formatters.output_formatter import OutputFormatter


class CLIBase:
    """Base class for all CLI domain wrapper objects.
    
    Provides access to the formatter so each CLI object can be responsible
    for its own display formatting.
    """
    
    def __init__(self, formatter: OutputFormatter):
        self._formatter = formatter
    
    @property
    def formatter(self) -> OutputFormatter:
        """Access the output formatter for display rendering."""
        return self._formatter

