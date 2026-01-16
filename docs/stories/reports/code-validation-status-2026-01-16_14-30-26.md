# Validation Status - code
Started: 2026-01-16 14:30:26
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
**behavior.py** - 5 violation(s)

[!] WARNING (line 85)
Line 85: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def guardrails(self):
        if self._guardrails is None:
            from ..actions.guardrails import Guardrails
            self._guardrails = Guardrails(self)
        return self._guardrails
```

[!] WARNING (line 92)
Line 92: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def content(self):
        if self._content is None:
            from ..actions.content import Content
            self._content = Content(self)
        return self._content
```

[!] WARNING (line 99)
Line 99: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def rules(self):
        if self._rules is None:
            from ..actions.rules.rules import Rules
            self._rules = Rules(behavior=self, bot_paths=self.bot_paths)
        return self._rules
```

[!] WARNING (line 106)
Line 106: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def actions(self):
        if self._actions is None:
            from ..actions.actions import Actions
            self._actions = Actions(self)
        return self._actions
```

[!] WARNING (line 113)
Line 113: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def trigger_words_obj(self):
        if self._trigger_words_obj is None:
            from ..ext.trigger_words import TriggerWords
            self._trigger_words_obj = TriggerWords(self)
        return self._trigger_words_obj
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
**behavior.py** - 5 violation(s)

[!] WARNING (line 84)
Line 84: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def guardrails(self):
        if self._guardrails is None:
            from ..actions.guardrails import Guardrails
            self._guardrails = Guardrails(self)
        return self._guardrails
```

[!] WARNING (line 91)
Line 91: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def content(self):
        if self._content is None:
            from ..actions.content import Content
            self._content = Content(self)
        return self._content
```

[!] WARNING (line 98)
Line 98: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def rules(self):
        if self._rules is None:
            from ..actions.rules.rules import Rules
            self._rules = Rules(behavior=self, bot_paths=self.bot_paths)
        return self._rules
```

[!] WARNING (line 105)
Line 105: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def actions(self):
        if self._actions is None:
            from ..actions.actions import Actions
            self._actions = Actions(self)
        return self._actions
```

[!] WARNING (line 112)
Line 112: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def trigger_words_obj(self):
        if self._trigger_words_obj is None:
            from ..ext.trigger_words import TriggerWords
            self._trigger_words_obj = TriggerWords(self)
        return self._trigger_words_obj
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
**scan_config.py** - 1 violation(s)

[!] WARNING (line 51)
Line 51: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    def code_files(self) -> List[Path]:
        """Get code files from changed_files or files."""
        if self._code_files is None:
            files_to_scan = self.changed_files if self.changed_files else self.files
            self._code_files = files_to_scan.get('src', [])
        return self._code_files
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
**story_graph_spec.py** - 2 violation(s)

[!] WARNING (line 39)
Line 39: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def story_graph(self) -> StoryGraph:
        if self._story_graph is None:
            working_dir = self._bot_paths.workspace_directory
            self._story_graph = StoryGraph(self._bot_paths, working_dir, require_file=False, story_graph_spec=self)
        return self._story_graph
```

[!] WARNING (line 61)
Line 61: None check guard clause detected. Assume variables are initialized - let code fail fast if None.

```python
    @property
    def template(self) -> Optional[StoryGraphTemplate]:
        if self._template is None:
            template_filename = self.template_filename
            if not template_filename:
                return None
            self._template = StoryGraphTemplate(self._sg_dir, template_filename)
        return self._template
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
Comparing: 0% (13,902/1,911,295) - 0 violations - ETA: 1364s  
Comparing: 1% (25,560/1,911,295) - 0 violations - ETA: 1475s  
Comparing: 1% (36,692/1,911,295) - 0 violations - ETA: 1532s  
Comparing: 3% (60,353/1,911,295) - 0 violations - ETA: 1226s  
Comparing: 3% (74,762/1,911,295) - 0 violations - ETA: 1228s  
Comparing: 4% (82,613/1,911,295) - 0 violations - ETA: 1328s  
Comparing: 4% (90,184/1,911,295) - 0 violations - ETA: 1413s  
Comparing: 5% (96,612/1,911,295) - 0 violations - ETA: 1502s  
Comparing: 5% (102,368/1,911,295) - 0 violations - ETA: 1590s  
Comparing: 5% (109,215/1,911,295) - 0 violations - ETA: 1650s  
Comparing: 6% (119,645/1,911,295) - 0 violations - ETA: 1647s  
Comparing: 6% (128,346/1,911,295) - 0 violations - ETA: 1667s  
Found 10 violations so far...
Found 20 violations so far...
Found 30 violations so far...
Found 40 violations so far...
Comparing: 7% (141,590/1,911,295) - 46 violations - ETA: 1624s  
Found 50 violations so far...
Found 60 violations so far...
Found 70 violations so far...
Found 80 violations so far...
Found 90 violations so far...
Found 100 violations so far...
Found 110 violations so far...
Found 120 violations so far...
Found 130 violations so far...
Found 140 violations so far...
Comparing: 8% (159,760/1,911,295) - 140 violations - ETA: 1535s  
Comparing: 9% (179,166/1,911,295) - 142 violations - ETA: 1450s  
Comparing: 10% (194,074/1,911,295) - 142 violations - ETA: 1415s  
Found 150 violations so far...
Found 160 violations so far...
Found 170 violations so far...
Found 180 violations so far...
Found 190 violations so far...
Found 200 violations so far...
Comparing: 11% (213,553/1,911,295) - 200 violations - ETA: 1351s  
Found 210 violations so far...
Found 220 violations so far...
Found 230 violations so far...
Found 240 violations so far...
Found 250 violations so far...
Found 260 violations so far...
Comparing: 12% (229,988/1,911,295) - 269 violations - ETA: 1315s  
Found 270 violations so far...
Found 280 violations so far...
Found 290 violations so far...
Found 300 violations so far...
Found 310 violations so far...
Comparing: 12% (247,170/1,911,295) - 311 violations - ETA: 1279s  
Comparing: 14% (269,113/1,911,295) - 311 violations - ETA: 1220s  
Comparing: 15% (290,979/1,911,295) - 311 violations - ETA: 1169s  
Comparing: 16% (308,564/1,911,295) - 311 violations - ETA: 1142s  
Comparing: 17% (328,946/1,911,295) - 311 violations - ETA: 1106s  
Comparing: 18% (351,833/1,911,295) - 311 violations - ETA: 1063s  
Comparing: 19% (372,415/1,911,295) - 311 violations - ETA: 1033s  
Comparing: 20% (388,260/1,911,295) - 311 violations - ETA: 1019s  
Comparing: 21% (405,620/1,911,295) - 311 violations - ETA: 1002s  
Comparing: 22% (431,299/1,911,295) - 311 violations - ETA: 960s  
Comparing: 23% (447,139/1,911,295) - 311 violations - ETA: 949s  
Comparing: 24% (468,955/1,911,295) - 311 violations - ETA: 922s  
Comparing: 25% (489,647/1,911,295) - 313 violations - ETA: 900s  
Comparing: 26% (509,139/1,911,295) - 313 violations - ETA: 881s  
Comparing: 27% (527,015/1,911,295) - 313 violations - ETA: 866s  
Comparing: 28% (540,109/1,911,295) - 313 violations - ETA: 863s  
Comparing: 29% (555,846/1,911,295) - 313 violations - ETA: 853s  
Comparing: 29% (572,595/1,911,295) - 313 violations - ETA: 841s  
Comparing: 30% (591,584/1,911,295) - 313 violations - ETA: 825s  
Comparing: 32% (613,157/1,911,295) - 313 violations - ETA: 804s  
Comparing: 33% (633,589/1,911,295) - 313 violations - ETA: 786s  
Comparing: 33% (646,544/1,911,295) - 313 violations - ETA: 782s  
Comparing: 34% (668,002/1,911,295) - 313 violations - ETA: 763s  
Comparing: 36% (688,524/1,911,295) - 313 violations - ETA: 745s  
Comparing: 36% (705,399/1,911,295) - 313 violations - ETA: 735s  
Comparing: 38% (726,681/1,911,295) - 313 violations - ETA: 717s  
Comparing: 39% (747,573/1,911,295) - 313 violations - ETA: 700s  
Comparing: 40% (769,179/1,911,295) - 313 violations - ETA: 683s  
Comparing: 41% (793,899/1,911,295) - 313 violations - ETA: 661s  
Comparing: 42% (816,089/1,911,295) - 313 violations - ETA: 644s  
Comparing: 43% (837,697/1,911,295) - 313 violations - ETA: 628s  
Comparing: 44% (859,505/1,911,295) - 313 violations - ETA: 611s  
Comparing: 46% (881,921/1,911,295) - 313 violations - ETA: 595s  
Comparing: 47% (898,887/1,911,295) - 313 violations - ETA: 585s  
Comparing: 47% (914,803/1,911,295) - 313 violations - ETA: 577s  
Comparing: 49% (936,586/1,911,295) - 313 violations - ETA: 562s  
Comparing: 50% (957,117/1,911,295) - 313 violations - ETA: 548s  
Comparing: 51% (976,285/1,911,295) - 313 violations - ETA: 536s  
Comparing: 52% (1,001,033/1,911,295) - 313 violations - ETA: 518s  
Comparing: 53% (1,018,635/1,911,295) - 313 violations - ETA: 508s  
Comparing: 54% (1,040,542/1,911,295) - 313 violations - ETA: 493s  
Comparing: 55% (1,060,834/1,911,295) - 313 violations - ETA: 481s  
Comparing: 56% (1,080,323/1,911,295) - 313 violations - ETA: 469s  
Comparing: 57% (1,102,414/1,911,295) - 313 violations - ETA: 454s  
Comparing: 58% (1,119,064/1,911,295) - 313 violations - ETA: 446s  
Comparing: 59% (1,142,290/1,911,295) - 313 violations - ETA: 430s  
Comparing: 61% (1,167,022/1,911,295) - 313 violations - ETA: 414s  
Comparing: 62% (1,186,383/1,911,295) - 313 violations - ETA: 403s  
Comparing: 62% (1,204,060/1,911,295) - 313 violations - ETA: 393s  
Comparing: 64% (1,226,493/1,911,295) - 313 violations - ETA: 379s  
Comparing: 65% (1,252,360/1,911,295) - 313 violations - ETA: 363s  
Comparing: 66% (1,274,150/1,911,295) - 313 violations - ETA: 350s  
Comparing: 67% (1,297,141/1,911,295) - 313 violations - ETA: 336s  
Comparing: 68% (1,312,985/1,911,295) - 313 violations - ETA: 328s  
Comparing: 69% (1,322,407/1,911,295) - 313 violations - ETA: 325s  
Comparing: 70% (1,340,843/1,911,295) - 313 violations - ETA: 314s  
Comparing: 71% (1,361,801/1,911,295) - 313 violations - ETA: 302s  
Comparing: 72% (1,379,617/1,911,295) - 313 violations - ETA: 292s  
Comparing: 73% (1,400,974/1,911,295) - 313 violations - ETA: 280s  
Comparing: 74% (1,426,890/1,911,295) - 313 violations - ETA: 264s  
Comparing: 75% (1,449,109/1,911,295) - 313 violations - ETA: 251s  
Comparing: 77% (1,473,837/1,911,295) - 313 violations - ETA: 237s  
Comparing: 78% (1,494,789/1,911,295) - 313 violations - ETA: 225s  
Comparing: 79% (1,511,945/1,911,295) - 313 violations - ETA: 216s  
Comparing: 80% (1,532,633/1,911,295) - 313 violations - ETA: 205s  
Comparing: 81% (1,549,359/1,911,295) - 313 violations - ETA: 196s  
Comparing: 81% (1,566,185/1,911,295) - 313 violations - ETA: 187s  
Comparing: 82% (1,581,770/1,911,295) - 313 violations - ETA: 179s  
Comparing: 83% (1,597,950/1,911,295) - 313 violations - ETA: 170s  
Comparing: 84% (1,613,808/1,911,295) - 313 violations - ETA: 162s  
Comparing: 85% (1,634,644/1,911,295) - 313 violations - ETA: 150s  
Comparing: 86% (1,649,937/1,911,295) - 313 violations - ETA: 142s  
Comparing: 87% (1,670,506/1,911,295) - 313 violations - ETA: 131s  
Comparing: 88% (1,693,493/1,911,295) - 313 violations - ETA: 118s  
Comparing: 89% (1,710,422/1,911,295) - 313 violations - ETA: 109s  
Comparing: 90% (1,726,711/1,911,295) - 313 violations - ETA: 100s  
Comparing: 91% (1,739,331/1,911,295) - 313 violations - ETA: 93s  
Comparing: 92% (1,764,660/1,911,295) - 313 violations - ETA: 79s  
Comparing: 93% (1,789,675/1,911,295) - 313 violations - ETA: 65s  
Comparing: 94% (1,804,504/1,911,295) - 313 violations - ETA: 58s  
Comparing: 95% (1,823,680/1,911,295) - 313 violations - ETA: 47s  
Comparing: 96% (1,835,120/1,911,295) - 313 violations - ETA: 41s  
Complete: 1848128 comparisons, 313 violations

## enforce_encapsulation
**bot_paths.py** - 1 violation(s)

[!] WARNING (line 63)
Method "update_workspace_directory" in class "BotPaths" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**bot_path.py** - 1 violation(s)

[!] WARNING (line 93)
Method "update_workspace_directory" in class "BotPath" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**cli_session.py** - 1 violation(s)

[!] WARNING (line 22)
Method "execute_command" in class "CLISession" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**ac_consolidation_scanner.py** - 1 violation(s)

[!] WARNING (line 26)
Method "_check_duplicate_ac" in class "ACConsolidationScanner" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**real_implementations_scanner.py** - 1 violation(s)

[!] WARNING (line 153)
Method "_find_src_locations" in class "RealImplementationsScanner" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**scanner_loader.py** - 1 violation(s)

[!] WARNING (line 27)
Method "_load_scanner_class" in class "ScannerLoader" has Law of Demeter violation (method chain depth 4) - encapsulate access to related objects

---

## enforce_encapsulation
**scanner_registry.py** - 1 violation(s)

[!] WARNING (line 37)
Method "loads_scanner_class_with_error" in class "ScannerRegistry" has Law of Demeter violation (method chain depth 4) - encapsulate access to related objects

---

## enforce_encapsulation
**strategy_action.py** - 1 violation(s)

[!] WARNING (line 89)
Method "_format_instructions_for_display" in class "StrategyAction" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## enforce_encapsulation
**validate_action.py** - 1 violation(s)

[!] WARNING (line 157)
Method "_format_rules_with_file_paths" in class "ValidateRulesAction" has Law of Demeter violation (method chain depth 3) - encapsulate access to related objects

---

## hide_business_logic_behind_properties
**complexity_metrics.py** - 1 violation(s)

[!] WARNING (line 182)
Function "calculate_lcom" exposes calculation timing. Use property with "get_" or no prefix instead (e.g., "total_value" not "calculate_total_value").

```python
    
    @staticmethod
    def calculate_lcom(class_node: ast.ClassDef) -> float:
    # ... (truncated)
```

---

## hide_business_logic_behind_properties
**block.py** - 1 violation(s)

[!] WARNING (line 71)
Function "calculate_complexity" exposes calculation timing. Use property with "get_" or no prefix instead (e.g., "total_value" not "calculate_total_value").

```python
        return self._code_structure_analyzer.analyzes_code_structure(self)
    
    def calculate_complexity(self, complexity_metrics) -> dict:
    # ... (truncated)
```

---

## hide_calculation_timing
**complexity_metrics.py** - 1 violation(s)

[!] WARNING (line 182)
Function "calculate_lcom" exposes calculation timing. Use property with "get_" or no prefix instead (e.g., "total_value" not "calculate_total_value").

```python
    
    @staticmethod
    def calculate_lcom(class_node: ast.ClassDef) -> float:
    # ... (truncated)
```

---

## hide_calculation_timing
**block.py** - 1 violation(s)

[!] WARNING (line 71)
Function "calculate_complexity" exposes calculation timing. Use property with "get_" or no prefix instead (e.g., "total_value" not "calculate_total_value").

```python
        return self._code_structure_analyzer.analyzes_code_structure(self)
    
    def calculate_complexity(self, complexity_metrics) -> dict:
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**action.py** - 1 violation(s)

[!] WARNING (line 23)
Class "Action" is 648 lines - should be under 300 lines (extract related methods into separate classes)

```python
logger = logging.getLogger(__name__)

class Action:
    context_class: Type[ActionContext] = ActionContext

    def __init__(self, behavior: 'Behavior', action_config: Dict[str, Any]=None, action_name: str=None):
        self.behavior = behavior
        self.action_config = action_config
        action_name = action_name or self._derive_action_name_from_class()
        self._action_name = action_name
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**bot.py** - 1 violation(s)

[!] WARNING (line 25)
Class "Bot" is 782 lines - should be under 300 lines (extract related methods into separate classes)

```python
        self.executed_instructions_from = f'{behavior}/{action}'

class Bot:
    _active_bot_instance: Optional['Bot'] = None
    _active_bot_name: Optional[str] = None

    def __init__(self, bot_name: str, bot_directory: Path, config_path: Path):
        import json; from pathlib import Path as P; log_path = P(r'c:\dev\augmented-teams\.cursor\debug.log'); log_path.parent.mkdir(parents=True, exist_ok=True); log_file = open(log_path, 'a', encoding='utf-8'); log_file.write(json.dumps({'location':'bot.py:24','message':'Bot.__init__ entry','data':{'bot_name':bot_name,'bot_directory_param':str(bot_directory),'bot_directory_name':bot_directory.name if bot_directory else None},'timestamp':__import__('time').time()*1000,'sessionId':'debug-session','hypothesisId':'H1'})+'\n'); log_file.close()
        self.name = bot_name
        self.bot_name = bot_name
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**cli_session.py** - 1 violation(s)

[!] WARNING (line 10)
Class "CLISession" is 517 lines - should be under 300 lines (extract related methods into separate classes)

```python
from agile_bot.src.cli.cli_results import CLICommandResponse

class CLISession:
    
    def __init__(self, bot, workspace_directory: Path, mode: str = None):
        self.bot = bot
        self.workspace_directory = Path(workspace_directory)
        self.mode = mode
    
    def execute_command(self, command: str) -> CLICommandResponse:
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**class_based_organization_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Class "ClassBasedOrganizationScanner" is 457 lines - should be under 300 lines (extract related methods into separate classes)

```python
from .violation import Violation

class ClassBasedOrganizationScanner(TestScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        return []
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**complexity_metrics.py** - 1 violation(s)

[!] WARNING (line 5)
Class "ComplexityMetrics" is 325 lines - should be under 300 lines (extract related methods into separate classes)

```python
import ast

class ComplexityMetrics:
    
    @staticmethod
    def cyclomatic_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 1
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**duplication_scanner.py** - 1 violation(s)

[!] WARNING (line 33)
Class "DuplicationScanner" is 2034 lines - should be under 300 lines (extract related methods into separate classes)

```python
        print(*safe_args, **kwargs)

class DuplicationScanner(CodeScanner):
    
    SCANNER_VERSION = "1.0"
    
    def _get_cache_dir(self, file_path: Optional[Path] = None) -> Path:
        if file_path:
            current = file_path.parent
            while current and current.parent != current:
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**excessive_guards_scanner.py** - 1 violation(s)

[!] WARNING (line 11)
Class "ExcessiveGuardsScanner" is 364 lines - should be under 300 lines (extract related methods into separate classes)

```python
logger = logging.getLogger(__name__)

class ExcessiveGuardsScanner(CodeScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**real_implementations_scanner.py** - 1 violation(s)

[!] WARNING (line 12)
Class "RealImplementationsScanner" is 467 lines - should be under 300 lines (extract related methods into separate classes)

```python
logger = logging.getLogger(__name__)

class RealImplementationsScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**specification_match_scanner.py** - 1 violation(s)

[!] WARNING (line 13)
Class "SpecificationMatchScanner" is 441 lines - should be under 300 lines (extract related methods into separate classes)

```python
logger = logging.getLogger(__name__)

class SpecificationMatchScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
    # ... (truncated)
```

---

## keep_classes_small_with_single_responsibility
**verb_noun_scanner.py** - 1 violation(s)

[!] WARNING (line 29)
Class "VerbNounScanner" is 498 lines - should be under 300 lines (extract related methods into separate classes)

```python
    nltk.download('wordnet', quiet=True)

class VerbNounScanner(StoryScanner):
    
    def scan_domain_concept(self, node: Any, rule_obj: Any) -> List[Dict[str, Any]]:
        return []
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        name = node.name
    # ... (truncated)
```

---

## keep_functions_small_focused
**utils.py** - 2 violation(s)

[!] WARNING (line 126)
Function "build_test_class_link" has high cyclomatic complexity (11) - should be under 10. Extract decision logic to helper functions.

```python
        return f" | [Test]({file_uri})"

def build_test_class_link(test_file: str, test_class: str, workspace_directory: Path, story_file_path: Optional[Path] = None) -> str:
    if not test_file or not test_class or test_class == '?':
        return ""
    
    try:
        from agile_bot.src.bot.workspace import get_python_workspace_root
        workspace_root = get_python_workspace_root()
        test_file_path = workspace_root / 'agile_bot' / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        line_number = find_test_class_line(test_file_path, test_class)
        
        if not line_number:
            return ""
        
        if story_file_path:
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = '/' + str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        
        rel_path = test_file_path.relative_to(workspace_root)
        rel_path_str = str(rel_path).replace('\\', '/')
        return f" | [Test]({rel_path_str}#L{line_number})"
    except (ValueError, AttributeError):
        test_file_path = workspace_directory / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        line_number = find_test_class_line(test_file_path, test_class)
        
        if not line_number:
            return ""
        
        try:
            from agile_bot.src.bot.workspace import get_python_workspace_root
            workspace_root = get_python_workspace_root()
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        except (ValueError, AttributeError):
            from agile_bot.src.actions.validate.file_link_builder import FileLinkBuilder
            link_builder = FileLinkBuilder(workspace_directory)
            file_uri = link_builder.get_file_uri(str(test_file_path), line_number)
            return f" | [Test]({file_uri})"

```

[!] WARNING (line 172)
Function "build_test_method_link" has high cyclomatic complexity (11) - should be under 10. Extract decision logic to helper functions.

```python
            return f" | [Test]({file_uri})"

def build_test_method_link(test_file: str, test_method: str, workspace_directory: Path, story_file_path: Optional[Path] = None) -> str:
    if not test_file or not test_method or test_method == '?':
        return ""
    
    try:
        from agile_bot.src.bot.workspace import get_python_workspace_root
        workspace_root = get_python_workspace_root()
        test_file_path = workspace_root / 'agile_bot' / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        line_number = find_test_method_line(test_file_path, test_method)
        
        if not line_number:
            return ""
        
        if story_file_path:
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = '/' + str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        
        rel_path = test_file_path.relative_to(workspace_root)
        rel_path_str = str(rel_path).replace('\\', '/')
        return f" | [Test]({rel_path_str}#L{line_number})"
    except (ValueError, AttributeError):
        test_file_path = workspace_directory / 'test' / test_file
        if not test_file_path.exists():
            return ""
        
        line_number = find_test_method_line(test_file_path, test_method)
        
        if not line_number:
            return ""
        
        try:
            from agile_bot.src.bot.workspace import get_python_workspace_root
            workspace_root = get_python_workspace_root()
            rel_path = test_file_path.relative_to(workspace_root)
            rel_path_str = str(rel_path).replace('\\', '/')
            return f" | [Test]({rel_path_str}#L{line_number})"
        except (ValueError, AttributeError):
            from agile_bot.src.actions.validate.file_link_builder import FileLinkBuilder
            link_builder = FileLinkBuilder(workspace_directory)
            file_uri = link_builder.get_file_uri(str(test_file_path), line_number)
            return f" | [Test]({file_uri})"

```

---

## keep_functions_small_focused
**action.py** - 1 violation(s)

[!] WARNING (line 346)
Function "get_instructions" has high cognitive complexity (16) - should be under 15. Reduce nesting and extract complex logic.

```python
        return inject_reminder_to_instructions(result, reminder)

    def get_instructions(self, context: ActionContext = None) -> Instructions:
        if context is None:
            context = self.context_class()
        
        self._save_guardrails_if_provided(context)
        
        if hasattr(context, 'scope') and context.scope:
            context.scope.apply_to_bot()
        
        instructions = self.instructions.copy()
        
        if self.action_config and 'instructions' in self.action_config:
            behavior_instructions = self.action_config.get('instructions', [])
            if behavior_instructions:
                if isinstance(behavior_instructions, list):
                    instructions._data['base_instructions'].extend(behavior_instructions)
                elif isinstance(behavior_instructions, str):
                    instructions._data['base_instructions'].append(behavior_instructions)
        
        self._load_behavior_guardrails(instructions)
        
        self._prepare_instructions(instructions, context)
        
        self._add_behavior_action_metadata(instructions)
        
        self._build_display_content(instructions)
        
        return instructions
    
```

---

## keep_functions_small_focused
**bot.py** - 1 violation(s)

[!] WARNING (line 529)
Function "save" has high cyclomatic complexity (16) - should be under 10. Extract decision logic to helper functions.

```python
            }
    
    def save(self, answers: Optional[Dict[str, str]] = None,
             evidence_provided: Optional[Dict[str, str]] = None,
             decisions: Optional[Dict[str, str]] = None,
             assumptions: Optional[List[str]] = None) -> Dict[str, Any]:
        from ..actions.clarify.requirements_clarifications import RequirementsClarifications
        from ..actions.clarify.required_context import RequiredContext
        from ..actions.strategy.strategy_decision import StrategyDecision
        from ..actions.strategy.strategy import Strategy
        
        current_behavior = self.behaviors.current
        if not current_behavior:
            return {
                'status': 'error',
                'message': 'No current behavior set'
            }
        
        try:
            saved_items = []
            
            if answers or evidence_provided:
                required_context = RequiredContext(current_behavior.folder)
                clarifications = RequirementsClarifications(
                    behavior_name=current_behavior.name,
                    bot_paths=current_behavior.bot_paths,
                    required_context=required_context,
                    key_questions_answered=answers or {},
                    evidence_provided=evidence_provided or {},
                    context=None
                )
                clarifications.save()
                if answers:
                    saved_items.append('answers')
                if evidence_provided:
                    saved_items.append('evidence')
            
            if decisions or assumptions:
                strategy = Strategy(current_behavior.folder)
                strategy_decision = StrategyDecision(
                    behavior_name=current_behavior.name,
                    bot_paths=current_behavior.bot_paths,
                    strategy=strategy,
                    decisions_made=decisions or {},
                    assumptions_made=assumptions or []
                )
                strategy_decision.save()
                if decisions:
                    saved_items.append('decisions')
                if assumptions:
    # ... (truncated)
```

---

## keep_functions_small_focused
**workspace.py** - 1 violation(s)

[i] INFO (line 20)
Function "get_base_actions_directory" has deep nesting (depth=5) - should be under 4 levels. Extract nested logic to helper functions.

```python
    return Path(workspace.strip())

def get_base_actions_directory(bot_directory: Path=None) -> Path:
    from ..utils import read_json_file
    
    if bot_directory is None:
        bot_directory = get_bot_directory()
    
    config_paths = [
        bot_directory / 'bot_config.json',
        bot_directory / 'config' / 'bot_config.json'
    ]
    
    python_workspace_root = get_python_workspace_root()
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                config = read_json_file(config_path)
                base_actions_path = config.get('baseActionsPath')
                if base_actions_path:
                    path = Path(base_actions_path)
                    if not path.is_absolute():
                        path = python_workspace_root / base_actions_path
                    return path
            except Exception:
                pass
    
    return python_workspace_root / 'agile_bot' / 'base_actions'

```

---

## keep_functions_small_focused
**adapters.py** - 1 violation(s)

[!] WARNING (line 124)
Function "serialize" has high cyclomatic complexity (11) - should be under 10. Extract decision logic to helper functions.

```python
        self.data = data
    
    def serialize(self) -> str:
        if isinstance(self.data, dict):
            if 'scope' in self.data and isinstance(self.data['scope'], dict):
                scope_data = self.data['scope']
                scope_type = scope_data.get('type', 'all')
                target = scope_data.get('target', [])
                
                if target:
                    target_str = ', '.join(str(t) for t in target)
                    return f"\x1b[1mScope:\x1b[0m {scope_type}: {target_str}"
                else:
                    return f"\x1b[1mScope:\x1b[0m {scope_type}"
            elif 'status' in self.data and 'behavior' in self.data and 'action' in self.data:
                lines = []
                lines.append(f"\x1b[1mStatus:\x1b[0m {self.data['status']}")
                lines.append(f"\x1b[1mBehavior:\x1b[0m {self.data['behavior']}")
                lines.append(f"\x1b[1mAction:\x1b[0m {self.data['action']}")
                if 'message' in self.data:
                    lines.append(f"\x1b[1mMessage:\x1b[0m {self.data['message']}")
                if 'result' in self.data:
                    lines.append(f"\x1b[1mResult:\x1b[0m {self.data['result']}")
                return '\n'.join(lines)
            else:
                lines = []
                for key, value in self.data.items():
                    lines.append(f"\x1b[1m{key}:\x1b[0m {value}")
                return '\n'.join(lines)
        import json
        return json.dumps(self.data, indent=2)
    
```

---

## keep_functions_small_focused
**cli_main.py** - 1 violation(s)

[!] WARNING (line 47)
Function "main" is 91 lines - should be under 50 lines (extract complex logic to helper functions)

```python
from agile_bot.src.cli.cli_session import CLISession

def main():
    bot_name = bot_directory.name
    workspace_directory = get_workspace_directory()
    bot_config_path = bot_directory / 'bot_config.json'
    
    if not bot_config_path.exists():
        print(f"ERROR: Bot config not found at {bot_config_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_directory,
            config_path=bot_config_path
        )
    except Exception as e:
        print(f"ERROR: Failed to initialize bot: {e}", file=sys.stderr)
        sys.exit(1)
    
    json_mode = os.environ.get('CLI_MODE', '').lower() == 'json'
    mode = 'json' if json_mode else None
    
    is_piped = not sys.stdin.isatty()
    
    if is_piped and not json_mode:
        first_line = sys.stdin.readline().strip()
        if '--format json' in first_line or '--format=json' in first_line:
            json_mode = True
            mode = 'json'
        remaining_input = sys.stdin.read()
        sys.stdin = io.StringIO(first_line + '\n' + remaining_input)
    
    cli_session = CLISession(bot=bot, workspace_directory=workspace_directory, mode=mode)
    
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
    # ... (truncated)
```

---

## keep_functions_small_focused
**cli_session.py** - 1 violation(s)

[!] WARNING (line 17)
Function "execute_command" is 222 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        self.mode = mode
    
    def execute_command(self, command: str) -> CLICommandResponse:
        verb, args = self._parse_command(command)
        
        if args and ('--format json' in args or '--format=json' in args):
            self.mode = 'json'
            args = args.replace('--format json', '').replace('--format=json', '').strip()
        
        cli_terminated = verb == 'exit'
        
        is_navigation_command = verb in ('next', 'back', 'current', 'scope', 'path', 'workspace')
        
        if verb == 'status':
            result = self.bot
        elif verb == 'bot':
            if not args:
                result = {
                    'status': 'info',
                    'current_bot': self.bot.bot_name,
                    'registered_bots': self.bot.bots,
                    'message': f"Current bot: {self.bot.bot_name}. Available bots: {', '.join(self.bot.bots)}. Usage: bot <name>"
                }
            else:
                target_bot_name = args.strip()
                try:
                    self.bot.active_bot = target_bot_name
                    self.bot = self.bot.active_bot
                    result = {
                        'status': 'success',
                        'message': f'Switched to bot: {target_bot_name}',
                        'bot_name': target_bot_name
                    }
                except ValueError as e:
                    result = {
                        'status': 'error',
                        'message': str(e)
                    }
        elif verb == 'save':
            params = self._parse_save_params(args)
            result = self.bot.save(**params)
            if self.mode == 'json':
                import json
                output = json.dumps(result, indent=2)
                return CLICommandResponse(
                    output=output,
                    status=result.get('status', 'success'),
                    cli_terminated=False
                )
        # Special case: "submitrules:behavior" calls bot.submit_behavior_rules()
    # ... (truncated)
```

---

## keep_functions_small_focused
**help.py** - 1 violation(s)

[i] INFO (line 132)
Function "__init__" has deep nesting (depth=5) - should be under 4 levels. Extract nested logic to helper functions.

```python
class Help:
    
    def __init__(self, bot=None):
        self.bot = bot
        self.commands = CommandsHelp()
        self.scope = ScopeHelp()
        
        if bot:
            behaviors_names = bot.behaviors.names if hasattr(bot, 'behaviors') else []
            actions_list = []
            if hasattr(bot, 'behaviors'):
                for behavior in bot.behaviors:
                    for action in behavior.actions:
                        if not any(a.action_name == action.action_name for a in actions_list):
                            actions_list.append(action)
            self.components = ComponentsHelp(behaviors_names, actions_list)
        else:
            self.components = ComponentsHelp()
    
```

---

## keep_functions_small_focused
**help_action.py** - 1 violation(s)

[!] WARNING (line 17)
Function "to_cli_type" has high cyclomatic complexity (15) - should be under 10. Extract decision logic to helper functions.

```python
    
    @staticmethod
    def to_cli_type(python_type) -> str:
        if python_type is type(None):
            return "none"
        
        if python_type == str:
            return "string"
        elif python_type == Path:
            return "path"
        elif python_type == int:
            return "int"
        elif python_type == float:
            return "float"
        elif python_type == bool:
            return "bool"
        elif python_type == dict:
            return "dict"
        elif python_type == list:
            return "list"
        elif python_type == tuple:
            return "tuple"
        elif python_type == set:
            return "set"
        
        origin = get_origin(python_type)
        if origin is dict:
            return "dict"
        elif origin is list:
            return "list"
        elif origin is tuple:
            return "tuple"
        elif origin is set:
            return "set"
        
        return "value"

```

---

## keep_functions_small_focused
**markdown_instructions.py** - 1 violation(s)

[!] WARNING (line 10)
Function "serialize" is 182 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        scope = self.instructions.scope
        if scope and (scope.value or scope.type.value == 'showAll'):
            from agile_bot.src.cli.adapters import MarkdownAdapter
            
            output_lines.append("## Scope")
            output_lines.append("")
            if scope.type.value == 'story':
                output_lines.append(f"**Story Scope:** {', '.join(scope.value)}")
            elif scope.type.value == 'files':
                output_lines.append(f"**File Scope:** {', '.join(scope.value)}")
            elif scope.type.value == 'showAll':
                output_lines.append("**Scope:** Show All (entire story graph)")
            else:
                output_lines.append(f"**Scope:** {scope.type.value} - {', '.join(scope.value) if scope.value else 'all'}")
            output_lines.append("")
            
            results = scope.results
            if results:
                from agile_bot.src.cli.adapter_factory import AdapterFactory
                try:
                    adapter = AdapterFactory.create(results, 'markdown')
                    scope_content = adapter.serialize()
                    output_lines.append(scope_content)
                except Exception:
                    pass
            
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
        
        behavior_metadata = instructions_dict.get('behavior_metadata', {})
        if behavior_metadata:
            behavior_name = behavior_metadata.get('name', 'unknown')
            output_lines.append(f"# Behavior: {behavior_name}")
            output_lines.append("")
            output_lines.append(f"## Behavior Instructions - {behavior_name}")
            output_lines.append("")
            
            behavior_description = behavior_metadata.get('description', '')
            if behavior_description:
                output_lines.append(f"The purpose of this behavior is to {behavior_description.lower()}")
                output_lines.append("")
            
            behavior_instructions = behavior_metadata.get('instructions', [])
    # ... (truncated)
```

---

## keep_functions_small_focused
**tty_instructions.py** - 1 violation(s)

[!] WARNING (line 10)
Function "serialize" is 152 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        behavior_metadata = instructions_dict.get('behavior_metadata', {})
        if behavior_metadata:
            behavior_name = behavior_metadata.get('name', 'unknown')
            output_lines.append(f"{self.add_bold(f'Behavior Instructions - {behavior_name}')}")
            
            behavior_description = behavior_metadata.get('description', '')
            if behavior_description:
                output_lines.append(f"The purpose of this behavior is to {behavior_description.lower()}")
                output_lines.append("")
            
            behavior_instructions = behavior_metadata.get('instructions', [])
            if behavior_instructions:
                if isinstance(behavior_instructions, list):
                    output_lines.extend(behavior_instructions)
                elif isinstance(behavior_instructions, str):
                    output_lines.append(behavior_instructions)
                output_lines.append("")
        
        action_metadata = instructions_dict.get('action_metadata', {})
        if action_metadata:
            action_name = action_metadata.get('name', 'unknown')
            output_lines.append(f"{self.add_bold(f'Action Instructions - {action_name}')}")
            
            action_description = action_metadata.get('description', '')
            if action_description:
                output_lines.append(f"The purpose of this action is to {action_description.lower()}")
                output_lines.append("")
            
            action_instructions = action_metadata.get('instructions', [])
            if action_instructions:
                output_lines.extend(action_instructions)
                output_lines.append("")
        
        output_lines.append("---")
        output_lines.append("")
        
        base_instructions = instructions_dict.get('base_instructions', [])
        output_lines.extend(base_instructions)
        
        clarification_data = instructions_dict.get('clarification', {})
        guardrails_dict = instructions_dict.get('guardrails', {})
        
        saved_answers = {}
        saved_evidence_provided = {}
    # ... (truncated)
```

---

## keep_functions_small_focused
**rules.py** - 1 violation(s)

[!] WARNING (line 123)
Function "from_parameters" has high cyclomatic complexity (15) - should be under 10. Extract decision logic to helper functions.

```python
    
    @classmethod
    def from_parameters(cls, parameters: Dict[str, Any], behavior, bot_paths, callbacks: Optional[ValidationCallbacks] = None) -> 'ValidationContext':
        from agile_bot.src.actions.action_context import ValidateActionContext, Scope, ScopeType, FileFilter
        from agile_bot.src.bot.behavior import Behavior
        
        if isinstance(behavior, str):
            behavior = Behavior(name=behavior, bot_paths=bot_paths)
        
        scope = None
        if 'scope' in parameters and parameters['scope']:
            scope_dict = parameters['scope']
            if isinstance(scope_dict, dict):
                scope_type_str = scope_dict.get('type', 'all')
                scope_type = ScopeType(scope_type_str)
                scope = Scope(
                    type=scope_type,
                    value=scope_dict.get('value', []),
                    exclude=scope_dict.get('exclude', []),
                    skiprule=scope_dict.get('skiprule', [])
                )
        elif 'test' in parameters or 'src' in parameters:
            file_paths = []
            if 'test' in parameters:
                test_files = parameters['test']
                if isinstance(test_files, str):
                    file_paths.append(test_files)
                elif isinstance(test_files, list):
                    file_paths.extend(test_files)
            if 'src' in parameters:
                src_files = parameters['src']
                if isinstance(src_files, str):
                    file_paths.append(src_files)
                elif isinstance(src_files, list):
                    file_paths.extend(src_files)
            
            if file_paths:
                scope = Scope(
                    type=ScopeType.FILES,
                    value=file_paths,
                    exclude=[],
                    skiprule=[]
                )
        
        all_files = parameters.get('all_files', False) or parameters.get('force_full', False)
        
        context = ValidateActionContext(
            scope=scope,
            background=parameters.get('background'),
            skip_cross_file=parameters.get('skip_cross_file', False),
    # ... (truncated)
```

---

## keep_functions_small_focused
**background_common_setup_scanner.py** - 1 violation(s)

[!] WARNING (line 9)
Function "scan_story_node" has high cognitive complexity (17) - should be under 15. Reduce nesting and extract complex logic.

```python
class BackgroundCommonSetupScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            background = story_data.get('background', [])
            
            if background:
                violation = self._check_background_has_when_then(background, node, rule_obj)
                if violation:
                    violations.append(violation)
                
                violation = self._check_background_scenario_specific(background, scenarios, node, rule_obj)
                if violation:
                    violations.append(violation)
            
            if len(scenarios) >= 3 and not background:
                violation = self._check_missing_background(scenarios, node, rule_obj)
                if violation:
                    violations.append(violation)
        
        return violations
    
```

---

## keep_functions_small_focused
**class_based_organization_scanner.py** - 1 violation(s)

[!] WARNING (line 15)
Function "scan_file" has high cyclomatic complexity (12) - should be under 10. Extract decision logic to helper functions.

```python
        return []
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        if not file_path.exists():
            return violations
        
        sub_epic_names = self._extract_sub_epic_names(story_graph)
        file_name = file_path.stem
        violation = self._check_file_name_matches_sub_epic(file_name, sub_epic_names, file_path, rule_obj, story_graph)
        if violation:
            violations.append(violation)
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        story_names = self._extract_story_names(story_graph)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if node.name.startswith('Test'):
                    violation = self._check_class_name_matches_story(node.name, story_names, file_path, rule_obj)
                    if violation:
                        violations.append(violation)
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if item.name.startswith('test_'):
                                violation = self._check_method_name_matches_scenario(
                                    item.name, node.name, story_names, story_graph, file_path, rule_obj
                                )
                                if violation:
                                    violations.append(violation)
        
        return violations
    
```

---

## keep_functions_small_focused
**complexity_metrics.py** - 4 violation(s)

[!] WARNING (line 22)
Function "cognitive_complexity" has high cognitive complexity (25) - should be under 15. Reduce nesting and extract complex logic.

```python
    
    @staticmethod
    def cognitive_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 0
        nesting_level = 0
        
        def visit_node(node: ast.AST, level: int):
            nonlocal complexity
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.With):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
            elif isinstance(node, ast.Assert):
                complexity += 1 + level
            else:
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
        
        for stmt in func_node.body:
            visit_node(stmt, 0)
        
        return complexity
    
```

[!] WARNING (line 78)
Function "detect_responsibilities_with_examples" has high cyclomatic complexity (14) - should be under 10. Extract decision logic to helper functions.

```python
    
    @staticmethod
    def detect_responsibilities_with_examples(func_node: ast.FunctionDef) -> Dict[str, List[Dict[str, Any]]]:
        responsibilities: Dict[str, List[Dict[str, Any]]] = {}
        
        def add_example(resp_type: str, node: ast.AST):
            if resp_type not in responsibilities:
                responsibilities[resp_type] = []
            if len(responsibilities[resp_type]) < 2:
                line = getattr(node, 'lineno', None)
                try:
                    code = ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
                    if len(code) > 80:
                        code = code[:77] + '...'
                except:
                    code = '<code unavailable>'
                responsibilities[resp_type].append({'line': line, 'code': code})
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                func_name = ComplexityMetrics._get_call_name(node)
                if func_name and ComplexityMetrics._is_io_operation(func_name, node):
                    add_example('I/O', node)
            
            if isinstance(node, ast.Assert):
                add_example('Validation', node)
            
            if isinstance(node, ast.Assign):
                if ComplexityMetrics._has_transformation(node):
                    add_example('Transformation', node)
            
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv)):
                    add_example('Computation', node)
        
        return responsibilities
    
```

[!] WARNING (line 297)
Function "detect_class_responsibilities_with_examples" has high cognitive complexity (26) - should be under 15. Reduce nesting and extract complex logic.

```python
    
    @staticmethod
    def detect_class_responsibilities_with_examples(class_node: ast.ClassDef) -> Dict[str, List[Dict[str, Any]]]:
        methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
        
        if len(methods) == 0:
            return {}
        
        responsibility_groups: Dict[str, List[Dict[str, Any]]] = {}
        
        for method in methods:
            responsibilities_detailed = ComplexityMetrics.detect_responsibilities_with_examples(method)
            if not responsibilities_detailed:
                if 'General' not in responsibility_groups:
                    responsibility_groups['General'] = []
                if len(responsibility_groups['General']) < 2:
                    code_sample = ComplexityMetrics._get_method_code_sample(method)
                    responsibility_groups['General'].append({
                        'method': method.name,
                        'line': method.lineno,
                        'code': code_sample
                    })
            else:
                for resp_type, examples in responsibilities_detailed.items():
                    if resp_type not in responsibility_groups:
                        responsibility_groups[resp_type] = []
                    if len(responsibility_groups[resp_type]) < 2 and examples:
                        first_example = examples[0]
                        responsibility_groups[resp_type].append({
                            'method': method.name,
                            'line': first_example.get('line'),
                            'code': first_example.get('code', '')
                        })
        
        return responsibility_groups

```

[!] WARNING (line 26)
Function "visit_node" has high cognitive complexity (24) - should be under 15. Reduce nesting and extract complex logic.

```python
        nesting_level = 0
        
        def visit_node(node: ast.AST, level: int):
            nonlocal complexity
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.With):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
            elif isinstance(node, ast.Assert):
                complexity += 1 + level
            else:
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level)
        
```

---

## keep_functions_small_focused
**cover_all_paths_scanner.py** - 1 violation(s)

[!] WARNING (line 11)
Function "scan_file" has high cyclomatic complexity (11) - should be under 10. Extract decision logic to helper functions.

```python
class CoverAllPathsScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        functions = Functions(tree)
        test_methods = [function.node for function in functions.get_many_functions if function.node.name.startswith('test_')]
        
        for test_method in test_methods:
            found_code_node = None
            for stmt in test_method.body:
                if isinstance(stmt, ast.Pass):
                    continue
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Constant, ast.Str)):
                    continue
                else:
                    for node in ast.walk(stmt):
                        if isinstance(node, (ast.Call, ast.Assign, ast.Assert, ast.Return, ast.Raise)):
                            found_code_node = node
                            break
                    if found_code_node is not None:
                        break
            
            if found_code_node is None:
                violations.append(Violation(
                    rule=rule_obj,
                    violation_message=f'Test method "{test_method.name}" has no actual test code - tests must exercise behavior paths, not just contain pass statements',
                    location=str(file_path),
                    line_number=test_method.lineno,
                    severity='error'
                ).to_dict())
        
        return violations

```

---

## keep_functions_small_focused
**dead_code_scanner.py** - 1 violation(s)

[!] WARNING (line 13)
Function "scan" is 52 lines - should be under 50 lines (extract complex logic to helper functions)

```python
class DeadCodeScanner(CodeScanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        violations = []
        
        all_files = []
        if code_files:
            all_files.extend(code_files)
        if test_files:
            all_files.extend(test_files)
        
        if not all_files:
            return violations
        
        definitions = {}
        usages = set()
        
        for file_path in all_files:
            if not file_path.exists() or not file_path.is_file():
                continue
            
            try:
                file_defs, file_usages = self._analyze_file(file_path)
                
                for name, (line_num, node_type) in file_defs.items():
                    qualified_name = f"{file_path.stem}.{name}"
                    definitions[qualified_name] = (file_path, line_num, node_type, name)
                    if name not in definitions:
                        definitions[name] = (file_path, line_num, node_type, name)
                
                usages.update(file_usages)
                
            except Exception as e:
                logger.debug(f"Error analyzing {file_path}: {e}")
                continue
        
        for qualified_name, (file_path, line_num, node_type, simple_name) in definitions.items():
            if '.' in qualified_name and simple_name in usages:
                continue
            
            if self._is_test_file(file_path):
                continue
            
    # ... (truncated)
```

---

## keep_functions_small_focused
**dependency_chaining_scanner.py** - 1 violation(s)

[!] WARNING (line 9)
Function "scan_domain_concept" has high cognitive complexity (26) - should be under 15. Reduce nesting and extract complex logic.

```python
class DependencyChainingScanner(DomainScanner):
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        has_instantiation = False
        instantiation_collaborators = []
        
        for i, responsibility_data in enumerate(node.responsibilities):
            responsibility_name = responsibility_data.get('name', '')
            resp_lower = responsibility_name.lower()
            
            if 'instantiated with' in resp_lower:
                has_instantiation = True
                collaborators = responsibility_data.get('collaborators', [])
                instantiation_collaborators = [c.strip() for c in collaborators]
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
        
        return violations
    
```

---

## keep_functions_small_focused
**domain_language_scanner.py** - 1 violation(s)

[!] WARNING (line 23)
Function "scan_domain_concept" has high cyclomatic complexity (11) - should be under 10. Extract decision logic to helper functions.

```python
    ]
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        node_name_lower = node.name.lower()
        for term in ['data', 'config', 'parameter', 'result']:
            if term in node_name_lower and not self._is_domain_specific(node.name):
                violations.append(
                    Violation(
                        rule=rule_obj,
                        violation_message=f'Domain concept "{node.name}" uses generic term "{term}". Use domain-specific language instead (e.g., "PortfolioData" → "Portfolio", "TargetConfig" → "TargetAllocation").',
                        location=node.map_location('name'),
                        line_number=None,
                        severity='warning'
                    ).to_dict()
                )
        
        for i, responsibility_data in enumerate(node.responsibilities):
            responsibility_name = responsibility_data.get('name', '')
            collaborators = responsibility_data.get('collaborators', [])
            resp_lower = responsibility_name.lower()
            
            for collab in collaborators:
                collab_lower = collab.lower()
                for term in self.GENERIC_TERMS:
                    if term in collab_lower and not self._is_domain_specific(collab):
                        violations.append(
                            Violation(
                                rule=rule_obj,
                                violation_message=f'Responsibility "{responsibility_name}" uses generic collaborator "{collab}". Use domain-specific language instead.',
                                location=node.map_location(f'responsibilities[{i}].collaborators'),
                                line_number=None,
                                severity='warning'
                            ).to_dict()
                        )
                        break
            
            for pattern in self.GENERATE_PATTERNS:
                if re.search(pattern, resp_lower):
                    violations.append(
                        Violation(
                            rule=rule_obj,
                            violation_message=f'Responsibility "{responsibility_name}" uses generate/calculate. Use property instead (e.g., "Get recommended trades" not "Generate recommendation").',
                            location=node.map_location(f'responsibilities[{i}].name'),
                            line_number=None,
                            severity='warning'
                        ).to_dict()
                    )
                    break
    # ... (truncated)
```

---

## keep_functions_small_focused
**duplication_scanner.py** - 3 violation(s)

[!] WARNING (line 105)
Function "scan_file" is 57 lines - should be under 50 lines (extract complex logic to helper functions)

```python
            logger.debug(f"Cache write failed for {file_path}: {e}")
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        _safe_print(f"[DuplicationScanner.scan_code_file] Called for: {file_path}")
        
        if not file_path.exists():
            _safe_print(f"[DuplicationScanner.scan_code_file] File does not exist: {file_path}")
            return violations
        
        file_start_time = datetime.now()
        
        try:
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                _safe_print(f"Skipping large file ({file_size/1024:.1f}KB): {file_path}")
                return violations
        except Exception as e:
            _safe_print(f"Could not check file size for {file_path}: {e}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            lines = content.split('\n')
            
            functions = []
            
            def extract_functions_from_node(node: ast.AST, parent_class: str = None):
                if isinstance(node, ast.ClassDef):
                    for child in node.body:
                        extract_functions_from_node(child, node.name)
                elif isinstance(node, ast.FunctionDef):
                    func_body = ast.unparse(node.body) if hasattr(ast, 'unparse') else str(node.body)
                    functions.append((node.name, func_body, node.lineno, node, parent_class))
            
            for node in tree.body:
                extract_functions_from_node(node, None)
            
            func_violations = self._check_duplicate_functions(functions, file_path, rule_obj, lines)
            violations.extend(func_violations)
            
            elapsed = (datetime.now() - file_start_time).total_seconds()
            if elapsed > FILE_SCAN_TIMEOUT:
                _safe_print(f"TIMEOUT: File scan exceeded {FILE_SCAN_TIMEOUT}s: {file_path} (stopping early)")
                return violations
            
            block_violations = self._check_duplicate_code_blocks(functions, lines, file_path, rule_obj)
            violations.extend(block_violations)
            
    # ... (truncated)
```

[!] WARNING (line 1788)
Function "scan_cross_file" is 231 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        return nearby_files
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: int = 20
    ) -> List[Dict[str, Any]]:
        violations = []
        
        if all_test_files is None:
            all_test_files = test_files
        if all_code_files is None:
            all_code_files = code_files
        
        changed_files = []
        if code_files:
            changed_files.extend(code_files)
        if test_files:
            changed_files.extend(test_files)
        
        all_files = []
        if all_code_files:
            all_files.extend(all_code_files)
        if all_test_files:
            all_files.extend(all_test_files)
        
        if not changed_files or not all_files:
            return violations
        
        all_files = self._filter_files_by_package_proximity(changed_files, all_files, max_files=max_cross_file_comparisons)
        
        if len(changed_files) < len(all_files):
            _safe_print(f"\n[CROSS-FILE] Incremental scan: Checking {len(changed_files)} changed file(s) against {len(all_files)} total files...")
        else:
            _safe_print(f"\n[CROSS-FILE] Full scan: Scanning {len(all_files)} files for cross-file duplication...")
        import sys
        
        def write_status(msg: str):
            if status_writer and hasattr(status_writer, 'write_cross_file_progress'):
                try:
                    status_writer.write_cross_file_progress(msg)
                except Exception as e:
                    logger.debug(f'Could not write to status file: {type(e).__name__}: {e}')
        
        write_status(f"\n## Cross-File Duplication Analysis")
    # ... (truncated)
```

[!] WARNING (line 696)
Function "extract_from_node" has high cyclomatic complexity (18) - should be under 10. Extract decision logic to helper functions.

```python
                             ast.AsyncFor, ast.AsyncWith)
        
        def extract_from_node(node):
            if isinstance(node, control_structures):
                num_nodes = len(list(ast.walk(node)))
                if min_nodes <= num_nodes <= max_nodes:
                    subtrees.append(node)
            
            if hasattr(node, 'body') and isinstance(node.body, list):
                for child in node.body:
                    extract_from_node(child)
            
            if hasattr(node, 'orelse') and isinstance(node.orelse, list):
                for child in node.orelse:
                    extract_from_node(child)
            
            if hasattr(node, 'handlers') and isinstance(node.handlers, list):
                for handler in node.handlers:
                    if hasattr(handler, 'body') and isinstance(handler.body, list):
                        for child in handler.body:
                            extract_from_node(child)
            
            if hasattr(node, 'finalbody') and isinstance(node.finalbody, list):
                for child in node.finalbody:
                    extract_from_node(child)
        
```

---

## keep_functions_small_focused
**function_size_scanner.py** - 1 violation(s)

[!] WARNING (line 138)
Function "visit_statement" has high cyclomatic complexity (33) - should be under 10. Extract decision logic to helper functions.

```python
        multi_line_lines = set()
        
        def visit_statement(stmt_node):
            if hasattr(stmt_node, 'end_lineno') and hasattr(stmt_node, 'lineno') and stmt_node.end_lineno and stmt_node.lineno:
                if stmt_node.end_lineno > stmt_node.lineno:
                    if isinstance(stmt_node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                        if hasattr(stmt_node, 'value') and stmt_node.value:
                            value = stmt_node.value
                            if hasattr(value, 'end_lineno') and hasattr(value, 'lineno') and value.end_lineno and value.lineno:
                                if value.end_lineno > value.lineno:
                                    for line_num in range(value.lineno + 1, value.end_lineno + 1):
                                        multi_line_lines.add(line_num)
                    
                    elif isinstance(stmt_node, ast.Expr):
                        if hasattr(stmt_node, 'value') and stmt_node.value:
                            value = stmt_node.value
                            if isinstance(value, ast.Call):
                                if hasattr(value, 'end_lineno') and hasattr(value, 'lineno') and value.end_lineno and value.lineno:
                                    if value.end_lineno > value.lineno:
                                        for line_num in range(value.lineno + 1, value.end_lineno + 1):
                                            multi_line_lines.add(line_num)
                    
                    elif isinstance(stmt_node, ast.Return):
                        if stmt_node.value:
                            if hasattr(stmt_node.value, 'end_lineno') and hasattr(stmt_node.value, 'lineno') and stmt_node.value.end_lineno and stmt_node.value.lineno:
                                if stmt_node.value.end_lineno > stmt_node.value.lineno:
                                    for line_num in range(stmt_node.value.lineno + 1, stmt_node.value.end_lineno + 1):
                                        multi_line_lines.add(line_num)
        
```

---

## keep_functions_small_focused
**given_precondition_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has high cognitive complexity (20) - should be under 15. Reduce nesting and extract complex logic.

```python
class GivenPreconditionScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_steps = self._get_scenario_steps(scenario)
                
                for step_idx, step in enumerate(scenario_steps):
                    if step.startswith('Given') or step.startswith('And'):
                        violation = self._check_given_is_functionality(step, node, scenario_idx, step_idx, rule_obj)
                        if violation:
                            violations.append(violation)
        
        return violations
    
```

---

## keep_functions_small_focused
**given_state_not_actions_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has high cognitive complexity (20) - should be under 15. Reduce nesting and extract complex logic.

```python
class GivenStateNotActionsScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_steps = self._get_scenario_steps(scenario)
                
                for step_idx, step in enumerate(scenario_steps):
                    if step.startswith('Given') or step.startswith('And'):
                        violation = self._check_given_is_action(step, node, scenario_idx, step_idx, rule_obj)
                        if violation:
                            violations.append(violation)
        
        return violations
    
```

---

## keep_functions_small_focused
**implementation_details_scanner.py** - 1 violation(s)

[!] WARNING (line 17)
Function "scan_story_node" has high cognitive complexity (18) - should be under 15. Reduce nesting and extract complex logic.

```python
    ]
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if not isinstance(node, Story):
            return violations
        
        if not hasattr(node, 'name') or not node.name:
            return violations
        
        name_lower = node.name.lower()
        
        for verb in self.IMPLEMENTATION_VERBS:
            pattern = rf'\b{verb}\b'
            if re.search(pattern, name_lower):
                words = name_lower.split()
                if verb in words[0] or (len(words) > 1 and verb in words[0:2]):
                    violation = Violation(
                        rule=rule_obj,
                        violation_message=f'Story "{node.name}" appears to be an implementation operation - should be a step within a story that describes user/system outcome',
                        location=node.name,
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
                    break
        
        return violations

```

---

## keep_functions_small_focused
**intention_revealing_names_scanner.py** - 1 violation(s)

[!] WARNING (line 254)
Function "visit_node" has high cognitive complexity (23) - should be under 15. Reduce nesting and extract complex logic.

```python
        docstring_ranges = []
        
        def visit_node(node):
            if hasattr(node, 'body') and isinstance(node.body, list) and len(node.body) > 0:
                first_stmt = node.body[0]
                if isinstance(first_stmt, ast.Expr):
                    if isinstance(first_stmt.value, (ast.Constant, ast.Str)):
                        if isinstance(first_stmt.value, ast.Constant):
                            docstring_value = first_stmt.value.value
                        else:
                            docstring_value = first_stmt.value.s
                        
                        if isinstance(docstring_value, str):
                            start_line = first_stmt.lineno if hasattr(first_stmt, 'lineno') else None
                            if start_line:
                                docstring_lines = docstring_value.count('\n')
                                end_line = start_line + docstring_lines + 2
                                docstring_ranges.append((start_line, end_line))
            
            for child in ast.iter_child_nodes(node):
                visit_node(child)
        
```

---

## keep_functions_small_focused
**object_oriented_helpers_scanner.py** - 1 violation(s)

[!] WARNING (line 15)
Function "scan_file" has high cognitive complexity (25) - should be under 15. Reduce nesting and extract complex logic.

```python
    HELPER_CALL_THRESHOLD = 2

    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations

        content, lines, tree = parsed

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test"):
                helper_used = self._uses_helper(node)
                param_count = self._count_params(node)
                parametrize_cols = self._parametrize_column_count(node)
                gwt_calls = self._given_when_then_calls(node)

                if (param_count >= self.PARAM_THRESHOLD or parametrize_cols >= self.PARAMETRIZE_THRESHOLD) and not helper_used:
                    message = (
                        f'Test "{node.name}" has many parameters ({max(param_count, parametrize_cols)}) '
                        f"but no helper/factory usage - consolidate with BotTestHelper or shared helper object."
                    )
                    violations.append(
                        Violation(
                            rule=rule_obj,
                            violation_message=message,
                            line_number=node.lineno,
                            location=str(file_path),
                            severity="warning",
                        ).to_dict()
                    )

                if gwt_calls >= self.HELPER_CALL_THRESHOLD and not helper_used:
                    message = (
                        f'Test "{node.name}" uses {gwt_calls} given/when/then helpers but no shared helper object; '
                        f"consolidate into BotTestHelper-style fixtures with standard data."
                    )
                    violations.append(
                        Violation(
                            rule=rule_obj,
                            violation_message=message,
                            line_number=node.lineno,
                            location=str(file_path),
                            severity="warning",
                        ).to_dict()
                    )

        return violations

```

---

## keep_functions_small_focused
**parameterized_tests_scanner.py** - 1 violation(s)

[!] WARNING (line 8)
Function "scan" has high cognitive complexity (22) - should be under 15. Reduce nesting and extract complex logic.

```python
class ParameterizedTestsScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List['Path']] = None,
        code_files: Optional[List['Path']] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for ParameterizedTestsScanner")
        
        violations = []
        story_map = StoryMap(story_graph)
        
        for epic in story_map.epics():
            for node in story_map.walk(epic):
                if isinstance(node, Story):
                    for scenario_outline in node.scenario_outlines:
                        if scenario_outline.examples_rows and len(scenario_outline.examples_rows) > 1:
                            location = scenario_outline.map_location()
                            violations.append(Violation(
                                rule=rule_obj,
                                violation_message=f"Scenario outline '{scenario_outline.name}' has {len(scenario_outline.examples_rows)} examples but may not use @pytest.mark.parametrize",
                                location=location,
                                severity='warning'
                            ).to_dict())
        
        return violations

```

---

## keep_functions_small_focused
**prefer_object_model_over_config_scanner.py** - 1 violation(s)

[!] WARNING (line 30)
Function "scan_file" has high cyclomatic complexity (13) - should be under 10. Extract decision logic to helper functions.

```python
        ]
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Dict[str, Any] = None) -> List[Violation]:
        violations = []
        
        # Use injected rule_obj if provided, otherwise fall back to self.rule_obj
        effective_rule = rule_obj if rule_obj is not None else self.rule_obj
        if not effective_rule:
            return violations
        
        self.current_file_path = file_path
        
        if not file_path.exists():
            return violations
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return violations
        
        lines = content.split('\n')
        
        if self._is_exception_file(file_path):
            return violations
        
        for line_num, line in enumerate(lines, start=1):
            if '# scanner ignore' in line or '# noqa' in line:
                continue
            
            if self._is_in_exception_context(lines, line_num):
                continue
            
            for pattern, description in self.config_access_patterns:
                if re.search(pattern, line):
                    violations.append(self._create_violation(
                        line_num,
                        f"{description}. Use object properties instead of accessing _config directly.",
                        effective_rule
                    ))
            
            if re.search(self.config_file_pattern, line):
                if self._looks_like_object_exists_context(lines, line_num):
                    violations.append(self._create_violation(
                        line_num,
                        "Reading config file directly when object model may exist. Use object properties instead.",
                        effective_rule
                    ))
        
        return violations
    
```

---

## keep_functions_small_focused
**resource_oriented_code_scanner.py** - 1 violation(s)

[!] WARNING (line 59)
Function "scan_cross_file" is 53 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        return []
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        violations = []
        
        all_files = []
        if code_files:
            all_files.extend(code_files)
        if test_files:
            all_files.extend(test_files)
        
        if not all_files:
            return violations
        
        loader_classes = {}
        all_classes = {}
        
        for file_path in all_files:
            if not file_path.exists():
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                
                classes = Classes(tree)
                for cls in classes.get_many_classes:
                    all_classes[(file_path, cls.node.name)] = cls.node
                    
                    is_agent, base_verb, suffix = VocabularyHelper.is_agent_noun(cls.node.name)
                    if is_agent:
                        loader_classes[cls.node.name] = (file_path, cls.node, suffix)
            except (SyntaxError, UnicodeDecodeError) as e:
                logger.debug(f'Skipping file {file_path} due to {type(e).__name__}: {e}')
                continue
        
        for loader_class_name, (loader_file, loader_node, suffix) in loader_classes.items():
            # Skip if it's a legitimate agent noun (domain entity, pattern, or service)
            if loader_class_name in self.LEGITIMATE_AGENT_NOUNS:
                continue
            
    # ... (truncated)
```

---

## keep_functions_small_focused
**scanner_registry.py** - 1 violation(s)

[!] WARNING (line 30)
Function "loads_scanner_class_with_error" has high cognitive complexity (19) - should be under 15. Reduce nesting and extract complex logic.

```python
        return scanner_class
    
    def loads_scanner_class_with_error(self, scanner_module_path: str) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        if not scanner_module_path:
            return None, None
        
        try:
            module_path, class_name = scanner_module_path.rsplit('.', 1)
            
            scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
            
            paths_to_try = [
                module_path,
                f'agile_bot.src.scanners.{scanner_name}_scanner'
            ]
            
            if self._bot_name:
                paths_to_try.append(f'agile_bot.bots.{self._bot_name}.src.scanners.{scanner_name}_scanner')
            
            for path in paths_to_try:
                try:
                    module = importlib.import_module(path)
                    if hasattr(module, class_name):
                        scanner_class = getattr(module, class_name)
                        
                        if isinstance(scanner_class, type) and hasattr(scanner_class, 'scan'):
                            if issubclass(scanner_class, Scanner):
                                return scanner_class, None
                except (ImportError, AttributeError):
                    continue
            
            return None, f"Scanner class not found: {scanner_module_path}"
        except Exception as e:
            return None, f"Error loading scanner {scanner_module_path}: {e}"

```

---

## keep_functions_small_focused
**scanner_status_formatter.py** - 1 violation(s)

[i] INFO (line 26)
Function "categorize_scanner_rules" has deep nesting (depth=5) - should be under 4 levels. Extract nested logic to helper functions.

```python
        return lines

    def categorize_scanner_rules(self, validation_rules: List[Dict[str, Any]]) -> Dict:
        executed_rules = []
        load_failed_rules = []
        execution_failed_rules = []
        no_scanner_rules = []
        for rule_dict in validation_rules:
            category = self._get_rule_category(rule_dict)
            if category == 'executed':
                executed_rules.append(self._build_executed_rule_entry(rule_dict))
            elif category == 'load_failed':
                load_failed_rules.append(self._build_failed_rule_entry(rule_dict))
            elif category == 'execution_failed':
                execution_failed_rules.append(self._build_failed_rule_entry(rule_dict))
            elif category == 'no_scanner':
                no_scanner_rules.append(self._get_rule_file(rule_dict))
        return {'executed': executed_rules, 'load_failed': load_failed_rules, 'execution_failed': execution_failed_rules, 'no_scanner': no_scanner_rules}

```

---

## keep_functions_small_focused
**scenarios_cover_all_cases_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has high cyclomatic complexity (12) - should be under 10. Extract decision logic to helper functions.

```python
class ScenariosCoverAllCasesScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            if len(scenarios) > 0:
                has_happy_path = False
                has_edge_case = False
                has_error_case = False
                
                for scenario_idx, scenario in enumerate(scenarios):
                    scenario_text = self._get_scenario_text(scenario)
                    
                    if self._is_happy_path(scenario_text):
                        has_happy_path = True
                    if self._is_edge_case(scenario_text):
                        has_edge_case = True
                    if self._is_error_case(scenario_text):
                        has_error_case = True
                
                if not has_happy_path:
                    violation = Violation(
                        rule=rule_obj,
                        violation_message='Story has no happy path scenario - add a scenario covering the normal success case',
                        location=node.map_location(),
                        severity='error'
                    ).to_dict()
                    violations.append(violation)
                
                if not has_edge_case and len(scenarios) > 1:
                    violation = Violation(
                        rule=rule_obj,
                        violation_message='Story has no edge case scenario - add scenarios covering boundary values and edge conditions',
                        location=node.map_location(),
                        severity='warning'
                    ).to_dict()
                    violations.append(violation)
                
                if not has_error_case and len(scenarios) > 1:
                    violation = Violation(
                        rule=rule_obj,
                        violation_message='Story has no error case scenario - add scenarios covering invalid inputs and error conditions',
                        location=node.map_location(),
                        severity='warning'
                    ).to_dict()
                    violations.append(violation)
    # ... (truncated)
```

---

## keep_functions_small_focused
**setup_similarity_scanner.py** - 1 violation(s)

[!] WARNING (line 16)
Function "scan" is 57 lines - should be under 50 lines (extract complex logic to helper functions)

```python
    MIN_INTRA_DUP = 2

    def scan(
        self,
        story_graph: Dict[str, Any],
        rule_obj: Any = None,
        test_files: Optional[List["Path"]] = None,
        code_files: Optional[List["Path"]] = None,
        on_file_scanned: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fingerprint_occurrences: Dict[Tuple[str, Tuple[str, ...]], List[Tuple[Path, int, str]]] = defaultdict(list)
        intra_duplicates: List[Dict[str, Any]] = []

        files = test_files or []
        for file_path in files:
            parsed = self._read_and_parse_file(file_path)
            if not parsed:
                continue
            content, lines, tree = parsed

            for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]:
                payloads = self._collect_payloads(func)
                per_func_counts: Dict[Tuple[str, Tuple[str, ...]], List[int]] = defaultdict(list)
                for fp, lineno in payloads:
                    per_func_counts[fp].append(lineno)
                    fingerprint_occurrences[fp].append((file_path, lineno, func.name))
                for fp, ln_list in per_func_counts.items():
                    if len(ln_list) >= self.MIN_INTRA_DUP:
                        first_line = sorted(ln_list)[0]
                        intra_duplicates.append(
                            Violation(
                                rule=rule_obj,
                                violation_message=(
                                    f'Test "{func.name}" builds {len(ln_list)} similar setup payloads; '
                                    f"centralize into a shared standard fixture/helper."
                                ),
                                line_number=first_line,
                                location=str(file_path),
                                severity="warning",
                            ).to_dict()
                        )

        for fp, occs in fingerprint_occurrences.items():
            if len(occs) >= self.MIN_REUSE:
                keyset = fp[0]
                key_text = ", ".join(keyset.split(",")) if keyset else "keys"
                # Emit up to 5 locations for context
                for file_path, lineno, func_name in occs[:5]:
                    violations.append(
    # ... (truncated)
```

---

## keep_functions_small_focused
**standard_data_reuse_scanner.py** - 1 violation(s)

[!] WARNING (line 23)
Function "scan_file" has high cyclomatic complexity (15) - should be under 10. Extract decision logic to helper functions.

```python
    }

    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations

        content, lines, tree = parsed

        for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]:
            dict_keysets = []
            for node in ast.walk(func):
                dict_node = None
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                    dict_node = node.value
                elif isinstance(node, ast.Call):
                    for arg in list(node.args) + [kw.value for kw in node.keywords]:
                        if isinstance(arg, ast.Dict):
                            dict_node = arg
                            break

                if dict_node and self._dict_has_canonical_keys(dict_node):
                    keyset = self._dict_keyset(dict_node)
                    dict_keysets.append((keyset, node.lineno))
                    if not self._is_uppercase_constant(getattr(node, "targets", [])):
                        violations.append(
                            Violation(
                                rule=rule_obj,
                                violation_message="Inline dict with standard test data fields - reuse a shared standard data set (e.g., STANDARD_STATE) instead of recreating ad-hoc.",
                                line_number=node.lineno,
                                location=str(file_path),
                                severity="warning",
                            ).to_dict()
                        )

            unique_keysets = {}
            for keyset, lineno in dict_keysets:
                unique_keysets.setdefault(keyset, []).append(lineno)
            if len(unique_keysets) > 1:
                lines = sorted({ln for lst in unique_keysets.values() for ln in lst})
                first_line = lines[0] if lines else func.lineno
                violations.append(
                    Violation(
                        rule=rule_obj,
                        violation_message="Test defines multiple ad-hoc data shapes for standard data fields; consolidate to a shared standard data set.",
                        line_number=first_line,
                        location=str(file_path),
                        severity="warning",
    # ... (truncated)
```

---

## keep_functions_small_focused
**story_map.py** - 1 violation(s)

[!] WARNING (line 23)
Function "map_location" has high cognitive complexity (22) - should be under 15. Reduce nesting and extract complex logic.

```python
        return self.data.get('name', '')
    
    def map_location(self, field: str = 'name') -> str:
        if isinstance(self, Epic):
            return f"epics[{self.epic_idx}].{field}"
        elif isinstance(self, SubEpic):
            if self.sub_epic_path:
                path_str = "".join([f".sub_epics[{idx}]" for idx in self.sub_epic_path])
                return f"epics[{self.epic_idx}]{path_str}.{field}"
            else:
                return f"epics[{self.epic_idx}].{field}"
        elif isinstance(self, Story):
            path_parts = [f"epics[{self.epic_idx}]"]
            if self.sub_epic_path:
                for idx in self.sub_epic_path:
                    path_parts.append(f"sub_epics[{idx}]")
            if self.story_group_idx is not None:
                path_parts.append(f"story_groups[{self.story_group_idx}]")
            path_parts.append(f"stories[{self.story_idx}]")
            path_parts.append(field)
            return ".".join(path_parts)
        return ""

```

---

## keep_functions_small_focused
**vocabulary_helper.py** - 1 violation(s)

[!] WARNING (line 62)
Function "is_agent_noun" has high cognitive complexity (20) - should be under 15. Reduce nesting and extract complex logic.

```python
    
    @staticmethod
    def is_agent_noun(word: str) -> tuple[bool, Optional[str], Optional[str]]:
        word_lower = word.lower()
        
        for suffix in VocabularyHelper.AGENT_SUFFIXES:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                base = word_lower[:-len(suffix)]
                
                if VocabularyHelper.is_verb(base):
                    return (True, base, suffix)
                
                if suffix == 'er' or suffix == 'or':
                    base_with_e = base + 'e'
                    if VocabularyHelper.is_verb(base_with_e):
                        return (True, base_with_e, suffix)
        
        return (False, None, None)
    
```

---

## keep_functions_small_focused
**json_scope.py** - 1 violation(s)

[!] WARNING (line 36)
Function "to_dict" has high cognitive complexity (19) - should be under 15. Reduce nesting and extract complex logic.

```python
        return self.scope.file_filter
    
    def to_dict(self) -> dict:
        result = {
            'type': self.scope.type.value,
            'filter': ', '.join(self.scope.value) if self.scope.value else '',
            'content': None,
            'graphLinks': []
        }
        
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
            files = self.scope._get_file_results()
            result['content'] = [{'path': str(f)} for f in files]
        
        return result
    
```

---

## keep_functions_small_focused
**markdown_scope.py** - 1 violation(s)

[!] WARNING (line 12)
Function "serialize" has high cognitive complexity (22) - should be under 15. Reduce nesting and extract complex logic.

```python
        self.workspace_directory = workspace_directory or Path.cwd()
    
    def serialize(self) -> str:
        lines = []
        
        lines.append(self.format_header(2, "🎯 Scope"))
        lines.append("")
        
        if self.scope.type.value == 'all':
            filter_display = "all (entire project)"
        else:
            filter_display = ', '.join(self.scope.value) if isinstance(self.scope.value, list) else str(self.scope.value) if self.scope.value else "all"
        
        lines.append(f"**🎯 Current Scope:** {filter_display}")
        lines.append("")
        
        results = self.scope.results
        
        if results is not None:
            from agile_bot.src.story_graph.story_graph import StoryGraph
            
            if isinstance(results, StoryGraph):
                from agile_bot.src.cli.adapter_factory import AdapterFactory
                story_graph_adapter = AdapterFactory.create(results, 'markdown')
                lines.append(story_graph_adapter.serialize())
            elif isinstance(results, list):
                if results:
                    for file_path in sorted(results):
                        try:
                            rel_path = file_path.relative_to(self.scope.workspace_directory)
                            lines.append(self.format_list_item(str(rel_path)))
                        except ValueError:
                            lines.append(self.format_list_item(str(file_path)))
                else:
                    lines.append("(no files found)")
        else:
            lines.append("(no scope set)")
        
        lines.append("")
        lines.append("To change scope (pick ONE - setting a new scope replaces the previous):")
        lines.append(self.format_list_item("`scope all` - Clear scope, work on entire project"))
        lines.append(self.format_list_item("`scope \"Story Name\"` - Filter by story (replaces any file scope)"))
        lines.append(self.format_list_item("`scope \"file:C:/path/to/**/*.py\"` - Filter by files (replaces any story scope)"))
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return ''.join(lines)
    
```

---

## keep_functions_small_focused
**scope.py** - 3 violation(s)

[!] WARNING (line 25)
Function "filter_story_graph" is 52 lines - should be under 50 lines (extract complex logic to helper functions)

```python
        return node_name in self.search_terms
    
    def filter_story_graph(self, story_graph: Dict[str, Any]) -> Dict[str, Any]:
        if not self.search_terms and not self.increments:
            return story_graph
        
        all_filter_names = self.search_terms
        
        def name_matches(name: str) -> bool:
            return any(filter_name.lower() in name.lower() for filter_name in all_filter_names)
        
        def filter_sub_epic(sub_epic: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            sub_epic_name = sub_epic.get('name', '')
            
            if name_matches(sub_epic_name):
                return sub_epic
            
            matching_story_groups = []
            for story_group in sub_epic.get('story_groups', []):
                matching_stories = []
                for story in story_group.get('stories', []):
                    if name_matches(story.get('name', '')):
                        matching_stories.append(story)
                
                if matching_stories:
                    matching_story_groups.append({
                        **story_group,
                        'stories': matching_stories
                    })
            
            matching_direct_stories = []
            for story in sub_epic.get('stories', []):
                if name_matches(story.get('name', '')):
                    matching_direct_stories.append(story)
            
            filtered_nested_sub_epics = []
            for nested_sub_epic in sub_epic.get('sub_epics', []):
                filtered_nested = filter_sub_epic(nested_sub_epic)
                if filtered_nested:
                    filtered_nested_sub_epics.append(filtered_nested)
            
            if matching_story_groups or matching_direct_stories or filtered_nested_sub_epics:
                filtered_sub_epic = {**sub_epic}
                if matching_story_groups:
                    filtered_sub_epic['story_groups'] = matching_story_groups
                if matching_direct_stories:
                    filtered_sub_epic['stories'] = matching_direct_stories
                if filtered_nested_sub_epics:
                    filtered_sub_epic['sub_epics'] = filtered_nested_sub_epics
                return filtered_sub_epic
    # ... (truncated)
```

[!] WARNING (line 112)
Function "filter_files" has high cyclomatic complexity (20) - should be under 10. Extract decision logic to helper functions.

```python
        return False
    
    def filter_files(self, file_list: List[Path]) -> List[Path]:
        if not self.include_patterns and not self.exclude_patterns:
            return file_list
        
        from pathlib import PurePath
        filtered = []
        
        for file_path in file_list:
            file_str = str(file_path).replace('\\', '/')
            file_path_obj = PurePath(file_str)
            
            if self.include_patterns:
                matches_include = False
                for pattern in self.include_patterns:
                    pattern_normalized = pattern.replace('\\', '/')
                    try:
                        if (file_path_obj.match(pattern_normalized) or
                            file_path_obj.match(f'**/{pattern_normalized}') or
                            pattern_normalized in file_str):
                            matches_include = True
                            break
                    except (ValueError, TypeError):
                        if pattern_normalized in file_str:
                            matches_include = True
                            break
                
                if not matches_include:
                    continue
            
            if self.exclude_patterns:
                matches_exclude = False
                for pattern in self.exclude_patterns:
                    pattern_normalized = pattern.replace('\\', '/')
                    try:
                        if (file_path_obj.match(pattern_normalized) or
                            file_path_obj.match(f'**/{pattern_normalized}') or
                            pattern_normalized in file_str):
                            matches_exclude = True
                            break
                    except (ValueError, TypeError):
                        if pattern_normalized in file_str:
                            matches_exclude = True
                            break
                
                if matches_exclude:
                    continue
            
            filtered.append(file_path)
    # ... (truncated)
```

[!] WARNING (line 34)
Function "filter_sub_epic" has high cyclomatic complexity (16) - should be under 10. Extract decision logic to helper functions.

```python
            return any(filter_name.lower() in name.lower() for filter_name in all_filter_names)
        
        def filter_sub_epic(sub_epic: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            sub_epic_name = sub_epic.get('name', '')
            
            if name_matches(sub_epic_name):
                return sub_epic
            
            matching_story_groups = []
            for story_group in sub_epic.get('story_groups', []):
                matching_stories = []
                for story in story_group.get('stories', []):
                    if name_matches(story.get('name', '')):
                        matching_stories.append(story)
                
                if matching_stories:
                    matching_story_groups.append({
                        **story_group,
                        'stories': matching_stories
                    })
            
            matching_direct_stories = []
            for story in sub_epic.get('stories', []):
                if name_matches(story.get('name', '')):
                    matching_direct_stories.append(story)
            
            filtered_nested_sub_epics = []
            for nested_sub_epic in sub_epic.get('sub_epics', []):
                filtered_nested = filter_sub_epic(nested_sub_epic)
                if filtered_nested:
                    filtered_nested_sub_epics.append(filtered_nested)
            
            if matching_story_groups or matching_direct_stories or filtered_nested_sub_epics:
                filtered_sub_epic = {**sub_epic}
                if matching_story_groups:
                    filtered_sub_epic['story_groups'] = matching_story_groups
                if matching_direct_stories:
                    filtered_sub_epic['stories'] = matching_direct_stories
                if filtered_nested_sub_epics:
                    filtered_sub_epic['sub_epics'] = filtered_nested_sub_epics
                return filtered_sub_epic
            
            return None
        
```

---

## keep_functions_small_focused
**tty_scope.py** - 1 violation(s)

[!] WARNING (line 11)
Function "serialize" has high cognitive complexity (22) - should be under 15. Reduce nesting and extract complex logic.

```python
        self.scope = scope
    
    def serialize(self) -> str:
        lines = []
        
        lines.append(self.add_bold("🎯 Scope"))
        
        if self.scope.type.value == 'all':
            filter_display = "all (entire project)"
        else:
            filter_display = ', '.join(self.scope.value) if isinstance(self.scope.value, list) else str(self.scope.value) if self.scope.value else "all"
        
        lines.append(f"🎯 {self.add_bold('Current Scope:')} {filter_display}")
        lines.append("")
        
        results = self.scope.results
        
        if results is not None:
            from agile_bot.src.story_graph.story_graph import StoryGraph
            
            if isinstance(results, StoryGraph):
                from agile_bot.src.cli.adapter_factory import AdapterFactory
                storyGrapgAdapter = AdapterFactory.create(results, 'tty')
                lines.append(storyGrapgAdapter.serialize())
            elif isinstance(results, list):
                if results:
                    for file_path in sorted(results):
                        try:
                            rel_path = file_path.relative_to(self.scope.workspace_directory)
                            lines.append(f"  - {rel_path}")
                        except ValueError:
                            lines.append(f"  - {file_path}")
                else:
                    lines.append("  (no files found)")
        else:
            lines.append("  (no scope set)")
        
        lines.append("To change scope (pick ONE - setting a new scope replaces the previous):")
        lines.append("scope all                            # Clear scope, work on entire project")
        lines.append('scope "Story Name"                   # Filter by story (replaces any file scope)')
        lines.append('scope "file:C:/path/to/**/*.py"      # Filter by files (replaces any story scope)')
        lines.append(self.subsection_separator())
        
        return '\n'.join(lines)
    
```

---

## keep_functions_small_focused
**build_action.py** - 1 violation(s)

[!] WARNING (line 170)
Function "inject_rules" has high cognitive complexity (19) - should be under 15. Reduce nesting and extract complex logic.

```python
        instructions._data['base_instructions'] = new_instructions

    def inject_rules(self, instructions) -> None:
        validate_action = self.rules
        rules_obj = validate_action.rules
        rules_text = rules_obj.formatted_rules_digest()
        rules_data = validate_action.inject_behavior_specific_rules()
        all_rules = rules_data.get('validation_rules', [])
        
        existing_instructions = instructions.get('base_instructions', [])
        new_instructions = []
        rules_section = []
        
        schema_path = self.behavior.bot_paths.workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        
        for line in existing_instructions:
            if isinstance(line, str):
                if '{{rules}}' in line:
                    continue
                if '{{schema}}' in line:
                    line = line.replace('{{schema}}', f'**Schema:** Story graph template at `{schema_path}`')
                if '{{description}}' in line:
                    line = line.replace('{{description}}', f'**Task:** Build {self.behavior.name} story graph from clarification and strategy data')
            new_instructions.append(line)
        
        if rules_text != 'No validation rules found.':
            rules_lines = rules_text.split('\n')
            rules_section.extend(rules_lines)
        
        if rules_section:
            while new_instructions and new_instructions[-1] == '':
                new_instructions.pop()
            new_instructions.append('')
            new_instructions.append('When building or adding to the story graph follow these rules,')
            new_instructions.extend(rules_section)
        
        instructions._data['base_instructions'] = new_instructions
        instructions.set('rules', all_rules)
    
```

---

## keep_functions_small_focused
**tty_required_context.py** - 1 violation(s)

[!] WARNING (line 9)
Function "serialize" has high cognitive complexity (23) - should be under 15. Reduce nesting and extract complex logic.

```python
        self.required_context = required_context
    
    def serialize(self) -> str:
        lines = []
        
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
        
        return '\n'.join(lines)
    
```

---

## keep_functions_small_focused
**tty_strategy.py** - 1 violation(s)

[!] WARNING (line 9)
Function "serialize" has high cognitive complexity (16) - should be under 15. Reduce nesting and extract complex logic.

```python
        self.strategy = strategy
    
    def serialize(self) -> str:
        lines = []
        
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
        
        assumptions = self.strategy.assumptions.assumptions
        if assumptions:
            lines.append("")
            lines.append(self.add_bold("Assumptions:"))
            for assumption in assumptions:
                lines.append(f"- {assumption}")
        
        return '\n'.join(lines)
    
```

---

## keep_functions_small_focused
**json_strategy_action.py** - 1 violation(s)

[!] WARNING (line 57)
Function "to_dict" has high cyclomatic complexity (15) - should be under 10. Extract decision logic to helper functions.

```python
        return self.action.typical_assumptions
    
    def to_dict(self) -> dict:
        import time
        with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H1','location':'json_strategy_action.py:67','message':'to_dict called','data':{'behavior_name':self.action.behavior.name if self.action.behavior else None,'has_strategy':bool(self.action.strategy)},'timestamp':int(time.time()*1000)})+'\n')
        
        result = {
            'action_name': self.action.action_name,
            'description': self.action.description,
            'order': self.action.order,
            'next_action': self.action.next_action,
            'workflow': self.action.workflow,
            'auto_confirm': self.action.auto_confirm,
            'skip_confirm': self.action.skip_confirm,
            'behavior': self.action.behavior.name if self.action.behavior else None,
        }
        
        if self.action.strategy:
            from agile_bot.src.actions.strategy.strategy_decision import StrategyDecision
            saved_data = StrategyDecision.load_all(self.action.behavior.bot_paths)
            
            with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H3,H4','location':'json_strategy_action.py:83','message':'loaded saved_data','data':{'saved_data_keys':list(saved_data.keys()) if saved_data else None,'saved_data':saved_data,'behavior_name':self.action.behavior.name},'timestamp':int(time.time()*1000)})+'\n')
            
            behavior_data = saved_data.get(self.action.behavior.name, {}) if saved_data else {}
            saved_decisions = behavior_data.get('decisions', {})
            saved_assumptions = behavior_data.get('assumptions', [])
            
            with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H3,H4','location':'json_strategy_action.py:93','message':'extracted behavior data','data':{'behavior_data':behavior_data,'saved_decisions':saved_decisions,'saved_assumptions':saved_assumptions},'timestamp':int(time.time()*1000)})+'\n')
            
            serialized_criteria = {}
            
            with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H2,H6','location':'json_strategy_action.py:102','message':'before serializing criteria','data':{'has_strategy_criteria':bool(self.action.strategy_criteria),'criteria_type':str(type(self.action.strategy_criteria)),'criteria_len':len(self.action.strategy_criteria) if self.action.strategy_criteria else 0},'timestamp':int(time.time()*1000)})+'\n')
            
            if self.action.strategy_criteria:
                for key, criteria in self.action.strategy_criteria.items():
                    if hasattr(criteria, 'to_dict'):
                        serialized_criteria[key] = criteria.to_dict()
                    else:
                        serialized_criteria[key] = {
                            'question': criteria.question if hasattr(criteria, 'question') else '',
                            'options': criteria.options if hasattr(criteria, 'options') else [],
                            'outcome': criteria.outcome if hasattr(criteria, 'outcome') else None
                        }
            
            with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H2,H6','location':'json_strategy_action.py:120','message':'after serializing criteria','data':{'serialized_count':len(serialized_criteria),'serialized_keys':list(serialized_criteria.keys())},'timestamp':int(time.time()*1000)})+'\n')
    # ... (truncated)
```

---

## maintain_vertical_density
**cli_session.py** - 1 violation(s)

[i] INFO (line 17)
Function "execute_command" is 331 lines - consider improving vertical density by extracting helper methods and declaring variables near usage

```python
        self.mode = mode
    
    def execute_command(self, command: str) -> CLICommandResponse:
        verb, args = self._parse_command(command)
        
        if args and ('--format json' in args or '--format=json' in args):
            self.mode = 'json'
            args = args.replace('--format json', '').replace('--format=json', '').strip()
        
        cli_terminated = verb == 'exit'
    # ... (truncated)
```

---

## maintain_vertical_density
**markdown_instructions.py** - 1 violation(s)

[i] INFO (line 10)
Function "serialize" is 208 lines - consider improving vertical density by extracting helper methods and declaring variables near usage

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        scope = self.instructions.scope
        if scope and (scope.value or scope.type.value == 'showAll'):
            from agile_bot.src.cli.adapters import MarkdownAdapter
            
    # ... (truncated)
```

---

## maintain_vertical_density
**tty_instructions.py** - 1 violation(s)

[i] INFO (line 10)
Function "serialize" is 179 lines - consider improving vertical density by extracting helper methods and declaring variables near usage

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        behavior_metadata = instructions_dict.get('behavior_metadata', {})
        if behavior_metadata:
            behavior_name = behavior_metadata.get('name', 'unknown')
            output_lines.append(f"{self.add_bold(f'Behavior Instructions - {behavior_name}')}")
    # ... (truncated)
```

---

## maintain_vertical_density
**duplication_scanner.py** - 2 violation(s)

[i] INFO (line 299)
Function "_check_duplicate_code_blocks" is 246 lines - consider improving vertical density by extracting helper methods and declaring variables near usage

```python
        return False
    
    def _check_duplicate_code_blocks(self, functions: List[tuple], lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        all_blocks = []
        for func_tuple in functions:
            func_name, func_body, func_line, func_node, _ = func_tuple
            blocks = self._extract_code_blocks(func_node, func_line, func_name)
            all_blocks.extend(blocks)
    # ... (truncated)
```

[i] INFO (line 1788)
Function "scan_cross_file" is 279 lines - consider improving vertical density by extracting helper methods and declaring variables near usage

```python
        return nearby_files
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
    # ... (truncated)
```

---

## never_swallow_exceptions
**action.py** - 1 violation(s)

[X] ERROR (line 436)
Except block only contains pass at line 436 - exceptions must be logged or rethrown, never swallowed

```python
                    if 'guardrails' not in instructions._data:
                        instructions.set('guardrails', {'required_context': required_context.instructions})
        except Exception:
            pass
    
```

---

## never_swallow_exceptions
**bot.py** - 1 violation(s)

[X] ERROR (line 632)
Except block only contains pass at line 632 - exceptions must be logged or rethrown, never swallowed

```python
                try:
                    self.execute(saved_behavior, saved_action)
                except:
                    pass
            
```

---

## never_swallow_exceptions
**markdown_bot.py** - 1 violation(s)

[X] ERROR (line 116)
Except block only contains pass at line 116 - exceptions must be logged or rethrown, never swallowed

```python
                lines.append(markdown_scope.serialize())
                lines.append("")
            except (AttributeError, TypeError):
                pass
        
```

---

## never_swallow_exceptions
**workspace.py** - 1 violation(s)

[X] ERROR (line 43)
Except block only contains pass at line 43 - exceptions must be logged or rethrown, never swallowed

```python
                        path = python_workspace_root / base_actions_path
                    return path
            except Exception:
                pass
    
```

---

## never_swallow_exceptions
**cli_main.py** - 2 violation(s)

[X] ERROR (line 36)
Except block only contains pass at line 36 - exceptions must be logged or rethrown, never swallowed

```python
                if 'WORKING_AREA' in mcp_env:
                    os.environ['WORKING_AREA'] = mcp_env['WORKING_AREA']
        except:
            pass
    
```

[X] ERROR (line 132)
Except block only contains pass at line 132 - exceptions must be logged or rethrown, never swallowed

```python
                    response = cli_session.execute_command(command)
                    print(response.output, flush=True)
        except (KeyboardInterrupt, EOFError):
            pass
    elif is_piped:
```

---

## never_swallow_exceptions
**cli_session.py** - 1 violation(s)

[X] ERROR (line 525)
Except block only contains pass at line 525 - exceptions must be logged or rethrown, never swallowed

```python
                    print(f"Error: {e}", file=sys.stderr)
                    
        except KeyboardInterrupt:
            pass

```

---

## never_swallow_exceptions
**behavior_matcher.py** - 1 violation(s)

[X] ERROR (line 86)
Except block only contains pass at line 86 - exceptions must be logged or rethrown, never swallowed

```python
            if patterns:
                triggers[action_name] = patterns
        except FileNotFoundError:
            pass

```

---

## never_swallow_exceptions
**markdown_instructions.py** - 1 violation(s)

[X] ERROR (line 37)
Except block only contains pass at line 37 - exceptions must be logged or rethrown, never swallowed

```python
                    scope_content = adapter.serialize()
                    output_lines.append(scope_content)
                except Exception:
                    pass
            
```

---

## never_swallow_exceptions
**verb_noun_scanner.py** - 1 violation(s)

[X] ERROR (line 523)
Except block only contains pass at line 523 - exceptions must be logged or rethrown, never swallowed

```python
                ).to_dict()
        
        except Exception:
            pass
        
```

---

## never_swallow_exceptions
**vocabulary_helper.py** - 3 violation(s)

[X] ERROR (line 16)
Except block only contains pass at line 16 - exceptions must be logged or rethrown, never swallowed

```python
    try:
        nltk.download('wordnet', quiet=True)
    except:
        pass

```

[X] ERROR (line 24)
Except block only contains pass at line 24 - exceptions must be logged or rethrown, never swallowed

```python
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        pass

```

[X] ERROR (line 32)
Except block only contains pass at line 32 - exceptions must be logged or rethrown, never swallowed

```python
    try:
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    except:
        pass

```

---

## never_swallow_exceptions
**scope.py** - 2 violation(s)

[X] ERROR (line 382)
Except block only contains pass at line 382 - exceptions must be logged or rethrown, never swallowed

```python
                
                self.filter(scope_type, value, exclude, skiprule)
        except (json.JSONDecodeError, IOError, ValueError):
            pass
    
```

[X] ERROR (line 404)
Except block only contains pass at line 404 - exceptions must be logged or rethrown, never swallowed

```python
                del state_data['scope']
                state_file.write_text(json.dumps(state_data, indent=2))
        except (json.JSONDecodeError, IOError):
            pass

```

---

## never_swallow_exceptions
**strategy_action.py** - 1 violation(s)

[X] ERROR (line 85)
Except block only contains pass at line 85 - exceptions must be logged or rethrown, never swallowed

```python
            if saved_clarifications and self.behavior.name in saved_clarifications:
                instructions.set('clarification', saved_clarifications[self.behavior.name])
        except Exception:
            pass
    
```

---

## place_imports_at_top
**cli_main.py** - 3 violation(s)

[X] ERROR (line 43)
Import statement found after non-import code. Move all imports to the top of the file.

```python

# Import agile_bot modules after environment setup
from agile_bot.src.bot.bot import Bot
from agile_bot.src.bot.workspace import get_workspace_directory
```

[X] ERROR (line 44)
Import statement found after non-import code. Move all imports to the top of the file.

```python
# Import agile_bot modules after environment setup
from agile_bot.src.bot.bot import Bot
from agile_bot.src.bot.workspace import get_workspace_directory
from agile_bot.src.cli.cli_session import CLISession
```

[X] ERROR (line 45)
Import statement found after non-import code. Move all imports to the top of the file.

```python
from agile_bot.src.bot.bot import Bot
from agile_bot.src.bot.workspace import get_workspace_directory
from agile_bot.src.cli.cli_session import CLISession

```

---

## simplify_control_flow
**action.py** - 6 violation(s)

[!] WARNING (line 116)
Function "_get_type_string" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return help_dict
    
    def _get_type_string(self, python_type) -> str:
        if python_type is type(None):
            return "none"
        if python_type == str:
            return "string"
        elif python_type == Path:
            return "path"
        elif python_type == int:
            return "int"
        elif python_type == float:
            return "float"
        elif python_type == bool:
            return "bool"
    # ... (truncated)
```

[!] WARNING (line 346)
Function "get_instructions" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return inject_reminder_to_instructions(result, reminder)

    def get_instructions(self, context: ActionContext = None) -> Instructions:
        if context is None:
            context = self.context_class()
        
        self._save_guardrails_if_provided(context)
        
        if hasattr(context, 'scope') and context.scope:
            context.scope.apply_to_bot()
        
        instructions = self.instructions.copy()
        
        if self.action_config and 'instructions' in self.action_config:
            behavior_instructions = self.action_config.get('instructions', [])
    # ... (truncated)
```

[!] WARNING (line 375)
Function "_save_guardrails_if_provided" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return instructions
    
    def _save_guardrails_if_provided(self, context: ActionContext):
        if hasattr(context, 'answers') and context.answers:
            try:
                from .clarify.requirements_clarifications import RequirementsClarifications
                from .clarify.required_context import RequiredContext
                
                required_context = None
                if hasattr(self, 'required_context'):
                    required_context = self.required_context
                elif self.behavior and hasattr(self.behavior, 'folder'):
                    required_context = RequiredContext(self.behavior.folder)
                
                if required_context:
    # ... (truncated)
```

[!] WARNING (line 425)
Function "_load_behavior_guardrails" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
                logging.getLogger(__name__).warning(f'Failed to save strategy data: {e}')
    
    def _load_behavior_guardrails(self, instructions):
        try:
            if not self.behavior or not hasattr(self.behavior, 'guardrails'):
                return
            
            guardrails_obj = self.behavior.guardrails
            if hasattr(guardrails_obj, 'required_context'):
                required_context = guardrails_obj.required_context
                if hasattr(required_context, 'instructions'):
                    if 'guardrails' not in instructions._data:
                        instructions.set('guardrails', {'required_context': required_context.instructions})
        except Exception:
            pass
    # ... (truncated)
```

[!] WARNING (line 441)
Function "_load_all_saved_guardrails" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        self._load_all_saved_guardrails(instructions)
    
    def _load_all_saved_guardrails(self, instructions):
        if not self.behavior:
            return
        
        try:
            from .clarify.requirements_clarifications import RequirementsClarifications
            from .clarify.required_context import RequiredContext
            
            required_context = None
            if hasattr(self.behavior, 'guardrails') and hasattr(self.behavior.guardrails, 'required_context'):
                required_context = self.behavior.guardrails.required_context
            else:
                required_context = RequiredContext(self.behavior.folder)
    # ... (truncated)
```

[!] WARNING (line 516)
Function "_add_behavior_action_metadata" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            logging.getLogger(__name__).debug(f'Could not load saved strategy decisions: {e}')
    
    def _add_behavior_action_metadata(self, instructions):
        if self.behavior:
            behavior_data = {
                'name': self.behavior.name if hasattr(self.behavior, 'name') else 'unknown',
                'description': self.behavior.description if hasattr(self.behavior, 'description') else '',
                'instructions': []
            }
            
            if hasattr(self.behavior, 'instructions') and self.behavior.instructions:
                behavior_instructions = self.behavior.instructions
                if isinstance(behavior_instructions, list):
                    behavior_data['instructions'] = list(behavior_instructions)
                elif isinstance(behavior_instructions, str):
    # ... (truncated)
```

---

## simplify_control_flow
**behaviors.py** - 1 violation(s)

[!] WARNING (line 270)
Function "load_state" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None

    def load_state(self):
        if self.bot_paths is None:
            self._init_to_first_behavior()
            return
        workspace_dir = self.bot_paths.workspace_directory
        state_file = workspace_dir / 'behavior_action_state.json'
        if not state_file.exists() or not self._behaviors:
            self._init_to_first_behavior()
            return
        try:
            state_data = json.loads(state_file.read_text(encoding='utf-8'))
            behavior_name = self._extract_behavior_name_from_state(state_data.get('current_behavior', ''))
            if behavior_name:
    # ... (truncated)
```

---

## simplify_control_flow
**bot.py** - 1 violation(s)

[!] WARNING (line 128)
Function "bots" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @property
    def bots(self) -> List[str]:
        registered_bots = []
        
        bots_parent_dir = self.bot_paths.bot_directory.parent
        
        if bots_parent_dir.exists() and bots_parent_dir.is_dir():
            for bot_dir in bots_parent_dir.iterdir():
                if bot_dir.is_dir():
                    bot_config = bot_dir / 'bot_config.json'
                    if bot_config.exists():
                        registered_bots.append(bot_dir.name)
        
        return sorted(registered_bots)
    # ... (truncated)
```

---

## simplify_control_flow
**workspace.py** - 1 violation(s)

[!] WARNING (line 20)
Function "get_base_actions_directory" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
    return Path(workspace.strip())

def get_base_actions_directory(bot_directory: Path=None) -> Path:
    from ..utils import read_json_file
    
    if bot_directory is None:
        bot_directory = get_bot_directory()
    
    config_paths = [
        bot_directory / 'bot_config.json',
        bot_directory / 'config' / 'bot_config.json'
    ]
    
    python_workspace_root = get_python_workspace_root()
    
    # ... (truncated)
```

---

## simplify_control_flow
**bot_path.py** - 1 violation(s)

[!] WARNING (line 22)
Function "_load_base_actions_directory" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        self._documentation_path = self._load_documentation_path()

    def _load_base_actions_directory(self) -> Path:
        config_paths = [
            self._bot_directory / 'bot_config.json',
            self._bot_directory / 'config' / 'bot_config.json'
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    config = read_json_file(config_path)
                    base_actions_path = config.get('baseActionsPath')
                    if base_actions_path:
                        path = Path(base_actions_path)
    # ... (truncated)
```

---

## simplify_control_flow
**adapters.py** - 1 violation(s)

[!] WARNING (line 124)
Function "serialize" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.data = data
    
    def serialize(self) -> str:
        if isinstance(self.data, dict):
            if 'scope' in self.data and isinstance(self.data['scope'], dict):
                scope_data = self.data['scope']
                scope_type = scope_data.get('type', 'all')
                target = scope_data.get('target', [])
                
                if target:
                    target_str = ', '.join(str(t) for t in target)
                    return f"\x1b[1mScope:\x1b[0m {scope_type}: {target_str}"
                else:
                    return f"\x1b[1mScope:\x1b[0m {scope_type}"
            elif 'status' in self.data and 'behavior' in self.data and 'action' in self.data:
    # ... (truncated)
```

---

## simplify_control_flow
**adapter_factory.py** - 1 violation(s)

[!] WARNING (line 84)
Function "create" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @classmethod
    def create(cls, domain_object: Any, channel: str, **kwargs):
        domain_type = type(domain_object).__name__
        
        if domain_type in ('dict', 'list', 'str'):
            if channel == 'json':
                from agile_bot.src.cli.adapters import GenericJSONAdapter
                return GenericJSONAdapter(domain_object)
            elif channel == 'tty':
                from agile_bot.src.cli.adapters import GenericTTYAdapter
                return GenericTTYAdapter(domain_object)
            elif channel == 'markdown':
                from agile_bot.src.cli.adapters import GenericMarkdownAdapter
                return GenericMarkdownAdapter(domain_object)
    # ... (truncated)
```

---

## simplify_control_flow
**cli_main.py** - 1 violation(s)

[!] WARNING (line 47)
Function "main" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
from agile_bot.src.cli.cli_session import CLISession

def main():
    bot_name = bot_directory.name
    workspace_directory = get_workspace_directory()
    bot_config_path = bot_directory / 'bot_config.json'
    
    if not bot_config_path.exists():
        print(f"ERROR: Bot config not found at {bot_config_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        bot = Bot(
            bot_name=bot_name,
            bot_directory=bot_directory,
    # ... (truncated)
```

---

## simplify_control_flow
**cli_session.py** - 2 violation(s)

[!] WARNING (line 17)
Function "execute_command" has nesting depth of 12 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.mode = mode
    
    def execute_command(self, command: str) -> CLICommandResponse:
        verb, args = self._parse_command(command)
        
        if args and ('--format json' in args or '--format=json' in args):
            self.mode = 'json'
            args = args.replace('--format json', '').replace('--format=json', '').strip()
        
        cli_terminated = verb == 'exit'
        
        is_navigation_command = verb in ('next', 'back', 'current', 'scope', 'path', 'workspace')
        
        if verb == 'status':
            result = self.bot
    # ... (truncated)
```

[!] WARNING (line 501)
Function "run" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return AdapterFactory.create(domain_object, channel)
    
    def run(self):
        try:
            while True:
                try:
                    line = input(f"[{self.bot.name}] > ").strip()
                    if not line:
                        continue
                    
                    response = self.execute_command(line)
                    print(response.output)
                    print("")
                    
                    if response.cli_terminated:
    # ... (truncated)
```

---

## simplify_control_flow
**help.py** - 1 violation(s)

[!] WARNING (line 132)
Function "__init__" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
class Help:
    
    def __init__(self, bot=None):
        self.bot = bot
        self.commands = CommandsHelp()
        self.scope = ScopeHelp()
        
        if bot:
            behaviors_names = bot.behaviors.names if hasattr(bot, 'behaviors') else []
            actions_list = []
            if hasattr(bot, 'behaviors'):
                for behavior in bot.behaviors:
                    for action in behavior.actions:
                        if not any(a.action_name == action.action_name for a in actions_list):
                            actions_list.append(action)
    # ... (truncated)
```

---

## simplify_control_flow
**help_action.py** - 1 violation(s)

[!] WARNING (line 17)
Function "to_cli_type" has nesting depth of 9 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def to_cli_type(python_type) -> str:
        if python_type is type(None):
            return "none"
        
        if python_type == str:
            return "string"
        elif python_type == Path:
            return "path"
        elif python_type == int:
            return "int"
        elif python_type == float:
            return "float"
        elif python_type == bool:
    # ... (truncated)
```

---

## simplify_control_flow
**markdown_instructions.py** - 1 violation(s)

[!] WARNING (line 10)
Function "serialize" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        scope = self.instructions.scope
        if scope and (scope.value or scope.type.value == 'showAll'):
            from agile_bot.src.cli.adapters import MarkdownAdapter
            
            output_lines.append("## Scope")
            output_lines.append("")
            if scope.type.value == 'story':
                output_lines.append(f"**Story Scope:** {', '.join(scope.value)}")
            elif scope.type.value == 'files':
    # ... (truncated)
```

---

## simplify_control_flow
**tty_instructions.py** - 1 violation(s)

[!] WARNING (line 10)
Function "serialize" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.instructions = instructions
    
    def serialize(self) -> str:
        instructions_dict = self.instructions.to_dict()
        output_lines = []
        
        behavior_metadata = instructions_dict.get('behavior_metadata', {})
        if behavior_metadata:
            behavior_name = behavior_metadata.get('name', 'unknown')
            output_lines.append(f"{self.add_bold(f'Behavior Instructions - {behavior_name}')}")
            
            behavior_description = behavior_metadata.get('description', '')
            if behavior_description:
                output_lines.append(f"The purpose of this behavior is to {behavior_description.lower()}")
                output_lines.append("")
    # ... (truncated)
```

---

## simplify_control_flow
**rules.py** - 2 violation(s)

[!] WARNING (line 68)
Function "_get_files_for_validation" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @classmethod
    def _get_files_for_validation(cls, behavior, context: 'ValidateActionContext') -> Dict[str, List[Path]]:
        from agile_bot.src.actions.validate.file_discovery import FileDiscovery
        from agile_bot.src.scope import ScopeType
        from agile_bot.src.actions.validate.validation_type import ValidationType
        
        validation_type = behavior.validation_type
        if validation_type == ValidationType.STORY_GRAPH:
            return {}

        if context.scope and context.scope.type == ScopeType.FILES:
            files_dict = {}
            for file_path_str in context.scope.value:
                file_path = Path(file_path_str)
    # ... (truncated)
```

[!] WARNING (line 123)
Function "from_parameters" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @classmethod
    def from_parameters(cls, parameters: Dict[str, Any], behavior, bot_paths, callbacks: Optional[ValidationCallbacks] = None) -> 'ValidationContext':
        from agile_bot.src.actions.action_context import ValidateActionContext, Scope, ScopeType, FileFilter
        from agile_bot.src.bot.behavior import Behavior
        
        if isinstance(behavior, str):
            behavior = Behavior(name=behavior, bot_paths=bot_paths)
        
        scope = None
        if 'scope' in parameters and parameters['scope']:
            scope_dict = parameters['scope']
            if isinstance(scope_dict, dict):
                scope_type_str = scope_dict.get('type', 'all')
                scope_type = ScopeType(scope_type_str)
    # ... (truncated)
```

---

## simplify_control_flow
**rules_action.py** - 1 violation(s)

[!] WARNING (line 37)
Function "_add_rules_list_to_display" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return [rule.name for rule in rules]
    
    def _add_rules_list_to_display(self, instructions, rule_names: list, rules: Rules) -> None:
        instructions.add_display("")
        instructions.add_display(f"## Rules Available ({len(rule_names)} total)")
        instructions.add_display("")
        rule_map = {rule.name: rule for rule in rules}
        for idx, rule_name in enumerate(rule_names, 1):
            rule = rule_map.get(rule_name)
            if rule:
                if hasattr(rule, '_rule_file_path'):
                    file_path = str(rule._rule_file_path)
                    file_path = file_path.replace('\\', '/')
                    instructions.add_display(f"{idx}. {rule_name} ({file_path})")
                elif hasattr(rule, 'rule_file'):
    # ... (truncated)
```

---

## simplify_control_flow
**arrange_act_assert_scanner.py** - 4 violation(s)

[!] WARNING (line 71)
Function "_detect_aaa_sections_ast" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations[0] if violations else None
    
    def _detect_aaa_sections_ast(self, test_node: ast.FunctionDef, content: str) -> Dict[str, List[ast.stmt]]:
        sections = {'arrange': [], 'act': [], 'assert': []}
        test_lines = content.split('\n')
        
        current_section = None
        
        for i, stmt in enumerate(test_node.body):
            if isinstance(stmt, (ast.Pass, ast.Expr)):
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Constant, ast.Str)):
                    continue
            
            if hasattr(stmt, 'lineno'):
                line_num = stmt.lineno - 1
    # ... (truncated)
```

[!] WARNING (line 102)
Function "_classify_statement" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return sections
    
    def _classify_statement(self, stmt: ast.stmt) -> Optional[str]:
        if isinstance(stmt, ast.Assert):
            return 'assert'
        
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name and ('assert' in func_name.lower() or 'verify' in func_name.lower()):
                    return 'assert'
        
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
    # ... (truncated)
```

[!] WARNING (line 138)
Function "_validate_aaa_structure" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _validate_aaa_structure(self, sections: Dict[str, List[ast.stmt]], test_node: ast.FunctionDef, 
                                file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        has_arrange = len(sections['arrange']) > 0
        has_act = len(sections['act']) > 0
        has_assert = len(sections['assert']) > 0
        
        test_lines = file_path.read_text(encoding='utf-8').split('\n')
        start_line = test_node.lineno - 1
        end_line = test_node.end_lineno if hasattr(test_node, 'end_lineno') else start_line + 50
        test_body_lines = test_lines[start_line:end_line]
        
        has_given_comment = any('# Given' in line or '# Arrange' in line for line in test_body_lines)
        has_when_comment = any('# When' in line or '# Act' in line for line in test_body_lines)
    # ... (truncated)
```

[!] WARNING (line 259)
Function "_has_actual_code" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _has_actual_code(self, test_node: ast.FunctionDef) -> bool:
        if not test_node.body:
            return False
        
        for stmt in test_node.body:
            if isinstance(stmt, ast.Pass):
                continue
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Constant, ast.Str)):
                continue
            else:
                for node in ast.walk(stmt):
                    if isinstance(node, (ast.Call, ast.Assign, ast.Assert, ast.Return, ast.Raise)):
                        return True
    # ... (truncated)
```

---

## simplify_control_flow
**ascii_only_scanner.py** - 1 violation(s)

[!] WARNING (line 26)
Function "_check_unicode_characters" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_unicode_characters(self, line: str, file_path: Path, line_num: int, rule_obj: Any) -> Optional[Dict[str, Any]]:
        try:
            line.encode('ascii')
        except UnicodeEncodeError:
            unicode_chars = []
            for char in line:
                try:
                    char.encode('ascii')
                except UnicodeEncodeError:
                    unicode_chars.append(char)
            
            if unicode_chars:
                problematic = [c for c in unicode_chars if ord(c) > 127]
    # ... (truncated)
```

---

## simplify_control_flow
**background_common_setup_scanner.py** - 1 violation(s)

[!] WARNING (line 89)
Function "_get_scenario_steps" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return steps
    
    def _get_scenario_steps(self, scenario: Dict[str, Any]) -> List[str]:
        if isinstance(scenario, dict):
            if 'steps' in scenario:
                return scenario['steps']
            elif 'scenario' in scenario:
                scenario_text = scenario['scenario']
                if isinstance(scenario_text, str):
                    return [s.strip() for s in scenario_text.split('\n') if s.strip()]
        return []

```

---

## simplify_control_flow
**bad_comments_scanner.py** - 5 violation(s)

[!] WARNING (line 30)
Function "_check_commented_code" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_commented_code(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        commented_block_start = None
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//') or stripped.startswith('#'):
                comment_content = stripped[2:].strip()
                
                if self._is_actual_commented_code(comment_content, lines, line_num):
                    if commented_block_start is None:
                        commented_block_start = line_num
    # ... (truncated)
```

[!] WARNING (line 88)
Function "_is_actual_commented_code" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
            ).to_dict()
    
    def _is_actual_commented_code(self, comment_content: str, lines: List[str], line_num: int) -> bool:
        if not comment_content:
            return False
        
        for i in range(1, min(3, len(lines) - line_num + 1)):
            if line_num + i - 1 < len(lines):
                next_line = lines[line_num + i - 1].strip()
                if next_line and not next_line.startswith('//') and not next_line.startswith('#'):
                    if re.search(r'\b(def|class|if|for|while|return|import|from|=\s*[^=]|\(|\[|\{)\b', next_line):
                        return False
        
        code_patterns = [
            r'^\s*\w+\s*=\s*[^=]',
    # ... (truncated)
```

[!] WARNING (line 153)
Function "_check_html_in_comments" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _check_html_in_comments(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        html_patterns = [
            r'<p>', r'</p>', r'<ul>', r'</ul>', r'<li>', r'</li>',
            r'<div>', r'</div>', r'<span>', r'</span>', r'<br>', r'<br/>'
        ]
        
        for line_num, line in enumerate(lines, 1):
            comment_text = self._extract_comment_text(line)
            
            if comment_text:
                for pattern in html_patterns:
    # ... (truncated)
```

[!] WARNING (line 194)
Function "_extract_comment_text" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _extract_comment_text(self, line: str) -> Optional[str]:
        in_single_quote = False
        in_double_quote = False
        in_triple_single = False
        in_triple_double = False
        escape_next = False
        
        i = 0
        while i < len(line):
            char = line[i]
            
            if escape_next:
                escape_next = False
    # ... (truncated)
```

[!] WARNING (line 247)
Function "_check_misleading_todos" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _check_misleading_todos(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        for line_num, line in enumerate(lines, 1):
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                if 'needs to be implemented' in line.lower() or 'not implemented' in line.lower():
                    next_lines = lines[line_num:line_num+5]
                    has_implementation = any(
                        re.search(r'\b(function|def|class|return|if|for|while)\b', l)
                        for l in next_lines
                    )
                    
                    if has_implementation:
    # ... (truncated)
```

---

## simplify_control_flow
**business_readable_test_names_scanner.py** - 2 violation(s)

[!] WARNING (line 112)
Function "_check_business_readable" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return set(words)
    
    def _check_business_readable(self, test_name: str, file_path: Path, node: ast.FunctionDef, rule_obj: Any, domain_language: set) -> Optional[Dict[str, Any]]:
        name_without_prefix = test_name[5:] if test_name.startswith('test_') else test_name
        
        test_words = self._extract_words_from_text(name_without_prefix)
        
        if domain_language and test_words:
            matching_domain_terms = test_words.intersection(domain_language)
            if len(matching_domain_terms) >= 1:
                return None
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
    # ... (truncated)
```

[!] WARNING (line 241)
Function "_extract_code_snippet" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return True
    
    def _extract_code_snippet(self, content: str, ast_node: Optional[ast.AST] = None, 
                             start_line: Optional[int] = None, end_line: Optional[int] = None,
                             context_before: int = 2, max_lines: int = 50) -> str:
        lines = content.split('\n')
        
        if ast_node is not None:
            start_line_0 = ast_node.lineno - 1 if hasattr(ast_node, 'lineno') and ast_node.lineno else 0
            
            if hasattr(ast_node, 'end_lineno') and ast_node.end_lineno:
                end_line_0 = ast_node.end_lineno
            else:
                end_line_0 = start_line_0 + 1
                for node in ast.walk(ast_node):
    # ... (truncated)
```

---

## simplify_control_flow
**class_based_organization_scanner.py** - 6 violation(s)

[!] WARNING (line 15)
Function "scan_file" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return []
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        if not file_path.exists():
            return violations
        
        sub_epic_names = self._extract_sub_epic_names(story_graph)
        file_name = file_path.stem
        violation = self._check_file_name_matches_sub_epic(file_name, sub_epic_names, file_path, rule_obj, story_graph)
        if violation:
            violations.append(violation)
        
        parsed = self._read_and_parse_file(file_path)
    # ... (truncated)
```

[!] WARNING (line 123)
Function "_find_expected_scenario_name" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _find_expected_scenario_name(self, method_name: str, story_graph: Dict[str, Any], class_name: str) -> Optional[str]:
        full_method_name = f"test_{method_name}" if not method_name.startswith('test_') else method_name
        method_name_norm = self._normalize_name(method_name)
        
        story_name_from_class = class_name[4:] if class_name.startswith('Test') else class_name
        story_name_normalized = self._normalize_name(story_name_from_class)
        
        epics = story_graph.get('epics', [])
        
        best_match = None
        best_match_type = None
        
        for epic in epics:
    # ... (truncated)
```

[!] WARNING (line 335)
Function "_get_sub_epics_spanned_by_test_methods" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        ).to_dict()
    
    def _get_sub_epics_spanned_by_test_methods(self, file_path: Path, story_graph: Dict[str, Any]) -> set:
        sub_epics = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.name.startswith('Test'):
                        class_name = node.name
                        
                        for item in node.body:
    # ... (truncated)
```

[!] WARNING (line 359)
Function "_find_sub_epic_for_method" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return sub_epics
    
    def _find_sub_epic_for_method(self, method_name: str, class_name: str, story_graph: Dict[str, Any]) -> Optional[str]:
        method_name_norm = self._normalize_name(method_name)
        story_name_from_class = class_name[4:] if class_name.startswith('Test') else class_name
        story_name_normalized = self._normalize_name(story_name_from_class)
        
        epics = story_graph.get('epics', [])
        
        for epic in epics:
            sub_epics = epic.get('sub_epics', [])
            for sub_epic in sub_epics:
                sub_epic_name = sub_epic.get('name', '')
                sub_epic_name_norm = self._normalize_name(sub_epic_name) if sub_epic_name else ''
                
    # ... (truncated)
```

[!] WARNING (line 420)
Function "_find_closest_sub_epic_names" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _find_closest_sub_epic_names(self, file_name: str, sub_epic_names: List[str], max_suggestions: int = 5) -> List[str]:
        if not sub_epic_names:
            return []
        
        scored_names = []
        file_name_lower = file_name.lower()
        
        for sub_epic_name in sub_epic_names:
            sub_epic_lower = sub_epic_name.lower()
            
            score = 0
            
            if file_name_lower == sub_epic_lower:
    # ... (truncated)
```

[!] WARNING (line 451)
Function "_is_helper_file_only" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return [name for _, name in scored_names[:max_suggestions]]
    
    def _is_helper_file_only(self, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.name.startswith('Test'):
                        return False
                elif isinstance(node, ast.FunctionDef):
                    if node.name.startswith('test_'):
                        return False
            
    # ... (truncated)
```

---

## simplify_control_flow
**code_representation_scanner.py** - 1 violation(s)

[!] WARNING (line 17)
Function "scan_domain_concept" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    ]
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        node_name_lower = node.name.lower()
        for pattern in self.ABSTRACT_PATTERNS:
            if pattern in node_name_lower:
                violations.append(
                    Violation(
                        rule=rule_obj,
                        violation_message=f'Domain concept "{node.name}" uses abstract terminology. Domain models should represent code closely - refactor code if needed.',
                        location=node.map_location('name'),
                        line_number=None,
                        severity='info'
    # ... (truncated)
```

---

## simplify_control_flow
**code_scanner.py** - 2 violation(s)

[!] WARNING (line 38)
Function "_extract_domain_terms" has nesting depth of 12 - use guard clauses and extract nested blocks to reduce nesting

```python
        return []
    
    def _extract_domain_terms(self, story_graph: Dict[str, Any]) -> set:
        domain_terms = set()
        
        common_domain_terms = {
            'json', 'data', 'param', 'params', 'parameter', 'parameters',
            'var', 'vars', 'variable', 'variables',
            'method', 'methods', 'class', 'classes', 'call', 'calls',
            'config', 'configuration', 'configurations',
            'agent', 'bot', 'workflow', 'story', 'epic', 'scenario', 'action',
            'behavior', 'rule', 'rules', 'validation', 'validate', 'scanner',
            'file', 'files', 'directory', 'directories', 'path', 'paths',
            'state', 'states', 'tool', 'tools', 'server', 'catalog', 'metadata'
        }
    # ... (truncated)
```

[!] WARNING (line 195)
Function "_extract_code_snippet" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            return None
    
    def _extract_code_snippet(self, content: str, ast_node: Optional[ast.AST] = None, 
                             start_line: Optional[int] = None, end_line: Optional[int] = None,
                             context_before: int = 2, max_lines: int = 50) -> str:
        lines = content.split('\n')
        
        if ast_node is not None:
            start_line_0 = ast_node.lineno - 1 if hasattr(ast_node, 'lineno') and ast_node.lineno else 0
            
            if hasattr(ast_node, 'end_lineno') and ast_node.end_lineno:
                end_line_0 = ast_node.end_lineno
            else:
                end_line_0 = start_line_0 + 1
                for node in ast.walk(ast_node):
    # ... (truncated)
```

---

## simplify_control_flow
**complete_refactoring_scanner.py** - 1 violation(s)

[!] WARNING (line 26)
Function "_check_fallback_legacy_support" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_fallback_legacy_support(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        fallback_comment_pattern = re.compile(
            r'#\s*(fallback|legacy).*',
            re.IGNORECASE
        )
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if fallback_comment_pattern.match(stripped):
                code_line_num = None
    # ... (truncated)
```

---

## simplify_control_flow
**complexity_metrics.py** - 5 violation(s)

[!] WARNING (line 8)
Function "cyclomatic_complexity" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def cyclomatic_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 1
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Assert):
                complexity += 1
        
        return complexity
    
```

[!] WARNING (line 22)
Function "cognitive_complexity" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def cognitive_complexity(func_node: ast.FunctionDef) -> int:
        complexity = 0
        nesting_level = 0
        
        def visit_node(node: ast.AST, level: int):
            nonlocal complexity
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.With):
                complexity += 1 + level
    # ... (truncated)
```

[!] WARNING (line 236)
Function "_get_accessed_attributes" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def _get_accessed_attributes(method_node: ast.FunctionDef, class_node: ast.ClassDef) -> Set[str]:
        attributes = set()
        
        class_attrs = set()
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        class_attrs.add(target.id)
        
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == 'self':
    # ... (truncated)
```

[!] WARNING (line 297)
Function "detect_class_responsibilities_with_examples" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def detect_class_responsibilities_with_examples(class_node: ast.ClassDef) -> Dict[str, List[Dict[str, Any]]]:
        methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
        
        if len(methods) == 0:
            return {}
        
        responsibility_groups: Dict[str, List[Dict[str, Any]]] = {}
        
        for method in methods:
            responsibilities_detailed = ComplexityMetrics.detect_responsibilities_with_examples(method)
            if not responsibilities_detailed:
                if 'General' not in responsibility_groups:
                    responsibility_groups['General'] = []
    # ... (truncated)
```

[!] WARNING (line 26)
Function "visit_node" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        nesting_level = 0
        
        def visit_node(node: ast.AST, level: int):
            nonlocal complexity
            
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.With):
                complexity += 1 + level
                for child in ast.iter_child_nodes(node):
                    visit_node(child, level + 1)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1 + level
    # ... (truncated)
```

---

## simplify_control_flow
**consistent_vocabulary_scanner.py** - 1 violation(s)

[!] WARNING (line 41)
Function "_check_vocabulary_consistency" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return list(set(terms))
    
    def _check_vocabulary_consistency(self, content: str, domain_terms: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        content_lower = content.lower()
        
        synonym_map = {
            'data': ['info', 'information', 'content'],
            'user': ['person', 'customer', 'client'],
            'system': ['application', 'app', 'service'],
        }
        
        for domain_term, synonyms in synonym_map.items():
            if domain_term in domain_terms:
    # ... (truncated)
```

---

## simplify_control_flow
**cover_all_paths_scanner.py** - 1 violation(s)

[!] WARNING (line 11)
Function "scan_file" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
class CoverAllPathsScanner(TestScanner):
    
    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations = []
        
        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations
        
        content, lines, tree = parsed
        
        functions = Functions(tree)
        test_methods = [function.node for function in functions.get_many_functions if function.node.name.startswith('test_')]
        
        for test_method in test_methods:
    # ... (truncated)
```

---

## simplify_control_flow
**dead_code_scanner.py** - 3 violation(s)

[!] WARNING (line 13)
Function "scan" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
class DeadCodeScanner(CodeScanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        violations = []
        
        all_files = []
        if code_files:
            all_files.extend(code_files)
    # ... (truncated)
```

[!] WARNING (line 115)
Function "_analyze_file" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _analyze_file(self, file_path: Path) -> Tuple[Dict[str, Tuple[int, str]], Set[str]]:
        definitions = {}
        usages = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.debug(f"Skipping {file_path}: {e}")
            return definitions, usages
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
    # ... (truncated)
```

[!] WARNING (line 153)
Function "_analyze_private_members" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return definitions, usages
    
    def _analyze_private_members(self, tree: ast.AST) -> Tuple[Dict[str, Tuple[int, str]], Set[str]]:
        private_defs = {}
        private_usages = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if item.name.startswith('_') and not item.name.startswith('__'):
                            private_defs[item.name] = (item.lineno, class_name)
                
    # ... (truncated)
```

---

## simplify_control_flow
**delegation_code_scanner.py** - 3 violation(s)

[!] WARNING (line 30)
Function "_check_delegation" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_delegation(self, class_node: ast.ClassDef, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        is_collection_class = self._is_collection_class(class_node.name)
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.FunctionDef):
                if node.name == '__init__':
                    continue
                
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.For):
                        if isinstance(stmt.iter, ast.Attribute):
    # ... (truncated)
```

[!] WARNING (line 76)
Function "_is_plain_collection" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return (name_lower.endswith('s') and len(name_lower) > 3) or 'collection' in name_lower
    
    def _is_plain_collection(self, class_node: ast.ClassDef, attr_name: str, content: str) -> bool:
        attr_name_lower = attr_name.lower()
        
        if attr_name_lower.startswith('_'):
            plain_list_indicators = ['pattern', 'spec', 'config', 'item', 'entry', 'element', 'adapter', 'line', 'file', 'path']
            if any(indicator in attr_name_lower for indicator in plain_list_indicators):
                return True
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id == attr_name:
                    if isinstance(node.annotation, ast.Subscript):
                        if isinstance(node.annotation.value, ast.Name):
    # ... (truncated)
```

[!] WARNING (line 106)
Function "_is_class_constant" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_class_constant(self, class_node: ast.ClassDef, attr_name: str) -> bool:
        attr_name_upper = attr_name.upper()
        
        if attr_name == attr_name_upper or attr_name.isupper():
            for node in class_node.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == attr_name:
                            if isinstance(node.value, (ast.List, ast.Dict, ast.Tuple)):
                                return True
                        elif isinstance(target, ast.Attribute) and target.attr == attr_name:
                            if isinstance(node.value, (ast.List, ast.Dict, ast.Tuple)):
                                return True
    # ... (truncated)
```

---

## simplify_control_flow
**dependency_chaining_code_scanner.py** - 4 violation(s)

[!] WARNING (line 30)
Function "_check_dependency_chaining" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_dependency_chaining(self, class_node: ast.ClassDef, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        init_method = None
        init_params = []
        for node in ast.walk(class_node):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                init_method = node
                init_params = [arg.arg for arg in node.args.args if arg.arg != 'self']
                break
        
        instance_attrs = self._collect_instance_attributes(class_node)
        
    # ... (truncated)
```

[!] WARNING (line 101)
Function "_collect_instance_attributes" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _collect_instance_attributes(self, class_node: ast.ClassDef) -> Set[str]:
        attrs = set()
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                            attrs.add(target.attr)
            
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == 'self':
                    attrs.add(node.attr)
    # ... (truncated)
```

[!] WARNING (line 122)
Function "_check_method_calls_for_instance_attrs" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return attrs
    
    def _check_method_calls_for_instance_attrs(
        self, func_node: ast.FunctionDef, class_name: str, file_path: Path, 
        rule_obj: Any, instance_attrs: Set[str]
    ) -> List[Dict[str, Any]]:
        violations = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
                        for arg in node.args:
                            violation = self._check_argument(
                                arg, node.func.attr, class_name, file_path, rule_obj, instance_attrs, func_node.lineno
    # ... (truncated)
```

[!] WARNING (line 141)
Function "_check_argument" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_argument(
        self, arg_node: ast.AST, method_name: str, class_name: str, file_path: Path, 
        rule_obj: Any, instance_attrs: Set[str], line_num: int
    ) -> Optional[Dict[str, Any]]:
        if isinstance(arg_node, ast.Attribute):
            if isinstance(arg_node.value, ast.Name) and arg_node.value.id == 'self':
                attr_name = arg_node.attr
                if attr_name in instance_attrs:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        return self._create_violation_with_snippet(
                            rule_obj=rule_obj,
                            violation_message=f'Passing self.{attr_name} as parameter to {method_name}(). Access it directly in the method through self.{attr_name} instead.',
    # ... (truncated)
```

---

## simplify_control_flow
**dependency_chaining_scanner.py** - 1 violation(s)

[!] WARNING (line 9)
Function "scan_domain_concept" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
class DependencyChainingScanner(DomainScanner):
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        has_instantiation = False
        instantiation_collaborators = []
        
        for i, responsibility_data in enumerate(node.responsibilities):
            responsibility_name = responsibility_data.get('name', '')
            resp_lower = responsibility_name.lower()
            
            if 'instantiated with' in resp_lower:
                has_instantiation = True
                collaborators = responsibility_data.get('collaborators', [])
    # ... (truncated)
```

---

## simplify_control_flow
**domain_language_scanner.py** - 1 violation(s)

[!] WARNING (line 23)
Function "scan_domain_concept" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    ]
    
    def scan_domain_concept(self, node: DomainConceptNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        node_name_lower = node.name.lower()
        for term in ['data', 'config', 'parameter', 'result']:
            if term in node_name_lower and not self._is_domain_specific(node.name):
                violations.append(
                    Violation(
                        rule=rule_obj,
                        violation_message=f'Domain concept "{node.name}" uses generic term "{term}". Use domain-specific language instead (e.g., "PortfolioData" → "Portfolio", "TargetConfig" → "TargetAllocation").',
                        location=node.map_location('name'),
                        line_number=None,
                        severity='warning'
    # ... (truncated)
```

---

## simplify_control_flow
**duplication_scanner.py** - 29 violation(s)

[!] WARNING (line 237)
Function "_is_simple_delegation" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_simple_delegation(self, func_node: ast.FunctionDef) -> bool:
        if self._is_simple_property_getter(func_node):
            return True
        
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        if len(executable_body) == 1:
            stmt = executable_body[0]
            if isinstance(stmt, ast.Return) and stmt.value:
                if isinstance(stmt.value, (ast.Call, ast.Subscript)):
                    if isinstance(stmt.value, ast.Call):
                        if isinstance(stmt.value.func, ast.Attribute):
                            if isinstance(stmt.value.func.value, ast.Name) and stmt.value.func.value.id == 'self':
                                return True
    # ... (truncated)
```

[!] WARNING (line 265)
Function "_is_simple_property_getter" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_simple_property_getter(self, func_node: ast.FunctionDef) -> bool:
        is_property = False
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                is_property = True
                break
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ('setter', 'deleter'):
                    pass
                elif hasattr(decorator, 'value') and isinstance(decorator.value, ast.Name):
                    if decorator.value.id == 'property':
                        is_property = True
                        break
    # ... (truncated)
```

[!] WARNING (line 299)
Function "_check_duplicate_code_blocks" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _check_duplicate_code_blocks(self, functions: List[tuple], lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        all_blocks = []
        for func_tuple in functions:
            func_name, func_body, func_line, func_node, _ = func_tuple
            blocks = self._extract_code_blocks(func_node, func_line, func_name)
            all_blocks.extend(blocks)
        
        SIMILARITY_THRESHOLD = 0.90
        
        comparison_count = 0
        similarity_scores = []
    # ... (truncated)
```

[!] WARNING (line 690)
Function "_extract_subtrees_from_function" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return blocks
    
    def _extract_subtrees_from_function(self, func_node: ast.FunctionDef, min_nodes: int, max_nodes: int) -> List[ast.AST]:
        subtrees = []
        
        control_structures = (ast.If, ast.For, ast.While, ast.Try, ast.With, 
                             ast.AsyncFor, ast.AsyncWith)
        
        def extract_from_node(node):
            if isinstance(node, control_structures):
                num_nodes = len(list(ast.walk(node)))
                if min_nodes <= num_nodes <= max_nodes:
                    subtrees.append(node)
            
            if hasattr(node, 'body') and isinstance(node.body, list):
    # ... (truncated)
```

[!] WARNING (line 741)
Function "_get_statement_end_line" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _get_statement_end_line(self, stmt: ast.stmt) -> int:
        if hasattr(stmt, 'end_lineno') and stmt.end_lineno:
            return stmt.end_lineno
        
        if isinstance(stmt, ast.If):
            end_line = stmt.lineno
            if stmt.body:
                end_line = max(end_line, self._get_body_end_line(stmt.body))
            if stmt.orelse:
                end_line = max(end_line, self._get_body_end_line(stmt.orelse))
            return end_line
        elif isinstance(stmt, (ast.For, ast.While, ast.AsyncFor)):
            end_line = stmt.lineno
    # ... (truncated)
```

[!] WARNING (line 802)
Function "_is_mostly_helper_calls" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_mostly_helper_calls(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        helper_count = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
            
    # ... (truncated)
```

[!] WARNING (line 849)
Function "_is_only_helper_calls" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return (helper_count / total_count) >= 0.6
    
    def _is_only_helper_calls(self, statements: List[ast.stmt]) -> bool:
        helper_patterns = [
            'given_', 'when_', 'then_',
            'create_', 'build_', 'make_', 'generate_',
            'verify_', 'assert_', 'check_', 'ensure_',
            'setup_', 'bootstrap_', 'initialize_',
            'get_', 'load_', 'fetch_'
        ]
        
        for stmt in statements:
            if isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call):
                    func_name = self._get_function_name(stmt.value.func)
    # ... (truncated)
```

[!] WARNING (line 917)
Function "_count_actual_code_statements" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _count_actual_code_statements(self, statements: List[ast.stmt]) -> int:
        count = 0
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            if isinstance(stmt, ast.Pass):
                continue
            
            if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign, 
                                 ast.Expr, ast.Return, ast.Raise, ast.Assert,
                                 ast.Delete, ast.Import, ast.ImportFrom,
                                 ast.Global, ast.Nonlocal)):
    # ... (truncated)
```

[!] WARNING (line 949)
Function "_is_string_formatting_pattern" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return count
    
    def _is_string_formatting_pattern(self, statements: List[ast.stmt]) -> bool:
        """Check if this is primarily string formatting/building operations"""
        if not statements:
            return False
        
        string_ops = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
    # ... (truncated)
```

[!] WARNING (line 1006)
Function "_is_test_pattern" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return (assertion_count / total_count) >= 0.6
    
    def _is_test_pattern(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        helper_count = 0
        assertion_count = 0
        other_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            if isinstance(stmt, ast.Assert):
    # ... (truncated)
```

[!] WARNING (line 1042)
Function "_is_sequential_output_building" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return test_pattern_ratio >= 0.75 and other_count <= 1
    
    def _is_sequential_output_building(self, statements: List[ast.stmt]) -> bool:
        """Check if this is just sequential appends/extends to any list (common output building)"""
        if not statements or len(statements) < 3:
            return False
        
        append_count = 0
        total_count = 0
        has_loop_with_appends = False
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
    # ... (truncated)
```

[!] WARNING (line 1092)
Function "_is_logging_or_output_pattern" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_logging_or_output_pattern(self, statements: List[ast.stmt]) -> bool:
        """Check if this is primarily logging, printing, or string output"""
        if not statements:
            return False
        
        output_count = 0
        total_count = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
            total_count += 1
    # ... (truncated)
```

[!] WARNING (line 1150)
Function "_is_list_building_pattern" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return (output_count / total_count) >= 0.6
    
    def _is_list_building_pattern(self, statements: List[ast.stmt]) -> bool:
        if not statements:
            return False
        
        list_building_count = 0
        total_count = 0
        has_append = False
        sequential_appends = 0
        
        for stmt in statements:
            if self._is_docstring_or_comment(stmt):
                continue
            
    # ... (truncated)
```

[!] WARNING (line 1206)
Function "_is_simple_property" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return (list_building_count / total_count) >= 0.7
    
    def _is_simple_property(self, func_node: ast.FunctionDef) -> bool:
        if not func_node.decorator_list:
            return False
        
        has_property_decorator = False
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                has_property_decorator = True
                break
            elif isinstance(decorator, ast.Attribute):
                if decorator.attr in ('setter', 'deleter'):
                    has_property_decorator = True
                    break
    # ... (truncated)
```

[!] WARNING (line 1230)
Function "_is_simple_constructor" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_simple_constructor(self, func_node: ast.FunctionDef) -> bool:
        if func_node.name != '__init__':
            return False
        
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
        
        self_assignments = 0
        other_statements = 0
        
        for stmt in executable_body:
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                if isinstance(stmt, ast.Assign):
                    targets = stmt.targets
    # ... (truncated)
```

[!] WARNING (line 1283)
Function "_operates_on_different_domains" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return entities
    
    def _operates_on_different_domains(self, block1: Dict[str, Any], block2: Dict[str, Any]) -> bool:
        domain_patterns1 = self._extract_domain_entities(block1)
        domain_patterns2 = self._extract_domain_entities(block2)
        
        if domain_patterns1 and domain_patterns2:
            if domain_patterns1 != domain_patterns2:
                func1 = block1['func_name']
                func2 = block2['func_name']
                if abs(len(func1) - len(func2)) <= 3:
                    crud_ops = ['create', 'read', 'get', 'update', 'delete', 'remove', 
                               'save', 'load', 'fetch', 'set', 'find', 'search']
                    func1_lower = func1.lower()
                    func2_lower = func2.lower()
    # ... (truncated)
```

[!] WARNING (line 1321)
Function "_calls_different_methods" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _calls_different_methods(self, block1_nodes: List[ast.stmt], block2_nodes: List[ast.stmt]) -> bool:
        calls1 = self._extract_method_calls(block1_nodes)
        calls2 = self._extract_method_calls(block2_nodes)
        
        if not calls1 or not calls2:
            return False
        
        if len(calls1) == len(calls2) and len(calls1) >= 2:
            method_names1 = {call for call in calls1}
            method_names2 = {call for call in calls2}
            
            if method_names1 != method_names2:
                same_calls = len(method_names1 & method_names2)
    # ... (truncated)
```

[!] WARNING (line 1342)
Function "_extract_method_calls" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _extract_method_calls(self, nodes: List[ast.stmt]) -> List[str]:
        method_calls = []
        
        for node in nodes:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Attribute):
                    method_calls.append(call.func.attr)
                elif isinstance(call.func, ast.Name):
                    method_calls.append(call.func.id)
            elif isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    call = node.value
    # ... (truncated)
```

[!] WARNING (line 1362)
Function "_extract_iteration_targets" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return method_calls
    
    def _extract_iteration_targets(self, nodes: List[ast.stmt]) -> Set[str]:
        """Extract the names of collections being iterated over (e.g., 'behaviors', 'actions')"""
        targets = set()
        
        for node in nodes:
            for child in ast.walk(node):
                if isinstance(child, ast.For):
                    # Extract what we're iterating over
                    if isinstance(child.iter, ast.Attribute):
                        # e.g., self.bot.behaviors -> 'behaviors'
                        targets.add(child.iter.attr)
                    elif isinstance(child.iter, ast.Name):
                        # e.g., items -> 'items'
    # ... (truncated)
```

[!] WARNING (line 1379)
Function "_extract_list_building_targets" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return targets
    
    def _extract_list_building_targets(self, nodes: List[ast.stmt]) -> Set[str]:
        """Extract the names of lists being built (e.g., 'behavior_names', 'action_names')"""
        targets = set()
        
        for node in nodes:
            # Look for assignments creating empty lists
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.List) and len(node.value.elts) == 0:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            targets.add(target.id)
            
            # Look for append calls
    # ... (truncated)
```

[!] WARNING (line 1402)
Function "_is_sequential_appends_with_different_content" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return targets
    
    def _is_sequential_appends_with_different_content(self, block1_nodes: List[ast.stmt], block2_nodes: List[ast.stmt]) -> bool:
        """Check if both blocks are just sequential appends but with different string content"""
        
        # Extract append content from block 1
        appends1 = []
        for node in block1_nodes:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'append':
                    if node.value.args:
                        arg = node.value.args[0]
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            appends1.append(arg.value)
        
    # ... (truncated)
```

[!] WARNING (line 1444)
Function "_normalize_block" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _normalize_block(self, statements: List[ast.stmt]) -> Optional[str]:
        try:
            normalized_parts = []
            for stmt in statements:
                stmt_type = type(stmt).__name__
                
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                    if isinstance(stmt.value.value, str) and stmt.value.value.strip().startswith('"""'):
                        continue
                
                if isinstance(stmt, ast.Assign):
                    normalized_parts.append(f"ASSIGN({len(stmt.targets)}_targets)")
                
    # ... (truncated)
```

[!] WARNING (line 1477)
Function "_get_block_preview" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            return None
    
    def _get_block_preview(self, statements: List[ast.stmt]) -> str:
        try:
            if hasattr(ast, 'unparse'):
                preview_lines = []
                for stmt in statements:
                    if self._is_docstring_or_comment(stmt):
                        continue
                    preview_lines.append(ast.unparse(stmt))
                return "\n".join(preview_lines)
            else:
                return str(statements)
        except Exception as e:
            _safe_print(f"Error generating block preview: {e}")
    # ... (truncated)
```

[!] WARNING (line 1527)
Function "_compare_ast_nodes_deep" has nesting depth of 11 - use guard clauses and extract nested blocks to reduce nesting

```python
        return 0.0
    
    def _compare_ast_nodes_deep(self, node1: ast.AST, node2: ast.AST) -> float:
        if type(node1) != type(node2):
            return 0.0
        
        if isinstance(node1, ast.Assign):
            return self._compare_assign_nodes(node1, node2)
        elif isinstance(node1, ast.AugAssign):
            return self._compare_augassign_nodes(node1, node2)
        elif isinstance(node1, ast.Expr) and isinstance(node1.value, ast.Call):
            if isinstance(node2, ast.Expr) and isinstance(node2.value, ast.Call):
                return self._compare_call_nodes(node1.value, node2.value)
            return 0.0
        elif isinstance(node1, ast.Assert):
    # ... (truncated)
```

[!] WARNING (line 1634)
Function "_compare_expr_structure" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        return 0.7 + 0.3 * self._compare_expr_structure(node1.exc, node2.exc)
    
    def _compare_expr_structure(self, expr1: ast.expr, expr2: ast.expr) -> float:
        if type(expr1) != type(expr2):
            return 0.0
        
        if isinstance(expr1, ast.Call):
            return self._compare_call_nodes(expr1, expr2)
        elif isinstance(expr1, ast.Attribute):
            return 0.8 + 0.2 * self._compare_expr_structure(expr1.value, expr2.value)
        elif isinstance(expr1, ast.Name):
            return 0.9
        elif isinstance(expr1, ast.Constant):
            if type(expr1.value) == type(expr2.value):
                return 0.8
    # ... (truncated)
```

[!] WARNING (line 1666)
Function "_log_violation_details" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
            return 0.7
    
    def _log_violation_details(self, file_path: Path, violations: List[Dict[str, Any]], lines: List[str]) -> None:
        if not violations:
            return
        
        
        _safe_print(f"\n[{file_path}] Found {len(violations)} duplication violation(s):")
        
        for idx, violation in enumerate(violations, 1):
            line_num = violation.get('line_number', '?')
            msg = violation.get('violation_message', '')
            
            _safe_print(f"\n  Violation {idx} (line {line_num}):")
            
    # ... (truncated)
```

[!] WARNING (line 1716)
Function "_filter_files_by_package_proximity" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        _safe_print("")
    
    def _filter_files_by_package_proximity(
        self,
        changed_files: List[Path],
        all_files: List[Path],
        max_parent_levels: int = 3,
        max_files: int = 20
    ) -> List[Path]:
        """Filter all_files to only include files in nearby packages.
        
        Priority:
        1. Same package (immediate siblings)
        2. Parent package
        3. Parent's parent package (up to max_parent_levels)
    # ... (truncated)
```

[!] WARNING (line 1788)
Function "scan_cross_file" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return nearby_files
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: int = 20
    ) -> List[Dict[str, Any]]:
        violations = []
        
        if all_test_files is None:
    # ... (truncated)
```

[!] WARNING (line 696)
Function "extract_from_node" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
                             ast.AsyncFor, ast.AsyncWith)
        
        def extract_from_node(node):
            if isinstance(node, control_structures):
                num_nodes = len(list(ast.walk(node)))
                if min_nodes <= num_nodes <= max_nodes:
                    subtrees.append(node)
            
            if hasattr(node, 'body') and isinstance(node.body, list):
                for child in node.body:
                    extract_from_node(child)
            
            if hasattr(node, 'orelse') and isinstance(node.orelse, list):
                for child in node.orelse:
                    extract_from_node(child)
    # ... (truncated)
```

---

## simplify_control_flow
**exact_variable_names_scanner.py** - 2 violation(s)

[!] WARNING (line 30)
Function "_extract_domain_concepts" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _extract_domain_concepts(self, story_graph: Dict[str, Any]) -> List[str]:
        concepts = []
        epics = story_graph.get('epics', [])
        for epic in epics:
            domain_concepts_list = epic.get('domain_concepts', [])
            for concept in domain_concepts_list:
                if isinstance(concept, dict):
                    concept_name = concept.get('name', '')
                    if concept_name:
                        concepts.append(concept_name.lower())
        return concepts
    
```

[!] WARNING (line 42)
Function "_check_variable_names" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return concepts
    
    def _check_variable_names(self, test_node: ast.FunctionDef, domain_concepts: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        for node in ast.walk(test_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id.lower()
                        
                        if var_name in ['data', 'result', 'value', 'item', 'obj', 'thing']:
                            line_number = target.lineno if hasattr(target, 'lineno') else None
                            violation = Violation(
                                rule=rule_obj,
    # ... (truncated)
```

---

## simplify_control_flow
**excessive_guards_scanner.py** - 6 violation(s)

[!] WARNING (line 87)
Function "_is_guard_pattern" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_guard_pattern(self, test_node: ast.AST) -> bool:
        if isinstance(test_node, ast.Call):
            if isinstance(test_node.func, ast.Name):
                if test_node.func.id == 'hasattr':
                    return True
        
        if isinstance(test_node, ast.Call):
            if isinstance(test_node.func, ast.Name):
                if test_node.func.id == 'isinstance':
                    return True
        
        if isinstance(test_node, ast.Call):
            if isinstance(test_node.func, ast.Attribute):
    # ... (truncated)
```

[!] WARNING (line 136)
Function "_is_optional_config_check" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return defaults.get(message_key, f'Line {line_number}: Guard clause detected.')

    def _is_optional_config_check(self, guard_node: ast.If, source_lines: List[str]) -> bool:
        test = guard_node.test
        if isinstance(test, ast.Call) and isinstance(test.func, ast.Attribute) and test.func.attr == 'exists':
            if self._is_followed_by_creation_logic(guard_node, source_lines):
                return True
            return False
        
        if isinstance(test, ast.Call) and isinstance(test.func, ast.Name) and test.func.id == 'hasattr':
            return True
        
        if guard_node.body:
            first_stmt = guard_node.body[0]
            if isinstance(first_stmt, ast.Return):
    # ... (truncated)
```

[!] WARNING (line 193)
Function "_is_followed_by_creation_logic" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return any(pattern in var_name for pattern in optional_patterns)
    
    def _is_followed_by_creation_logic(self, guard_node: ast.If, source_lines: List[str]) -> bool:
        if guard_node.orelse:
            for stmt in guard_node.orelse:
                if self._contains_creation_call(stmt):
                    return True
        
        start_line = guard_node.lineno - 1
        end_line = guard_node.end_lineno if hasattr(guard_node, 'end_lineno') else start_line + len(guard_node.body) + 1
        
        if guard_node.orelse:
            for stmt in guard_node.orelse:
                if hasattr(stmt, 'lineno'):
                    stmt_start = stmt.lineno - 1
    # ... (truncated)
```

[!] WARNING (line 223)
Function "_contains_creation_call" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _contains_creation_call(self, node: ast.AST) -> bool:
        creation_methods = ['write_text', 'write_bytes', 'mkdir', 'touch']
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in creation_methods:
                        return True
        return False

```

[!] WARNING (line 259)
Function "_is_lazy_initialization" has nesting depth of 9 - use guard clauses and extract nested blocks to reduce nesting

```python
        return optional_params
    
    def _is_lazy_initialization(self, guard_node: ast.If, func_node: ast.FunctionDef) -> bool:
        """Check if this is a lazy initialization pattern in a property."""
        # Check if function is a property
        is_property = False
        if func_node.decorator_list:
            for decorator in func_node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == 'property':
                    is_property = True
                    break
                if isinstance(decorator, ast.Attribute) and decorator.attr in ('getter', 'setter'):
                    is_property = True
                    break
        
    # ... (truncated)
```

[!] WARNING (line 295)
Function "_check_guard_pattern" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _check_guard_pattern(self, guard_node: ast.If, file_path: Path, rule_obj: Any, source_lines: List[str], content: str, func_node: ast.FunctionDef = None, optional_params: set = None) -> Optional[Dict[str, Any]]:
        test = guard_node.test
        
        if optional_params is None:
            optional_params = set()
        
        # Check if this is lazy initialization in a property
        if func_node and self._is_lazy_initialization(guard_node, func_node):
            return None
        
        # Check if this is a None check for a parameter with default None
        if isinstance(test, ast.Compare):
            for op in test.ops:
    # ... (truncated)
```

---

## simplify_control_flow
**full_result_assertions_scanner.py** - 4 violation(s)

[!] WARNING (line 34)
Function "scan_file" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    }

    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations

        content, lines, tree = parsed

        for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]:
            alias_targets = self._collect_result_aliases(func)
            if self._has_full_object_assert(func, alias_targets):
                continue
    # ... (truncated)
```

[!] WARNING (line 62)
Function "_is_single_field_assert" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations

    def _is_single_field_assert(self, test_expr: ast.AST, aliases: Set[str]) -> bool:
        targets = aliases or set()
        if isinstance(test_expr, ast.Compare):
            left = test_expr.left
            if self._is_subscript_or_attr_on_target(left, targets):
                return True
            for comp in test_expr.comparators:
                if self._is_subscript_or_attr_on_target(comp, targets):
                    return True
        if isinstance(test_expr, ast.Compare):
            sides = [test_expr.left] + list(test_expr.comparators)
            for side in sides:
                if isinstance(side, ast.Call) and isinstance(side.func, ast.Name) and side.func.id == "len":
    # ... (truncated)
```

[!] WARNING (line 101)
Function "_has_full_object_assert" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return isinstance(node, ast.Name) and node.id in (self.TARGET_NAMES | aliases)

    def _has_full_object_assert(self, func_node: ast.FunctionDef, aliases: Set[str]) -> bool:
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare):
                left = node.test.left
                comps = node.test.comparators
                if any(self._is_target_name(expr, aliases) for expr in [left, *comps]):
                    if not any(isinstance(expr, (ast.Subscript, ast.Attribute)) for expr in [left, *comps]):
                        return True
        return False

```

[!] WARNING (line 111)
Function "_collect_result_aliases" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False

    def _collect_result_aliases(self, func_node: ast.FunctionDef) -> Set[str]:
        aliases: Set[str] = set()
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
                source = node.value
                source_name = None
                if isinstance(source, ast.Name) and source.id in (self.TARGET_NAMES | aliases):
                    source_name = source.id
                elif isinstance(source, ast.Call):
                    source_name = self._infer_call_name(source)
                    if source_name and source_name in self.TARGET_NAMES:
                        pass
    # ... (truncated)
```

---

## simplify_control_flow
**function_size_scanner.py** - 4 violation(s)

[!] WARNING (line 135)
Function "_get_multi_line_expression_line_numbers" has nesting depth of 9 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations[0] if violations else None
    
    def _get_multi_line_expression_line_numbers(self, func_node: ast.FunctionDef) -> set:
        multi_line_lines = set()
        
        def visit_statement(stmt_node):
            if hasattr(stmt_node, 'end_lineno') and hasattr(stmt_node, 'lineno') and stmt_node.end_lineno and stmt_node.lineno:
                if stmt_node.end_lineno > stmt_node.lineno:
                    if isinstance(stmt_node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                        if hasattr(stmt_node, 'value') and stmt_node.value:
                            value = stmt_node.value
                            if hasattr(value, 'end_lineno') and hasattr(value, 'lineno') and value.end_lineno and value.lineno:
                                if value.end_lineno > value.lineno:
                                    for line_num in range(value.lineno + 1, value.end_lineno + 1):
                                        multi_line_lines.add(line_num)
    # ... (truncated)
```

[!] WARNING (line 170)
Function "_get_data_structure_line_numbers" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return multi_line_lines
    
    def _get_data_structure_line_numbers(self, func_node: ast.FunctionDef) -> set:
        data_structure_lines = set()
        
        top_level_data_structures = []
        
        def visit_node(node, parent_is_ds=False):
            is_data_structure = isinstance(node, (ast.List, ast.Dict, ast.Set, ast.Tuple))
            
            if is_data_structure and not parent_is_ds:
                top_level_data_structures.append(node)
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, parent_is_ds=is_data_structure)
    # ... (truncated)
```

[!] WARNING (line 196)
Function "_get_comment_and_docstring_line_numbers" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return data_structure_lines
    
    def _get_comment_and_docstring_line_numbers(self, func_node: ast.FunctionDef, source_lines: List[str], func_start_line: int) -> set:
        comment_and_docstring_lines = set()
        
        if func_node.body:
            first_stmt = func_node.body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, (ast.Str, ast.Constant)):
                string_value = first_stmt.value
                if isinstance(string_value, ast.Constant) and isinstance(string_value.value, str):
                    if hasattr(first_stmt, 'end_lineno') and hasattr(first_stmt, 'lineno') and first_stmt.end_lineno and first_stmt.lineno:
                        for line_num in range(first_stmt.lineno, first_stmt.end_lineno + 1):
                            comment_and_docstring_lines.add(line_num)
                elif isinstance(string_value, ast.Str):
                    if hasattr(first_stmt, 'end_lineno') and hasattr(first_stmt, 'lineno') and first_stmt.end_lineno and first_stmt.lineno:
    # ... (truncated)
```

[!] WARNING (line 138)
Function "visit_statement" has nesting depth of 9 - use guard clauses and extract nested blocks to reduce nesting

```python
        multi_line_lines = set()
        
        def visit_statement(stmt_node):
            if hasattr(stmt_node, 'end_lineno') and hasattr(stmt_node, 'lineno') and stmt_node.end_lineno and stmt_node.lineno:
                if stmt_node.end_lineno > stmt_node.lineno:
                    if isinstance(stmt_node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                        if hasattr(stmt_node, 'value') and stmt_node.value:
                            value = stmt_node.value
                            if hasattr(value, 'end_lineno') and hasattr(value, 'lineno') and value.end_lineno and value.lineno:
                                if value.end_lineno > value.lineno:
                                    for line_num in range(value.lineno + 1, value.end_lineno + 1):
                                        multi_line_lines.add(line_num)
                    
                    elif isinstance(stmt_node, ast.Expr):
                        if hasattr(stmt_node, 'value') and stmt_node.value:
    # ... (truncated)
```

---

## simplify_control_flow
**given_precondition_scanner.py** - 2 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
class GivenPreconditionScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_steps = self._get_scenario_steps(scenario)
                
                for step_idx, step in enumerate(scenario_steps):
                    if step.startswith('Given') or step.startswith('And'):
                        violation = self._check_given_is_functionality(step, node, scenario_idx, step_idx, rule_obj)
    # ... (truncated)
```

[!] WARNING (line 28)
Function "_get_scenario_steps" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_scenario_steps(self, scenario: Dict[str, Any]) -> List[str]:
        steps = []
        if isinstance(scenario, dict):
            if 'steps' in scenario:
                steps = scenario['steps']
            elif 'scenario' in scenario:
                scenario_text = scenario['scenario']
                if isinstance(scenario_text, str):
                    steps = [s.strip() for s in scenario_text.split('\n') if s.strip()]
        return steps
    
```

---

## simplify_control_flow
**given_state_not_actions_scanner.py** - 2 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
class GivenStateNotActionsScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_steps = self._get_scenario_steps(scenario)
                
                for step_idx, step in enumerate(scenario_steps):
                    if step.startswith('Given') or step.startswith('And'):
                        violation = self._check_given_is_action(step, node, scenario_idx, step_idx, rule_obj)
    # ... (truncated)
```

[!] WARNING (line 28)
Function "_get_scenario_steps" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_scenario_steps(self, scenario: Dict[str, Any]) -> List[str]:
        steps = []
        
        if isinstance(scenario, dict):
            if 'steps' in scenario:
                steps = scenario['steps']
            elif 'scenario' in scenario:
                scenario_text = scenario['scenario']
                if isinstance(scenario_text, str):
                    steps = [s.strip() for s in scenario_text.split('\n') if s.strip()]
            elif 'given' in scenario or 'when' in scenario or 'then' in scenario:
                if 'given' in scenario:
                    given = scenario['given']
    # ... (truncated)
```

---

## simplify_control_flow
**given_when_then_helpers_scanner.py** - 3 violation(s)

[!] WARNING (line 43)
Function "_get_helper_functions" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_helper_functions(self, tree: ast.AST, content: str) -> Set[str]:
        helpers = set()
        
        defined_helpers = self._get_defined_helper_functions(tree)
        helpers.update(defined_helpers.keys())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ''
                if any(helper_mod in module for helper_mod in ['conftest', 'test_helpers', '_helpers']):
                    for alias in node.names:
                        name = alias.name
                        for pattern in self.HELPER_PATTERNS:
    # ... (truncated)
```

[!] WARNING (line 62)
Function "_get_defined_helper_functions" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return helpers
    
    def _get_defined_helper_functions(self, tree: ast.AST) -> Dict[str, int]:
        helpers = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                for pattern in self.HELPER_PATTERNS:
                    if re.match(pattern, func_name, re.IGNORECASE):
                        helpers[func_name] = node.lineno
                        break
        
        return helpers
    
```

[!] WARNING (line 140)
Function "_find_inline_code_blocks" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _find_inline_code_blocks(self, test_node: ast.FunctionDef, test_body_lines: List[str],
                                 helper_functions: Set[str], tree: ast.AST) -> List[Tuple[int, int, List[str]]]:
        blocks = []
        current_block_start = None
        current_block_lines = []
        
        body_start_line = test_node.lineno
        
        docstring_range = self._get_docstring_line_range(test_node)
        
        in_multiline_call = False
        paren_balance = 0
        
    # ... (truncated)
```

---

## simplify_control_flow
**import_placement_scanner.py** - 2 violation(s)

[!] WARNING (line 29)
Function "_find_import_section_end" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _find_import_section_end(self, lines: List[str]) -> int:
        import_section_end = 0
        
        while import_section_end < len(lines) and not lines[import_section_end].strip():
            import_section_end += 1
        
        if import_section_end < len(lines):
            line = lines[import_section_end].strip()
            if line.startswith('"""') or line.startswith("'''"):
                quote_char = line[:3]
                import_section_end += 1
                while import_section_end < len(lines):
                    if quote_char in lines[import_section_end]:
    # ... (truncated)
```

[!] WARNING (line 105)
Function "_skip_try_import_error_block" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return stripped == 'try:' or stripped.startswith('try:')
    
    def _skip_try_import_error_block(self, lines: List[str], start_line: int) -> int:
        if start_line >= len(lines):
            return start_line
        
        try_line = lines[start_line]
        base_indent = len(try_line) - len(try_line.lstrip())
        
        current_line = start_line + 1
        
        while current_line < len(lines):
            line = lines[current_line]
            stripped = line.strip()
            
    # ... (truncated)
```

---

## simplify_control_flow
**intention_revealing_names_scanner.py** - 4 violation(s)

[!] WARNING (line 63)
Function "_check_variable_names" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_variable_names(self, tree: ast.AST, file_path: Path, rule_obj: Any, content: str, domain_terms: set = None, docstring_ranges: List[tuple] = None) -> List[Dict[str, Any]]:
        violations = []
        
        if domain_terms is None:
            domain_terms = set()
        if docstring_ranges is None:
            docstring_ranges = []
        
        generic_names = ['info', 'thing', 'stuff', 'temp']
        
        acceptable_single_letter_names = self._collect_loop_and_comprehension_var_names(tree)
        
        for node in ast.walk(tree):
    # ... (truncated)
```

[!] WARNING (line 153)
Function "_collect_loop_and_comprehension_var_names" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
            ).to_dict()
    
    def _collect_loop_and_comprehension_var_names(self, tree: ast.AST) -> set:
        acceptable_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                self._add_target_var_names(node.target, acceptable_names)
            
            elif isinstance(node, ast.ExceptHandler):
                if node.name:
                    acceptable_names.add(node.name)
            
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in node.generators:
    # ... (truncated)
```

[!] WARNING (line 251)
Function "_get_docstring_ranges" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_docstring_ranges(self, tree: ast.AST) -> List[tuple]:
        docstring_ranges = []
        
        def visit_node(node):
            if hasattr(node, 'body') and isinstance(node.body, list) and len(node.body) > 0:
                first_stmt = node.body[0]
                if isinstance(first_stmt, ast.Expr):
                    if isinstance(first_stmt.value, (ast.Constant, ast.Str)):
                        if isinstance(first_stmt.value, ast.Constant):
                            docstring_value = first_stmt.value.value
                        else:
                            docstring_value = first_stmt.value.s
                        
    # ... (truncated)
```

[!] WARNING (line 254)
Function "visit_node" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        docstring_ranges = []
        
        def visit_node(node):
            if hasattr(node, 'body') and isinstance(node.body, list) and len(node.body) > 0:
                first_stmt = node.body[0]
                if isinstance(first_stmt, ast.Expr):
                    if isinstance(first_stmt.value, (ast.Constant, ast.Str)):
                        if isinstance(first_stmt.value, ast.Constant):
                            docstring_value = first_stmt.value.value
                        else:
                            docstring_value = first_stmt.value.s
                        
                        if isinstance(docstring_value, str):
                            start_line = first_stmt.lineno if hasattr(first_stmt, 'lineno') else None
                            if start_line:
    # ... (truncated)
```

---

## simplify_control_flow
**meaningful_context_scanner.py** - 2 violation(s)

[!] WARNING (line 29)
Function "_check_magic_numbers" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_magic_numbers(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        content = '\n'.join(lines)
        
        magic_number_patterns = [
            r'\b(200|404|500)\b',  # HTTP status codes
            r'\b(86400|3600)\b',  # Time constants (seconds in day/hour)
        ]
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip lines that are defining the patterns themselves (scanner definitions)
    # ... (truncated)
```

[!] WARNING (line 80)
Function "_check_numbered_variables" has nesting depth of 13 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_numbered_variables(self, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        try:
            tree = ast.parse(content, filename=str(file_path))
            
            numbered_var_pattern = re.compile(r'^\w+\d+$')
            
            # Meaningful patterns that should NOT be flagged as violations
            meaningful_patterns = [
                # Indexing schemes (0-indexed, 1-indexed)
                re.compile(r'^.+_(0|1)$'),  # e.g., start_line_0, end_line_1
                # ANY variable ending in 1 or 2 (comparison/pairing pattern)
    # ... (truncated)
```

---

## simplify_control_flow
**minimize_mutable_state_scanner.py** - 1 violation(s)

[!] WARNING (line 24)
Function "_check_mutable_patterns" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_mutable_patterns(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        mutable_patterns = [
            r'\.push\s*\(',
            r'\.pop\s*\(',
            r'\.splice\s*\(',
            r'\+\+\s*;',
            r'--\s*;',
            r'=\s*\{.*\}\s*\.\w+\s*=',
            r'\.append\s*\(',
            r'\.extend\s*\(',
            r'\.insert\s*\(',
    # ... (truncated)
```

---

## simplify_control_flow
**no_guard_clauses_scanner.py** - 2 violation(s)

[!] WARNING (line 28)
Function "_check_guard_clause_patterns" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_guard_clause_patterns(self, lines: List[str], file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        guard_patterns = [
            (r'if\s+(not\s+)?\w+\.exists\(\):', 'File existence check - test should fail if file missing'),
            (r'if\s+(not\s+)?isinstance\([^)]+\):', 'Type check guard clause - test should fail if wrong type'),
            (r'if\s+(not\s+)?hasattr\([^)]+\):', 'Attribute existence check - test should fail if attribute missing'),
            (r'if\s+(not\s+)?\w+:', 'Variable truthiness check - test should fail if variable is None/empty'),
        ]
        
        in_test_function = False
        test_function_indent = 0
        
    # ... (truncated)
```

[!] WARNING (line 93)
Function "_check_function_guard_clauses" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_function_guard_clauses(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.If):
                guard_patterns = [
                    self._is_file_exists_check,
                    self._is_type_check,
                    self._is_hasattr_check,
                    self._is_variable_truthiness_check,
                ]
                
                for pattern_check in guard_patterns:
    # ... (truncated)
```

---

## simplify_control_flow
**object_oriented_helpers_scanner.py** - 3 violation(s)

[!] WARNING (line 70)
Function "_parametrize_column_count" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        )

    def _parametrize_column_count(self, func_node: ast.FunctionDef) -> int:
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute) and decorator.func.attr == "parametrize":
                    if decorator.args:
                        first_arg = decorator.args[0]
                        if isinstance(first_arg, (ast.Constant, ast.Str)) and isinstance(first_arg.value, str):
                            columns = [c.strip() for c in first_arg.value.split(",") if c.strip()]
                            return len(columns)
        return 0

```

[!] WARNING (line 81)
Function "_given_when_then_calls" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return 0

    def _given_when_then_calls(self, func_node: ast.FunctionDef) -> int:
        count = 0
        for inner in ast.walk(func_node):
            if isinstance(inner, ast.Call):
                func = inner.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name.startswith(("given_", "when_", "then_")):
                    count += 1
        return count
    # ... (truncated)
```

[!] WARNING (line 95)
Function "_uses_helper" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return count

    def _uses_helper(self, func_node: ast.FunctionDef) -> bool:
        for inner in ast.walk(func_node):
            if isinstance(inner, ast.Call):
                if isinstance(inner.func, ast.Name) and "helper" in inner.func.id.lower():
                    return True
                if isinstance(inner.func, ast.Attribute) and "helper" in inner.func.attr.lower():
                    return True
            if isinstance(inner, ast.Assign):
                for target in inner.targets:
                    if isinstance(target, ast.Name) and "helper" in target.id.lower():
                        return True
        return False

```

---

## simplify_control_flow
**one_concept_per_test_scanner.py** - 1 violation(s)

[!] WARNING (line 100)
Function "_detect_multiple_concepts" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations[0] if violations else None
    
    def _detect_multiple_concepts(self, test_node: ast.FunctionDef, content: str) -> List[str]:
        concepts = []
        
        has_setup = False
        has_action = False
        has_validation = False
        has_cleanup = False
        
        for stmt in test_node.body:
            if isinstance(stmt, ast.Assign):
                has_setup = True
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = self._get_call_name(stmt.value)
    # ... (truncated)
```

---

## simplify_control_flow
**parameterized_tests_scanner.py** - 1 violation(s)

[!] WARNING (line 8)
Function "scan" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
class ParameterizedTestsScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
        rule_obj: Any = None,
        test_files: Optional[List['Path']] = None,
        code_files: Optional[List['Path']] = None,
        on_file_scanned: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        if not rule_obj:
            raise ValueError("rule_obj parameter is required for ParameterizedTestsScanner")
        
        violations = []
        story_map = StoryMap(story_graph)
    # ... (truncated)
```

---

## simplify_control_flow
**prefer_object_model_over_config_scanner.py** - 1 violation(s)

[!] WARNING (line 91)
Function "_is_in_exception_context" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return any(exc in file_str for exc in exception_paths)
    
    def _is_in_exception_context(self, lines: List[str], current_line: int) -> bool:
        current_indent = len(lines[current_line - 1]) - len(lines[current_line - 1].lstrip())
        
        for i in range(current_line - 2, max(0, current_line - 50), -1):
            line = lines[i]
            line_indent = len(line) - len(line.lstrip())
            
            if line_indent <= current_indent and ('def ' in line):
                for pattern in self.exception_patterns:
                    if re.search(pattern, line):
                        return True
                return False
        
    # ... (truncated)
```

---

## simplify_control_flow
**primitive_vs_object_scanner.py** - 1 violation(s)

[!] WARNING (line 67)
Function "_check_function_parameters" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _check_function_parameters(self, func_node: ast.FunctionDef, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if self._is_presentation_boundary(func_node.name, content, func_node):
            return violations
        
        # Skip __init__ methods - they often need primitives for construction
        if func_node.name == '__init__':
            return violations
        
        for arg in func_node.args.args:
            if arg.arg in ('self', 'cls'):
                continue
    # ... (truncated)
```

---

## simplify_control_flow
**property_encapsulation_code_scanner.py** - 2 violation(s)

[!] WARNING (line 28)
Function "_check_encapsulation" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_encapsulation(self, class_node: ast.ClassDef, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        class_source = ast.get_source_segment(content, class_node) or ''
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        field_name = target.id
                        if not field_name.startswith('_') and not field_name.startswith('__'):
                            parent = self._get_parent_function(node)
                            if parent and isinstance(parent, ast.FunctionDef) and parent.name == '__init__':
                                violations.append(
    # ... (truncated)
```

[!] WARNING (line 82)
Function "_get_parent_function" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_parent_function(self, node: ast.AST) -> Optional[ast.FunctionDef]:
        for parent in ast.walk(node):
            if isinstance(parent, ast.FunctionDef):
                for child in ast.walk(parent):
                    if child == node:
                        return parent
        return None

```

---

## simplify_control_flow
**real_implementations_scanner.py** - 7 violation(s)

[!] WARNING (line 188)
Function "_has_production_code_imports" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return imports
    
    def _has_production_code_imports(
        self, imports: List[ast.Import | ast.ImportFrom], src_locations: List[str], project_path: Path
    ) -> bool:
        if not imports:
            return False
        
        for imp in imports:
            if isinstance(imp, ast.ImportFrom):
                module = imp.module or ''
                if self._is_production_module(module, src_locations, project_path):
                    return True
            elif isinstance(imp, ast.Import):
                for alias in imp.names:
    # ... (truncated)
```

[!] WARNING (line 246)
Function "_is_test_infrastructure_import" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_test_infrastructure_import(self, imp: ast.Import | ast.ImportFrom) -> bool:
        test_infra_modules = ['pytest', 'pathlib', 'json', 'typing', 'unittest', 'mock', 'unittest.mock']
        
        if isinstance(imp, ast.ImportFrom):
            module = imp.module or ''
            return module.split('.')[0] in test_infra_modules if module else False
        elif isinstance(imp, ast.Import):
            for alias in imp.names:
                if alias.name.split('.')[0] in test_infra_modules:
                    return True
        return False
    
```

[!] WARNING (line 258)
Function "_is_empty_or_todo_only" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_empty_or_todo_only(self, method: ast.FunctionDef, source_lines: List[str]) -> bool:
        if not method.body:
            return True
        
        method_start = method.lineno - 1
        method_end = method.end_lineno if hasattr(method, 'end_lineno') else method_start + 50
        if method_start < len(source_lines):
            method_source = source_lines[method_start:method_end]
        else:
            method_source = []
        
        has_todo = any('TODO' in line or 'FIXME' in line for line in method_source)
        if has_todo:
    # ... (truncated)
```

[!] WARNING (line 305)
Function "_has_production_code_calls" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        return not has_actual_code
    
    def _has_production_code_calls(
        self, method: ast.FunctionDef, imports: List[ast.Import | ast.ImportFrom],
        src_locations: List[str], project_path: Path, file_path: Path = None, tree: ast.AST = None
    ) -> bool:
        calls = []
        for node in ast.walk(method):
            if isinstance(node, ast.Call):
                calls.append(node)
        
        if not calls:
            return False
        
        for call in calls:
    # ... (truncated)
```

[!] WARNING (line 348)
Function "_helper_calls_production_code" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _helper_calls_production_code(
        self, helper_name: str, file_path: Path, tree: ast.AST,
        src_locations: List[str], project_path: Path
    ) -> bool:
        helper_func = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == helper_name:
                helper_func = node
                break
        
        if helper_func:
            helper_imports = self._find_imports(tree)
    # ... (truncated)
```

[!] WARNING (line 403)
Function "_file_has_production_code_calls" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _file_has_production_code_calls(self, file_path: Path, src_locations: List[str], project_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            imports = self._find_imports(tree)
            
            if self._has_production_code_imports(imports, src_locations, project_path):
                return True
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if self._has_production_code_calls(node, imports, src_locations, project_path, file_path, tree):
                        return True
    # ... (truncated)
```

[!] WARNING (line 420)
Function "_is_production_function" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _is_production_function(
        self, name: str, imports: List[ast.Import | ast.ImportFrom],
        src_locations: List[str], project_path: Path
    ) -> bool:
        for imp in imports:
            if isinstance(imp, ast.ImportFrom):
                if imp.module and self._is_production_module(imp.module, src_locations, project_path):
                    for alias in imp.names:
                        if alias.asname == name or alias.name == name:
                            return True
            elif isinstance(imp, ast.Import):
                for alias in imp.names:
                    if alias.asname == name or alias.name == name:
    # ... (truncated)
```

---

## simplify_control_flow
**resource_oriented_code_scanner.py** - 2 violation(s)

[!] WARNING (line 59)
Function "scan_cross_file" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return []
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
        test_files: Optional[List[Path]] = None,
        code_files: Optional[List[Path]] = None,
        all_test_files: Optional[List[Path]] = None,
        all_code_files: Optional[List[Path]] = None,
        status_writer: Optional[Any] = None,
        max_cross_file_comparisons: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        violations = []
        
        all_files = []
    # ... (truncated)
```

[!] WARNING (line 153)
Function "_class_uses_as_attribute" has nesting depth of 10 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _class_uses_as_attribute(self, class_node: ast.ClassDef, loader_class_name: str, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding='utf-8')
            if loader_class_name not in content:
                return False
        except (UnicodeDecodeError, IOError):
            return False
        
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
    # ... (truncated)
```

---

## simplify_control_flow
**scanner_loader.py** - 1 violation(s)

[!] WARNING (line 22)
Function "_load_scanner_class" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return self._load_scanner_class(scanner_module_path)
    
    def _load_scanner_class(self, scanner_module_path: str) -> Tuple[Optional[type], Optional[str]]:
        try:
            module_path, class_name = scanner_module_path.rsplit('.', 1)
            
            import re
            scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
            
            paths_to_try = [
                module_path,
                f'agile_bot.src.scanners.{scanner_name}_scanner'
            ]
            
            if self.bot_name:
    # ... (truncated)
```

---

## simplify_control_flow
**scanner_registry.py** - 1 violation(s)

[!] WARNING (line 30)
Function "loads_scanner_class_with_error" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return scanner_class
    
    def loads_scanner_class_with_error(self, scanner_module_path: str) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        if not scanner_module_path:
            return None, None
        
        try:
            module_path, class_name = scanner_module_path.rsplit('.', 1)
            
            scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
            
            paths_to_try = [
                module_path,
                f'agile_bot.src.scanners.{scanner_name}_scanner'
            ]
    # ... (truncated)
```

---

## simplify_control_flow
**scanner_status_formatter.py** - 1 violation(s)

[!] WARNING (line 26)
Function "categorize_scanner_rules" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return lines

    def categorize_scanner_rules(self, validation_rules: List[Dict[str, Any]]) -> Dict:
        executed_rules = []
        load_failed_rules = []
        execution_failed_rules = []
        no_scanner_rules = []
        for rule_dict in validation_rules:
            category = self._get_rule_category(rule_dict)
            if category == 'executed':
                executed_rules.append(self._build_executed_rule_entry(rule_dict))
            elif category == 'load_failed':
                load_failed_rules.append(self._build_failed_rule_entry(rule_dict))
            elif category == 'execution_failed':
                execution_failed_rules.append(self._build_failed_rule_entry(rule_dict))
    # ... (truncated)
```

---

## simplify_control_flow
**scenarios_cover_all_cases_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
class ScenariosCoverAllCasesScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            if len(scenarios) > 0:
                has_happy_path = False
                has_edge_case = False
                has_error_case = False
                
                for scenario_idx, scenario in enumerate(scenarios):
    # ... (truncated)
```

---

## simplify_control_flow
**scenarios_on_story_docs_scanner.py** - 1 violation(s)

[!] WARNING (line 67)
Function "_extract_story_names_from_epic" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    return story_names

def _extract_story_names_from_epic(epic_data: Dict[str, Any]) -> Set[str]:
    story_names = set()
    for story in epic_data.get('stories', []):
        if isinstance(story, dict) and 'name' in story:
            story_names.add(story['name'])
        elif isinstance(story, str):
            story_names.add(story)
    for story_group in epic_data.get('story_groups', []):
        for story in story_group.get('stories', []):
            if isinstance(story, dict) and 'name' in story:
                story_names.add(story['name'])
            elif isinstance(story, str):
                story_names.add(story)
    # ... (truncated)
```

---

## simplify_control_flow
**scenario_outline_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan_story_node" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
class ScenarioOutlineScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_text = self._get_scenario_text(scenario)
                
                if 'Scenario Outline' in scenario_text:
                    has_examples = 'Examples:' in scenario_text or 'examples' in str(scenario).lower()
                    
    # ... (truncated)
```

---

## simplify_control_flow
**scenario_specific_given_scanner.py** - 2 violation(s)

[!] WARNING (line 9)
Function "scan_story_node" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
class ScenarioSpecificGivenScanner(StoryScanner):
    
    def scan_story_node(self, node: StoryNode, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        if isinstance(node, Story):
            story_data = node.data
            scenarios = story_data.get('scenarios', [])
            background = story_data.get('background', [])
            
            for scenario_idx, scenario in enumerate(scenarios):
                scenario_steps = self._get_scenario_steps(scenario)
                
                if scenario_steps:
                    first_step = scenario_steps[0]
    # ... (truncated)
```

[!] WARNING (line 34)
Function "_get_scenario_steps" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _get_scenario_steps(self, scenario: Dict[str, Any]) -> List[str]:
        steps = []
        if isinstance(scenario, dict):
            if 'steps' in scenario:
                steps = scenario['steps']
            elif 'scenario' in scenario:
                scenario_text = scenario['scenario']
                if isinstance(scenario_text, str):
                    steps = [s.strip() for s in scenario_text.split('\n') if s.strip()]
        return steps

```

---

## simplify_control_flow
**setup_similarity_scanner.py** - 2 violation(s)

[!] WARNING (line 16)
Function "scan" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    MIN_INTRA_DUP = 2

    def scan(
        self,
        story_graph: Dict[str, Any],
        rule_obj: Any = None,
        test_files: Optional[List["Path"]] = None,
        code_files: Optional[List["Path"]] = None,
        on_file_scanned: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fingerprint_occurrences: Dict[Tuple[str, Tuple[str, ...]], List[Tuple[Path, int, str]]] = defaultdict(list)
        intra_duplicates: List[Dict[str, Any]] = []

        files = test_files or []
    # ... (truncated)
```

[!] WARNING (line 79)
Function "_collect_payloads" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations

    def _collect_payloads(self, func_node: ast.FunctionDef) -> List[Tuple[Tuple[str, Tuple[str, ...]], int]]:
        payloads: List[Tuple[Tuple[str, Tuple[str, ...]], int]] = []
        for node in ast.walk(func_node):
            dict_node = None
            lineno = getattr(node, "lineno", None)

            if isinstance(node, ast.Dict):
                dict_node = node
            elif isinstance(node, ast.Call):
                for arg in list(node.args) + [kw.value for kw in node.keywords]:
                    if isinstance(arg, ast.Dict):
                        dict_node = arg
                        lineno = getattr(arg, "lineno", lineno)
    # ... (truncated)
```

---

## simplify_control_flow
**specification_match_scanner.py** - 8 violation(s)

[!] WARNING (line 35)
Function "_check_test_method_names" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_test_method_names(self, tree: ast.AST, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        vague_patterns = [
            r'^test_(init|setup|create|new|get|set|run|execute|do|handle|process|check|verify|test)$',
            r'^test_\w+_(init|setup|create|new|get|set|run|execute|do|handle|process|check|verify)$',
        ]
        
        functions = Functions(tree)
        for function in functions.get_many_functions:
            if function.node.name.startswith('test_'):
                is_vague = False
                for pattern in vague_patterns:
    # ... (truncated)
```

[!] WARNING (line 103)
Function "_check_variable_names" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violation_dict
    
    def _check_variable_names(self, tree: ast.AST, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        generic_names = ['data', 'result', 'value', 'item', 'obj', 'thing', 'name', 'root', 'path', 'config']
        
        test_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_methods.append(node)
        
        for test_method in test_methods:
            for child in ast.walk(test_method):
                if isinstance(child, ast.Assign):
    # ... (truncated)
```

[!] WARNING (line 128)
Function "_is_in_helper_call" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _is_in_helper_call(self, assign_node: ast.Assign, test_method: ast.FunctionDef) -> bool:
        if isinstance(assign_node.value, ast.Call):
            func = assign_node.value.func
            if isinstance(func, ast.Name):
                func_name = func.id
                if func_name.startswith(('verify_', 'given_', 'when_', 'then_', 'create_', 'setup_')):
                    return True
            elif isinstance(func, ast.Attribute):
                func_name = func.attr
                if func_name.startswith(('verify_', 'given_', 'when_', 'then_', 'create_', 'setup_')):
                    return True
        return False
    
```

[!] WARNING (line 141)
Function "_check_assertions" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def _check_assertions(self, tree: ast.AST, content: str, file_path: Path, rule_obj: Any) -> List[Dict[str, Any]]:
        violations = []
        
        implementation_patterns = [
            r'\._(private|internal|_flag|_state|_cache)',
            r'\.called\b',
            r'\.assert_called',
            r'\._validate',
        ]
        
        test_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
    # ... (truncated)
```

[!] WARNING (line 208)
Function "_extract_domain_terms" has nesting depth of 12 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _extract_domain_terms(self, story_graph: Dict[str, Any]) -> set:
        domain_terms = set()
        
        if not story_graph:
            return domain_terms
        
        epics = story_graph.get('epics', [])
        for epic in epics:
            if isinstance(epic, dict):
                epic_name = epic.get('name', '')
                if epic_name:
                    domain_terms.update(self._extract_words_from_text(epic_name))
                
    # ... (truncated)
```

[!] WARNING (line 321)
Function "_find_matching_story" has nesting depth of 12 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _find_matching_story(self, scenario: Optional[str], test_name: str, story_graph: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not story_graph:
            return None
        
        scenario_name = None
        if scenario:
            scenario_match = re.search(r'SCENARIO:\s*(.+?)(?:\n|$)', scenario, re.IGNORECASE)
            if scenario_match:
                scenario_name = scenario_match.group(1).strip()
        
        test_keywords = set(self._extract_words_from_text(test_name))
        
        epics = story_graph.get('epics', [])
    # ... (truncated)
```

[!] WARNING (line 357)
Function "_check_variable_matches" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _check_variable_matches(self, test_method: ast.FunctionDef, story: Dict[str, Any], 
                                domain_terms: set, rule_obj: Any, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        variable_names = []
        for node in ast.walk(test_method):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_names.append((target.id, node.lineno if hasattr(node, 'lineno') else None))
        
        for var_name, line_number in variable_names:
            var_name_lower = var_name.lower()
    # ... (truncated)
```

[!] WARNING (line 397)
Function "_check_assertion_matches" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_assertion_matches(self, test_method: ast.FunctionDef, story: Dict[str, Any], 
                                 rule_obj: Any, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        
        acceptance_criteria = story.get('acceptance_criteria', [])
        if not acceptance_criteria:
            return violations
        
        assertions = []
        has_pytest_raises = False
        has_helper_assertions = False
        
        for node in ast.walk(test_method):
    # ... (truncated)
```

---

## simplify_control_flow
**standard_data_reuse_scanner.py** - 1 violation(s)

[!] WARNING (line 23)
Function "scan_file" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
    }

    def scan_file(self, file_path: Path, rule_obj: Any = None, story_graph: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        parsed = self._read_and_parse_file(file_path)
        if not parsed:
            return violations

        content, lines, tree = parsed

        for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]:
            dict_keysets = []
            for node in ast.walk(func):
                dict_node = None
    # ... (truncated)
```

---

## simplify_control_flow
**story_map.py** - 1 violation(s)

[!] WARNING (line 23)
Function "map_location" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return self.data.get('name', '')
    
    def map_location(self, field: str = 'name') -> str:
        if isinstance(self, Epic):
            return f"epics[{self.epic_idx}].{field}"
        elif isinstance(self, SubEpic):
            if self.sub_epic_path:
                path_str = "".join([f".sub_epics[{idx}]" for idx in self.sub_epic_path])
                return f"epics[{self.epic_idx}]{path_str}.{field}"
            else:
                return f"epics[{self.epic_idx}].{field}"
        elif isinstance(self, Story):
            path_parts = [f"epics[{self.epic_idx}]"]
            if self.sub_epic_path:
                for idx in self.sub_epic_path:
    # ... (truncated)
```

---

## simplify_control_flow
**swallowed_exceptions_scanner.py** - 1 violation(s)

[!] WARNING (line 24)
Function "_check_swallowed_exceptions" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_swallowed_exceptions(self, tree: ast.AST, file_path: Path, rule_obj: Any, content: str) -> List[Dict[str, Any]]:
        violations = []
        
        try_blocks = TryBlocks(tree)
        for try_block in try_blocks.get_many_try_blocks:
            for handler in try_block.exception_handlers:
                handler_body = handler.body
                if len(handler_body) == 0:
                    line_number = handler.lineno if hasattr(handler, 'lineno') else None
                    violation = self._create_violation_with_snippet(
                        rule_obj=rule_obj,
                        violation_message=f'Empty except block at line {line_number} - exceptions must be logged or rethrown, never swallowed',
                        file_path=file_path,
    # ... (truncated)
```

---

## simplify_control_flow
**test_file_naming_scanner.py** - 3 violation(s)

[!] WARNING (line 99)
Function "_get_sub_epics_spanned_by_test_methods" has nesting depth of 8 - use guard clauses and extract nested blocks to reduce nesting

```python
        ).to_dict()
    
    def _get_sub_epics_spanned_by_test_methods(self, file_path: Path, story_graph: Dict[str, Any]) -> set:
        sub_epics = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            
            # Find all test methods
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.name.startswith('Test'):
                        class_name = node.name
                        
    # ... (truncated)
```

[!] WARNING (line 124)
Function "_find_sub_epic_for_method" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return sub_epics
    
    def _find_sub_epic_for_method(self, method_name: str, class_name: str, story_graph: Dict[str, Any]) -> Optional[str]:
        method_name_norm = self._to_snake_case(method_name)
        story_name_from_class = class_name[4:] if class_name.startswith('Test') else class_name
        story_name_normalized = self._to_snake_case(story_name_from_class)
        
        epics = story_graph.get('epics', [])
        
        for epic in epics:
            sub_epics = epic.get('sub_epics', [])
            for sub_epic in sub_epics:
                sub_epic_name = sub_epic.get('name', '')
                sub_epic_name_norm = self._to_snake_case(sub_epic_name) if sub_epic_name else ''
                
    # ... (truncated)
```

[!] WARNING (line 189)
Function "_find_closest_sub_epic_names" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _find_closest_sub_epic_names(self, file_name: str, sub_epic_names: List[str], max_suggestions: int = 5) -> List[str]:
        if not sub_epic_names:
            return []
        
        scored_names = []
        file_name_lower = file_name.lower()
        
        for sub_epic_name in sub_epic_names:
            sub_epic_lower = sub_epic_name.lower()
            
            # Simple similarity: check for common substrings
            score = 0
            
    # ... (truncated)
```

---

## simplify_control_flow
**type_safety_scanner.py** - 2 violation(s)

[!] WARNING (line 131)
Function "_check_parameters_get_pattern" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _check_parameters_get_pattern(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any, content: str) -> List[Dict[str, Any]]:
        violations = []
        found_lines = set()
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'get':
                        if isinstance(node.func.value, ast.Name):
                            var_name = node.func.value.id
                            if var_name in ('parameters', 'params', 'kwargs'):
                                line_no = node.lineno
                                if line_no not in found_lines:
    # ... (truncated)
```

[!] WARNING (line 161)
Function "_is_dict_any_annotation" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations[:3]
    
    def _is_dict_any_annotation(self, annotation: ast.AST) -> bool:
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id == 'Dict':
                    if isinstance(annotation.slice, ast.Tuple):
                        if len(annotation.slice.elts) >= 2:
                            second_arg = annotation.slice.elts[1]
                            if isinstance(second_arg, ast.Name) and second_arg.id == 'Any':
                                return True
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id == 'dict':
                    if isinstance(annotation.slice, ast.Tuple):
                        if len(annotation.slice.elts) >= 2:
    # ... (truncated)
```

---

## simplify_control_flow
**ubiquitous_language_scanner.py** - 1 violation(s)

[!] WARNING (line 127)
Function "_check_classes_against_domain_model" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return classes_used
    
    def _check_classes_against_domain_model(
        self, 
        classes_under_test: List[Tuple[str, int, str]], 
        domain_entities: Set[str],
        file_path: Path,
        rule_obj: Any
    ) -> List[Dict[str, Any]]:
        """
        Check if classes being tested are in the domain model.
        Flag violations for:
        1. Classes not in domain model
        2. Agent nouns (Handler, Manager, Service, Processor) detected via NLTK
        """
    # ... (truncated)
```

---

## simplify_control_flow
**unnecessary_parameter_passing_scanner.py** - 3 violation(s)

[!] WARNING (line 50)
Function "_collect_instance_attributes" has nesting depth of 7 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _collect_instance_attributes(self, class_node: ast.ClassDef) -> set:
        attrs = set()
        
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                for stmt in ast.walk(node):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                    attrs.add(target.attr)
        
        for node in class_node.body:
    # ... (truncated)
```

[!] WARNING (line 101)
Function "_parameter_used_like_instance_attr" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return violations
    
    def _parameter_used_like_instance_attr(self, method_node: ast.FunctionDef, param_name: str) -> bool:
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == param_name:
                    return False
            
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == param_name:
                        return False
        
        return True
    
```

[!] WARNING (line 114)
Function "_check_property_extraction" has nesting depth of 11 - use guard clauses and extract nested blocks to reduce nesting

```python
        return True
    
    def _check_property_extraction(self, method_node: ast.FunctionDef, instance_attrs: set,
                                  file_path: Path, rule_obj: Any, lines: List[str], content: str) -> List[Dict[str, Any]]:
        violations = []
        
        assignments = []
        for i, stmt in enumerate(method_node.body):
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        attr_path = self._extract_self_attribute_path(stmt.value)
                        if attr_path:
                            assignments.append({
                                'var_name': target.id,
    # ... (truncated)
```

---

## simplify_control_flow
**verb_noun_scanner.py** - 1 violation(s)

[!] WARNING (line 383)
Function "_check_noun_only" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return None
    
    def _check_noun_only(self, name: str, node: StoryNode, node_type: str, rule_obj: Any) -> Optional[Dict[str, Any]]:
        try:
            tokens, tags = self._get_tokens_and_tags(name)
            
            if not tags:
                return None
            
            has_verb = any(self._is_verb(tag[1]) for tag in tags)
            
            if not has_verb and tokens:
                first_token = tokens[0]
                if '-' in first_token:
                    parts = first_token.split('-')
    # ... (truncated)
```

---

## simplify_control_flow
**vocabulary_helper.py** - 2 violation(s)

[!] WARNING (line 62)
Function "is_agent_noun" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def is_agent_noun(word: str) -> tuple[bool, Optional[str], Optional[str]]:
        word_lower = word.lower()
        
        for suffix in VocabularyHelper.AGENT_SUFFIXES:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                base = word_lower[:-len(suffix)]
                
                if VocabularyHelper.is_verb(base):
                    return (True, base, suffix)
                
                if suffix == 'er' or suffix == 'or':
                    base_with_e = base + 'e'
                    if VocabularyHelper.is_verb(base_with_e):
    # ... (truncated)
```

[!] WARNING (line 130)
Function "is_actor_or_role" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
    
    @staticmethod
    def is_actor_or_role(word: str) -> bool:
        try:
            word_lower = word.lower()
            
            synsets = wn.synsets(word_lower)
            
            if not synsets:
                return False
            
            for synset in synsets:
                hypernyms = set()
                for path in synset.hypernym_paths():
                    hypernyms.update(path)
    # ... (truncated)
```

---

## simplify_control_flow
**json_scope.py** - 2 violation(s)

[!] WARNING (line 36)
Function "to_dict" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return self.scope.file_filter
    
    def to_dict(self) -> dict:
        result = {
            'type': self.scope.type.value,
            'filter': ', '.join(self.scope.value) if self.scope.value else '',
            'content': None,
            'graphLinks': []
        }
        
        if self.scope.type.value in ('story', 'showAll'):
            story_graph = self.scope._get_story_graph_results()
            if story_graph:
                from agile_bot.src.story_graph.json_story_graph import JSONStoryGraph
                graph_adapter = JSONStoryGraph(story_graph)
    # ... (truncated)
```

[!] WARNING (line 94)
Function "_enrich_sub_epic_with_links" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
                    self._enrich_sub_epic_with_links(sub_epic, test_dir, docs_stories_map, epic['name'])
    
    def _enrich_sub_epic_with_links(self, sub_epic: dict, test_dir: Path, docs_stories_map: Path, epic_name: str, parent_path: str = None):
        if parent_path:
            sub_epic_doc_folder = Path(parent_path) / f"⚙️ {sub_epic['name']}"
        else:
            sub_epic_doc_folder = docs_stories_map / f"🎯 {epic_name}" / f"⚙️ {sub_epic['name']}"
        
        if 'links' not in sub_epic:
            sub_epic['links'] = []
        
        if 'test_file' in sub_epic and sub_epic['test_file']:
            test_file_path = test_dir / sub_epic['test_file']
            if test_file_path.exists():
                sub_epic['links'].append({
    # ... (truncated)
```

---

## simplify_control_flow
**markdown_scope.py** - 1 violation(s)

[!] WARNING (line 12)
Function "serialize" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.workspace_directory = workspace_directory or Path.cwd()
    
    def serialize(self) -> str:
        lines = []
        
        lines.append(self.format_header(2, "🎯 Scope"))
        lines.append("")
        
        if self.scope.type.value == 'all':
            filter_display = "all (entire project)"
        else:
            filter_display = ', '.join(self.scope.value) if isinstance(self.scope.value, list) else str(self.scope.value) if self.scope.value else "all"
        
        lines.append(f"**🎯 Current Scope:** {filter_display}")
        lines.append("")
    # ... (truncated)
```

---

## simplify_control_flow
**scope.py** - 2 violation(s)

[!] WARNING (line 112)
Function "filter_files" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return False
    
    def filter_files(self, file_list: List[Path]) -> List[Path]:
        if not self.include_patterns and not self.exclude_patterns:
            return file_list
        
        from pathlib import PurePath
        filtered = []
        
        for file_path in file_list:
            file_str = str(file_path).replace('\\', '/')
            file_path_obj = PurePath(file_str)
            
            if self.include_patterns:
                matches_include = False
    # ... (truncated)
```

[!] WARNING (line 262)
Function "_get_file_results" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            return None
    
    def _get_file_results(self) -> List[Path]:
        import glob as glob_module
        
        all_files = []
        paths = self.value if isinstance(self.value, list) else [self.value]
        
        for path_str in paths:
            has_glob = any(char in path_str for char in ['*', '?', '['])
            
            if has_glob:
                if not Path(path_str).is_absolute():
                    pattern = str(self.workspace_directory / path_str)
                else:
    # ... (truncated)
```

---

## simplify_control_flow
**scoping_parameter.py** - 1 violation(s)

[!] WARNING (line 275)
Function "_add_epic_stories" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            self._add_story_name(story, story_names)
    
    def _add_epic_stories(self, increment: Dict[str, Any], story_names: Set[str]) -> None:
        for epic in increment.get('epics', []):
            for sub_epic in epic.get('sub_epics', []):
                for story in sub_epic.get('stories', []):
                    self._add_story_name(story, story_names)
                
                for story_group in sub_epic.get('story_groups', []):
                    for story in story_group.get('stories', []):
                        self._add_story_name(story, story_names)
    
```

---

## simplify_control_flow
**tty_scope.py** - 1 violation(s)

[!] WARNING (line 11)
Function "serialize" has nesting depth of 6 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.scope = scope
    
    def serialize(self) -> str:
        lines = []
        
        lines.append(self.add_bold("🎯 Scope"))
        
        if self.scope.type.value == 'all':
            filter_display = "all (entire project)"
        else:
            filter_display = ', '.join(self.scope.value) if isinstance(self.scope.value, list) else str(self.scope.value) if self.scope.value else "all"
        
        lines.append(f"🎯 {self.add_bold('Current Scope:')} {filter_display}")
        lines.append("")
        
    # ... (truncated)
```

---

## simplify_control_flow
**build_action.py** - 2 violation(s)

[!] WARNING (line 104)
Function "_replace_schema_placeholders" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return behavior_to_content.get(self.behavior.name, [])
    
    def _replace_schema_placeholders(self, instructions) -> None:
        base_instructions = instructions.get('base_instructions', [])
        new_instructions = []
        
        template = self.story_graph_template
        description_lines_list = []
        schema_explanation_lines = []
        
        if template and template.exists:
            template_path = template.template_path
            if template_path:
                bot_dir = self.behavior.bot_paths.bot_directory
                try:
    # ... (truncated)
```

[!] WARNING (line 207)
Function "_replace_content_with_file_references" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        instructions.set('rules', all_rules)
    
    def _replace_content_with_file_references(self, instructions) -> None:
        bot_dir = self.behavior.bot_paths.bot_directory
        
        
        
        if 'rules' in instructions._data and instructions._data['rules']:
            all_rules = instructions._data['rules']
            rule_files = []
            bots_dir = self.behavior.bot_paths.python_workspace_root / 'agile_bot' / 'bots'
            
            for rule in all_rules:
                rule_path = None
                if isinstance(rule, dict):
    # ... (truncated)
```

---

## simplify_control_flow
**tty_required_context.py** - 1 violation(s)

[!] WARNING (line 9)
Function "serialize" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.required_context = required_context
    
    def serialize(self) -> str:
        lines = []
        
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
    # ... (truncated)
```

---

## simplify_control_flow
**tty_strategy.py** - 1 violation(s)

[!] WARNING (line 9)
Function "serialize" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        self.strategy = strategy
    
    def serialize(self) -> str:
        lines = []
        
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
    # ... (truncated)
```

---

## simplify_control_flow
**render_instruction_builder.py** - 3 violation(s)

[!] WARNING (line 28)
Function "_add_spec_instructions" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return working_dir

    def _add_spec_instructions(self, base_instructions_list: List[str], executed_specs: List['RenderSpec'], template_specs: List['RenderSpec']) -> None:
        if executed_specs:
            insert_position = 1
            for i, line in enumerate(base_instructions_list):
                if i > 0 and line == "" and i > 1:
                    prev_line = base_instructions_list[i-1]
                    if prev_line.strip().startswith('-') or (prev_line.startswith('  ') and prev_line.strip()):
                        insert_position = i + 1
                        break
            
            synchronizer_lines = self.format_executed_synchronizers(executed_specs).split('\n')
            for line in reversed(synchronizer_lines):
                base_instructions_list.insert(insert_position, line)
    # ... (truncated)
```

[!] WARNING (line 119)
Function "_process_for_each_loops" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        parts.append('')
    
    def _process_for_each_loops(self, instructions_list: List[str], render_specs: List['RenderSpec']) -> List[str]:
        new_instructions = []
        i = 0
        while i < len(instructions_list):
            line = instructions_list[i]
            
            if '{{#for_each_render_config}}' in line:
                loop_start = i + 1
                loop_end = None
                for j in range(loop_start, len(instructions_list)):
                    if '{{/for_each_render_config}}' in instructions_list[j]:
                        loop_end = j
                        break
    # ... (truncated)
```

[!] WARNING (line 151)
Function "_expand_template_for_spec" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
        return new_instructions
    
    def _expand_template_for_spec(self, template_lines: List[str], spec: 'RenderSpec') -> List[str]:
        instructions = spec.config_data.get('instructions', 'No instructions provided')
        if isinstance(instructions, list):
            instructions = '\n'.join(instructions)
        
        replacements = {
            '{render_config.name}': spec.name,
            '{render_config.instructions}': instructions,
            '{render_config.synchronizer}': spec.synchronizer.synchronizer_class_path if spec.synchronizer else 'N/A',
            '{render_config.template}': spec.config_data.get('template', 'N/A'),
            '{render_config.input}': spec.input or 'N/A',
            '{render_config.output}': spec.output or 'N/A',
            '{render_config.path}': spec.config_data.get('path', 'N/A')
    # ... (truncated)
```

---

## simplify_control_flow
**json_strategy_action.py** - 1 violation(s)

[!] WARNING (line 57)
Function "to_dict" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return self.action.typical_assumptions
    
    def to_dict(self) -> dict:
        import time
        with open(r'c:\dev\augmented-teams\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'sessionId':'debug-session','runId':'initial','hypothesisId':'H1','location':'json_strategy_action.py:67','message':'to_dict called','data':{'behavior_name':self.action.behavior.name if self.action.behavior else None,'has_strategy':bool(self.action.strategy)},'timestamp':int(time.time()*1000)})+'\n')
        
        result = {
            'action_name': self.action.action_name,
            'description': self.action.description,
            'order': self.action.order,
            'next_action': self.action.next_action,
            'workflow': self.action.workflow,
            'auto_confirm': self.action.auto_confirm,
            'skip_confirm': self.action.skip_confirm,
    # ... (truncated)
```

---

## simplify_control_flow
**strategy_action.py** - 1 violation(s)

[!] WARNING (line 88)
Function "_format_instructions_for_display" has nesting depth of 5 - use guard clauses and extract nested blocks to reduce nesting

```python
            pass
    
    def _format_instructions_for_display(self, instructions) -> str:
        output_lines = super()._format_instructions_for_display(instructions).split('\n')
        
        instructions_dict = instructions.to_dict()
        
        strategy_criteria = instructions_dict.get('strategy_criteria', {})
        if strategy_criteria:
            output_lines.append("")
            output_lines.append("**Decisions:**")
            
            criteria_template = strategy_criteria.get('criteria', {})
            if criteria_template:
                for criteria_key, criteria_data in criteria_template.items():
    # ... (truncated)
```

---

## simplify_control_flow
**validate_action.py** - 3 violation(s)

[!] WARNING (line 32)
Function "_prepare_instructions" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return self._rules

    def _prepare_instructions(self, instructions, context: ValidateActionContext):
        rules_text = self._format_rules_with_file_paths()
        
        schema_path = self.behavior.bot_paths.workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        
        scope_text = self._format_scope_description(context)
        
        scanner_output = self._run_scanners_and_format_results(context)
        
        replacements = {
            'rules': rules_text if rules_text else 'No rules defined',
            'scanner_output': scanner_output,
            'schema': f'**Schema:** Story graph at `{schema_path}`',
    # ... (truncated)
```

[!] WARNING (line 89)
Function "_run_scanners_and_format_results" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            instructions._data['rules'] = rule_files

    def _run_scanners_and_format_results(self, context: ValidateActionContext) -> str:
        logger.info('Running scanners for instructions display...')
        
        try:
            result = self._executor.execute_synchronous(context)
            
            instructions_dict = result.get('instructions', {})
            report_link = instructions_dict.get('report_link', '')
            
            if report_link:
                import re
                match = re.search(r'\[.*?\]\((.*?)\)', report_link)
                if match:
    # ... (truncated)
```

[!] WARNING (line 124)
Function "_format_scope_description" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            return f'Error running scanners: {e}\n\nPlease review the validation report file in docs/stories/reports/'
    
    def _format_scope_description(self, context: ValidateActionContext) -> str:
        if context.scope:
            scope_type = context.scope.type.value
            scope_value = context.scope.value
            
            if scope_type == 'epic':
                return f"epic(s): {', '.join(scope_value)}"
            elif scope_type == 'story':
                return f"story/stories: {', '.join(scope_value)}"
            elif scope_type == 'files':
                return f"file(s): {', '.join(scope_value)}"
            else:
                return "all epics, sub-epics, stories, and domain concepts in the story graph"
    # ... (truncated)
```

---

## simplify_control_flow
**validation_scope.py** - 1 violation(s)

[!] WARNING (line 157)
Function "_get_explicit_files_for_behavior" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
            return 'src'

    def _get_explicit_files_for_behavior(self, file_key, behavior_dir):
        has_files_scope = (self._parameters.get('scope', {}).get('type') == 'files' if isinstance(self._parameters.get('scope'), dict) else False)
        
        if file_key in self._scope_config:
            files = self.files(file_key)
            if files:
                return files
        
        if behavior_dir in self._scope_config:
            files = self.files(behavior_dir)
            if files:
                return files
        
    # ... (truncated)
```

---

## simplify_control_flow
**cursor_command_visitor.py** - 1 violation(s)

[!] WARNING (line 136)
Function "_build_behavior_command" has nesting depth of 4 - use guard clauses and extract nested blocks to reduce nesting

```python
        return "\n".join(lines)
    
    def _build_behavior_command(self, behavior_name: str) -> str:
        bot_dir_str = str(self.bot_directory).replace('\\', '\\')
        workspace_str = str(self.workspace_root).replace('\\', '\\')
        
        behavior = self.bot.behaviors.find_by_name(behavior_name)
        if not behavior:
            return ""
        
        action_names = []
        if self.data_collector:
            action_names = self.data_collector.get_behavior_actions(behavior)
        
        behavior_name_underscore = behavior_name.replace('-', '_')
    # ... (truncated)
```

---

## stop_writing_useless_comments
**utils.py** - 4 violation(s)

[X] ERROR (line 13)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

def parse_command_text(text: str) -> tuple[str, str]:
    """Parse command text into verb and arguments.
    
    Args:
        text: Command text to parse (e.g., "scope --filter=story")
        
    Returns:
        Tuple of (verb, args) where verb is lowercase and args is the rest
    """
    parts = text.split(maxsplit=1)
```

[X] ERROR (line 219)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

def _find_ast_node_line(file_path: Path, node_name: str, node_type: type) -> Optional[int]:
    """Generic helper to find AST node line number by name and type.
    
    Args:
        file_path: Path to Python file to parse
        node_name: Name of the node to find
        node_type: Type of AST node to look for (ast.ClassDef, ast.FunctionDef, etc.)
        
    Returns:
        Line number where node is defined, or None if not found
    """
    if not file_path.exists() or not node_name or node_name == '?':
```

[X] ERROR (line 244)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

def find_test_class_line(test_file_path: Path, test_class_name: str) -> Optional[int]:
    """Find line number where a test class is defined."""
    return _find_ast_node_line(test_file_path, test_class_name, ast.ClassDef)
```

[X] ERROR (line 248)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

def find_test_method_line(test_file_path: Path, test_method_name: str) -> Optional[int]:
    """Find line number where a test method/function is defined."""
    return _find_ast_node_line(test_file_path, test_method_name, ast.FunctionDef)
```

---

## stop_writing_useless_comments
**action.py** - 7 violation(s)

[X] ERROR (line 148)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _get_parameter_description(self, param_name: str) -> str:
        """Get meaningful description for a parameter by delegating to domain objects."""
        from .clarify.requirements_clarifications import RequirementsClarifications
```

[X] ERROR (line 567)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_behavior_section(self, output_lines: list):
        """Format behavior instructions section."""
        if not self.behavior:
```

[X] ERROR (line 587)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_action_section(self, output_lines: list):
        """Format action instructions section."""
        action_name = self.action_name if hasattr(self, 'action_name') else 'unknown'
```

[X] ERROR (line 602)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_key_questions(self, key_questions, output_lines: list):
        """Format key questions section."""
        if not key_questions:
```

[X] ERROR (line 617)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_evidence(self, evidence, output_lines: list):
        """Format evidence section."""
        if not evidence:
```

[X] ERROR (line 631)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_guardrails_section(self, guardrails_dict: dict, output_lines: list):
        """Format guardrails section with required context."""
        if not guardrails_dict:
```

[X] ERROR (line 646)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _format_instructions_for_display(self, instructions) -> str:
        """Format instructions for display by building sections."""
        instructions_dict = instructions.to_dict()
```

---

## stop_writing_useless_comments
**behavior.py** - 1 violation(s)

[X] ERROR (line 131)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def submitRules(self) -> Dict[str, Any]:
        """Submit behavior rules instructions to AI chat.
        
        Executes the rules action to get instructions, then submits them to chat.
        
        Returns:
            Status dict with success message and submission details
        """
        if not self.bot:
```

---

## stop_writing_useless_comments
**bot.py** - 12 violation(s)

[X] ERROR (line 212)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _clear_scope_and_return_result(self, message: str):
        """Helper to clear scope, save, and return success result.
        
        Args:
            message: Success message to include in result
            
        Returns:
            ScopeCommandResult with success status
        """
        self._scope.clear()
```

[X] ERROR (line 230)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _normalize_scope_filter(self, scope_filter: str) -> str:
        """Normalize scope filter by removing quotes and 'set ' prefix."""
        scope_filter_lower = scope_filter.lower().strip()
```

[X] ERROR (line 243)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _determine_scope_type(self, prefix: str):
        """Determine ScopeType from prefix string."""
        from ..scope.scope import ScopeType
```

[X] ERROR (line 256)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _looks_like_file_path(self, values: list) -> bool:
        """Check if values look like file paths."""
        import os
```

[X] ERROR (line 261)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _parse_delimited_scope(self, scope_filter: str):
        """Parse scope filter with = or : delimiter."""
        delimiter = '=' if '=' in scope_filter else ':'
```

[X] ERROR (line 278)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _parse_spaced_scope(self, scope_filter: str):
        """Parse scope filter with space separator."""
        parts = scope_filter.split(None, 1)
```

[X] ERROR (line 297)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _parse_undelimited_scope(self, scope_filter: str):
        """Parse scope filter without delimiters - auto-detect."""
        scope_values = [v.strip() for v in scope_filter.split(',') if v.strip()]
```

[X] ERROR (line 306)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def scope(self, scope_filter: Optional[str] = None):
        """Set or get scope filter for the bot."""
        from ..scope.scope import ScopeType
```

[X] ERROR (line 384)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

    def _navigate_and_save(self, behavior, action_name: str, message_prefix: str = "Moved to") -> Dict[str, Any]:
        """Helper to navigate to an action and save state.
        
        Args:
            behavior: The behavior containing the action
            action_name: Name of action to navigate to
            message_prefix: Prefix for success message (default: "Moved to")
            
        Returns:
            Success status dict with navigation details
        """
        behavior.actions.navigate_to(action_name)
```

[X] ERROR (line 599)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def submit_behavior_rules(self, behavior_name: str) -> Dict[str, Any]:
        """Get rules for a behavior and submit them to AI chat.
        
        This is a convenience method that:
        1. Saves current position
        2. Navigates to behavior
        3. Submits rules using behavior.submitRules()
        4. Restores previous position
        
        Args:
            behavior_name: Name of the behavior to get rules for
            
        Returns:
            Status dict with success message and submission details
        """
        saved_behavior = self.behaviors.current.name if self.behaviors.current else None
```

[X] ERROR (line 645)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def submit_instructions(self, instructions, behavior_name: str = None, action_name: str = None) -> Dict[str, Any]:
        """Submit given Instructions object to AI chat.
        
        Args:
            instructions: Instructions object with display_content to submit
            behavior_name: Optional behavior name (for reporting, will be inferred if not provided)
            action_name: Optional action name (for reporting, will be inferred if not provided)
            
        Returns:
            Status dict with success message, behavior/action info, and submission details
        """
        display_content = instructions.display_content
```

[X] ERROR (line 712)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def submit_current_action(self) -> Dict[str, Any]:
        """Submit current action instructions to AI agent.
        
        Gets the current action's instructions (including display_content with all 
        behavior instructions, action instructions, base instructions, and guardrails),
        copies them to clipboard, and opens Cursor chat.
        
        Returns:
            Status dict with success message, current context, and instructions content
        """
        current_behavior = self.behaviors.current
```

---

## stop_writing_useless_comments
**cli_session.py** - 6 violation(s)

[X] ERROR (line 417)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _prepare_action_context(self, action, args: str):
        """Prepare action context with optional arguments."""
        from ..actions.action_context import ActionContext
```

[X] ERROR (line 427)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _build_instructions_from_dict(self, instructions_dict, action):
        """Build Instructions object from result dictionary."""
        from ..instructions.instructions import Instructions
```

[X] ERROR (line 450)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _execute_non_workflow_action(self, action, action_name: str, args: str):
        """Execute non-workflow action and return instructions."""
        try:
```

[X] ERROR (line 469)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _handle_action_shortcut(self, action_name: str, args: str) -> Any:
        """Handle shortcut command for executing an action."""
        if not self.bot.behaviors.current:
```

[X] ERROR (line 179)
Useless comment: "# Return submit result instead of instructions" - delete it or improve the code instead

```python
                            output_lines.append("  ✓ Cursor chat opened")
                        
                        # Return submit result instead of instructions
                        return CLICommandResponse(
```

[X] ERROR (line 215)
Useless comment: "# Return submit result instead of instructions" - delete it or improve the code instead

```python
                                    output_lines.append("  ✓ Cursor chat opened")
                                
                                # Return submit result instead of instructions
                                return CLICommandResponse(
```

---

## stop_writing_useless_comments
**help_action.py** - 2 violation(s)

[X] ERROR (line 216)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _get_scope_description(self, action_name: str) -> str:
        """Get scope description based on action."""
        if action_name == 'validate':
```

[X] ERROR (line 222)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _get_parameter_description(self, action_name: str, param_name: str) -> str:
        """Get parameter description by delegating to domain objects."""
        from ..actions.clarify.requirements_clarifications import RequirementsClarifications
```

---

## stop_writing_useless_comments
**scan_config.py** - 6 violation(s)

[X] ERROR (line 9)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
@dataclass
class ScanConfig:
    """Configuration for scanner execution.
    
    This consolidates scanner parameters to avoid excessive parameter passing.
    """
    
```

[X] ERROR (line 34)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def __post_init__(self):
        """Ensure files dict is initialized."""
        if self.files is None:
```

[X] ERROR (line 42)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @property
    def test_files(self) -> List[Path]:
        """Get test files from changed_files or files."""
        if self._test_files is None:
```

[X] ERROR (line 50)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @property
    def code_files(self) -> List[Path]:
        """Get code files from changed_files or files."""
        if self._code_files is None:
```

[X] ERROR (line 58)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @property
    def all_test_files(self) -> List[Path]:
        """Get all test files (for cross-file scanning)."""
        if self._all_test_files is None:
```

[X] ERROR (line 65)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @property
    def all_code_files(self) -> List[Path]:
        """Get all code files (for cross-file scanning)."""
        if self._all_code_files is None:
```

---

## stop_writing_useless_comments
**duplication_scanner.py** - 6 violation(s)

[X] ERROR (line 950)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_string_formatting_pattern(self, statements: List[ast.stmt]) -> bool:
        """Check if this is primarily string formatting/building operations"""
        if not statements:
```

[X] ERROR (line 1043)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_sequential_output_building(self, statements: List[ast.stmt]) -> bool:
        """Check if this is just sequential appends/extends to any list (common output building)"""
        if not statements or len(statements) < 3:
```

[X] ERROR (line 1093)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_logging_or_output_pattern(self, statements: List[ast.stmt]) -> bool:
        """Check if this is primarily logging, printing, or string output"""
        if not statements:
```

[X] ERROR (line 1363)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _extract_iteration_targets(self, nodes: List[ast.stmt]) -> Set[str]:
        """Extract the names of collections being iterated over (e.g., 'behaviors', 'actions')"""
        targets = set()
```

[X] ERROR (line 1380)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _extract_list_building_targets(self, nodes: List[ast.stmt]) -> Set[str]:
        """Extract the names of lists being built (e.g., 'behavior_names', 'action_names')"""
        targets = set()
```

[X] ERROR (line 1403)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_sequential_appends_with_different_content(self, block1_nodes: List[ast.stmt], block2_nodes: List[ast.stmt]) -> bool:
        """Check if both blocks are just sequential appends but with different string content"""
        
```

---

## stop_writing_useless_comments
**excessive_guards_scanner.py** - 4 violation(s)

[X] ERROR (line 51)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_guard_clause(self, if_node: ast.If, source_lines: List[str]) -> bool:
        """
        Detect two guard clause patterns:
        
        1. ACTUAL GUARD: Early exit for edge cases
           if x is None: return
           
        2. INVERTED GUARD: Positive check wrapping main workflow (should be inverted)
           if x is not None: do_main_work()
           
        DON'T flag: Legitimate branching (if/elif/else)
           if x: do_x()
           elif y: do_y()
           else: do_z()
        """
        # Skip if this has elif/else - that's legitimate branching
```

[X] ERROR (line 233)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python

    def _get_optional_parameters(self, func_node: ast.FunctionDef) -> set:
        """Extract parameter names that have default values of None."""
        optional_params = set()
```

[X] ERROR (line 260)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_lazy_initialization(self, guard_node: ast.If, func_node: ast.FunctionDef) -> bool:
        """Check if this is a lazy initialization pattern in a property."""
        # Check if function is a property
```

[X] ERROR (line 236)
Useless comment: "# Get parameters with defaults" - delete it or improve the code instead

```python
        optional_params = set()
        
        # Get parameters with defaults
        args = func_node.args
```

---

## stop_writing_useless_comments
**resource_oriented_code_scanner.py** - 1 violation(s)

[X] ERROR (line 125)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _is_domain_entity(self, file_path: Path, class_node: ast.ClassDef) -> bool:
        """Check if a class is a domain entity (dataclass in domain.py or similar domain model file)."""
        # Check if it's in a domain model file
```

---

## stop_writing_useless_comments
**test_scanner.py** - 1 violation(s)

[X] ERROR (line 27)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _empty_violation_list(self) -> List[Dict[str, Any]]:
        """Helper method for default empty implementations."""
        return []
```

---

## stop_writing_useless_comments
**ubiquitous_language_scanner.py** - 5 violation(s)

[X] ERROR (line 40)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _extract_domain_entities_from_story_graph(self, story_graph: Dict[str, Any]) -> Set[str]:
        """
        Extract domain entity names (nouns/classes) from story graph.
        Look in domain_concepts sections for entity names.
        """
        if not story_graph:
```

[X] ERROR (line 56)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _extract_from_node(self, node: Dict[str, Any], entities: Set[str]):
        """Recursively extract domain concepts from any node."""
        domain_concepts = node.get('domain_concepts', [])
```

[X] ERROR (line 72)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _to_class_name(self, concept_name: str) -> str:
        """
        Convert domain concept name to expected class name.
        'REPL Session' -> 'REPLSession'
        'Behavior Action State' -> 'BehaviorActionState'
        Preserves acronyms (all-caps words stay all-caps)
        """
        def convert_word(word: str) -> str:
```

[X] ERROR (line 86)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def _extract_classes_under_test(self, tree: ast.AST, content: str, lines: List[str]) -> List[Tuple[str, int, str]]:
        """
        Extract all class instantiations and imports from test file.
        Returns list of (class_name, line_number, code_snippet)
        """
        classes_used = []
```

[X] ERROR (line 113)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
            
            def _get_code_snippet(self, lines: List[str], line_num: int, context: int = 2) -> str:
                """Get code snippet around the line."""
                start = max(0, line_num - context - 1)
```

---

## stop_writing_useless_comments
**scope.py** - 2 violation(s)

[X] ERROR (line 167)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @staticmethod
    def get_parameter_description() -> str:
        """Get description for scope parameter."""
        return "Scope structure: {'type': 'story'|'epic'|'increment'|'all', 'value': <names|priorities>}"
```

[X] ERROR (line 386)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    
    def apply_to_bot(self):
        """Legacy method - save scope to state file.
        
        Note: workspace_directory parameter removed as it's already available via self.workspace_directory
        """
        self.save()
```

---

## stop_writing_useless_comments
**requirements_clarifications.py** - 2 violation(s)

[X] ERROR (line 10)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @staticmethod
    def get_answers_parameter_description() -> str:
        """Get description for key_questions_answered/answers parameter."""
        return "Dict mapping question keys to answer strings"
```

[X] ERROR (line 15)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @staticmethod
    def get_evidence_parameter_description() -> str:
        """Get description for evidence_provided/evidence parameter."""
        return "Dict mapping evidence types to evidence content"
```

---

## stop_writing_useless_comments
**strategy_decision.py** - 2 violation(s)

[X] ERROR (line 10)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @staticmethod
    def get_decisions_parameter_description() -> str:
        """Get description for decisions_made/decisions/choices parameter."""
        return "Dict mapping decision criteria keys to selected options/values"
```

[X] ERROR (line 15)
Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

```python
    @staticmethod
    def get_assumptions_parameter_description() -> str:
        """Get description for assumptions_made/assumptions parameter."""
        return "List of assumption strings"
```

---

## use_clear_function_parameters
**rules.py** - 5 violation(s)

[!] WARNING (line 370)
Function "_process_scanner_result" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
            return data

    def _process_scanner_result(self, rule, rule_result: dict, scanner_results: Any, scanner_path: str, scanner_name: str, logger) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        execution_status = rule.scanner_execution_status or 'SUCCESS'
    # ... (truncated)
```

[!] WARNING (line 386)
Function "_execute_scanner" has 9 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return f'  [OK] {rule.rule_file}: Scanner executed successfully ({violations_count} violations)'

    def _execute_scanner(self, rule, rule_result: dict, context: ValidationContext, scanner_path: str, logger, files: Dict, changed_files: Dict, all_files: Dict) -> str:
        scanner_name = scanner_path.split('.')[-1] if '.' in scanner_path else scanner_path
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ... (truncated)
```

[!] WARNING (line 417)
Function "_process_rule" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
            raise

    def _process_rule(self, rule, rule_result: dict, context: ValidationContext, logger, files: Dict, changed_files: Dict, all_files: Dict) -> str:
        scanner_path = rule.scanner_path
        if not scanner_path:
    # ... (truncated)
```

[!] WARNING (line 429)
Function "validate" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return self._execute_scanner(rule, rule_result, context, scanner_path, logger, files, changed_files, all_files)

    def validate(self, context: ValidationContext, files: Optional[Dict[str, List[Path]]]=None, callbacks: Optional[ValidationCallbacks]=None, skiprule: Optional[List[str]]=None, exclude: Optional[List[str]]=None) -> List[Dict[str, Any]]:
        if isinstance(context, ValidationContext):
            return self._execute_validation(context)
    # ... (truncated)
```

[!] WARNING (line 434)
Function "_create_legacy_context" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return self._execute_validation(self._create_legacy_context(context, files, callbacks, skiprule, exclude))

    def _create_legacy_context(self, story_graph: Dict, files: Optional[Dict], callbacks: Optional[ValidationCallbacks], skiprule: Optional[List[str]], exclude: Optional[List[str]]) -> ValidationContext:
        return ValidationContext(story_graph=story_graph, files=files or {}, callbacks=callbacks or ValidationCallbacks(), skiprule=skiprule or [], exclude=exclude or [], skip_cross_file=True, all_files=False, behavior=self.behavior, bot_paths=getattr(self, 'bot_paths', None), working_dir=Path.cwd())

```

---

## use_clear_function_parameters
**active_language_scanner.py** - 1 violation(s)

[!] WARNING (line 168)
Function "_create_capability_noun_violation" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return None
    
    def _create_capability_noun_violation(self, name: str, node: StoryNode, node_type: str, rule_obj: Any, noun_type: str) -> Dict[str, Any]:
        location = node.map_location()
        message = f'{node_type.capitalize()} name "{name}" uses capability noun'
    # ... (truncated)
```

---

## use_clear_function_parameters
**business_readable_test_names_scanner.py** - 4 violation(s)

[!] WARNING (line 31)
Function "_check_test_function_node" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_test_function_node(self, node: Any, file_path: Path, rule_obj: Any, domain_language: set, violations: list) -> None:
        if not isinstance(node, ast.FunctionDef):
            return
    # ... (truncated)
```

[!] WARNING (line 112)
Function "_check_business_readable" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return set(words)
    
    def _check_business_readable(self, test_name: str, file_path: Path, node: ast.FunctionDef, rule_obj: Any, domain_language: set) -> Optional[Dict[str, Any]]:
        name_without_prefix = test_name[5:] if test_name.startswith('test_') else test_name
        
    # ... (truncated)
```

[!] WARNING (line 241)
Function "_extract_code_snippet" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return True
    
    def _extract_code_snippet(self, content: str, ast_node: Optional[ast.AST] = None, 
                             start_line: Optional[int] = None, end_line: Optional[int] = None,
                             context_before: int = 2, max_lines: int = 50) -> str:
    # ... (truncated)
```

[!] WARNING (line 275)
Function "_create_violation_with_snippet" has 12 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return code_snippet
    
    def _create_violation_with_snippet(
        self, 
        rule_obj: Any,
    # ... (truncated)
```

---

## use_clear_function_parameters
**class_based_organization_scanner.py** - 2 violation(s)

[!] WARNING (line 99)
Function "_check_method_name_matches_scenario" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return None
    
    def _check_method_name_matches_scenario(self, method_name: str, class_name: str, story_names: List[str], 
                                           story_graph: Dict[str, Any], file_path: Path, rule_obj: Any) -> Optional[Dict[str, Any]]:
        scenario_name_from_method = method_name[5:] if method_name.startswith('test_') else method_name
    # ... (truncated)
```

[!] WARNING (line 296)
Function "_check_file_name_matches_sub_epic" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return name.lower()
    
    def _check_file_name_matches_sub_epic(self, file_name: str, sub_epic_names: List[str], file_path: Path, rule_obj: Any, story_graph: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        name_without_prefix = file_name[5:] if file_name.startswith('test_') else file_name
        
    # ... (truncated)
```

---

## use_clear_function_parameters
**clear_parameters_scanner.py** - 2 violation(s)

[!] WARNING (line 18)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        self.story_graph = None
    
    def scan(self, story_graph: Dict[str, Any], rule_obj: Any = None, test_files: Optional[List['Path']] = None, code_files: Optional[List['Path']] = None, on_file_scanned: Optional[Any] = None) -> List[Dict[str, Any]]:
        self.story_graph = story_graph
        return super().scan(story_graph, rule_obj, test_files=test_files, code_files=code_files, on_file_scanned=on_file_scanned)
    # ... (truncated)
```

[!] WARNING (line 75)
Function "_check_parameters" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def _check_parameters(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any, domain_terms: set = None, content: str = None) -> Optional[Dict[str, Any]]:
        if domain_terms is None:
            domain_terms = set()
    # ... (truncated)
```

---

## use_clear_function_parameters
**code_scanner.py** - 4 violation(s)

[!] WARNING (line 11)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class CodeScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

[!] WARNING (line 167)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

[!] WARNING (line 195)
Function "_extract_code_snippet" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
            return None
    
    def _extract_code_snippet(self, content: str, ast_node: Optional[ast.AST] = None, 
                             start_line: Optional[int] = None, end_line: Optional[int] = None,
                             context_before: int = 2, max_lines: int = 50) -> str:
    # ... (truncated)
```

[!] WARNING (line 229)
Function "_create_violation_with_snippet" has 12 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return code_snippet
    
    def _create_violation_with_snippet(
        self, 
        rule_obj: Any,
    # ... (truncated)
```

---

## use_clear_function_parameters
**dead_code_scanner.py** - 2 violation(s)

[!] WARNING (line 13)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class DeadCodeScanner(CodeScanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

[!] WARNING (line 211)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

---

## use_clear_function_parameters
**dependency_chaining_code_scanner.py** - 2 violation(s)

[!] WARNING (line 122)
Function "_check_method_calls_for_instance_attrs" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return attrs
    
    def _check_method_calls_for_instance_attrs(
        self, func_node: ast.FunctionDef, class_name: str, file_path: Path, 
        rule_obj: Any, instance_attrs: Set[str]
    # ... (truncated)
```

[!] WARNING (line 141)
Function "_check_argument" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_argument(
        self, arg_node: ast.AST, method_name: str, class_name: str, file_path: Path, 
        rule_obj: Any, instance_attrs: Set[str], line_num: int
    # ... (truncated)
```

---

## use_clear_function_parameters
**domain_language_code_scanner.py** - 3 violation(s)

[!] WARNING (line 37)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def scan(self, story_graph: Dict[str, Any], rule_obj: Any = None, test_files: Optional[List['Path']] = None, code_files: Optional[List['Path']] = None, on_file_scanned: Optional[Any] = None) -> List[Dict[str, Any]]:
        self.story_graph = story_graph
        return super().scan(story_graph, rule_obj, test_files=test_files, code_files=code_files, on_file_scanned=on_file_scanned)
    # ... (truncated)
```

[!] WARNING (line 82)
Function "_check_domain_language" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_domain_language(self, class_node: ast.ClassDef, file_path: Path, rule_obj: Any, 
                               domain_terms: set, generic_names: set) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

[!] WARNING (line 107)
Function "_check_function_domain_language" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_function_domain_language(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any,
                                      domain_terms: set, generic_names: set, 
                                      enclosing_class: Optional[str] = None) -> List[Dict[str, Any]]:
    # ... (truncated)
```

---

## use_clear_function_parameters
**domain_scanner.py** - 1 violation(s)

[!] WARNING (line 10)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class DomainScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

---

## use_clear_function_parameters
**duplication_scanner.py** - 1 violation(s)

[!] WARNING (line 1788)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return nearby_files
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

---

## use_clear_function_parameters
**excessive_guards_scanner.py** - 2 violation(s)

[!] WARNING (line 35)
Function "_check_function_guards" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_function_guards(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any, source_lines: List[str], content: str) -> List[Dict[str, Any]]:
        violations = []
        
    # ... (truncated)
```

[!] WARNING (line 295)
Function "_check_guard_pattern" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def _check_guard_pattern(self, guard_node: ast.If, file_path: Path, rule_obj: Any, source_lines: List[str], content: str, func_node: ast.FunctionDef = None, optional_params: set = None) -> Optional[Dict[str, Any]]:
        test = guard_node.test
        
    # ... (truncated)
```

---

## use_clear_function_parameters
**function_size_scanner.py** - 1 violation(s)

[!] WARNING (line 34)
Function "_check_function_size" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_function_size(self, func_node: ast.FunctionDef, file_path: Path, rule_obj: Any, source_lines: List[str], content: str) -> Optional[Dict[str, Any]]:
        if not hasattr(func_node, 'end_lineno') or not func_node.end_lineno:
            logger.debug(f'Function node missing end_lineno at {file_path}:{func_node.lineno}')
    # ... (truncated)
```

---

## use_clear_function_parameters
**generic_capability_scanner.py** - 1 violation(s)

[!] WARNING (line 40)
Function "_check_verb_pattern" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return 'unknown'
    
    def _check_verb_pattern(
        self, 
        name: str, 
    # ... (truncated)
```

---

## use_clear_function_parameters
**given_precondition_scanner.py** - 1 violation(s)

[!] WARNING (line 39)
Function "_check_given_is_functionality" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return steps
    
    def _check_given_is_functionality(self, step: str, node: StoryNode, scenario_idx: int, step_idx: int, rule_obj: Any) -> Optional[Dict[str, Any]]:
        step_lower = step.lower()
        
    # ... (truncated)
```

---

## use_clear_function_parameters
**given_state_not_actions_scanner.py** - 1 violation(s)

[!] WARNING (line 58)
Function "_check_given_is_action" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return steps
    
    def _check_given_is_action(self, step: str, node: StoryNode, scenario_idx: int, step_idx: int, rule_obj: Any) -> Optional[Dict[str, Any]]:
        action_verbs = [
            'invokes', 'invoked', 'calls', 'called', 'executes', 'executed',
    # ... (truncated)
```

---

## use_clear_function_parameters
**given_when_then_helpers_scanner.py** - 2 violation(s)

[!] WARNING (line 86)
Function "_check_test_method" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
            return None
    
    def _check_test_method(self, test_node: ast.FunctionDef, content: str, file_path: Path, 
                          rule_obj: Any, helper_functions: Set[str], tree: ast.AST) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

[!] WARNING (line 224)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return None, [], False, 0
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

---

## use_clear_function_parameters
**intention_revealing_names_scanner.py** - 3 violation(s)

[!] WARNING (line 19)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        self.story_graph = None
    
    def scan(self, story_graph: Dict[str, Any], rule_obj: Any = None, test_files: Optional[List['Path']] = None, code_files: Optional[List['Path']] = None, on_file_scanned: Optional[Any] = None) -> List[Dict[str, Any]]:
        self.story_graph = story_graph
        return super().scan(story_graph, rule_obj, test_files=test_files, code_files=code_files, on_file_scanned=on_file_scanned)
    # ... (truncated)
```

[!] WARNING (line 63)
Function "_check_variable_names" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_variable_names(self, tree: ast.AST, file_path: Path, rule_obj: Any, content: str, domain_terms: set = None, docstring_ranges: List[tuple] = None) -> List[Dict[str, Any]]:
        violations = []
        
    # ... (truncated)
```

[!] WARNING (line 111)
Function "_create_generic_name_violation" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _create_generic_name_violation(
        self, 
        rule_obj: Any, 
    # ... (truncated)
```

---

## use_clear_function_parameters
**parameterized_tests_scanner.py** - 1 violation(s)

[!] WARNING (line 8)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class ParameterizedTestsScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

---

## use_clear_function_parameters
**primitive_vs_object_scanner.py** - 1 violation(s)

[!] WARNING (line 138)
Function "_create_primitive_violation" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def _create_primitive_violation(
        self,
        rule_obj: Any,
    # ... (truncated)
```

---

## use_clear_function_parameters
**real_implementations_scanner.py** - 3 violation(s)

[!] WARNING (line 33)
Function "_check_test_methods_call_production_code" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_test_methods_call_production_code(
        self, content: str, lines: List[str], file_path: Path, rule_obj: Any, story_graph: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
    # ... (truncated)
```

[!] WARNING (line 305)
Function "_has_production_code_calls" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return not has_actual_code
    
    def _has_production_code_calls(
        self, method: ast.FunctionDef, imports: List[ast.Import | ast.ImportFrom],
        src_locations: List[str], project_path: Path, file_path: Path = None, tree: ast.AST = None
    # ... (truncated)
```

[!] WARNING (line 348)
Function "_helper_calls_production_code" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def _helper_calls_production_code(
        self, helper_name: str, file_path: Path, tree: ast.AST,
        src_locations: List[str], project_path: Path
    # ... (truncated)
```

---

## use_clear_function_parameters
**resource_oriented_code_scanner.py** - 1 violation(s)

[!] WARNING (line 59)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return []
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

---

## use_clear_function_parameters
**scanner.py** - 2 violation(s)

[!] WARNING (line 16)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class Scanner(ABC):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

[!] WARNING (line 56)
Function "scan_cross_file" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return self._empty_violation_list()
    
    def scan_cross_file(
        self,
        rule_obj: Any = None,
    # ... (truncated)
```

---

## use_clear_function_parameters
**scenarios_on_story_docs_scanner.py** - 1 violation(s)

[!] WARNING (line 90)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        self._in_scope_story_names: Optional[Set[str]] = None
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

---

## use_clear_function_parameters
**setup_similarity_scanner.py** - 1 violation(s)

[!] WARNING (line 16)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
    MIN_INTRA_DUP = 2

    def scan(
        self,
        story_graph: Dict[str, Any],
    # ... (truncated)
```

---

## use_clear_function_parameters
**specification_match_scanner.py** - 3 violation(s)

[!] WARNING (line 71)
Function "_create_violation_with_line_number" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return False
    
    def _create_violation_with_line_number(
        self,
        rule_obj: Any,
    # ... (truncated)
```

[!] WARNING (line 177)
Function "_check_specification_matches" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return ""
    
    def _check_specification_matches(self, tree: ast.AST, content: str, file_path: Path, 
                                    rule_obj: Any, story_graph: Dict[str, Any]) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

[!] WARNING (line 357)
Function "_check_variable_matches" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return None
    
    def _check_variable_matches(self, test_method: ast.FunctionDef, story: Dict[str, Any], 
                                domain_terms: set, rule_obj: Any, file_path: Path) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

---

## use_clear_function_parameters
**spine_optional_scanner.py** - 2 violation(s)

[!] WARNING (line 8)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class SpineOptionalScanner(StoryScanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

[!] WARNING (line 102)
Function "_check_all_stories_mandatory" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_all_stories_mandatory(self, all_stories: List[Story], sequential_stories: List[Story], optional_stories: List[Story], story_group: StoryGroup, rule_obj: Any) -> Optional[Dict[str, Any]]:
        if len(all_stories) < 2:
            return None
    # ... (truncated)
```

---

## use_clear_function_parameters
**story_scanner.py** - 1 violation(s)

[!] WARNING (line 9)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class StoryScanner(Scanner):
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

---

## use_clear_function_parameters
**unnecessary_parameter_passing_scanner.py** - 3 violation(s)

[!] WARNING (line 34)
Function "_check_class" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def _check_class(self, class_node: ast.ClassDef, file_path: Path, rule_obj: Any, lines: List[str], content: str) -> List[Dict[str, Any]]:
        violations = []
        
    # ... (truncated)
```

[!] WARNING (line 73)
Function "_check_method_parameters" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return attrs
    
    def _check_method_parameters(self, method_node: ast.FunctionDef, instance_attrs: set, 
                                file_path: Path, rule_obj: Any, lines: List[str], content: str) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

[!] WARNING (line 114)
Function "_check_property_extraction" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return True
    
    def _check_property_extraction(self, method_node: ast.FunctionDef, instance_attrs: set,
                                  file_path: Path, rule_obj: Any, lines: List[str], content: str) -> List[Dict[str, Any]]:
        violations = []
    # ... (truncated)
```

---

## use_clear_function_parameters
**validation_scanner_status_builder.py** - 3 violation(s)

[!] WARNING (line 37)
Function "_categorize_rule_by_status" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return result

    def _categorize_rule_by_status(self, status: str, rule_dict: Dict, rule_file: str, scanner_status: Dict, result: Dict):
        if status == 'EXECUTED':
            result['executed'].append(self._build_executed_rule_info(rule_dict, rule_file, scanner_status))
    # ... (truncated)
```

[!] WARNING (line 233)
Function "_get_rule_status_display" has vague parameter name "info" - use descriptive name

```python
        return lines

    def _get_rule_status_display(self, info: Dict) -> tuple:
        status, violations = (info.get('status', 'UNKNOWN'), info.get('violations', 0))
        if status in ('EXECUTION_FAILED', 'LOAD_FAILED'):
    # ... (truncated)
```

[!] WARNING (line 247)
Function "_format_rule_scanner_info" has vague parameter name "info" - use descriptive name

```python
        return ('🟨', f'{violations} VIOLATION(S)')

    def _format_rule_scanner_info(self, info: Dict) -> List[str]:
        lines = []
        status = info.get('status', 'UNKNOWN')
    # ... (truncated)
```

---

## use_clear_function_parameters
**vertical_slice_scanner.py** - 1 violation(s)

[!] WARNING (line 14)
Function "scan" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return violations
    
    def scan(
        self, 
        story_graph: Dict[str, Any], 
    # ... (truncated)
```

---

## use_clear_function_parameters
**json_scope.py** - 1 violation(s)

[!] WARNING (line 94)
Function "_enrich_sub_epic_with_links" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
                    self._enrich_sub_epic_with_links(sub_epic, test_dir, docs_stories_map, epic['name'])
    
    def _enrich_sub_epic_with_links(self, sub_epic: dict, test_dir: Path, docs_stories_map: Path, epic_name: str, parent_path: str = None):
        if parent_path:
            sub_epic_doc_folder = Path(parent_path) / f"⚙️ {sub_epic['name']}"
    # ... (truncated)
```

---

## use_clear_function_parameters
**render_instruction_builder.py** - 1 violation(s)

[!] WARNING (line 42)
Function "_update_instructions_dict" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
                base_instructions_list.insert(insert_position, line)

    def _update_instructions_dict(self, instructions: Dict[str, Any], base_instructions_list: List[str], render_instructions: Dict[str, Any], template_specs: List['RenderSpec'], executed_specs: List['RenderSpec'], render_specs: List['RenderSpec'], working_dir: Path) -> None:
        instructions['base_instructions'] = base_instructions_list
        instructions['render_instructions'] = render_instructions
    # ... (truncated)
```

---

## use_clear_function_parameters
**validation_executor.py** - 1 violation(s)

[!] WARNING (line 86)
Function "_process_scanner_status" has 6 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
        return {'counts': counts, 'lines': scanner_status_lines}

    def _process_scanner_status(self, status, counts, scanner_status_lines, rule_file, scanner_status):
        if status == 'EXECUTED':
            counts['executed'] += 1
    # ... (truncated)
```

---

## use_clear_function_parameters
**cursor_command_visitor.py** - 1 violation(s)

[!] WARNING (line 244)
Function "__init__" has 8 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
class CursorBehaviorWrapper(BaseBehaviorAdapter):
    
    def __init__(self, behavior, workspace_root: Path, bot_location: Path, bot_name: str, is_current: bool, bot, generator_ref):
        self.workspace_root = workspace_root
        self.bot_location = bot_location
    # ... (truncated)
```

---

## use_clear_function_parameters
**violation.py** - 1 violation(s)

[!] WARNING (line 58)
Function "create_from_rule_and_context" has 7 parameters - consider using existing domain objects with properties instead of passing primitives. Extend domain objects (Behaviors, Behavior, Actions, RenderSpec, etc.) with properties that encapsulate the needed data rather than creating new parameter objects.

```python
    
    @classmethod
    def create_from_rule_and_context(
        cls,
        rule: 'Rule',
    # ... (truncated)
```

---

## use_domain_language
**orchestrator.py** - 1 violation(s)

[!] WARNING (line 92)
Function "generate_for_all_actions" uses generate/calculate. Use property instead (e.g., "recommended_trades" not "generate_recommendation").

---

## use_domain_language
**complexity_metrics.py** - 1 violation(s)

[!] WARNING (line 182)
Function "calculate_lcom" uses generate/calculate. Use property instead (e.g., "recommended_trades" not "generate_recommendation").

---

