# JavaScript Scanners Setup

## Completed: January 27, 2026

### Overview

Created a complete parallel structure of JavaScript code scanners matching all Python scanners. JavaScript scanners use `esprima` (via Node.js subprocess) to parse JavaScript AST and apply the same validation rules as Python scanners.

### Structure

```
src/scanners/code/
├── python/              (65 Python scanners)
│   ├── code_scanner.py
│   ├── test_scanner.py
│   └── ... (63 more scanners)
└── javascript/          (65 JavaScript scanners) ← NEW
    ├── js_code_scanner.py      (base for JS code scanners)
    ├── js_test_scanner.py      (base for JS test scanners)
    ├── function_size_scanner.py (✅ IMPLEMENTED)
    ├── duplication_scanner.py   (✅ IMPLEMENTED)
    ├── exception_handling_scanner.py (✅ IMPLEMENTED)
    ├── useless_comments_scanner.py (✅ IMPLEMENTED)
    ├── consistent_naming_scanner.py (✅ IMPLEMENTED)
    └── ... (60 more stub scanners)
```

### Created Files

**Base Classes (2):**
- `js_code_scanner.py` - Base for JavaScript code validation
- `js_test_scanner.py` - Base for JavaScript test validation

**Fully Implemented Scanners (5):**
1. `function_size_scanner.py` - Detects oversized functions
   - Handles FunctionDeclaration, ArrowFunctionExpression, FunctionExpression, MethodDefinition
   - Max 20 lines per function
   
2. `duplication_scanner.py` - Finds duplicate code
   - Cross-file function duplication detection
   - Intra-file duplication detection
   - 85% similarity threshold
   
3. `exception_handling_scanner.py` - Validates try-catch blocks
   - Detects empty catch blocks
   - Catches with only console.log
   - Catch blocks without error parameters
   
4. `useless_comments_scanner.py` - Identifies redundant comments
   - Comments that just repeat code
   - Empty TODO/FIXME comments
   - Obvious end-of-block comments
   
5. `consistent_naming_scanner.py` - Enforces naming conventions
   - Classes should be PascalCase
   - Functions/variables should be camelCase
   - Detects mixed styles (snake_case vs camelCase)

**Stub Scanners (58):**

*Code Scanners (32):*
- abstraction_levels_scanner.py
- bad_comments_scanner.py
- calculation_timing_code_scanner.py
- class_size_scanner.py
- clear_parameters_scanner.py
- complete_refactoring_scanner.py
- consistent_indentation_scanner.py
- dead_code_scanner.py
- domain_grouping_code_scanner.py
- domain_language_code_scanner.py
- error_handling_isolation_scanner.py
- excessive_guards_scanner.py
- explicit_dependencies_scanner.py
- import_placement_scanner.py
- intention_revealing_names_scanner.py
- meaningful_context_scanner.py
- minimize_mutable_state_scanner.py
- natural_english_code_scanner.py
- open_closed_principle_scanner.py
- prefer_object_model_over_config_scanner.py
- primitive_vs_object_scanner.py
- property_encapsulation_code_scanner.py
- resource_oriented_code_scanner.py
- separate_concerns_scanner.py
- simplify_control_flow_scanner.py
- single_responsibility_scanner.py
- swallowed_exceptions_scanner.py
- technical_abstraction_code_scanner.py
- third_party_isolation_scanner.py
- type_safety_scanner.py
- unnecessary_parameter_passing_scanner.py
- vertical_density_scanner.py

*Test Scanners (26):*
- arrange_act_assert_scanner.py
- ascii_only_scanner.py
- business_readable_test_names_scanner.py
- class_based_organization_scanner.py
- consistent_vocabulary_scanner.py
- cover_all_paths_scanner.py
- descriptive_function_names_scanner.py
- exact_variable_names_scanner.py
- fixture_placement_scanner.py
- full_result_assertions_scanner.py
- given_when_then_helpers_scanner.py
- mock_boundaries_scanner.py
- no_fallbacks_scanner.py
- no_guard_clauses_scanner.py
- object_oriented_helpers_scanner.py
- observable_behavior_scanner.py
- one_concept_per_test_scanner.py
- real_implementations_scanner.py
- setup_similarity_scanner.py
- specification_match_scanner.py
- standard_data_reuse_scanner.py
- story_graph_match_scanner.py
- test_boundary_behavior_scanner.py
- test_file_naming_scanner.py
- test_quality_scanner.py
- ubiquitous_language_scanner.py

### Dependencies

**Installed:**
- `esprima` (npm package) - JavaScript AST parser

### How It Works

1. **JavaScript Parsing:**
   - Base `JSCodeScanner` uses `subprocess` to call Node.js with esprima
   - JavaScript code is parsed into AST (JSON format)
   - AST is analyzed in Python

2. **Scanner Implementation Pattern:**
   ```python
   class FunctionSizeScanner(JSCodeScanner):
       def scan_file_with_context(self, context):
           parsed = self._parse_js_file(context.path)
           if not parsed:
               return []
           
           content, ast, lines = parsed
           # Analyze AST and create violations
           return violations
   ```

3. **AST Structure:**
   - Esprima provides JSON AST with node types like:
     - `FunctionDeclaration`
     - `ArrowFunctionExpression`
     - `TryStatement`
     - `ClassDeclaration`
     - etc.

### Key Differences from Python Scanners

| Aspect | Python Scanner | JavaScript Scanner |
|--------|---------------|-------------------|
| AST Parsing | `ast.parse()` (built-in) | `esprima` via subprocess |
| AST Format | Python AST objects | JSON dictionaries |
| Function Types | 2 (def, async def) | 4+ (function, arrow, expression, method) |
| Error Handling | `ast.Try` nodes | `TryStatement` nodes |
| Implementation | 70%+ complete | 8% complete (5/63 implemented) |

### Usage with Rules

To use JavaScript scanners, update rule files to reference JavaScript scanner paths:

**Example:**
```json
{
  "scanner": "scanners.code.javascript.function_size_scanner.FunctionSizeScanner"
}
```

Instead of:
```json
{
  "scanner": "scanners.code.python.function_size_scanner.FunctionSizeScanner"
}
```

### Next Steps

1. **Implement Priority Scanners:**
   - vertical_density_scanner.py (currently stub in Python too)
   - import_placement_scanner.py
   - simplify_control_flow_scanner.py
   - class_size_scanner.py

2. **Create JavaScript-Specific Rules:**
   - Copy Python rules from `bots/story_bot/behaviors/code/rules/`
   - Update scanner paths to `.javascript.` variants
   - Adjust examples to JavaScript syntax

3. **Testing:**
   - Create unit tests for implemented scanners
   - Validate against real JavaScript codebase

4. **Documentation:**
   - Add JavaScript AST traversal guide
   - Document esprima node types
   - Create scanner implementation examples

### Generator Script

A generator script (`generate_js_scanners.py`) was created to automatically generate scanner stubs. This can be rerun to add new scanners as the Python scanner set grows.

### Benefits

✅ Complete parity with Python scanner structure  
✅ Same validation rules applicable to JavaScript  
✅ Easy to maintain - parallel structure  
✅ Extensible - add new scanners easily  
✅ Type-safe - TypeScript-compatible approach  

### Summary

- **Total JavaScript Scanners:** 65 (2 base + 63 validators)
- **Fully Implemented:** 5 scanners (8%)
- **Stub/TODO:** 58 scanners (92%)
- **Dependencies Added:** esprima (npm)
- **Ready for:** JavaScript file validation in agile_bots project
