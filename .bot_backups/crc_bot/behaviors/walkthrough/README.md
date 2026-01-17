# Walkthrough Behavior

**Order**: 7 (after exploration)  
**Purpose**: Validate domain model through scenario realization walkthroughs

## Overview

The walkthrough behavior traces object flows through domain model concepts to validate the model can support key stories and scenarios. By walking through explicit Object.method(param: value) calls with actual return values, it identifies gaps, contradictions, and areas for improvement in the domain model.

## Goals

- **Validate** domain model supports story requirements
- **Identify** missing concepts, responsibilities, or collaborators
- **Update** story-graph.json domain model immediately when gaps discovered
- **Discover** contradictions or overly complex flows
- **Refine** domain model based on realization insights
- **Document** key object flows and model updates for implementation reference

## Inputs

- `story-graph.json` with domain model and stories
- Domain model diagrams (from domain behavior)
- Story scenarios and acceptance criteria

## Outputs

- `story-graph.json` updated with:
  - Realization scenarios in domain concepts (scope and walks)
  - Refined domain concepts with added responsibilities, collaborators, and new concepts discovered during walkthrough
- `walkthrough-realizations.md` documenting traced scenarios and model updates
- Recommendations for domain model improvements

## Actions

1. **Clarify**: Identify which scenarios to trace, areas of risk/uncertainty
2. **Strategy**: Decide walkthrough depth and prioritization
3. **Build**: Trace scenarios using object flow format, update domain model as needed
4. **Validate**: Verify walkthroughs align to model and expose any gaps
5. **Render**: Generate walkthrough realization documents

## Key Format

Each scenario includes a **Scope** showing the dot-notation path to the scenario:

```
Scope: Run Interactive REPL.Execute Operations.Execute Action Operation Through CLI.Execute Instructions Operation
```

Followed by multiple **Walk Throughs** showing granular traces:

```
Walk 1 - Covers: Steps 1-3 (parse and navigate)

ObjectName
    result: actual_value = Object.method(param: value)
        -> nested: value = Collaborator.method(param: value)
            -> deeper: value = AnotherObject.method(param: value)
            return deeper: value
        return nested: value
    return result: actual_value

Walk 2 - Covers: Step 4 (execute)

AnotherObject
    result: value = AnotherObject.method(param: value)
        ...
```

This structure is stored in `story-graph.json` domain concepts:
- `scope`: Dot-notation path to parent context
- `walks`: Array of individual walks, each with `covers` and `object_flow`

## Rules

1. **use_object_flow_format.json**: Use Object.method(param: value) with nested calls and actual return values
2. **align_to_domain_model.json**: Use exact concept names, responsibilities, and collaborators from model
3. **trace_complete_scenarios.json**: Trace from start to completion, identify gaps, update model as needed
4. **document_covers_mapping.json**: Document Covers mapping (Epic → Sub-Epic → Story → AC → Scenario → Steps) for traceability
5. **update_domain_model_on_discovery.json**: When discovering missing responsibilities, collaborators, or concepts, immediately update story-graph.json domain model

## Guardrails

- **Key Questions**: Which scenarios to trace, areas of risk, depth needed
- **Strategy Decisions**: 
  - Walkthrough purpose (business complexity, architecture complexity, integration complexity, new frameworks, mixed)
  - Walkthrough depth (high-level, story-level, detailed, mixed)

## When to Use

- After **domain** and **design** behaviors have defined the model
- Before **code** behavior to validate model will work
- When architectural uncertainty or integration complexity exists
- When object interactions are poorly understood
- To verify model supports critical scenarios

## Strategy

Focus walkthrough effort on:
- **Architectural uncertainty**: Novel patterns, new technology
- **Integration complexity**: Multiple systems, data transformation
- **Business complexity**: Complex rules, regulatory requirements
- **Key domain concepts**: Core business objects and their interactions

Stop when:
- Tracing same patterns repeatedly (diminishing returns)
- Model has been validated for key scenarios
- No new gaps or contradictions are being discovered

## Example Scenario

**Scope**: Run Interactive REPL.Manage Scope.Set Scope Through CLI.Set Scope With Story Names

**Walk 1 - Covers**: Steps 1-2 (parse and set)

```
CLIScope
    result: "Scope set to: Story1, Story2" = CLIScope.set_scope(scope_string: "Story1, Story2")
        -> scope: {type: STORY, value: ["Story1", "Story2"]} = CLIScope._parse_scope_string(scope_string: "Story1, Story2")
        -> session.scope = scope
        return result: "Scope set to: Story1, Story2"
```

**Walk 2 - Covers**: Step 3 (validate and display)

```
CLIScope
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

## Integration with Other Behaviors

- **Consumes**: Domain model from `domain` behavior, design patterns from `design` behavior
- **Produces**: Validated model with realization scenarios, recommendations for improvements
- **Informs**: `code` behavior with detailed object flow examples for implementation

