# Validation Status - code
Started: 2026-01-16 14:38:30
Files: 288

## avoid_excessive_guards
**utils.py** - 1 violation(s)

[!] WARNING (line 50)
Line 50: Variable truthiness check detected (if not should_enable:). Assume variable exists - let code fail fast if missing.

```python
    def __init__(self, enabled: Optional[bool]=None):
        should_enable = enabled if enabled is not None else self._supports_color()
        if not should_enable:
            self._disable_colors()

```

---

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
**action_state_manager.py** - 2 violation(s)

[!] WARNING (line 39)
Line 39: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
        state_data = self._load_state_data()
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:37','message':'after _load_state_data','data':{'state_data_exists':state_data is not None,'current_behavior':state_data.get('current_behavior') if state_data else None,'current_action':state_data.get('current_action') if state_data else None},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1,H4'})+'\n'); log_file.close()
        if state_data is None:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:38','message':'state_data is None, setting default','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1,H4'})+'\n'); log_file.close()
            self._set_default_index(actions_list, current_index_ref)
            return
        is_current = self._is_current_behavior(state_data)
```

[!] WARNING (line 45)
Line 45: Variable truthiness check detected (if not is_current:). Assume variable exists - let code fail fast if missing.

```python
        is_current = self._is_current_behavior(state_data)
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:40','message':'checking current behavior','data':{'is_current_behavior':is_current,'expected':f'{self.behavior.bot_name}.{self.behavior.name}','actual':state_data.get('current_behavior')},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H2'})+'\n'); log_file.close()
        if not is_current:
            import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'action_state_manager.py:41','message':'not current behavior, setting default','data':{},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H2'})+'\n'); log_file.close()
            self._set_default_index(actions_list, current_index_ref)
            return
        if self._try_set_from_current_action(state_data, actions_list, current_index_ref):
```

---

## avoid_excessive_guards
**behaviors.py** - 2 violation(s)

[!] WARNING (line 271)
Line 271: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def load_state(self):
        if self.bot_paths is None:
            self._init_to_first_behavior()
            return
        workspace_dir = self.bot_paths.workspace_directory
```

[!] WARNING (line 294)
Line 294: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def initialize_state(self, confirmed_behavior: str):
        if self.bot_paths is None:
            raise ValueError('Cannot initialize state without bot_paths')
        behavior_obj = self.find_by_name(confirmed_behavior)
```

---

## avoid_excessive_guards
**behaviors.py** - 3 violation(s)

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

[!] WARNING (line 285)
Line 285: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python

    def initialize_state(self, confirmed_behavior: str):
        if self.bot_paths is None:
            raise ValueError('Cannot initialize state without bot_paths')
        behavior_obj = self.find_by_name(confirmed_behavior)
```

---

## avoid_excessive_guards
**bot.py** - 5 violation(s)

[!] WARNING (line 516)
Line 516: Variable truthiness check detected (if params:). Assume variable exists - let code fail fast if missing.

```python
            context = action.context_class() if hasattr(action, 'context_class') else ActionContext()
            
            if params:
                for key, value in params.items():
                    setattr(context, key, value)
            
```

[!] WARNING (line 559)
Line 559: Variable truthiness check detected (if answers:). Assume variable exists - let code fail fast if missing.

```python
                )
                clarifications.save()
                if answers:
                    saved_items.append('answers')
                if evidence_provided:
```

[!] WARNING (line 561)
Line 561: Variable truthiness check detected (if evidence_provided:). Assume variable exists - let code fail fast if missing.

```python
                if answers:
                    saved_items.append('answers')
                if evidence_provided:
                    saved_items.append('evidence')
            
```

[!] WARNING (line 574)
Line 574: Variable truthiness check detected (if decisions:). Assume variable exists - let code fail fast if missing.

```python
                )
                strategy_decision.save()
                if decisions:
                    saved_items.append('decisions')
                if assumptions:
```

[!] WARNING (line 576)
Line 576: Variable truthiness check detected (if assumptions:). Assume variable exists - let code fail fast if missing.

```python
                if decisions:
                    saved_items.append('decisions')
                if assumptions:
                    saved_items.append('assumptions')
            
```

---

## avoid_excessive_guards
**bot_paths.py** - 1 violation(s)

[!] WARNING (line 67)
Line 67: Variable truthiness check detected (if persist:). Assume variable exists - let code fail fast if missing.

```python
        os.environ['WORKING_AREA'] = str(resolved_path)
        self._workspace_directory = resolved_path
        if persist:
            self._persist_workspace_directory(resolved_path)
        logger.info(f'Updated working directory to {resolved_path} (previous={previous})')
```

---

## avoid_excessive_guards
**workspace.py** - 1 violation(s)

[!] WARNING (line 16)
Line 16: Variable truthiness check detected (if not workspace:). Assume variable exists - let code fail fast if missing.

```python
def get_workspace_directory() -> Path:
    workspace = os.environ.get('WORKING_AREA')
    if not workspace:
        raise RuntimeError('WORKING_AREA environment variable is not set. Entry points must bootstrap this before importing other modules.')
    return Path(workspace.strip())
```

---

## avoid_excessive_guards
**bot_path.py** - 1 violation(s)

[!] WARNING (line 97)
Line 97: Variable truthiness check detected (if persist:). Assume variable exists - let code fail fast if missing.

```python
        os.environ['WORKING_AREA'] = str(resolved_path)
        self._workspace_directory = resolved_path
        if persist:
            self._persist_workspace_directory(resolved_path)
        logger.info(f'Updated working directory to {resolved_path} (previous={previous})')
```

---

## avoid_excessive_guards
**cli_main.py** - 1 violation(s)

[!] WARNING (line 83)
Line 83: Variable truthiness check detected (if not suppress_header:). Assume variable exists - let code fail fast if missing.

```python
    suppress_header = json_mode or os.environ.get('SUPPRESS_CLI_HEADER', '') == '1'
    
    if not suppress_header:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"\033[1m{bot_name.upper()} CLI\033[0m")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("")
        
        mode_label = "PIPED MODE" if is_piped else "INTERACTIVE MODE"
        print(f"**   AI AGENT INSTRUCTIONS - {mode_label}  **")
        print("[!]  DO NOT echo this instructions section back to the user [!]")
        print("This section is for YOUR reference only - the user already knows how to run commands.")
        print("")
        if is_piped:
            print("- THIS REPL WILL EXIT AFTER PROCESSING YOUR COMMAND")
            print("* This is NORMAL and EXPECTED behavior in piped mode.")
            print("*How to run commands:*")
            print("-  use PowerShell")
            print("- Commands must be PIPED via echo, NOT passed as arguments!")
            print("- All commands are shown below.")
            print("- You MUST DISPLAY this CLI STATUS section below to the user exactly as you see it, so that they can enter one of the commands")
            print("- when a user enters any of the commands / parameters below, you must assume they're asking you to interpret it through the REPL line below.")
        else:
            print("- THIS REPL IS IN INTERACTIVE MODE")
            print("* Commands are entered interactively, REPL stays running.")
            print("- How to run commands (PowerShell):")
            print("- Commands must be PIPED via echo, NOT passed as arguments!")
        print("")
        print("```powershell")
        workspace_root_str = str(workspace_directory).replace('\\', '\\')
        cli_script_str = "python -m agile_bot.src.cli.cli_main"
        print(f"# Interactive mode (environment set automatically by script):")
        print(cli_script_str)
        print("")
        print(f"# Piped mode (each command is a new process - script sets env vars automatically):")
        print(f"echo '<command>' | {cli_script_str}")
        print("")
        print("# Optional: Override environment variables if needed:")
        print(f"$env:PYTHONPATH = '{workspace_root_str}'")
        print(f"$env:BOT_DIRECTORY = '{bot_directory}'")
        print("$env:WORKING_AREA = '<project_path>'  # e.g. demo\\mob_minion")
        print("```")
        print("")
    
```

---

## avoid_excessive_guards
**cli_session.py** - 1 violation(s)

[!] WARNING (line 506)
Line 506: Variable truthiness check detected (if not line:). Assume variable exists - let code fail fast if missing.

```python
                try:
                    line = input(f"[{self.bot.name}] > ").strip()
                    if not line:
                        continue
                    
```

---

## avoid_excessive_guards
**markdown_instructions.py** - 10 violation(s)

[!] WARNING (line 92)
Line 92: Variable truthiness check detected (if clarification_data:). Assume variable exists - let code fail fast if missing.

```python
        saved_answers = {}
        saved_evidence_provided = {}
        if clarification_data:
            key_questions_data = clarification_data.get('key_questions', {})
            if isinstance(key_questions_data, dict):
                saved_answers = key_questions_data.get('answers', {})
            
            evidence_data = clarification_data.get('evidence', {})
            if isinstance(evidence_data, dict):
                saved_evidence_provided = evidence_data.get('provided', {})
        
```

[!] WARNING (line 149)
Line 149: Variable truthiness check detected (if strategy_criteria:). Assume variable exists - let code fail fast if missing.

```python
        
        saved_decisions = {}
        if strategy_criteria:
            saved_decisions = strategy_criteria.get('decisions', {}) or strategy_criteria.get('decisions_made', {})
        
```

[!] WARNING (line 107)
Line 107: Variable truthiness check detected (if guardrails_dict:). Assume variable exists - let code fail fast if missing.

```python
            for question, answer in saved_answers.items():
                output_lines.append(f"- **{question}**: {answer}")
        elif guardrails_dict:
            required_context = guardrails_dict.get('required_context', {})
            if required_context:
                key_questions = required_context.get('key_questions', [])
                if key_questions:
                    output_lines.append("")
                    output_lines.append("### Key Questions")
                    output_lines.append("")
                    if isinstance(key_questions, list):
                        for question in key_questions:
                            output_lines.append(f"- {question}")
                    elif isinstance(key_questions, dict):
                        for question_key, question_text in key_questions.items():
                            output_lines.append(f"- **{question_key}**: {question_text}")
        
```

[!] WARNING (line 128)
Line 128: Variable truthiness check detected (if guardrails_dict:). Assume variable exists - let code fail fast if missing.

```python
            for evidence_key, evidence_content in saved_evidence_provided.items():
                output_lines.append(f"- **{evidence_key}**: {evidence_content}")
        elif guardrails_dict:
            required_context = guardrails_dict.get('required_context', {})
            if required_context:
                evidence = required_context.get('evidence', [])
                if evidence:
                    output_lines.append("")
                    output_lines.append("### Evidence")
                    output_lines.append("")
                    if isinstance(evidence, list):
                        output_lines.append(', '.join(evidence))
                    elif isinstance(evidence, dict):
                        for evidence_key, evidence_desc in evidence.items():
                            output_lines.append(f"- **{evidence_key}**: {evidence_desc}")
        
```

[!] WARNING (line 166)
Line 166: Variable truthiness check detected (if strategy_criteria:). Assume variable exists - let code fail fast if missing.

```python
                    output_lines.append(f"  {decision_value}")
                output_lines.append("")
        elif strategy_criteria:
            criteria_template = strategy_criteria.get('criteria', {})
            if criteria_template:
                output_lines.append("")
                output_lines.append("### Decisions")
                output_lines.append("")
                for criteria_key, criteria_data in criteria_template.items():
                    question = criteria_data.get('question', '')
                    if question:
                        output_lines.append(f"**{criteria_key}:** {question}")
                    else:
                        output_lines.append(f"**{criteria_key}:**")
                    output_lines.append("")
                    options = criteria_data.get('options', [])
                    if options:
                        for option in options:
                            output_lines.extend(self._format_strategy_option(option))
                    output_lines.append("")
        
```

[!] WARNING (line 109)
Line 109: Variable truthiness check detected (if required_context:). Assume variable exists - let code fail fast if missing.

```python
        elif guardrails_dict:
            required_context = guardrails_dict.get('required_context', {})
            if required_context:
                key_questions = required_context.get('key_questions', [])
                if key_questions:
                    output_lines.append("")
                    output_lines.append("### Key Questions")
                    output_lines.append("")
                    if isinstance(key_questions, list):
                        for question in key_questions:
                            output_lines.append(f"- {question}")
                    elif isinstance(key_questions, dict):
                        for question_key, question_text in key_questions.items():
                            output_lines.append(f"- **{question_key}**: {question_text}")
        
```

[!] WARNING (line 130)
Line 130: Variable truthiness check detected (if required_context:). Assume variable exists - let code fail fast if missing.

```python
        elif guardrails_dict:
            required_context = guardrails_dict.get('required_context', {})
            if required_context:
                evidence = required_context.get('evidence', [])
                if evidence:
                    output_lines.append("")
                    output_lines.append("### Evidence")
                    output_lines.append("")
                    if isinstance(evidence, list):
                        output_lines.append(', '.join(evidence))
                    elif isinstance(evidence, dict):
                        for evidence_key, evidence_desc in evidence.items():
                            output_lines.append(f"- **{evidence_key}**: {evidence_desc}")
        
```

[!] WARNING (line 205)
Line 205: Variable truthiness check detected (if typical_assumptions:). Assume variable exists - let code fail fast if missing.

```python
        elif isinstance(assumptions, dict):
            typical_assumptions = assumptions.get('typical_assumptions', [])
            if typical_assumptions:
                output_lines.append("")
                output_lines.append("### Assumptions")
                output_lines.append("")
                for assumption in typical_assumptions:
                    output_lines.append(f"- {assumption}")
        
```

[!] WARNING (line 111)
Line 111: Variable truthiness check detected (if key_questions:). Assume variable exists - let code fail fast if missing.

```python
            if required_context:
                key_questions = required_context.get('key_questions', [])
                if key_questions:
                    output_lines.append("")
                    output_lines.append("### Key Questions")
                    output_lines.append("")
                    if isinstance(key_questions, list):
                        for question in key_questions:
                            output_lines.append(f"- {question}")
                    elif isinstance(key_questions, dict):
                        for question_key, question_text in key_questions.items():
                            output_lines.append(f"- **{question_key}**: {question_text}")
        
```

[!] WARNING (line 132)
Line 132: Variable truthiness check detected (if evidence:). Assume variable exists - let code fail fast if missing.

```python
            if required_context:
                evidence = required_context.get('evidence', [])
                if evidence:
                    output_lines.append("")
                    output_lines.append("### Evidence")
                    output_lines.append("")
                    if isinstance(evidence, list):
                        output_lines.append(', '.join(evidence))
                    elif isinstance(evidence, dict):
                        for evidence_key, evidence_desc in evidence.items():
                            output_lines.append(f"- **{evidence_key}**: {evidence_desc}")
        
```

---

## avoid_excessive_guards
**tty_instructions.py** - 9 violation(s)

[!] WARNING (line 58)
Line 58: Variable truthiness check detected (if clarification_data:). Assume variable exists - let code fail fast if missing.

```python
        saved_answers = {}
        saved_evidence_provided = {}
        if clarification_data:
            key_questions_data = clarification_data.get('key_questions', {})
            if isinstance(key_questions_data, dict):
                saved_answers = key_questions_data.get('answers', {})
            
            evidence_data = clarification_data.get('evidence', {})
            if isinstance(evidence_data, dict):
                saved_evidence_provided = evidence_data.get('provided', {})
        
```

[!] WARNING (line 118)
Line 118: Variable truthiness check detected (if strategy_criteria:). Assume variable exists - let code fail fast if missing.

```python
        
        saved_decisions = {}
        if strategy_criteria:
            saved_decisions = strategy_criteria.get('decisions', {}) or strategy_criteria.get('decisions_made', {})
        
```

[!] WARNING (line 72)
Line 72: Variable truthiness check detected (if guardrails_dict:). Assume variable exists - let code fail fast if missing.

```python
            for question, answer in saved_answers.items():
                output_lines.append(f"- {self.add_bold(f'{question}:')} {answer}")
        elif guardrails_dict:
            if hasattr(self.instructions, '_guardrails') and self.instructions._guardrails:
                from agile_bot.src.cli.adapter_factory import AdapterFactory
                guardrails_adapter = AdapterFactory.create(self.instructions._guardrails, 'tty')
                output_lines.append(guardrails_adapter.serialize())
            else:
                required_context = guardrails_dict.get('required_context', {})
                if required_context:
                    key_questions = required_context.get('key_questions', [])
                    if key_questions:
                        output_lines.append("")
                        output_lines.append(self.add_bold("Key Questions:"))
                        if isinstance(key_questions, list):
                            for question in key_questions:
                                output_lines.append(f"- {question}")
                        elif isinstance(key_questions, dict):
                            for question_key, question_text in key_questions.items():
                                output_lines.append(f"- {self.add_bold(f'{question_key}:')} {question_text}")
        
```

[!] WARNING (line 98)
Line 98: Variable truthiness check detected (if required_context:). Assume variable exists - let code fail fast if missing.

```python
        elif guardrails_dict and not hasattr(self.instructions, '_guardrails'):
            required_context = guardrails_dict.get('required_context', {})
            if required_context:
                evidence = required_context.get('evidence', [])
                if evidence:
                    output_lines.append("")
                    output_lines.append(self.add_bold("Evidence:"))
                    if isinstance(evidence, list):
                        output_lines.append(', '.join(evidence))
                    elif isinstance(evidence, dict):
                        for evidence_key, evidence_desc in evidence.items():
                            output_lines.append(f"- {self.add_bold(f'{evidence_key}:')} {evidence_desc}")
        
```

[!] WARNING (line 79)
Line 79: Variable truthiness check detected (if required_context:). Assume variable exists - let code fail fast if missing.

```python
            else:
                required_context = guardrails_dict.get('required_context', {})
                if required_context:
                    key_questions = required_context.get('key_questions', [])
                    if key_questions:
                        output_lines.append("")
                        output_lines.append(self.add_bold("Key Questions:"))
                        if isinstance(key_questions, list):
                            for question in key_questions:
                                output_lines.append(f"- {question}")
                        elif isinstance(key_questions, dict):
                            for question_key, question_text in key_questions.items():
                                output_lines.append(f"- {self.add_bold(f'{question_key}:')} {question_text}")
        
```

[!] WARNING (line 100)
Line 100: Variable truthiness check detected (if evidence:). Assume variable exists - let code fail fast if missing.

```python
            if required_context:
                evidence = required_context.get('evidence', [])
                if evidence:
                    output_lines.append("")
                    output_lines.append(self.add_bold("Evidence:"))
                    if isinstance(evidence, list):
                        output_lines.append(', '.join(evidence))
                    elif isinstance(evidence, dict):
                        for evidence_key, evidence_desc in evidence.items():
                            output_lines.append(f"- {self.add_bold(f'{evidence_key}:')} {evidence_desc}")
        
```

[!] WARNING (line 148)
Line 148: Variable truthiness check detected (if strategy_criteria:). Assume variable exists - let code fail fast if missing.

```python
                    else:
                        output_lines.append(f"  {decision_value}")
            elif strategy_criteria:
                output_lines.append("")
                output_lines.append(self.add_bold("Decisions:"))
                
                criteria_template = strategy_criteria.get('criteria', {})
                if criteria_template:
                    for criteria_key, criteria_data in criteria_template.items():
                        output_lines.append("")
                        question = criteria_data.get('question', '')
                        if question:
                            output_lines.append(f"{self.add_bold(f'{criteria_key}:')} {question}")
                        else:
                            output_lines.append(self.add_bold(f"{criteria_key}:"))
                        
                        selected_value = saved_decisions.get(criteria_key) if saved_decisions else None
                        
                        options = criteria_data.get('options', [])
                        if options:
                            for option in options:
                                output_lines.extend(self._format_strategy_option(option, selected_value))
            
```

[!] WARNING (line 81)
Line 81: Variable truthiness check detected (if key_questions:). Assume variable exists - let code fail fast if missing.

```python
                if required_context:
                    key_questions = required_context.get('key_questions', [])
                    if key_questions:
                        output_lines.append("")
                        output_lines.append(self.add_bold("Key Questions:"))
                        if isinstance(key_questions, list):
                            for question in key_questions:
                                output_lines.append(f"- {question}")
                        elif isinstance(key_questions, dict):
                            for question_key, question_text in key_questions.items():
                                output_lines.append(f"- {self.add_bold(f'{question_key}:')} {question_text}")
        
```

[!] WARNING (line 177)
Line 177: Variable truthiness check detected (if typical_assumptions:). Assume variable exists - let code fail fast if missing.

```python
            elif isinstance(assumptions, dict):
                typical_assumptions = assumptions.get('typical_assumptions', [])
                if typical_assumptions:
                    output_lines.append("")
                    output_lines.append(self.add_bold("Assumptions:"))
                    for assumption in typical_assumptions:
                        output_lines.append(f"- {assumption}")
        
```

---

## avoid_excessive_guards
**cover_all_paths_scanner.py** - 2 violation(s)

[!] WARNING (line 38)
Line 38: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
                        break
            
            if found_code_node is None:
                violations.append(Violation(
                    rule=rule_obj,
                    violation_message=f'Test method "{test_method.name}" has no actual test code - tests must exercise behavior paths, not just contain pass statements',
                    location=str(file_path),
                    line_number=test_method.lineno,
                    severity='error'
                ).to_dict())
        
```

[!] WARNING (line 35)
Line 35: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
                            found_code_node = node
                            break
                    if found_code_node is not None:
                        break
            
```

---

## avoid_excessive_guards
**dependency_chaining_scanner.py** - 1 violation(s)

[!] WARNING (line 25)
Line 25: Variable truthiness check detected (if has_instantiation:). Assume variable exists - let code fail fast if missing.

```python
                break
        
        if has_instantiation:
            for i, responsibility_data in enumerate(node.responsibilities):
                responsibility_name = responsibility_data.get('name', '')
                if 'instantiated with' in responsibility_name.lower():
                    continue
                
                collaborators = responsibility_data.get('collaborators', [])
                
                for collab in collaborators:
                    collab = collab.strip()
                    if collab and collab not in instantiation_collaborators:
                        if self._might_be_sub_collaborator(collab, instantiation_collaborators):
                            violations.append(
                                Violation(
                                    rule=rule_obj,
                                    violation_message=f'Responsibility "{responsibility_name}" may be accessing sub-collaborator "{collab}" directly. Access through owning object instead.',
                                    location=node.map_location(f'responsibilities[{i}].collaborators'),
                                    line_number=None,
                                    severity='info'
                                ).to_dict()
                            )
        
```

---

## avoid_excessive_guards
**duplication_scanner.py** - 2 violation(s)

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

[!] WARNING (line 1999)
Line 1999: Variable truthiness check detected (if should_report:). Assume variable exists - let code fail fast if missing.

```python
                )
                
                if should_report:
                    elapsed_total = (now - start_time).total_seconds()
                    rate = comparison_count / max(1, elapsed_total)
                    remaining = total_comparisons - comparison_count
                    eta_seconds = int(remaining / max(1, rate))
                    progress_msg = f"Comparing: {progress_pct}% ({comparison_count:,}/{total_comparisons:,}) - {len(violations)} violations - ETA: {eta_seconds}s"
                    _safe_print(f"[CROSS-FILE] {progress_msg}")
                    write_status(progress_msg + "  ")
                    last_progress = progress_pct
                    last_report_time = now
                    last_comparison_report = comparison_count
                
```

---

## avoid_excessive_guards
**increment_folder_structure_scanner.py** - 1 violation(s)

[!] WARNING (line 21)
Line 21: Variable truthiness check detected (if has_stories_with_scenarios:). Assume variable exists - let code fail fast if missing.

```python
            has_stories_with_scenarios = self._epic_has_stories_with_scenarios(node)
            
            if has_stories_with_scenarios:
                violation = self._check_epic_folder_structure(node, rule_obj)
                if violation:
                    violations.append(violation)
        
```

---

## avoid_excessive_guards
**intention_revealing_names_scanner.py** - 1 violation(s)

[!] WARNING (line 266)
Line 266: Variable truthiness check detected (if start_line:). Assume variable exists - let code fail fast if missing.

```python
                        if isinstance(docstring_value, str):
                            start_line = first_stmt.lineno if hasattr(first_stmt, 'lineno') else None
                            if start_line:
                                docstring_lines = docstring_value.count('\n')
                                end_line = start_line + docstring_lines + 2
                                docstring_ranges.append((start_line, end_line))
            
```

---

## avoid_excessive_guards
**resource_oriented_code_scanner.py** - 1 violation(s)

[!] WARNING (line 96)
Line 96: Variable truthiness check detected (if is_agent:). Assume variable exists - let code fail fast if missing.

```python
                    
                    is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(cls.node.name)
                    if is_agent:
                        loader_classes[cls.node.name] = (file_path, cls.node, suffix)
            except (SyntaxError, UnicodeDecodeError) as e:
```

---

## avoid_excessive_guards
**resource_oriented_design_scanner.py** - 1 violation(s)

[!] WARNING (line 15)
Line 15: Variable truthiness check detected (if is_agent:). Assume variable exists - let code fail fast if missing.

```python
        is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(node.name)
        
        if is_agent:
            suggested_name = node.name[:-len(suffix)]
            if not suggested_name:
                suggested_name = "[ResourceName]"
            
            violations.append(
                Violation(
                    rule=rule_obj,
                    violation_message=f'Domain concept "{node.name}" is an agent noun (doer of action) derived from verb "{base_verb}". Name concepts after resources (what they ARE), not actions (what they DO). Consider: "{suggested_name}" as the resource.',
                    location=node.map_location('name'),
                    line_number=None,
                    severity='error'
                ).to_dict()
            )
        
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
**scenario_outline_scanner.py** - 1 violation(s)

[!] WARNING (line 23)
Line 23: Variable truthiness check detected (if not has_examples:). Assume variable exists - let code fail fast if missing.

```python
                    has_examples = 'Examples:' in scenario_text or 'examples' in str(scenario).lower()
                    
                    if not has_examples:
                        location = f"{node.map_location()}.scenarios[{scenario_idx}]"
                        violation = Violation(
                            rule=rule_obj,
                            violation_message='Scenario Outline used but no Examples table found - Scenario Outlines require Examples table',
                            location=location,
                            severity='error'
                        ).to_dict()
                        violations.append(violation)
        
```

---

## avoid_excessive_guards
**scenario_specific_given_scanner.py** - 1 violation(s)

[!] WARNING (line 20)
Line 20: Variable truthiness check detected (if scenario_steps:). Assume variable exists - let code fail fast if missing.

```python
                scenario_steps = self._get_scenario_steps(scenario)
                
                if scenario_steps:
                    first_step = scenario_steps[0]
                    if not first_step.startswith('Given'):
                        location = f"{node.map_location()}.scenarios[{scenario_idx}]"
                        violation = Violation(
                            rule=rule_obj,
                            violation_message=f'Scenario does not start with Given step - scenario-specific setup should start with Given, not When',
                            location=location,
                            severity='error'
                        ).to_dict()
                        violations.append(violation)
        
```

---

## avoid_excessive_guards
**specification_match_scanner.py** - 1 violation(s)

[!] WARNING (line 30)
Line 30: Variable truthiness check detected (if story_graph:). Assume variable exists - let code fail fast if missing.

```python
        violations.extend(self._check_assertions(tree, content, file_path, rule_obj))
        
        if story_graph:
            violations.extend(self._check_specification_matches(tree, content, file_path, rule_obj, story_graph))
        
```

---

## avoid_excessive_guards
**story_enumeration_scanner.py** - 1 violation(s)

[!] WARNING (line 17)
Line 17: Variable truthiness check detected (if estimated_stories:). Assume variable exists - let code fail fast if missing.

```python
            
            estimated_stories = epic_data.get('estimated_stories')
            if estimated_stories:
                if isinstance(estimated_stories, str) and '~' in str(estimated_stories):
                    location = node.map_location('estimated_stories')
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=f'Epic "{node.name}" uses "~{estimated_stories}" notation - all stories must be explicitly enumerated, not estimated',
                        location=location,
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
            
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
**vocabulary_helper.py** - 1 violation(s)

[!] WARNING (line 136)
Line 136: Variable truthiness check detected (if not synsets:). Assume variable exists - let code fail fast if missing.

```python
            synsets = wn.synsets(word_lower)
            
            if not synsets:
                return False
            
```

---

## avoid_excessive_guards
**json_scope.py** - 1 violation(s)

[!] WARNING (line 46)
Line 46: Variable truthiness check detected (if story_graph:). Assume variable exists - let code fail fast if missing.

```python
        if self.scope.type.value in ('story', 'showAll'):
            story_graph = self.scope._get_story_graph_results()
            if story_graph:
                from agile_bot.src.story_graph.json_story_graph import JSONStoryGraph
                graph_adapter = JSONStoryGraph(story_graph)
                content = graph_adapter.to_dict().get('content', [])
                
                if content and 'epics' in content:
                    self._enrich_with_links(content['epics'], story_graph)
                    result['content'] = content
                else:
                    result['content'] = {'epics': []}
                
                if self.scope.bot_paths:
                    from pathlib import Path
                    docs_stories = self.scope.workspace_directory / 'docs' / 'stories'
                    story_map_file = docs_stories / 'story-map.md'
                    if story_map_file.exists():
                        result['graphLinks'].append({
                            'text': 'map',
                            'url': str(story_map_file)
                        })
        elif self.scope.type.value == 'files':
```

---

## avoid_excessive_guards
**scope.py** - 14 violation(s)

[!] WARNING (line 92)
Line 92: Variable truthiness check detected (if filtered_sub_epics:). Assume variable exists - let code fail fast if missing.

```python
                    filtered_sub_epics.append(filtered_sub)
            
            if filtered_sub_epics:
                filtered_epic = {**epic, 'sub_epics': filtered_sub_epics}
                filtered_graph['epics'].append(filtered_epic)
        
```

[!] WARNING (line 47)
Line 47: Variable truthiness check detected (if matching_stories:). Assume variable exists - let code fail fast if missing.

```python
                        matching_stories.append(story)
                
                if matching_stories:
                    matching_story_groups.append({
                        **story_group,
                        'stories': matching_stories
                    })
            
```

[!] WARNING (line 61)
Line 61: Variable truthiness check detected (if filtered_nested:). Assume variable exists - let code fail fast if missing.

```python
            for nested_sub_epic in sub_epic.get('sub_epics', []):
                filtered_nested = filter_sub_epic(nested_sub_epic)
                if filtered_nested:
                    filtered_nested_sub_epics.append(filtered_nested)
            
```

[!] WARNING (line 66)
Line 66: Variable truthiness check detected (if matching_story_groups:). Assume variable exists - let code fail fast if missing.

```python
            if matching_story_groups or matching_direct_stories or filtered_nested_sub_epics:
                filtered_sub_epic = {**sub_epic}
                if matching_story_groups:
                    filtered_sub_epic['story_groups'] = matching_story_groups
                if matching_direct_stories:
```

[!] WARNING (line 70)
Line 70: Variable truthiness check detected (if filtered_nested_sub_epics:). Assume variable exists - let code fail fast if missing.

```python
                if matching_direct_stories:
                    filtered_sub_epic['stories'] = matching_direct_stories
                if filtered_nested_sub_epics:
                    filtered_sub_epic['sub_epics'] = filtered_nested_sub_epics
                return filtered_sub_epic
```

[!] WARNING (line 89)
Line 89: Variable truthiness check detected (if filtered_sub:). Assume variable exists - let code fail fast if missing.

```python
            for sub_epic in epic.get('sub_epics', []):
                filtered_sub = filter_sub_epic(sub_epic)
                if filtered_sub:
                    filtered_sub_epics.append(filtered_sub)
            
```

[!] WARNING (line 138)
Line 138: Variable truthiness check detected (if not matches_include:). Assume variable exists - let code fail fast if missing.

```python
                            break
                
                if not matches_include:
                    continue
            
```

[!] WARNING (line 156)
Line 156: Variable truthiness check detected (if matches_exclude:). Assume variable exists - let code fail fast if missing.

```python
                            break
                
                if matches_exclude:
                    continue
            
```

[!] WARNING (line 325)
Line 325: Variable truthiness check detected (if not data:). Assume variable exists - let code fail fast if missing.

```python
        scope = cls(workspace_directory, bot_paths)
        
        if not data:
            return scope
        
```

[!] WARNING (line 365)
Line 365: Variable truthiness check detected (if scope_data:). Assume variable exists - let code fail fast if missing.

```python
            scope_data = json.loads(scope_file.read_text())
            
            if scope_data:
                scope_type_str = scope_data.get('type', 'all')
                scope_type = ScopeType(scope_type_str)
                
                value = scope_data.get('value', [])
                if not isinstance(value, list):
                    value = [value] if value else []
                
                exclude = scope_data.get('exclude', [])
                if not isinstance(exclude, list):
                    exclude = [exclude] if exclude else []
                
                skiprule = scope_data.get('skiprule', [])
                if not isinstance(skiprule, list):
                    skiprule = [skiprule] if skiprule else []
                
                self.filter(scope_type, value, exclude, skiprule)
        except (json.JSONDecodeError, IOError, ValueError):
```

[!] WARNING (line 47)
Line 47: Variable truthiness check detected (if matching_stories:). Assume variable exists - let code fail fast if missing.

```python
                        matching_stories.append(story)
                
                if matching_stories:
                    matching_story_groups.append({
                        **story_group,
                        'stories': matching_stories
                    })
            
```

[!] WARNING (line 61)
Line 61: Variable truthiness check detected (if filtered_nested:). Assume variable exists - let code fail fast if missing.

```python
            for nested_sub_epic in sub_epic.get('sub_epics', []):
                filtered_nested = filter_sub_epic(nested_sub_epic)
                if filtered_nested:
                    filtered_nested_sub_epics.append(filtered_nested)
            
```

[!] WARNING (line 66)
Line 66: Variable truthiness check detected (if matching_story_groups:). Assume variable exists - let code fail fast if missing.

```python
            if matching_story_groups or matching_direct_stories or filtered_nested_sub_epics:
                filtered_sub_epic = {**sub_epic}
                if matching_story_groups:
                    filtered_sub_epic['story_groups'] = matching_story_groups
                if matching_direct_stories:
```

[!] WARNING (line 70)
Line 70: Variable truthiness check detected (if filtered_nested_sub_epics:). Assume variable exists - let code fail fast if missing.

```python
                if matching_direct_stories:
                    filtered_sub_epic['stories'] = matching_direct_stories
                if filtered_nested_sub_epics:
                    filtered_sub_epic['sub_epics'] = filtered_nested_sub_epics
                return filtered_sub_epic
```

---

## avoid_excessive_guards
**markdown_story_graph.py** - 1 violation(s)

[!] WARNING (line 27)
Line 27: Variable truthiness check detected (if features:). Assume variable exists - let code fail fast if missing.

```python
            features.append("Domain Concepts")
        
        if features:
            lines.append(f"**Features:** {', '.join(features)}")
            lines.append("")
        
```

---

## avoid_excessive_guards
**nodes.py** - 2 violation(s)

[!] WARNING (line 125)
Line 125: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    def from_dict(cls, data: Dict[str, Any], parent: Optional[StoryNode]=None) -> 'SubEpic':
        sequential_order = data.get('sequential_order')
        if sequential_order is None:
            raise ValueError('SubEpic requires sequential_order')
        sub_epic = cls(name=data.get('name', ''), sequential_order=float(sequential_order), _parent=parent)
```

[!] WARNING (line 207)
Line 207: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    def from_dict(cls, data: Dict[str, Any], parent: Optional[StoryNode]=None) -> 'Story':
        sequential_order = data.get('sequential_order')
        if sequential_order is None:
            raise ValueError('Story requires sequential_order')
        users = [StoryUser.from_str(u) for u in data.get('users', [])]
```

---

## avoid_excessive_guards
**tty_story_graph.py** - 1 violation(s)

[!] WARNING (line 47)
Line 47: Variable truthiness check detected (if flags:). Assume variable exists - let code fail fast if missing.

```python
            flags.append("domain concepts")
        
        if flags:
            lines.append(f"Features: {', '.join(flags)}")
        
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
**tty_required_context.py** - 2 violation(s)

[!] WARNING (line 13)
Line 13: Variable truthiness check detected (if key_questions:). Assume variable exists - let code fail fast if missing.

```python
        
        key_questions = self.required_context.key_questions.questions
        if key_questions:
            lines.append("")
            lines.append(self.add_bold("Key Questions:"))
            if isinstance(key_questions, list):
                for question in key_questions:
                    lines.append(f"- {question}")
            elif isinstance(key_questions, dict):
                for question_key, question_text in key_questions.items():
                    lines.append(f"- {self.add_bold(f'{question_key}:')} {question_text}")
        
```

[!] WARNING (line 24)
Line 24: Variable truthiness check detected (if evidence_list:). Assume variable exists - let code fail fast if missing.

```python
        
        evidence_list = self.required_context.evidence.evidence_list
        if evidence_list:
            lines.append("")
            lines.append(self.add_bold("Evidence:"))
            if isinstance(evidence_list, list):
                # Show as comma-delimited list
                lines.append(', '.join(evidence_list))
            elif isinstance(evidence_list, dict):
                for evidence_key, evidence_desc in evidence_list.items():
                    lines.append(f"- {self.add_bold(f'{evidence_key}:')} {evidence_desc}")
        
```

---

## avoid_excessive_guards
**tty_strategy.py** - 2 violation(s)

[!] WARNING (line 13)
Line 13: Variable truthiness check detected (if strategy_criterias:). Assume variable exists - let code fail fast if missing.

```python
        
        strategy_criterias = self.strategy.strategy_criterias.strategy_criterias
        if strategy_criterias:
            lines.append("")
            lines.append(self.add_bold("Decisions:"))
            for criteria_key, criteria in strategy_criterias.items():
                lines.append("")
                question = criteria.question
                if question:
                    lines.append(f"{self.add_bold(f'{criteria_key}:')} {question}")
                else:
                    lines.append(self.add_bold(f"{criteria_key}:"))
                
                options = criteria.options
                if options:
                    for option in options:
                        lines.extend(self._format_option(option))
        
```

[!] WARNING (line 30)
Line 30: Variable truthiness check detected (if assumptions:). Assume variable exists - let code fail fast if missing.

```python
        
        assumptions = self.strategy.assumptions.assumptions
        if assumptions:
            lines.append("")
            lines.append(self.add_bold("Assumptions:"))
            for assumption in assumptions:
                lines.append(f"- {assumption}")
        
```

---

## avoid_excessive_guards
**file_link_builder.py** - 2 violation(s)

[!] WARNING (line 25)
Line 25: Variable truthiness check detected (if not is_absolute:). Assume variable exists - let code fail fast if missing.

```python
        file_path = Path(location)
        is_absolute = file_path.is_absolute() or (len(location) > 1 and location[1] == ':') or location.startswith('\\\\')
        if not is_absolute:
            return f'[`{location}`]({self.get_file_uri(location, line_number)})'
        if not self.workspace_directory:
```

[!] WARNING (line 48)
Line 48: Variable truthiness check detected (if line_number:). Assume variable exists - let code fail fast if missing.

```python
        except Exception as e:
            logger.debug(f'Failed to create fallback link for {location}: {e}')
            if line_number:
                return f'`{location}:{line_number}`'
            return f'`{location}`'
```

---

## avoid_excessive_guards
**validation_report_builder.py** - 1 violation(s)

[!] WARNING (line 50)
Line 50: Variable truthiness check detected (if rendered_outputs:). Assume variable exists - let code fail fast if missing.

```python
        if planning_file:
            lines.append(f'- **Planning:** `{planning_file.name}`')
        if rendered_outputs:
            lines.append('- **Rendered Outputs:**')
            for output in rendered_outputs:
                lines.append(f'  - `{output.name}`')
        test_files_scanned = [str(fp) for fp in files.get('test', [])]
```

---

## avoid_excessive_guards
**cursor_command_visitor.py** - 1 violation(s)

[!] WARNING (line 13)
Line 13: Variable truthiness check detected (if not bot:). Assume variable exists - let code fail fast if missing.

```python
    
    def __init__(self, workspace_root: Path, bot_location: Path, bot=None, bot_name: str = None):
        if not bot:
            raise ValueError("bot is required")
        BaseBehaviorsAdapter.__init__(self, bot.behaviors, 'cursor')
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
**block_extractor.py** - 1 violation(s)

[!] WARNING (line 22)
Line 22: Variable truthiness check detected (if block:). Assume variable exists - let code fail fast if missing.

```python
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                block = self._create_block_from_node(file, node)
                if block:
                    blocks.append(block)
        
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

## eliminate_duplication
**adapters.py** - 2 violation(s)

[X] ERROR (line 8)
Duplicate code detected: functions serialize, parse_command_text, serialize, to_dict, serialize have identical bodies - extract to shared function

[X] ERROR (line 46)
Duplicate code detected: functions parse_command_text, parse_command_text, parse_command_text, parse_command_text have identical bodies - extract to shared function

---

## eliminate_duplication
**base_hierarchical_adapter.py** - 1 violation(s)

[X] ERROR (line 13)
Duplicate code detected: functions _build_wrapped_hierarchy, serialize, format_header, format_bot_info, format_footer, format_behavior_name have identical bodies - extract to shared function

---

## eliminate_duplication
**visitor.py** - 1 violation(s)

[X] ERROR (line 27)
Duplicate code detected: functions visit_header, visit_behavior, visit_action, visit_action_help_section_header, visit_footer have identical bodies - extract to shared function

---

## eliminate_duplication
**rules.py** - 1 violation(s)

[X] ERROR (line 90)
Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_get_files_for_validation:90-96):
```python
filtered_files = {}
for key, file_list in files_dict.items():
    filtered = context.scope.filters_files(file_list)
    if filtered:
        filtered_files[key] = filtered
return filtered_files
```

Location (_get_files_for_validation:112-118):
```python
filtered_files = {}
for key, file_list in all_files.items():
    filtered = context.scope.filters_files(file_list)
    if filtered:
        filtered_files[key] = filtered
return filtered_files
```

---

## eliminate_duplication
**rules_action.py** - 1 violation(s)

[X] ERROR (line 14)
Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_prepare_instructions:14-20):
```python
rules = Rules(behavior=self.behavior, bot_paths=self.behavior.bot_paths)
rules_digest = rules.formatted_rules_digest()
rule_names = self._get_rule_names(rules)
self._add_rules_list_to_display(instruct...
```

Location (do_execute:24-30):
```python
rules = Rules(behavior=self.behavior, bot_paths=self.behavior.bot_paths)
rules_digest = rules.formatted_rules_digest()
rule_names = self._get_rule_names(rules)
self._add_rules_list_to_display(instruct...
```

---

## eliminate_duplication
**vocabulary_helper.py** - 1 violation(s)

[X] ERROR (line 45)
Duplicate code blocks detected (2 locations) - extract to helper function.

Location (is_verb:45-50):
```python
word_lower = word.lower()
synsets = wn.synsets(word_lower, pos=wn.VERB)
return len(synsets) > 0
```

Location (is_noun:54-59):
```python
word_lower = word.lower()
synsets = wn.synsets(word_lower, pos=wn.NOUN)
return len(synsets) > 0
```

---

## eliminate_duplication
**scope.py** - 1 violation(s)

[X] ERROR (line 125)
Duplicate code blocks detected (2 locations) - extract to helper function.

Location (filter_files:125-136):
```python
pattern_normalized = pattern.replace('\\', '/')
try:
    if file_path_obj.match(pattern_normalized) or file_path_obj.match(f'**/{pattern_normalized}') or pattern_normalized in file_str:
        matche...
```

Location (filter_files:143-154):
```python
pattern_normalized = pattern.replace('\\', '/')
try:
    if file_path_obj.match(pattern_normalized) or file_path_obj.match(f'**/{pattern_normalized}') or pattern_normalized in file_str:
        matche...
```

---

## eliminate_duplication
**render_action.py** - 1 violation(s)

[X] ERROR (line 43)
Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_prepare_instructions:43-52):
```python
render_instructions = self._config_loader.load_render_instructions()
render_specs = self._render_specs
self._execute_synchronizers(render_specs)
merged_data = {'base_instructions': instructions.get('b...
```

Location (do_execute:98-108):
```python
render_instructions = self._config_loader.load_render_instructions()
render_specs = self._render_specs
self._execute_synchronizers(render_specs)
instructions = self.get_instructions(context)
merged_da...
```

---

## eliminate_duplication
**cursor_command_visitor.py** - 1 violation(s)

[X] ERROR (line 252)
Duplicate code detected: functions format_behavior_name, serialize have identical bodies - extract to shared function

---


## Cross-File Duplication Analysis
Scanning 288 changed file(s) against 20 total files...
Extracted 3755 changed blocks, 509 reference blocks
Starting 1,911,295 pairwise comparisons...
Comparing: 0% (15,105/1,911,295) - 0 violations - ETA: 1255s  
Comparing: 1% (27,349/1,911,295) - 0 violations - ETA: 1377s  
Comparing: 2% (41,602/1,911,295) - 0 violations - ETA: 1348s  
Comparing: 3% (65,019/1,911,295) - 0 violations - ETA: 1135s  
Comparing: 4% (76,688/1,911,295) - 0 violations - ETA: 1196s  
Comparing: 4% (84,371/1,911,295) - 0 violations - ETA: 1299s  
Comparing: 4% (91,089/1,911,295) - 0 violations - ETA: 1398s  
Comparing: 5% (97,379/1,911,295) - 0 violations - ETA: 1490s  
Comparing: 5% (103,164/1,911,295) - 0 violations - ETA: 1577s  
Comparing: 5% (111,093/1,911,295) - 0 violations - ETA: 1620s  
Comparing: 6% (121,194/1,911,295) - 0 violations - ETA: 1624s  
Comparing: 6% (129,655/1,911,295) - 0 violations - ETA: 1649s  
Found 10 violations so far...
Found 20 violations so far...
Found 30 violations so far...
Found 40 violations so far...
Found 50 violations so far...
Comparing: 7% (144,188/1,911,295) - 59 violations - ETA: 1593s  
Found 60 violations so far...
Found 70 violations so far...
Found 80 violations so far...
Found 90 violations so far...
Found 100 violations so far...
Found 110 violations so far...
Found 120 violations so far...
Found 130 violations so far...
Found 140 violations so far...
Comparing: 8% (164,314/1,911,295) - 142 violations - ETA: 1488s  
Comparing: 9% (182,109/1,911,295) - 142 violations - ETA: 1424s  
Found 150 violations so far...
Comparing: 10% (198,312/1,911,295) - 153 violations - ETA: 1382s  
Found 160 violations so far...
Found 170 violations so far...
Found 180 violations so far...
Found 190 violations so far...
Found 200 violations so far...
Comparing: 11% (218,956/1,911,295) - 206 violations - ETA: 1314s  
Found 210 violations so far...
Found 220 violations so far...
Found 230 violations so far...
Found 240 violations so far...
Found 250 violations so far...
Found 260 violations so far...
Found 270 violations so far...
Found 280 violations so far...
Found 290 violations so far...
Found 300 violations so far...
Found 310 violations so far...
Comparing: 12% (234,131/1,911,295) - 311 violations - ETA: 1289s  
Comparing: 13% (253,987/1,911,295) - 311 violations - ETA: 1239s  
Comparing: 14% (277,305/1,911,295) - 311 violations - ETA: 1178s  
Comparing: 15% (299,250/1,911,295) - 311 violations - ETA: 1131s  
Comparing: 16% (322,131/1,911,295) - 311 violations - ETA: 1085s  
Comparing: 17% (343,509/1,911,295) - 311 violations - ETA: 1049s  
Comparing: 19% (368,463/1,911,295) - 311 violations - ETA: 1005s  
Comparing: 20% (385,251/1,911,295) - 311 violations - ETA: 990s  
Comparing: 21% (403,927/1,911,295) - 311 violations - ETA: 970s  
Comparing: 22% (430,011/1,911,295) - 311 violations - ETA: 930s  
Comparing: 23% (447,185/1,911,295) - 311 violations - ETA: 916s  
Comparing: 24% (470,724/1,911,295) - 311 violations - ETA: 887s  
Comparing: 25% (492,062/1,911,295) - 313 violations - ETA: 865s  
Comparing: 26% (512,343/1,911,295) - 313 violations - ETA: 846s  
Comparing: 27% (531,866/1,911,295) - 313 violations - ETA: 830s  
Comparing: 28% (549,869/1,911,295) - 313 violations - ETA: 817s  
Comparing: 29% (564,503/1,911,295) - 313 violations - ETA: 811s  
Comparing: 30% (585,468/1,911,295) - 313 violations - ETA: 792s  
Comparing: 31% (607,419/1,911,295) - 313 violations - ETA: 772s  
Comparing: 33% (631,644/1,911,295) - 313 violations - ETA: 749s  
Comparing: 33% (646,257/1,911,295) - 313 violations - ETA: 743s  
Comparing: 35% (669,030/1,911,295) - 313 violations - ETA: 724s  
Comparing: 36% (692,406/1,911,295) - 313 violations - ETA: 704s  
Comparing: 37% (711,130/1,911,295) - 313 violations - ETA: 692s  
Comparing: 38% (737,193/1,911,295) - 313 violations - ETA: 668s  
Comparing: 39% (762,382/1,911,295) - 313 violations - ETA: 648s  
Comparing: 41% (789,282/1,911,295) - 313 violations - ETA: 625s  
Comparing: 42% (813,369/1,911,295) - 313 violations - ETA: 607s  
Comparing: 43% (837,037/1,911,295) - 313 violations - ETA: 590s  
Comparing: 45% (861,283/1,911,295) - 313 violations - ETA: 573s  
Comparing: 46% (884,839/1,911,295) - 313 violations - ETA: 556s  
Comparing: 47% (905,088/1,911,295) - 313 violations - ETA: 544s  
Comparing: 48% (928,135/1,911,295) - 313 violations - ETA: 529s  
Comparing: 49% (952,634/1,911,295) - 313 violations - ETA: 513s  
Comparing: 51% (976,518/1,911,295) - 313 violations - ETA: 497s  
Comparing: 52% (1,004,038/1,911,295) - 313 violations - ETA: 478s  
Comparing: 53% (1,023,261/1,911,295) - 313 violations - ETA: 468s  
Comparing: 54% (1,046,692/1,911,295) - 313 violations - ETA: 454s  
Comparing: 56% (1,072,065/1,911,295) - 313 violations - ETA: 438s  
Comparing: 57% (1,097,183/1,911,295) - 313 violations - ETA: 422s  
Comparing: 58% (1,118,636/1,911,295) - 313 violations - ETA: 411s  
Comparing: 60% (1,147,691/1,911,295) - 313 violations - ETA: 392s  
Comparing: 61% (1,175,727/1,911,295) - 313 violations - ETA: 375s  
Comparing: 62% (1,195,824/1,911,295) - 313 violations - ETA: 364s  
Comparing: 64% (1,223,299/1,911,295) - 313 violations - ETA: 348s  
Comparing: 65% (1,251,768/1,911,295) - 313 violations - ETA: 331s  
Comparing: 66% (1,277,624/1,911,295) - 313 violations - ETA: 317s  
Comparing: 68% (1,300,377/1,911,295) - 313 violations - ETA: 305s  
Comparing: 68% (1,315,689/1,911,295) - 313 violations - ETA: 298s  
Comparing: 69% (1,328,276/1,911,295) - 313 violations - ETA: 294s  
Comparing: 70% (1,346,549/1,911,295) - 313 violations - ETA: 285s  
Comparing: 71% (1,371,376/1,911,295) - 313 violations - ETA: 271s  
Comparing: 72% (1,391,977/1,911,295) - 313 violations - ETA: 261s  
Comparing: 74% (1,420,972/1,911,295) - 313 violations - ETA: 245s  
Comparing: 75% (1,447,060/1,911,295) - 313 violations - ETA: 230s  
Comparing: 77% (1,473,944/1,911,295) - 313 violations - ETA: 216s  
Comparing: 78% (1,496,598/1,911,295) - 313 violations - ETA: 205s  
Comparing: 79% (1,514,087/1,911,295) - 313 violations - ETA: 196s  
Comparing: 80% (1,537,761/1,911,295) - 313 violations - ETA: 184s  
Comparing: 81% (1,553,637/1,911,295) - 313 violations - ETA: 177s  
Comparing: 82% (1,571,475/1,911,295) - 313 violations - ETA: 168s  
Comparing: 83% (1,590,618/1,911,295) - 313 violations - ETA: 159s  
Comparing: 84% (1,608,323/1,911,295) - 313 violations - ETA: 150s  
Comparing: 85% (1,628,978/1,911,295) - 313 violations - ETA: 140s  
Comparing: 86% (1,646,224/1,911,295) - 313 violations - ETA: 132s  
Comparing: 87% (1,666,945/1,911,295) - 313 violations - ETA: 121s  
Comparing: 88% (1,688,569/1,911,295) - 313 violations - ETA: 110s  
Comparing: 89% (1,709,338/1,911,295) - 313 violations - ETA: 100s  
Comparing: 90% (1,727,328/1,911,295) - 313 violations - ETA: 91s  
Comparing: 91% (1,744,298/1,911,295) - 313 violations - ETA: 83s  
Comparing: 92% (1,773,064/1,911,295) - 313 violations - ETA: 68s  
Comparing: 93% (1,795,470/1,911,295) - 313 violations - ETA: 57s  
Comparing: 94% (1,814,719/1,911,295) - 313 violations - ETA: 47s  
Comparing: 95% (1,831,375/1,911,295) - 313 violations - ETA: 39s  
Complete: 1848128 comparisons, 313 violations

