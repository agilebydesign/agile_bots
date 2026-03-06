---
title: never-swallow-exceptions
priority: 99
---

## never-swallow-exceptions

CRITICAL: Never swallow exceptions silently. Empty catch blocks hide failures and make debugging impossible. Always log
handle
or rethrow exceptions with context.