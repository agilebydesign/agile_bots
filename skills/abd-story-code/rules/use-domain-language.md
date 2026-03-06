---
title: use-domain-language
priority: 99
---

## use-domain-language

CRITICAL: Code must use domain-specific language
not generic terms. NEVER use Dict[str
Any]
List[str]
or generic 'data'/'config'/'parameters' - use typed domain objects. Objects should expose properties representing what they contain (e.g.
recommended_trades)
not methods that 'generate' or 'calculate' things.