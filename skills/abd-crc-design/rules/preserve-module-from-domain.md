---
title: preserve-module-from-domain
priority: 1
---

## preserve-module-from-domain

Preserve module field from domain phase and verify accuracy. Module MUST match source code folder structure using dot notation.

**DO**

Preserve module field and verify it matches actual file locations after design refinements

MUST preserve module field from domain phase - do not remove or change arbitrarily

```
From domain phase:
```

```
CLIBot
```

```
    module: 'repl_cli.cli_bot'
```

```
Design phase preserves:
```

```
CLIBot
```

```
    module: 'repl_cli.cli_bot'
```

```
    instantiated_with: ['Bot', 'REPLSession']
```

```
    responsibilities: [...detailed design...]
```

```
(Module field preserved exactly as defined in domain phase)
```

If class moves during design
update module to reflect new actual location

```
Domain phase: Scanner was in 'scanners'
```

```
Design phase: Scanner moved to 'scanners.domain_model'
```

```
Scanner
```

```
    module: 'scanners.domain_model'  (updated to match new location)
```

```
    responsibilities: [...]
```

```
(Module updated because actual file location changed)
```

Verify module accuracy - ensure it still matches folder structure after design changes

```
Portfolio
```

```
    module: 'domain.portfolio'
```

```
    ownership: { has: ['Holding'], references: ['MarketData'] }
```

```
Verify: Does src/domain/portfolio/ folder exist? YES ✓
```

```
Verify: Is Portfolio class still in that folder? YES ✓
```

```
(Module field verified to match actual source location)
```

**DO NOT**

Don't remove module field
don't change it without reason
don't use incorrect paths

Don't remove module field during design refinement

```
Portfolio
```

```
    instantiated_with: ['Customer']
```

```
    responsibilities: [...]
```

```
(WRONG: module field missing)
```

```
(Must include: module: 'domain.portfolio')
```

Don't change module arbitrarily - only update if actual file location changed

```
Domain phase had:
```

```
Scanner
```

```
    module: 'scanners'
```

```
Design phase changes to:
```

```
Scanner
```

```
    module: 'validation.scanners' (WRONG: changed without file moving)
```

```
(Only change module if file actually moved to new folder)
```

Don't use generic module names when preserving from domain

```
DomainModelSynchronizer
```

```
    module: 'utils' (WRONG: too generic)
```

```
(Should be specific: 'synchronizers.domain_model')
```