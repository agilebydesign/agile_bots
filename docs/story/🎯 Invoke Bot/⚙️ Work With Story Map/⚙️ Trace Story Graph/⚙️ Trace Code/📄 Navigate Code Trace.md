# 📄 Navigate Code Trace

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map)

**User:** Developer
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Trace Story Graph](..) / [⚙️ Trace Code](.)  
**Sequential Order:** 4.0
**Story Type:** user

## Story Description

Navigate Code Trace functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-clicking-a-method-call-navigates-to-target-node"></a>
### Scenario: [Clicking a method call navigates to target node](#scenario-clicking-a-method-call-navigates-to-target-node) (happy_path)

**Steps:**
```gherkin
Given the trace shows method call "{target_node}" inside code box "{source_node}"
When Developer clicks the method call "{target_node}"
Then Trace Editor scrolls to the "{target_node}" node and highlights it
```

**Examples:**

| Source Node | Target Node | Expected Result |
| --- | --- | --- |
| approve_transfer | apply_rules | navigate and highlight target node |


<a id="scenario-nested-method-call-expands-parents"></a>
### Scenario: [Nested method call expands parents](#scenario-nested-method-call-expands-parents) (edge_case)

**Steps:**
```gherkin
Given the trace shows collapsed node "{collapsed_node}" with nested call "{target_node}"
When Developer clicks the nested call "{target_node}"
Then Trace Editor expands parent nodes and navigates to "{target_node}"
```

**Examples:**

| Collapsed Node | Target Node | Expected Result |
| --- | --- | --- |
| apply_rules | write_entry | parents expanded and target visible |


<a id="scenario-not-traced-method-shows-indicator"></a>
### Scenario: [Not traced method shows indicator](#scenario-not-traced-method-shows-indicator) (error_case)

**Steps:**
```gherkin
Given the trace does not include method "{method_call}" with trace state "{trace_state}"
When Developer clicks the method call "{method_call}"
Then Trace Editor shows indicator "{expected_indicator}" and does not navigate
```

**Examples:**

| Method Call | Trace State | Expected Indicator |
| --- | --- | --- |
| external_library_call | not_traced | Not traced |

