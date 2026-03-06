---
title: rule-change-impact
priority: 99
---

## rule-change-impact

Compare current validation violations against a saved baseline to detect the impact of rule or scanner changes. Run validate with --save-baseline before changing rules
then run again after to see the diff.

**DO**

Save a baseline before modifying rules or scanners
then compare after

Baseline captures violation snapshot. After rule/scanner change
diff shows new violations
resolved violations
and severity changes.

```
Before change: save baseline with 12 violations
```

```
After change: 10 violations remain, 2 resolved, 3 new -> net impact visible
```

**DO NOT**

Do not modify rules without checking impact

Changing rules without a baseline means you cannot measure impact. Always save a baseline first.

```
No baseline: 'No baseline found' info message shown
```

```
Stale baseline: results may not reflect recent changes
```