---
title: use-ascii-only
priority: 18
---

## use-ascii-only

All test code must use ASCII-only characters. No Unicode symbols
emojis
or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')

**DO**

Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')

Use ASCII status indicators

```
print('[PASS] Agent initialized successfully')
```

```
print('[ERROR] Configuration file not found')
```

```
print('[FAIL] Test assertion failed')
```

Use ASCII in assertions

```
assert result.status == 'success'
```

```
assert result.message == 'Agent initialized'
```

Use ASCII arrows and bullets

```
print('-> Next step')
```

```
print('* Item 1')
```

```
print('- Bullet point')
```

**DO NOT**

Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

Don't use Unicode checkmarks

```
print('[checkmark] Agent initialized')  # WRONG - use [PASS]
```

Don't use emojis

```
print('[check_emoji] Configuration loaded')  # WRONG - use [OK]
```

Don't use Unicode arrows or symbols

```
print('[arrow] Next step')  # WRONG - use '->'
```