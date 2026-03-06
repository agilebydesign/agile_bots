---
title: refactor-completely-not-partially
priority: 99
---

## refactor-completely-not-partially

CRITICAL: When refactoring
replace old code completely - don't try to support both legacy and new patterns. Write new code
delete old code
fix tests. Clean breaks are better than compatibility bridges that create technical debt.