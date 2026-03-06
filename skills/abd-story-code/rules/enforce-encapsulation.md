---
title: enforce-encapsulation
priority: 99
---

## enforce-encapsulation

CRITICAL: Hide implementation details and expose minimal interface. Make fields private by default
expose behavior not data. NEVER pass raw dicts/lists that expose internal structure - use typed objects that encapsulate the data. Follow Law of Demeter (principle of least knowledge).