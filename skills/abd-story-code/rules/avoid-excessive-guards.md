---
title: avoid-excessive-guards
priority: 99
---

## avoid-excessive-guards

Excessive guard clauses add to cyclomatic complexity and make code harder to read. Centralize error handling in one place rather than scattering defensive checks throughout the code. Let code fail fast with clear errors rather than silently handling missing components.