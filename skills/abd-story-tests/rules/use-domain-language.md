---
title: use-domain-language
priority: 1
---

## use-domain-language

Use Ubiquitous Language (DDD): Same vocabulary in domain model
stories
scenarios
AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)

**DO**

Use domain language for classes
methods
and test names. Example: class GatherContextAction
def inject_guardrails()
test_agent_loads_config_when_file_exists

Class names from domain model entities/nouns

```
class GatherContextAction:
```

```
class BotConfig:
```

```
class Guardrails:
```

```
class REPLSession:
```

Method names from domain responsibilities/verbs

```
def inject_guardrails_into_instructions(self):
```

```
def load_and_merge_instructions(self):
```

```
def route_to_behavior_action(self):
```

Test names read like plain English with 'when' for conditions

```
def test_agent_loads_configuration_when_file_exists(self):
```

```
def test_validation_rejects_config_when_required_fields_missing(self):
```

Refine while preserving domain language

```
def inject_key_questions_into_instructions(self):
```

```
def load_behavior_validation_rules(self):
```

**DO NOT**

Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong)
def execute_with_guardrails (wrong)
test_agt_init_sets_vars (wrong)

Don't use generic technical class names

```
class Action:
```

```
class Loader:
```

```
class Handler:
```

```
class Manager:
```

```
class Service:
```

```
class Processor:
```

Don't use generic execute/process/handle methods

```
def execute_with_guardrails(self):
```

```
def process(self):
```

```
def handle_request(self):
```

```
def fetch_patterns(self):
```

Don't use technical jargon or abbreviations in test names

```
def test_agt_init_sets_vars(self):
```

```
def test_validates_json_schema(self):
```

```
def test_config_loader_execute(self):
```

Don't use implementation-specific names not in domain model

```
class StdioHandler:
```

```
def populate_config(self):
```

```
def enhance_instructions(self):
```