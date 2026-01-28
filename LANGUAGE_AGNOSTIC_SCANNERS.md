# Language-Agnostic Scanner System

## Overview

The scanner registry now automatically detects file language (Python vs JavaScript) and loads the appropriate scanner. Scanner names are identical across languages - the system handles routing automatically.

## How It Works

### 1. Scanner Registry Auto-Detection

When a rule references a scanner, the registry:

1. **Checks for language-specific path:**
   - If path contains `.code.python.` or `.code.javascript.`, loads that specific scanner

2. **Loads both language variants:**
   - Tries to load `scanners.code.python.{scanner_name}`
   - Tries to load `scanners.code.javascript.{scanner_name}`
   - Creates a `LanguageAgnosticScanner` wrapper with both

3. **Routes at scan time:**
   - When scanning `.js` files → uses JavaScript scanner
   - When scanning `.py` files → uses Python scanner
   - Default for other files → uses Python scanner

### 2. Rule Configuration

Rules now reference scanners **WITHOUT** language prefix:

**OLD (language-specific):**
```json
{
  "name": "keep_functions_small_focused",
  "scanner": "scanners.code.python.function_size_scanner.FunctionSizeScanner"
}
```

**NEW (language-agnostic):**
```json
{
  "name": "keep_functions_small_focused",
  "scanner": "scanners.function_size_scanner.FunctionSizeScanner"
}
```

The system will:
- Load `scanners.code.python.function_size_scanner.FunctionSizeScanner`
- Load `scanners.code.javascript.function_size_scanner.FunctionSizeScanner`
- Route to correct one based on file extension

### 3. Scanner Implementation Requirements

For multi-language support, scanners must:

1. **Have identical names** across languages:
   - `src/scanners/code/python/function_size_scanner.py`
   - `src/scanners/code/javascript/function_size_scanner.py`

2. **Have identical class names:**
   ```python
   class FunctionSizeScanner(CodeScanner):  # Python
   class FunctionSizeScanner(JSCodeScanner):  # JavaScript
   ```

3. **Implement same validation logic** (different syntax, same rules)

## Migration Guide

### Updating Existing Rules

Rules with language-specific paths can be updated in two ways:

**Option 1: Update to language-agnostic (recommended)**
```bash
# Change this:
"scanner": "scanners.code.python.duplication_scanner.DuplicationScanner"

# To this:
"scanner": "scanners.duplication_scanner.DuplicationScanner"
```

**Option 2: Keep language-specific (still works)**
```json
{
  "scanner": "scanners.code.python.duplication_scanner.DuplicationScanner"
}
```
This will only scan Python files and skip JavaScript files.

### Creating New JavaScript Scanners

When creating a new JavaScript scanner:

1. **Match the Python scanner name exactly:**
   ```
   src/scanners/code/python/my_new_scanner.py
   src/scanners/code/javascript/my_new_scanner.py  ← Same name!
   ```

2. **Match the class name:**
   ```python
   # Python
   class MyNewScanner(CodeScanner):
       pass
   
   # JavaScript
   class MyNewScanner(JSCodeScanner):  ← Same class name!
       pass
   ```

3. **Reference without language in rules:**
   ```json
   {
     "scanner": "scanners.my_new_scanner.MyNewScanner"
   }
   ```

## Implementation Details

### LanguageAgnosticScanner Class

The wrapper scanner:

```python
class LanguageAgnosticScanner(Scanner):
    def __init__(self, python_scanner_class, js_scanner_class, rule):
        # Holds both scanner classes
        # Creates instances lazily based on file type
    
    def _get_scanner_for_file(self, file_path):
        # Returns JavaScript scanner for .js files
        # Returns Python scanner for .py and other files
    
    def scan_file_with_context(self, context):
        # Delegates to appropriate scanner
```

### Scanner Registry Logic

```python
def loads_scanner_class_with_error(self, scanner_module_path):
    # If path has language → load specific scanner
    if '.code.python.' in path or '.code.javascript.' in path:
        return self._load_single_scanner(path)
    
    # Otherwise → load both and wrap
    py_scanner, js_scanner = self._load_both_languages(path)
    return ConfiguredLanguageAgnosticScanner
```

## Examples

### Example 1: Function Size Validation

**Rule (language-agnostic):**
```json
{
  "name": "keep_functions_small_focused",
  "scanner": "scanners.function_size_scanner.FunctionSizeScanner",
  "description": "Functions should be small and focused"
}
```

**What happens:**
1. Registry loads both:
   - `scanners.code.python.function_size_scanner.FunctionSizeScanner`
   - `scanners.code.javascript.function_size_scanner.FunctionSizeScanner`

2. During validation:
   - `src/utils.py` → scanned by Python scanner
   - `src/panel/bot_panel.js` → scanned by JavaScript scanner

### Example 2: Exception Handling

**Rule:**
```json
{
  "name": "use_exceptions_properly",
  "scanner": "scanners.exception_handling_scanner.ExceptionHandlingScanner"
}
```

**Behavior:**
- Python files: Checks for `try/except` blocks
- JavaScript files: Checks for `try/catch` blocks
- Same validation rules, different syntax

### Example 3: Code Duplication

**Rule:**
```json
{
  "name": "eliminate_duplication",
  "scanner": "scanners.duplication_scanner.DuplicationScanner"
}
```

**Behavior:**
- Scans Python files with Python AST
- Scans JavaScript files with JavaScript AST (esprima)
- Finds duplicates within and across files of same language

## Benefits

✅ **Single rule definition** for multiple languages  
✅ **Automatic language detection** based on file extension  
✅ **Backwards compatible** with language-specific paths  
✅ **Easy to extend** - just add new language folders  
✅ **Type-safe** - same validation logic, language-specific implementation  

## Scanner Status in Reports

Validation reports will show:
- `EXECUTED` - Scanner ran successfully
- `LOAD_FAILED` - Scanner not found for this language
- `EXECUTION_FAILED` - Scanner crashed during execution

If JavaScript scanner doesn't exist yet:
- Python files → validates normally
- JavaScript files → skipped (no scanner available)

## Future Extensions

To add support for a new language:

1. Create folder: `src/scanners/code/typescript/`
2. Implement: `typescript_code_scanner.py` base class
3. Create scanners with identical names to Python/JS
4. Update `_get_scanner_for_file()` to handle `.ts` extension
5. Rules automatically support TypeScript!

## Current Status

- **Python Scanners:** 65 (100% complete)
- **JavaScript Scanners:** 65 (8% implemented, 92% stubs)
- **Language-Agnostic Rules:** Ready to use
- **Backward Compatibility:** Maintained

## Migration Checklist

- [ ] Update rules to remove `.code.python.` from scanner paths
- [ ] Test validation with mixed Python/JavaScript codebase
- [ ] Implement priority JavaScript scanners
- [ ] Update rule documentation
- [ ] Create JavaScript-specific rule examples
