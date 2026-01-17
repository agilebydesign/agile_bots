# Domain Walkthrough Realizations: {solution_name}

**Date**: {date}  
**Status**: {status}  
**Domain Model Version**: {domain_model_version}

## Purpose

This document validates the domain model by tracing object flows through key scenarios. Each walkthrough proves the model can fulfill story requirements by showing explicit method calls, parameters, nested collaborations, and return values.

**Coverage Tracking**: Each walkthrough explicitly maps to story graph nodes (Epic → Sub-Epic → Story → AC → Scenario → Steps). This "Covers" information is also stored in story-graph.json domain concepts as realization scenarios.

---

## Walkthrough Strategy

**Purpose**: {walkthrough_purpose}  
**Depth**: {walkthrough_depth}  
**Focus Areas**: {focus_areas}  
**Stopping Criteria**: {stopping_criteria}

**Scenarios Selected**:
{scenarios_selected}

**Rationale**:
{strategy_rationale}

---

## Realization Scenarios

### Scenario 1: {scenario_name}

**Purpose**: {what_this_validates}  
**Concepts Traced**: {primary_concepts}

**Scope**: {epic_name}.{sub_epic_name}.{story_name}.{scenario_name}  


#### Walk Throughs

**Walk 1: Covers**: {walk_scope}
```
{ObjectName}
    {result}: {actual_value} = {Object}.{method}({param}: {value})
        -> {nested_result}: {nested_value} = {Collaborator}.{method}({param}: {value})
            -> {deeper_result}: {deeper_value} = {DeepCollaborator}.{method}({param}: {value})
            return {deeper_result}: {deeper_value}
        -> {sibling_result}: {sibling_value} = {AnotherCollaborator}.{method}({param}: {value})
        return {nested_result}: {nested_value}
    return {result}: {actual_value}
```

**Walk 2 - Covers**: {walk_scope}
```
{ObjectName}
    {result}: {actual_value} = {Object}.{method}({param}: {value})
        -> {nested_result}: {nested_value} = {Collaborator}.{method}({param}: {value})
            -> {deeper_result}: {deeper_value} = {DeepCollaborator}.{method}({param}: {value})
            return {deeper_result}: {deeper_value}
        -> {sibling_result}: {sibling_value} = {AnotherCollaborator}.{method}({param}: {value})
        return {nested_result}: {nested_value}
    return {result}: {actual_value}
```
**Walk ..**

---

**Example: Execute Build Instructions**

**Purpose**: Validate REPLSession can parse commands, navigate to actions, and execute operations  
**Concepts Traced**: REPLSession, CommandParser, CLIBot, CLIBehavior, CLIAction

**Scope**: Run Interactive REPL.Execute Operations.Execute Action Operation Through CLI.Execute Instructions Operation

#### Walk Throughs

**Walk 1 - Covers**: Steps 1-3 (parse command and navigate)

```
REPLSession
    command: {behavior: "shape", action: "build", operation: "instructions"} = REPLSession.run_repl_loop()
        -> is_interactive: True = TTYDetector.is_interactive()
        -> command: {behavior: "shape", action: "build", operation: "instructions"} = CommandParser.parse_command(input_line: "shape.build.instructions")
            -> behavior_name: "shape" = CommandParser.extract_behavior(input_line: "shape.build.instructions")
            -> action_name: "build" = CommandParser.extract_action(input_line: "shape.build.instructions")
            -> operation_name: "instructions" = CommandParser.extract_operation(input_line: "shape.build.instructions")
            return command: {behavior: "shape", action: "build", operation: "instructions"}
        -> cli_behavior: <CLIBehavior wrapping shape> = CLIBot.behaviors.get_behavior(name: "shape")
            -> domain_behavior: <Behavior shape> = Bot.behaviors.find_behavior(name: "shape")
            return cli_behavior: <CLIBehavior wrapping shape>
        -> cli_action: <CLIAction wrapping build> = cli_behavior.actions.get_action(name: "build")
            -> domain_action: <Action build> = Behavior.actions.find_action(name: "build")
            return cli_action: <CLIAction wrapping build>
        return command: {behavior: "shape", action: "build", operation: "instructions"}
```

**Walk 2 - Covers**: Step 4 (execute operation)

```
CLIAction
    result: "Build knowledge graph..." = cli_action.execute_operation(operation: "instructions", args: "")
        -> context: {} = CLIAction._parse_args_to_context(args: "")
        -> instruction_dict: {template: "...", rules: [...]} = Action.get_instructions(context)
        -> formatted: "Build knowledge graph..." = CLIAction._format_result(instruction_dict)
        return result: "Build knowledge graph..."
```

**Walk 3 - Covers**: Step 5 (display status)

```
REPLSession
    status: "STORY_BOT CLI\n[x] shape..." = StatusDisplay.render(CLIBot)
        -> header: "STORY_BOT CLI\nBot Path: ..." = HeaderDisplay.render(CLIBot)
        -> tree: "[x] shape\n[*] domain..." = HierarchyTreeDisplay.render(CLIBot)
        -> footer: "Commands: status | back..." = FooterDisplay.render()
        return status: "STORY_BOT CLI\n...\nCommands: ..."
```

**Validation Result**: ✅ Model supports this scenario  
**Gaps Found**: None  
**Recommendations**: None

---

### Scenario 2: Set and Validate Scope

**Purpose**: Validate CLIScope can parse scope strings, create Scope objects with filters, and validate against story graph  
**Concepts Traced**: CLIScope, Scope, KnowledgeGraphFilter, StoryGraph

**Scope**: Run Interactive REPL.Manage Scope.Set Scope Through CLI.Set Scope With Story Names

#### Walk Throughs

**Walk 1 - Covers**: Steps 1-2 (parse and set scope)

```
CLIBot
    result: "Scope set to: Story1, Story2" = CLIScope.set_scope(scope_string: "Story1, Story2")
        -> scope: {type: STORY, value: ["Story1", "Story2"], filter: <KnowledgeGraphFilter>} = CLIScope._parse_scope_string(scope_string: "Story1, Story2")
            -> scope_type: STORY = Scope.infer_type(value: ["Story1", "Story2"])
            -> filter: <KnowledgeGraphFilter> = Scope.__post_init__(type: STORY)
                return filter: <KnowledgeGraphFilter>
            return scope: {type: STORY, value: ["Story1", "Story2"], filter: <KnowledgeGraphFilter>}
        -> session.scope = scope
        return result: "Scope set to: Story1, Story2"
```

**Walk 2 - Covers**: Step 3 (validate and display scope)

```
CLIBot
    display: "Scope Filter: Story1 ✓, Story2 ✓" = CLIScope.view_scope()
        -> validation: [("Story1", True), ("Story2", True)] = Scope.validate_scope(story_graph)
            -> results: [("Story1", True), ("Story2", True)] = KnowledgeGraphFilter.check_nodes(nodes: ["Story1", "Story2"], graph)
                -> story1_exists: True = KnowledgeGraphFilter.find_node(graph, "Story1")
                -> story2_exists: True = KnowledgeGraphFilter.find_node(graph, "Story2")
                return results: [("Story1", True), ("Story2", True)]
            return validation: [("Story1", True), ("Story2", True)]
        -> formatted: "Scope Filter: Story1 ✓, Story2 ✓" = CLIScope._format_scope_display(scope, validation_results)
        return display: "Scope Filter: Story1 ✓, Story2 ✓"
```

**Validation Result**: ⚠️ Partial - found gap  
**Gaps Found**: 
- Scope missing "Validates against story graph" responsibility
- KnowledgeGraphFilter missing "check_nodes" and "find_node" responsibilities

**Recommendations**:
- Update Scope concept to include: "Validates against story graph: ValidationResults, StoryGraph, KnowledgeGraphFilter"
- Update KnowledgeGraphFilter to include: "Checks nodes exist in graph: ValidationResults, StoryGraph"

---

### Scenario 3: {next_scenario_name}

**Purpose**: {what_this_validates}  
**Concepts Traced**: {primary_concepts}

**Scope**: {epic_name}.{sub_epic_name}.{story_name}.{scenario_name}

#### Walk Throughs

**Walk 1 - Covers**: {walk_scope}

```
{ObjectName}
    {result}: {actual_value} = {Object}.{method}({param}: {value})
        -> {nested_result}: {nested_value} = {Collaborator}.{method}({param}: {value})
        return {nested_result}: {nested_value}
    return {result}: {actual_value}
```

**Walk 2 - Covers**: {walk_scope}

```
{ObjectName}
    {result}: {actual_value} = {Object}.{method}({param}: {value})
        ...
```

**Validation Result**: {result_status}  
**Gaps Found**: {gaps_or_none}  
**Recommendations**: {recommendations_or_none}

---

_(Continue with additional scenarios using same format)_

---

## Model Updates Discovered

### New Responsibilities Added

**Scope**
- Added: "Validates against story graph: ValidationResults, StoryGraph, KnowledgeGraphFilter"
- Rationale: Walkthrough showed validation is needed but wasn't in model

**KnowledgeGraphFilter**
- Added: "Checks nodes exist in graph: ValidationResults, StoryGraph"
- Added: "Finds node by name: Node, StoryGraph"
- Rationale: Validation requires checking individual nodes in graph

### New Concepts Discovered

**ValidationResults**
- Description: Results of validating scope nodes against story graph
- Responsibilities:
  - "Shows valid nodes: List[NodeName]"
  - "Shows invalid nodes: List[NodeName]"
  - "Formats as display string: str"
- Collaborators: None (value object)
- Rationale: Needed to return structured validation data

### Responsibilities Removed

None

### Responsibilities Modified

**CLIScope** - Changed: "Parses scope string" → "Parses scope string and creates Scope object"
- Rationale: Clarify that parsing includes object creation, not just string splitting

---

## Model Validation Summary

**Total Scenarios Traced**: {total_scenarios}  
**Scenarios Validated**: {validated_count} ✅  
**Scenarios with Gaps**: {gaps_count} ⚠️  
**New Concepts Discovered**: {new_concepts_count}  
**Responsibilities Added**: {responsibilities_added_count}  
**Responsibilities Modified**: {responsibilities_modified_count}

**Model Confidence**: {confidence_level}

---

## Recommended Next Steps

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

---

## Source Material

- **Story Graph**: `story-graph.json`
- **Domain Model**: From story-graph.json domain_concepts
- **Realization Scenarios**: Stored in story-graph.json domain_concepts with "Covers" mapping
- **Stories Traced**: {stories_traced}
- **ACs/Scenarios Traced**: {scenarios_traced_count}
- **Story Graph Coverage**: {coverage_stats}

---

## Walkthrough Notes

{walkthrough_notes}

**Patterns Observed**:
{patterns_observed}

**Areas Needing More Detail**:
{areas_needing_detail}

---

## Story Graph Integration

Each walkthrough realization is stored in `story-graph.json` under the relevant domain concept with the following format:

```json
{
  "concept_name": "REPLSession",
  "realizations": [
    {
      "name": "Execute Build Instructions",
      "scope": "Run Interactive REPL.Execute Operations.Execute Action Operation Through CLI.Execute Instructions Operation",
      "walks": [
        {
          "walk_number": 1,
          "covers": "Steps 1-3 (parse command and navigate)",
          "object_flow": "REPLSession\n    command: {...} = REPLSession.run_repl_loop()\n        ..."
        },
        {
          "walk_number": 2,
          "covers": "Step 4 (execute operation)",
          "object_flow": "CLIAction\n    result: \"...\" = cli_action.execute_operation(...)\n        ..."
        },
        {
          "walk_number": 3,
          "covers": "Step 5 (display status)",
          "object_flow": "REPLSession\n    status: \"...\" = StatusDisplay.render(...)\n        ..."
        }
      ]
    }
  ]
}
```

**Walk Covers Examples**:
- Story-level walkthrough: `"covers": "Steps 1-3"`
- Sub-epic-level walkthrough: `"covers": "Stories: Story1, Story2"`
- Epic-level walkthrough: `"covers": "Sub-epics: Execute Operations, Manage Scope"`
- Partial story coverage: `"covers": "Steps 1, 3, 5 (skip error handling)"`
- Error flow: `"covers": "Step 2 (error case when validation fails)"`

This allows traceability from domain concepts to the stories they support, with granular coverage tracking per walk.
