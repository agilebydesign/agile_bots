---
title: create-parameterized-tests-for-scenarios
priority: 9
---

## create-parameterized-tests-for-scenarios

If scenarios have Examples tables
create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input
expected'
[(1
2)
(3
4)])

**DO**

Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths
count'
[(['p1'
'p2']
2)
(['p3']
1)])

Use @pytest.mark.parametrize for Examples table rows

```
@pytest.mark.parametrize('rule_paths,expected_count', [
```

```
    (['path1', 'path2'], 2),
```

```
    (['path3'], 1),
```

```
])
```

```
def test_scanner_discovery(rule_paths, expected_count):
```

Each example row becomes a test case

```
# Examples table:
```

```
# | input | expected |
```

```
# | 1     | 2        |
```

```
# | 3     | 4        |
```

```
# -> @pytest.mark.parametrize('input,expected', [(1,2), (3,4)])
```

Test body uses parameters from Examples

```
def test_calculation(input, expected):
```

```
    result = calculate(input)
```

```
    assert result == expected
```

**DO NOT**

Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

Don't hardcode single example when table has multiple

```
def test_scanner():
```

```
    paths = ['path1']  # WRONG - ignores other Examples rows
```

Don't duplicate test methods for each example

```
def test_with_2_scanners(): ...  # WRONG
```

```
def test_with_1_scanner(): ...   # WRONG - use parametrize
```

Don't write loops inside tests instead of parametrize

```
def test_all_cases():
```

```
    for case in cases:  # WRONG - use parametrize for isolation
```