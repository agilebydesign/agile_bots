# Trace and Edit - Increment Exploration

**Navigation:** [Story Map](../map/story-map-outline.drawio) | [Increments](../prioritization/story-map-increments.drawio)



## Stories (4 total)

### Display Code Trace

**Acceptance Criteria:**
- **WHEN** Developer views scenario with linked test
  **THEN** Trace Editor parses test method for function/method calls
  **AND** Trace Editor follows each call to find implementation in workspace
  **AND** Trace Editor builds call hierarchy from test to implementation code
- **WHEN** Trace Editor builds hierarchy
  **THEN** Trace Editor displays test method as root node
  **AND** Trace Editor displays called functions/methods as child nodes
  **AND** Trace Editor recursively traces calls within each implementation
  **AND** Trace Editor expands hierarchy to 3 levels by default
- **WHEN** Trace Editor displays code box for node
  **THEN** code box shows symbol name (class.method or function name)
  **AND** code box shows file path and line number
  **AND** code box shows source code with syntax highlighting
  **AND** code box shows line numbers beside code
- **WHEN** hierarchy exceeds 3 levels
  **THEN** Trace Editor shows collapsed nodes beyond level 3
  **AND** Trace Editor lazy-loads deeper levels on expand
- **WHEN** call target not found in workspace
  **THEN** Trace Editor skips external/library calls
  **BUT** continues tracing other calls
- **WHEN** scenario has no linked test
  **THEN** Trace Editor shows "No test linked" indicator
  **BUT** does not show error
- **WHEN** linked test file not found
  **THEN** Trace Editor shows test reference with warning indicator
  **BUT** still renders trace UI structure
- **WHEN** test method has no calls
  **THEN** Trace Editor displays empty code trace section
- **WHEN** call tree exceeds depth limit
  **THEN** Trace Editor truncates at maximum depth
  **AND** Trace Editor shows truncation indicator

### Edit Code Step

**Acceptance Criteria:**
- **WHEN** Trace Editor displays code trace
  **THEN** Trace Editor expands hierarchy by default
  **AND** Trace Editor displays code snippet in editable box for each node
  **AND** Trace Editor shows line numbers beside code
- **WHEN** Developer modifies code in edit box
  **AND** Developer triggers save (blur or Ctrl+S)
  **THEN** Trace Editor saves changes to source file
  **AND** Trace Editor shows save confirmation indicator
- **WHEN** Developer modifies test code
  **THEN** Trace Editor saves changes to test file
- **WHEN** Developer modifies implementation code
  **THEN** Trace Editor saves changes to code file
- **WHEN** save operation fails
  **THEN** Trace Editor shows error indicator
  **BUT** preserves user edits in edit box
- **WHEN** Developer presses Escape in edit box
  **THEN** Trace Editor reverts to previous value
  **BUT** does not save changes

### Open Source File

**Acceptance Criteria:**
- **WHEN** Developer clicks Open button on code node
  **THEN** Editor opens source file
  **AND** Editor navigates to specific line number
- **WHEN** Developer clicks Open on test node
  **THEN** Editor opens test file
  **AND** Editor navigates to test method line
- **WHEN** source file not found
  **THEN** Trace Editor shows file not found error
  **BUT** does not crash
- **WHEN** line number exceeds file length
  **THEN** Editor opens file at end
  **AND** Trace Editor shows line not found warning
- **WHEN** Developer clicks Open while file already open
  **THEN** Editor focuses existing tab
  **AND** Editor navigates to line

### Navigate Code Trace

**Acceptance Criteria:**
- **WHEN** Developer clicks on method call within code box
  **THEN** Trace Editor navigates to code box for that method
  **AND** Trace Editor scrolls hierarchy to show target node
  **AND** Trace Editor highlights target code box
- **WHEN** Developer clicks on property access within code box
  **THEN** Trace Editor navigates to code box for that property
- **WHEN** Developer clicks on nested method/property call
  **THEN** Trace Editor expands parent nodes if collapsed
  **AND** Trace Editor navigates to nested code box
- **WHEN** clicked method/property not in trace hierarchy
  **THEN** Trace Editor shows "Not traced" indicator
  **BUT** does not navigate
- **WHEN** Developer expands code node
  **THEN** Trace Editor lazy-loads source code for node
  **AND** Trace Editor displays code with line numbers
  **AND** Trace Editor shows loading indicator during fetch
- **WHEN** Developer collapses previously expanded node
  **THEN** Trace Editor hides code snippet
  **BUT** preserves loaded content in memory
- **WHEN** Developer clicks Expand All button
  **THEN** Trace Editor expands entire hierarchy
  **BUT** does not auto-load code snippets
- **WHEN** Developer clicks Collapse All button
  **THEN** Trace Editor collapses entire hierarchy
- **WHEN** Developer clicks Toggle Code button
  **THEN** Trace Editor shows/hides code for all expanded nodes
- **WHEN** Developer hovers over code node
  **THEN** Trace Editor shows full path tooltip
- **WHEN** source file not found during lazy load
  **THEN** Trace Editor shows file not found message in node
  **BUT** does not collapse node

---

## Source Material

Scope: Trace Code sub-epic under Trace Story Graph > Work With Story Map > Invoke Bot
Increment: Trace and Edit (priority 4)
Stories: Display Code Trace, Edit Code Step, Open Source File, Navigate Code Trace
