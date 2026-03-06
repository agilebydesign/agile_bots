---
title: production-code-explicit-dependencies
priority: 16
---

## production-code-explicit-dependencies

Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader
domain_graph=graph)

**DO**

Inject all dependencies through constructor. Example: def __init__(self
config_loader
domain_graph): self._loader = config_loader

Inject dependencies through constructor

```
class Agent:
```

```
    def __init__(self, config_loader: ConfigLoader, domain_graph: DomainGraph):
```

```
        self._config_loader = config_loader; self._domain_graph = domain_graph
```

Test easily injects test doubles

```
mock_loader = Mock(spec=ConfigLoader)
```

```
mock_loader.load.return_value = {'name': 'bot'}
```

```
agent = Agent(config_loader=mock_loader, domain_graph=mock_graph)
```

Dependencies are explicit and visible

```
# All dependencies visible in constructor signature
```

```
Agent(name, workspace, config_loader, domain_graph, validator)
```

**DO NOT**

Don't access globals
singletons
or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

Don't access global state

```
config = GlobalConfig.instance()  # WRONG - hidden global dependency
```

Don't use singletons

```
loader = ConfigLoader.get_instance()  # WRONG - hidden singleton
```

Don't create dependencies internally

```
def __init__(self):
```

```
    self._loader = ConfigLoader()  # WRONG - should be injected
```

Don't import and instantiate inside methods

```
def load(self):
```

```
    from loader import Loader; loader = Loader()  # WRONG - inject via constructor
```