# Refactoring: Scanner Configuration Object

## Problem

The `Rule.scan()` method had a "Long Parameter List" code smell with 7 parameters:

```python
def scan(
    self, 
    story_graph: Dict[str, Any], 
    files: Optional[Dict[str, List[Path]]] = None, 
    on_file_scanned: Optional[Any] = None, 
    skip_cross_file: bool = False, 
    changed_files: Optional[Dict[str, List[Path]]] = None, 
    status_writer: Optional[Any] = None, 
    max_cross_file_comparisons: int = 20
) -> Dict[str, Any]:
```

**Issues:**
- Hard to remember parameter order
- Most parameters are configuration that doesn't change between scans
- Difficult to add new configuration options
- Poor encapsulation of related data

## Solution

Created a `ScanConfig` dataclass to encapsulate all scanner configuration:

```python
@dataclass
class ScanConfig:
    """Configuration for scanner execution."""
    
    # Core scan data
    story_graph: Dict[str, Any]
    files: Optional[Dict[str, List[Path]]] = None
    changed_files: Optional[Dict[str, List[Path]]] = None
    
    # Scanner behavior configuration
    skip_cross_file: bool = False
    max_cross_file_comparisons: int = 20
    
    # Callbacks and output
    on_file_scanned: Optional[Callable] = None
    status_writer: Optional[Any] = None
```

### New Signature

```python
def scan(self, config: ScanConfig) -> Dict[str, Any]:
    """Execute scanner with the provided configuration."""
```

## Benefits

1. **Single Responsibility**: Config object groups related parameters
2. **Easier to Extend**: Add new config options without changing method signatures
3. **Better Encapsulation**: Derived properties (test_files, code_files) computed on demand
4. **Clearer Intent**: Configuration is explicit and self-documenting
5. **Type Safety**: Dataclass provides validation and IDE support

## Usage

### Before
```python
scanner_results = rule.scan(
    context.story_graph, 
    all_files or files, 
    on_file_scanned=context.callbacks.on_file_scanned, 
    skip_cross_file=context.skip_cross_file, 
    changed_files=changed_files, 
    status_writer=context.status_writer, 
    max_cross_file_comparisons=max_cross_file
)
```

### After
```python
scan_config = ScanConfig(
    story_graph=context.story_graph,
    files=all_files or files,
    changed_files=changed_files,
    skip_cross_file=context.skip_cross_file,
    max_cross_file_comparisons=max_cross_file,
    on_file_scanned=context.callbacks.on_file_scanned,
    status_writer=context.status_writer
)
scanner_results = rule.scan(scan_config)
```

## Derived Properties

The `ScanConfig` class provides computed properties that eliminate redundant logic:

```python
@property
def test_files(self) -> List[Path]:
    """Get test files from changed_files or files."""
    files_to_scan = self.changed_files if self.changed_files else self.files
    return files_to_scan.get('test', [])

@property
def code_files(self) -> List[Path]:
    """Get code files from changed_files or files."""
    files_to_scan = self.changed_files if self.changed_files else self.files
    return files_to_scan.get('src', [])
```

This logic was previously duplicated in the `scan()` method.

## Files Changed

- **Created:** `agile_bot/src/rules/scan_config.py` - New configuration class
- **Modified:** `agile_bot/src/rules/rule.py` - Updated to use ScanConfig
- **Modified:** `agile_bot/src/rules/rules.py` - Updated caller to create ScanConfig

## Design Pattern

This refactoring applies the **Parameter Object** pattern from Martin Fowler's "Refactoring":

> "When you see a group of data items that regularly travel together, appearing in function after function, it's time to make them a class."

## Future Enhancements

The `ScanConfig` class can be extended to include:
- Scanner-specific options (e.g., timeout, max file size)
- Output formatting preferences
- Caching configuration
- Parallel execution settings

All without changing the `Rule.scan()` method signature.
