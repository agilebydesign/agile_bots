---
title: use-exact-variable-names
priority: 21
---

## use-exact-variable-names

Use exact variable names from specification scenarios. When spec mentions agent_name
workspace_root
config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec)
not name = 'story_bot'

**DO**

Use exact names from specification in tests and production. Example: agent_name
workspace_root
config_path - all from spec

Test variables match specification exactly

```
# Spec says: agent_name='story_bot', workspace_root
```

```
agent_name = 'story_bot'
```

```
agent = Agent(agent_name=agent_name, workspace_root=workspace_root)
```

Production code uses same names as specification

```
class Agent:
```

```
    def __init__(self, agent_name: str, workspace_root: Path):
```

```
        self.agent_name = agent_name; self.workspace_root = workspace_root
```

Consistent naming across test and production

```
# Spec: load_domain_graph from domain_graph_path
```

```
agent.load_domain_graph(domain_graph_path)
```

```
assert agent.domain_graph is not None
```

**DO NOT**

Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

Don't use abbreviated variable names

```
name = 'story_bot'  # WRONG - spec says 'agent_name'
```

```
root = tmp_path  # WRONG - spec says 'workspace_root'
```

Don't mix different terms for same concept

```
graph_file = path  # WRONG - spec says 'domain_graph_path'
```

```
assert agent.graph  # WRONG - spec says 'domain_graph'
```

Don't use vague parameter names

```
def load(self, path):  # WRONG - spec says 'domain_graph_path'
```