
from typing import Optional, Dict, Type
import importlib
import re
from pathlib import Path
from scanners.scanner import Scanner

class LanguageAgnosticScanner(Scanner):
    """Wrapper scanner that delegates to language-specific scanner based on file extension."""
    
    def __init__(self, python_scanner_class: Type[Scanner], js_scanner_class: Type[Scanner], rule):
        super().__init__(rule)
        self._python_scanner_class = python_scanner_class
        self._js_scanner_class = js_scanner_class
        self._python_instance = None
        self._js_instance = None
    
    def _get_scanner_for_file(self, file_path: Path) -> Optional[Scanner]:
        """Get the appropriate scanner based on file extension."""
        if not file_path:
            # Default to Python for non-file contexts
            if not self._python_instance:
                self._python_instance = self._python_scanner_class(self.rule)
            return self._python_instance
        
        file_ext = file_path.suffix.lower()
        
        if file_ext == '.js':
            if not self._js_instance:
                self._js_instance = self._js_scanner_class(self.rule)
            return self._js_instance
        else:
            # Default to Python for .py and other files
            if not self._python_instance:
                self._python_instance = self._python_scanner_class(self.rule)
            return self._python_instance
    
    def scan_file_with_context(self, context):
        """Delegate to appropriate scanner based on file extension."""
        scanner = self._get_scanner_for_file(context.path)
        if scanner:
            return scanner.scan_file_with_context(context)
        return []
    
    def scan_with_context(self, context):
        """Delegate to appropriate scanner based on file extensions in context."""
        # Group files by extension
        py_files = []
        js_files = []
        
        if hasattr(context, 'files') and context.files:
            if hasattr(context.files, 'paths'):
                for file_path in context.files.paths:
                    if file_path.suffix == '.js':
                        js_files.append(file_path)
                    else:
                        py_files.append(file_path)
        
        violations = []
        
        # Scan Python files with Python scanner
        if py_files and self._python_scanner_class:
            if not self._python_instance:
                self._python_instance = self._python_scanner_class(self.rule)
            violations.extend(self._python_instance.scan_with_context(context))
        
        # Scan JavaScript files with JS scanner  
        if js_files and self._js_scanner_class:
            if not self._js_instance:
                self._js_instance = self._js_scanner_class(self.rule)
            violations.extend(self._js_instance.scan_with_context(context))
        
        # If no specific files, default to Python scanner
        if not py_files and not js_files:
            if not self._python_instance:
                self._python_instance = self._python_scanner_class(self.rule)
            violations.extend(self._python_instance.scan_with_context(context))
        
        return violations


class ScannerRegistry:
    
    def __init__(self, bot_name: str = None):
        self._bot_name = bot_name
        self._scanner_cache: Dict[str, Type[Scanner]] = {}
    
    def finds_scanner_by_rule(self, rule) -> Optional[Type[Scanner]]:
        if not hasattr(rule, 'scanner_path') or not rule.scanner_path:
            return None
        
        if rule.scanner_path in self._scanner_cache:
            return self._scanner_cache[rule.scanner_path]
        
        scanner_class = self.loads_scanner_class(rule.scanner_path)
        if scanner_class:
            self._scanner_cache[rule.scanner_path] = scanner_class
        
        return scanner_class
    
    def loads_scanner_class(self, scanner_module_path: str) -> Optional[Type[Scanner]]:
        scanner_class, _ = self.loads_scanner_class_with_error(scanner_module_path)
        return scanner_class
    
    def loads_scanner_class_with_error(self, scanner_module_path: str, target_language: str = None) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        if not scanner_module_path:
            return None, None
        
        try:
            module_path, class_name = scanner_module_path.rsplit('.', 1)
            
            # Strip out .python. or .javascript. to normalize the path
            module_path = module_path.replace('.code.python.', '.code.').replace('.code.javascript.', '.code.')
            
            # If target_language is specified, load only that language's scanner
            if target_language == 'javascript':
                js_scanner, error = self._load_language_scanner(module_path, class_name, 'javascript')
                if js_scanner:
                    return js_scanner, None
                return None, error or f"JavaScript scanner not found: {scanner_module_path}"
            
            if target_language == 'python':
                py_scanner, error = self._load_language_scanner(module_path, class_name, 'python')
                if py_scanner:
                    return py_scanner, None
                return None, error or f"Python scanner not found: {scanner_module_path}"
            
            # No target language specified - load language-agnostic scanner (both Python and JavaScript)
            py_scanner, js_scanner = self._load_both_languages(module_path, class_name)
            
            if py_scanner or js_scanner:
                # Create a configured wrapper class
                class ConfiguredLanguageAgnosticScanner(LanguageAgnosticScanner):
                    def __init__(self, rule):
                        super().__init__(py_scanner, js_scanner, rule)
                
                return (ConfiguredLanguageAgnosticScanner, None)
            
            return None, f"Scanner class not found in any language: {scanner_module_path}"
        except Exception as e:
            return None, f"Error loading scanner {scanner_module_path}: {e}"
    
    def _load_single_scanner(self, module_path: str, class_name: str) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        """Load a scanner from a specific path."""
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, class_name):
                scanner_class = getattr(module, class_name)
                if isinstance(scanner_class, type) and issubclass(scanner_class, Scanner):
                    return scanner_class, None
        except (ImportError, AttributeError):
            pass
        return None, f"Scanner not found at {module_path}.{class_name}"
    
    def _load_language_scanner(self, module_path: str, class_name: str, language: str) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        """Load scanner for a specific language (python or javascript)."""
        scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
        
        paths = [
            f'scanners.code.{language}.{scanner_name}_scanner',
            module_path.replace('scanners.', f'scanners.code.{language}.')
        ]
        
        for path in paths:
            scanner, _ = self._load_single_scanner(path, class_name)
            if scanner:
                return scanner, None
        
        return None, f"Scanner not found for {language}: {module_path}.{class_name}"
    
    def _load_both_languages(self, module_path: str, class_name: str) -> tuple[Optional[Type[Scanner]], Optional[Type[Scanner]]]:
        """Load both Python and JavaScript versions of a scanner."""
        scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
        
        # First try loading directly from the module path (for non-code scanners like story/scenario scanners)
        direct_scanner, _ = self._load_single_scanner(module_path, class_name)
        if direct_scanner:
            # Return as Python scanner since it's language-agnostic
            return direct_scanner, None
        
        # Try Python scanner
        py_paths = [
            f'scanners.code.python.{scanner_name}_scanner',
            module_path.replace('scanners.', 'scanners.code.python.')
        ]
        
        py_scanner = None
        for path in py_paths:
            scanner, _ = self._load_single_scanner(path, class_name)
            if scanner:
                py_scanner = scanner
                break
        
        # Try JavaScript scanner
        js_paths = [
            f'scanners.code.javascript.{scanner_name}_scanner',
            module_path.replace('scanners.', 'scanners.code.javascript.')
        ]
        
        js_scanner = None
        for path in js_paths:
            scanner, _ = self._load_single_scanner(path, class_name)
            if scanner:
                js_scanner = scanner
                break
        
        return py_scanner, js_scanner

