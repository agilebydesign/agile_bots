# Validation Status - code
Started: 2026-01-16 16:49:06
Files: 288

## avoid_excessive_guards
**actions.py** - 2 violation(s)

[!] WARNING (line 127)
Line 127: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def close_current(self):
        if self.current is None:
            if self._actions:
                self._current_index = 0
            else:
                return
        
```

[!] WARNING (line 187)
Line 187: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
            if not action_names:
                return False
            if self.current is not None:
                return self.current.action_name == action_names[-1]
            state_file = self._state_manager.get_state_file_path()
```

---

## avoid_excessive_guards
**behaviors.py** - 1 violation(s)

[!] WARNING (line 271)
Line 271: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def load_state(self):
        if self.bot_paths is None:
            self._init_to_first_behavior()
            return
        workspace_dir = self.bot_paths.workspace_directory
```

---

## avoid_excessive_guards
**behaviors.py** - 2 violation(s)

[!] WARNING (line 212)
Line 212: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def close_current(self):
        if self._current_index is not None:
            next_behavior = self.next()
            if next_behavior:
                self._current_index += 1
                self.save_state()

```

[!] WARNING (line 264)
Line 264: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def load_state(self):
        if self.bot_paths is None:
            self._init_to_first_behavior()
            return
        workspace_dir = self.bot_paths.workspace_directory
```

---

## avoid_excessive_guards
**duplication_scanner.py** - 1 violation(s)

[!] WARNING (line 1900)
Line 1900: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
            
            cached_blocks = self._load_blocks_from_cache(file_path)
            if cached_blocks is not None:
                cache_hits += 1
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = content.split('\n')
                    for block in cached_blocks:
                        block['file_path'] = file_path
                        block['lines'] = lines
                        all_blocks.append(block)
                except Exception as e:
                    logger.debug(f'Error rehydrating cached blocks for {file_path}: {e}')
                continue
            
```

---

## avoid_excessive_guards
**scenarios_on_story_docs_scanner.py** - 1 violation(s)

[!] WARNING (line 106)
Line 106: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
        
        if isinstance(node, Story):
            if self._in_scope_story_names is not None:
                if node.name not in self._in_scope_story_names:
                    return violations
            
```

---

## avoid_excessive_guards
**story_map.py** - 1 violation(s)

[!] WARNING (line 37)
Line 37: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
                for idx in self.sub_epic_path:
                    path_parts.append(f"sub_epics[{idx}]")
            if self.story_group_idx is not None:
                path_parts.append(f"story_groups[{self.story_group_idx}]")
            path_parts.append(f"stories[{self.story_idx}]")
```

---

## avoid_excessive_guards
**requirements_clarifications.py** - 1 violation(s)

[!] WARNING (line 41)
Line 41: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
        
        final_context = existing_context or []
        if self.context is not None:
            if isinstance(self.context, list):
                final_context = final_context if isinstance(final_context, list) else []
                final_context.extend(self.context)
            else:
                final_context = final_context if isinstance(final_context, list) else []
                final_context.append(self.context)
        
```

---

## avoid_excessive_guards
**ast_elements.py** - 1 violation(s)

[!] WARNING (line 135)
Line 135: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    def has_bare_except(self) -> bool:
        for handler in self._node.handlers:
            if handler.type is None:
                return True
        return False
```

---

## avoid_excessive_guards
**block.py** - 5 violation(s)

[!] WARNING (line 62)
Line 62: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    
    def has_similarity(self, other: 'Block', similarity_calculator) -> bool:
        if self._similarity_calculator is None:
            self._similarity_calculator = similarity_calculator
        return self._similarity_calculator.calculates_block_similarity(self, other)
```

[!] WARNING (line 67)
Line 67: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    
    def analyze_structure(self, code_structure_analyzer) -> List['Violation']:
        if self._code_structure_analyzer is None:
            self._code_structure_analyzer = code_structure_analyzer
        return self._code_structure_analyzer.analyzes_code_structure(self)
```

[!] WARNING (line 72)
Line 72: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    
    def calculate_complexity(self, complexity_metrics) -> dict:
        if self._complexity_metrics is None:
            self._complexity_metrics = complexity_metrics
        return {}
```

[!] WARNING (line 77)
Line 77: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    
    def check_class_naming(self, class_naming_checker) -> List['Violation']:
        if self._class_naming_checker is None:
            self._class_naming_checker = class_naming_checker
        return self._class_naming_checker.checks_class_name_matches_story(self) + \
```

[!] WARNING (line 83)
Line 83: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    
    def check_method_naming(self, method_naming_checker) -> List['Violation']:
        if self._method_naming_checker is None:
            self._method_naming_checker = method_naming_checker
        return self._method_naming_checker.checks_method_name_matches_scenario(self) + \
```

---

## avoid_excessive_guards
**file.py** - 2 violation(s)

[!] WARNING (line 52)
Line 52: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def content(self) -> Optional[str]:
        if self._content is None:
            self._load_content()
        return self._content
```

[!] WARNING (line 58)
Line 58: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    def parse_safely(self) -> bool:
        try:
            if self._content is None:
                self._load_content()
            
```

---

## avoid_unnecessary_parameter_passing
**render_action.py** - 2 violation(s)

[!] WARNING (line 46)
Instance property "self._render_specs" is extracted to variable "render_specs" and passed to internal method "_execute_synchronizers". Access via self._render_specs directly instead.

[!] WARNING (line 100)
Instance property "self._render_specs" is extracted to variable "render_specs" and passed to internal method "_execute_synchronizers". Access via self._render_specs directly instead.

---

## avoid_unnecessary_parameter_passing
**strategy_criteria.py** - 1 violation(s)

[!] WARNING (line 10)
Internal method "_format_options" receives parameter "options" that matches instance attribute. Consider accessing via self.options instead.

---

## chain_dependencies_properly
**prefer_object_model_over_config_scanner.py** - 1 violation(s)

[!] WARNING (line 30)
Method "scan_file" in class "PreferObjectModelOverConfigScanner" takes parameter "rule_obj" that is already injected in __init__. Use self.rule_obj instead.

```python
        ]
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Dict[str, Any] = None) -> List[Violation]:
        violations = []
        
    # ... (truncated)
```

---

## delegate_to_lowest_level
**tty_behavior.py** - 1 violation(s)

[i] INFO (line 24)
Method "names" in class "TTYBehaviors" iterates through "behaviors" instead of delegating to collection class. Delegate to collection class instead.

---

## delegate_to_lowest_level
**base_hierarchical_adapter.py** - 1 violation(s)

[i] INFO (line 129)
Method "_build_wrapped_hierarchy" in class "BaseActionsAdapter" iterates through "actions" instead of delegating to collection class. Delegate to collection class instead.

---

## delegate_to_lowest_level
**file_discovery.py** - 1 violation(s)

[i] INFO (line 24)
Method "_matches_any_exclude_pattern" in class "FileDiscovery" iterates through "exclude_patterns" instead of delegating to collection class. Delegate to collection class instead.

---

## delegate_to_lowest_level
**scope.py** - 1 violation(s)

[i] INFO (line 30)
Method "_collect_blocks_from_files" in class "Scope" iterates through "files" instead of delegating to collection class. Delegate to collection class instead.

---

## eliminate_duplication
**markdown_behavior.py** - 2 violation(s)

[X] ERROR (line 13)
Duplicate code detected: functions serialize, serialize have identical bodies - extract to shared function

[X] ERROR (line 17)
Duplicate code detected: functions parse_command_text, parse_command_text have identical bodies - extract to shared function

---

## eliminate_duplication
**tty_behavior.py** - 2 violation(s)

[X] ERROR (line 36)
Duplicate code detected: functions serialize, serialize have identical bodies - extract to shared function

[X] ERROR (line 40)
Duplicate code detected: functions parse_command_text, parse_command_text have identical bodies - extract to shared function

---

## eliminate_duplication
**json_bot.py** - 1 violation(s)

[X] ERROR (line 37)
Duplicate code detected: functions format_header, format_bot_info, format_footer have identical bodies - extract to shared function

---

