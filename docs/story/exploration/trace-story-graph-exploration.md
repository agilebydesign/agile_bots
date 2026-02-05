# Trace Story Graph - Increment Exploration

**Navigation:** [📋 Story Map](../map/{story_map_filename}) | [📊 Increments](../increments/{increments_filename})




## Stories (16 total)

---

### Trace Story

### 📝 Display Stories In Trace Editor

**Acceptance Criteria:**  
- **WHEN** Developer selects story in Panel scope section  
  **AND** Developer clicks Trace Story button  
  **THEN** Trace Editor opens  
  **AND** Trace Editor displays story name in header  
  **AND** Trace Editor displays users section with actor list  
  **AND** Trace Editor displays acceptance criteria section  
- **WHEN** story has no acceptance criteria  
  **THEN** Trace Editor displays empty acceptance criteria section  
- **WHEN** Developer clicks Open button on story header  
  **THEN** Trace Editor opens story source file  
  **AND** Editor navigates to story name line  
- **WHEN** story source file not found  
  **THEN** Trace Editor shows file not found error  
  **BUT** does not crash  
- **WHEN** Developer clicks Open while file already open  
  **THEN** Editor focuses existing tab  
  **AND** Editor navigates to story line
### 📝 Edit Stories in Trace Editor

**Acceptance Criteria:**  
- **WHEN** Developer modifies story name field  
  **AND** Developer triggers save (blur or Ctrl+S)  
  **THEN** Trace Editor saves changes to story data  
  **AND** Trace Editor preserves story structure  
  **AND** Trace Editor shows save confirmation indicator  
- **WHEN** Developer modifies acceptance criteria text  
  **THEN** Trace Editor saves changes on blur  
- **WHEN** Developer adds user to users list  
  **THEN** Trace Editor inserts new user entry  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer removes user from users list  
  **THEN** Trace Editor removes user entry  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer modifies user name  
  **THEN** Trace Editor updates user entry on blur  
- **WHEN** Developer enters duplicate user name  
  **THEN** Trace Editor shows validation warning  
  **BUT** allows save (duplicates permitted)  
- **WHEN** Developer enters invalid data  
  **THEN** Trace Editor shows validation error  
  **BUT** does not save invalid data  
- **WHEN** save operation fails  
  **THEN** Trace Editor shows error indicator  
  **AND** Trace Editor preserves user edits in editor  

---
### 📝 Display Scenario Steps

**Acceptance Criteria:**  
- **WHEN** story is displayed in Trace Editor  
  **AND** story has scenarios  
  **THEN** Trace Editor displays scenarios section with scenario items  
  **AND** Trace Editor displays nested scenarios as expandable items  
- **WHEN** story has no scenarios  
  **THEN** Trace Editor displays empty scenarios section  
  **BUT** does not show error  
- **WHEN** Developer clicks expand on scenario item  
  **THEN** Trace Editor displays scenario details inline  
- **WHEN** Developer views scenario in trace editor  
  **THEN** Trace Editor displays Given steps section  
  **AND** Trace Editor displays When steps section  
  **AND** Trace Editor displays Then steps section  
- **WHEN** scenario has no Given steps  
  **THEN** Trace Editor omits Given section  
  **BUT** displays When and Then sections  
- **WHEN** scenario step contains multiple lines  
  **THEN** Trace Editor displays step with preserved formatting  
### 📝 Edit Scenarios in Trace Editor

**Acceptance Criteria:**  
- **WHEN** Developer modifies scenario step text  
  **AND** Developer triggers save (blur or Ctrl+S)  
  **THEN** Trace Editor saves changes to story data  
  **AND** Trace Editor preserves scenario structure  
- **WHEN** Developer adds new step to scenario  
  **THEN** Trace Editor inserts step in appropriate section  
- **WHEN** Developer clears step text  
  **THEN** Trace Editor removes empty step on save  
- **WHEN** save fails  
  **THEN** Trace Editor shows error indicator  
  **BUT** preserves user edits  
### 📝 Open Scenario Source

**Acceptance Criteria:**  
- **WHEN** Developer clicks Open button on scenario  
  **THEN** Trace Editor opens story source file  
  **AND** Editor navigates to scenario line  
- **WHEN** scenario line not found in file  
  **THEN** Trace Editor opens file at story location  
  **AND** Trace Editor shows line not found warning  
- **WHEN** Developer clicks Open while file already open  
  **THEN** Editor focuses existing tab  
  **AND** Editor navigates to scenario line  
### 📝 Display Examples Table

**Acceptance Criteria:**  
- **WHEN** Developer views scenario with examples  
  **THEN** Trace Editor displays examples as editable table  
  **AND** Trace Editor displays column headers from example data  
  **AND** Trace Editor displays rows with example values  
- **WHEN** scenario has no examples  
  **THEN** Trace Editor shows empty examples section with Add Example button  
  **BUT** does not show table headers  
- **WHEN** example table has many rows  
  **THEN** Trace Editor displays scrollable table  
  **AND** Trace Editor keeps headers visible while scrolling  
### 📝 Add / Remove Examples

**Acceptance Criteria:**  
- **WHEN** Developer clicks Add Examples  
  **THEN** Trace Editor creates a new examples table  
  **AND** Trace Editor inserts the table into the examples collection  
  **AND** Trace Editor focuses the first cell of the new table  
- **WHEN** Developer removes an examples table  
  **THEN** Trace Editor removes the selected table from the collection  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer removes the last examples table  
  **THEN** Trace Editor shows an empty examples section  
  **BUT** does not remove the examples collection container  

### 📝 Edit Example

**Acceptance Criteria:**  
- **WHEN** Developer clicks Add Row button on examples table  
  **THEN** Trace Editor inserts new row at end of table  
  **AND** Trace Editor populates row with empty cells matching columns  
  **AND** Trace Editor focuses first cell in new row  
- **WHEN** Developer presses Enter on last row  
  **THEN** Trace Editor inserts new row below current row  
- **WHEN** table has no columns yet  
  **THEN** Trace Editor prompts Developer to add column first  
  **BUT** does not insert empty row  
- **WHEN** Developer clicks Delete button on example row  
  **THEN** Trace Editor removes row from table  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer removes last row  
  **THEN** Trace Editor displays empty table with headers  
  **BUT** does not remove column structure  
- **WHEN** Developer confirms row deletion  
  **THEN** Trace Editor removes row immediately  
  **BUT** does not prompt for single row deletion  
- **WHEN** Developer clicks Add Column button  
  **THEN** Trace Editor displays column name input dialog  
- **WHEN** Developer enters column name and confirms  
  **THEN** Trace Editor adds new column to table  
  **AND** Trace Editor adds empty cell to each existing row  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer enters duplicate column name  
  **THEN** Trace Editor shows validation error  
  **BUT** does not add duplicate column  
- **WHEN** Developer cancels column dialog  
  **THEN** Trace Editor closes dialog  
  **BUT** does not modify table  
- **WHEN** Developer clicks Delete on column header  
  **THEN** Trace Editor shows confirmation dialog  
  **AND** Dialog warns that column data will be lost  
- **WHEN** Developer confirms column deletion  
  **THEN** Trace Editor removes column from table  
  **AND** Trace Editor removes column data from all rows  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer removes last column  
  **THEN** Trace Editor removes all example data  
  **AND** Trace Editor shows empty examples section  
- **WHEN** Developer cancels deletion  
  **THEN** Trace Editor preserves column and data  
- **WHEN** Developer double-clicks column header  
  **THEN** Trace Editor displays inline text editor on header  
- **WHEN** Developer modifies header text and saves  
  **THEN** Trace Editor updates column name  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer enters duplicate column name  
  **THEN** Trace Editor shows validation error  
  **BUT** does not save duplicate name  
- **WHEN** Developer clears header text  
  **THEN** Trace Editor shows validation error  
  **BUT** does not allow empty column name  

### 📝 Edit Example Cell Data

**Acceptance Criteria:**  
- **WHEN** Developer clicks on example cell  
  **THEN** Trace Editor activates inline editor on cell  
  **AND** Trace Editor selects existing cell content  
- **WHEN** Developer modifies cell content and triggers save  
  **THEN** Trace Editor updates cell value  
  **AND** Trace Editor saves changes to story data  
- **WHEN** Developer enters longer cell content  
  **THEN** Trace Editor expands cell width to fit roughly 7-12 words  
  **AND** Trace Editor grows cell height for content beyond that  
- **WHEN** Developer presses Tab in cell  
  **THEN** Trace Editor saves current cell  
  **AND** Trace Editor moves focus to next cell in row  
- **WHEN** Developer presses Enter in cell  
  **THEN** Trace Editor saves current cell  
  **AND** Trace Editor moves focus to cell below  
- **WHEN** Developer presses Escape in cell  
  **THEN** Trace Editor reverts cell to previous value  
  **BUT** does not save changes  


---

### Trace Code

### 📝 Display Code Trace

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

### 📝 Edit Code Step

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

### 📝 Open Source File

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

### 📝 Navigate Code Trace

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

This section references existing source material.

Lines 17936-18272 from story-graph.json
