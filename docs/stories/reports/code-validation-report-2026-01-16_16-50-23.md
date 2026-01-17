# Validation Report - Code

**Generated:** 2026-01-16 16:50:25
**Project:** agile_bots
**Behavior:** code
**Action:** validate

## Summary

Validated story map and domain model and 288 code file(s) against **32 validation rules**.

## Content Validated

- **Clarification:** `clarification.json`
- **Rendered Outputs:**
  - `story-graph.json`
- **Code Files Scanned:**
  - `src\actions\action.py`
  - `src\actions\action_context.py`
  - `src\actions\action_factory.py`
  - `src\actions\action_state_manager.py`
  - `src\actions\actions.py`
  - `src\actions\activity_tracker.py`
  - `src\actions\behavior_action_status_builder.py`
  - `src\actions\build\build_action.py`
  - `src\actions\build\json_build_action.py`
  - `src\actions\build\markdown_build_action.py`
  - `src\actions\build\story_graph_data.py`
  - `src\actions\build\story_graph_spec.py`
  - `src\actions\build\story_graph_template.py`
  - `src\actions\build\tty_build_action.py`
  - `src\actions\clarify\clarify_action.py`
  - `src\actions\clarify\evidence.py`
  - `src\actions\clarify\json_clarify_action.py`
  - `src\actions\clarify\key_questions.py`
  - `src\actions\clarify\markdown_clarify_action.py`
  - `src\actions\clarify\required_context.py`
  - `src\actions\clarify\requirements_clarifications.py`
  - `src\actions\clarify\tty_clarify_action.py`
  - `src\actions\content.py`
  - `src\actions\guardrails\guardrails.py`
  - `src\actions\guardrails\tty_guardrails.py`
  - `src\actions\guardrails\tty_required_context.py`
  - `src\actions\guardrails\tty_strategy.py`
  - `src\actions\json_actions.py`
  - `src\actions\markdown_action.py`
  - `src\actions\markdown_actions.py`
  - `src\actions\render\evidence.py`
  - `src\actions\render\json_render_action.py`
  - `src\actions\render\markdown_render_action.py`
  - `src\actions\render\render_action.py`
  - `src\actions\render\render_config_loader.py`
  - `src\actions\render\render_instruction_builder.py`
  - `src\actions\render\render_spec.py`
  - `src\actions\render\synchronizer.py`
  - `src\actions\render\template.py`
  - `src\actions\render\tty_render_action.py`
  - `src\actions\strategy\assumptions.py`
  - `src\actions\strategy\json_persistent.py`
  - `src\actions\strategy\json_strategy_action.py`
  - `src\actions\strategy\markdown_strategy_action.py`
  - `src\actions\strategy\strategy.py`
  - `src\actions\strategy\strategy_action.py`
  - `src\actions\strategy\strategy_criteria.py`
  - `src\actions\strategy\strategy_criterias.py`
  - `src\actions\strategy\strategy_decision.py`
  - `src\actions\strategy\tty_strategy_action.py`
  - `src\actions\tty_action.py`
  - `src\actions\tty_actions.py`
  - `src\actions\validate\background_validation_handler.py`
  - `src\actions\validate\file_discovery.py`
  - `src\actions\validate\file_link_builder.py`
  - `src\actions\validate\json_validate_action.py`
  - `src\actions\validate\markdown_validate_action.py`
  - `src\actions\validate\story_graph.py`
  - `src\actions\validate\tty_validate_action.py`
  - `src\actions\validate\validate_action.py`
  - `src\actions\validate\validation_executor.py`
  - `src\actions\validate\validation_report_builder.py`
  - `src\actions\validate\validation_report_formatter.py`
  - `src\actions\validate\validation_report_writer.py`
  - `src\actions\validate\validation_scope.py`
  - `src\actions\validate\validation_stats.py`
  - `src\actions\validate\validation_type.py`
  - `src\actions\validate\validation_violations_builder.py`
  - `src\actions\validate\violation_formatter.py`
  - `src\actions\workflow_status_builder.py`
  - `src\behaviors\behavior.py`
  - `src\behaviors\behaviors.py`
  - `src\behaviors\json_behavior.py`
  - `src\behaviors\markdown_behavior.py`
  - `src\behaviors\tty_behavior.py`
  - `src\bot\behavior.py`
  - `src\bot\behaviors.py`
  - `src\bot\bot.py`
  - `src\bot\bot_paths.py`
  - `src\bot\json_bot.py`
  - `src\bot\markdown_bot.py`
  - `src\bot\tty_bot (1).py`
  - `src\bot\tty_bot.py`
  - `src\bot\workspace.py`
  - `src\bot_path\bot_path.py`
  - `src\bot_path\json_bot_path.py`
  - `src\bot_path\markdown_bot_path.py`
  - `src\bot_path\path_resolver.py`
  - `src\bot_path\tty_bot_path.py`
  - `src\cli\action_data_collector.py`
  - `src\cli\adapter_factory.py`
  - `src\cli\adapters.py`
  - `src\cli\base_hierarchical_adapter.py`
  - `src\cli\cli_generator.py`
  - `src\cli\cli_main.py`
  - `src\cli\cli_results.py`
  - `src\cli\cli_session.py`
  - `src\cli\cursor\cursor_command_visitor.py`
  - `src\cli\description_extractor.py`
  - `src\cli\formatter.py`
  - `src\cli\help_context.py`
  - `src\cli\orchestrator.py`
  - `src\cli\visitor.py`
  - `src\exit_result\exit_result.py`
  - `src\exit_result\json_exit_result.py`
  - `src\exit_result\markdown_exit_result.py`
  - `src\exit_result\tty_exit_result.py`
  - `src\ext\behavior_matcher.py`
  - `src\ext\bot_matcher.py`
  - `src\ext\trigger_domain.py`
  - `src\ext\trigger_router.py`
  - `src\ext\trigger_router_entry.py`
  - `src\ext\trigger_words.py`
  - `src\help\help.py`
  - `src\help\help_action.py`
  - `src\help\json_help.py`
  - `src\help\markdown_help.py`
  - `src\help\tty_help.py`
  - `src\instructions\context_data_injector.py`
  - `src\instructions\instructions.py`
  - `src\instructions\json_instructions.py`
  - `src\instructions\markdown_instructions.py`
  - `src\instructions\reminders.py`
  - `src\instructions\tty_instructions.py`
  - `src\navigation\json_navigation.py`
  - `src\navigation\markdown_navigation.py`
  - `src\navigation\navigation.py`
  - `src\navigation\tty_navigation.py`
  - `src\rules\rule.py`
  - `src\rules\rule_filter.py`
  - `src\rules\rule_loader.py`
  - `src\rules\rules.py`
  - `src\rules\rules_action.py`
  - `src\rules\rules_digest_guidance.py`
  - `src\rules\scan_config.py`
  - `src\scanners\abstraction_levels_scanner.py`
  - `src\scanners\ac_consolidation_scanner.py`
  - `src\scanners\active_language_scanner.py`
  - `src\scanners\actor_alternation_scanner.py`
  - `src\scanners\arrange_act_assert_scanner.py`
  - `src\scanners\ascii_only_scanner.py`
  - `src\scanners\background_common_setup_scanner.py`
  - `src\scanners\bad_comments_scanner.py`
  - `src\scanners\behavioral_ac_scanner.py`
  - `src\scanners\business_readable_test_names_scanner.py`
  - `src\scanners\calculation_timing_code_scanner.py`
  - `src\scanners\calculation_timing_scanner.py`
  - `src\scanners\class_based_organization_scanner.py`
  - `src\scanners\class_size_scanner.py`
  - `src\scanners\clear_parameters_scanner.py`
  - `src\scanners\code_representation_code_scanner.py`
  - `src\scanners\code_representation_scanner.py`
  - `src\scanners\code_scanner.py`
  - `src\scanners\communication_verb_scanner.py`
  - `src\scanners\complete_refactoring_scanner.py`
  - `src\scanners\complexity_metrics.py`
  - `src\scanners\consistent_indentation_scanner.py`
  - `src\scanners\consistent_naming_scanner.py`
  - `src\scanners\consistent_vocabulary_scanner.py`
  - `src\scanners\cover_all_paths_scanner.py`
  - `src\scanners\dead_code_scanner.py`
  - `src\scanners\delegation_code_scanner.py`
  - `src\scanners\delegation_scanner.py`
  - `src\scanners\dependency_chaining_code_scanner.py`
  - `src\scanners\dependency_chaining_scanner.py`
  - `src\scanners\descriptive_function_names_scanner.py`
  - `src\scanners\domain_concept_node.py`
  - `src\scanners\domain_grouping_code_scanner.py`
  - `src\scanners\domain_grouping_scanner.py`
  - `src\scanners\domain_language_code_scanner.py`
  - `src\scanners\domain_language_scanner.py`
  - `src\scanners\domain_scanner.py`
  - `src\scanners\duplication_scanner.py`
  - `src\scanners\encapsulation_scanner.py`
  - `src\scanners\enumerate_ac_permutations_scanner.py`
  - `src\scanners\enumerate_stories_scanner.py`
  - `src\scanners\error_handling_isolation_scanner.py`
  - `src\scanners\exact_variable_names_scanner.py`
  - `src\scanners\exception_classification_scanner.py`
  - `src\scanners\exception_handling_scanner.py`
  - `src\scanners\excessive_guards_scanner.py`
  - `src\scanners\exhaustive_decomposition_scanner.py`
  - `src\scanners\explicit_dependencies_scanner.py`
  - `src\scanners\fixture_placement_scanner.py`
  - `src\scanners\full_result_assertions_scanner.py`
  - `src\scanners\function_size_scanner.py`
  - `src\scanners\generic_capability_scanner.py`
  - `src\scanners\given_precondition_scanner.py`
  - `src\scanners\given_state_not_actions_scanner.py`
  - `src\scanners\given_when_then_helpers_scanner.py`
  - `src\scanners\implementation_details_scanner.py`
  - `src\scanners\import_placement_scanner.py`
  - `src\scanners\increment_folder_structure_scanner.py`
  - `src\scanners\intention_revealing_names_scanner.py`
  - `src\scanners\invest_principles_scanner.py`
  - `src\scanners\meaningful_context_scanner.py`
  - `src\scanners\minimize_mutable_state_scanner.py`
  - `src\scanners\mock_boundaries_scanner.py`
  - `src\scanners\natural_english_code_scanner.py`
  - `src\scanners\natural_english_scanner.py`
  - `src\scanners\no_fallbacks_scanner.py`
  - `src\scanners\no_guard_clauses_scanner.py`
  - `src\scanners\noun_redundancy_scanner.py`
  - `src\scanners\object_oriented_helpers_scanner.py`
  - `src\scanners\observable_behavior_scanner.py`
  - `src\scanners\one_concept_per_test_scanner.py`
  - `src\scanners\open_closed_principle_scanner.py`
  - `src\scanners\parameterized_tests_scanner.py`
  - `src\scanners\plain_english_scenarios_scanner.py`
  - `src\scanners\prefer_object_model_over_config_scanner.py`
  - `src\scanners\present_ac_consolidation_scanner.py`
  - `src\scanners\primitive_vs_object_scanner.py`
  - `src\scanners\property_encapsulation_code_scanner.py`
  - `src\scanners\property_encapsulation_scanner.py`
  - `src\scanners\reaction_chaining_scanner.py`
  - `src\scanners\real_implementations_scanner.py`
  - `src\scanners\resource_oriented_code_scanner.py`
  - `src\scanners\resource_oriented_design_scanner.py`
  - `src\scanners\resources\ast_elements.py`
  - `src\scanners\resources\block.py`
  - `src\scanners\resources\block_extractor.py`
  - `src\scanners\resources\file.py`
  - `src\scanners\resources\line.py`
  - `src\scanners\resources\scan.py`
  - `src\scanners\resources\scope.py`
  - `src\scanners\resources\violation.py`
  - `src\scanners\scanner.py`
  - `src\scanners\scanner_execution_error.py`
  - `src\scanners\scanner_loader.py`
  - `src\scanners\scanner_orchestrator.py`
  - `src\scanners\scanner_registry.py`
  - `src\scanners\scanner_status_formatter.py`
  - `src\scanners\scenario_outline_scanner.py`
  - `src\scanners\scenario_specific_given_scanner.py`
  - `src\scanners\scenarios_cover_all_cases_scanner.py`
  - `src\scanners\scenarios_on_story_docs_scanner.py`
  - `src\scanners\separate_concerns_scanner.py`
  - `src\scanners\setup_similarity_scanner.py`
  - `src\scanners\simplify_control_flow_scanner.py`
  - `src\scanners\single_responsibility_scanner.py`
  - `src\scanners\specification_match_scanner.py`
  - `src\scanners\specificity_scanner.py`
  - `src\scanners\spine_optional_scanner.py`
  - `src\scanners\standard_data_reuse_scanner.py`
  - `src\scanners\story_enumeration_scanner.py`
  - `src\scanners\story_filename_scanner.py`
  - `src\scanners\story_graph_match_scanner.py`
  - `src\scanners\story_map.py`
  - `src\scanners\story_scanner.py`
  - `src\scanners\story_sizing_scanner.py`
  - `src\scanners\swallowed_exceptions_scanner.py`
  - `src\scanners\technical_abstraction_code_scanner.py`
  - `src\scanners\technical_abstraction_scanner.py`
  - `src\scanners\technical_language_scanner.py`
  - `src\scanners\test_boundary_behavior_scanner.py`
  - `src\scanners\test_file_naming_scanner.py`
  - `src\scanners\test_quality_scanner.py`
  - `src\scanners\test_scanner.py`
  - `src\scanners\third_party_isolation_scanner.py`
  - `src\scanners\type_safety_scanner.py`
  - `src\scanners\ubiquitous_language_scanner.py`
  - `src\scanners\unnecessary_parameter_passing_scanner.py`
  - `src\scanners\useless_comments_scanner.py`
  - `src\scanners\validation_scanner_status_builder.py`
  - `src\scanners\verb_noun_scanner.py`
  - `src\scanners\vertical_density_scanner.py`
  - `src\scanners\vertical_slice_scanner.py`
  - `src\scanners\violation.py`
  - `src\scanners\vocabulary_helper.py`
  - `src\scope\action_scope.py`
  - `src\scope\json_scope.py`
  - `src\scope\json_scope_command_result.py`
  - `src\scope\markdown_scope.py`
  - `src\scope\markdown_scope_command_result.py`
  - `src\scope\scope.py`
  - `src\scope\scope_action_context.py`
  - `src\scope\scope_command_result.py`
  - `src\scope\scope_matcher.py`
  - `src\scope\scoping_parameter.py`
  - `src\scope\tty_scope.py`
  - `src\scope\tty_scope_command_result.py`
  - `src\story_graph\domain.py`
  - `src\story_graph\json_story_graph.py`
  - `src\story_graph\markdown_story_graph.py`
  - `src\story_graph\nodes.py`
  - `src\story_graph\story_graph.py`
  - `src\story_graph\tty_story_graph.py`
  - `src\utils.py`
  - **Total:** 288 src file(s)

## Scanner Execution Status

### 🟩 Overall Status: ALL CLEAN

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 31 | Scanners ran without errors |
| 🟩 Clean Rules | 31 | No violations found |
| [i] No Scanner | 1 | Rule has no scanner configured |

**Total Rules:** 32
- **Rules with Scanners:** 31
  - 🟩 **Executed Successfully:** 31
- [i] **Rules without Scanners:** 1

### 🟩 Successfully Executed Scanners

- 🟩 **[Avoid Excessive Guards](#avoid-excessive-guards)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.excessive_guards_scanner.ExcessiveGuardsScanner`
- 🟩 **[Avoid Unnecessary Parameter Passing](#avoid-unnecessary-parameter-passing)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.unnecessary_parameter_passing_scanner.UnnecessaryParameterPassingScanner`
- 🟩 **[Chain Dependencies Properly](#chain-dependencies-properly)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.dependency_chaining_code_scanner.DependencyChainingCodeScanner`
- 🟩 **[Classify Exceptions By Caller Needs](#classify-exceptions-by-caller-needs)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.exception_classification_scanner.ExceptionClassificationScanner`
- 🟩 **[Delegate To Lowest Level](#delegate-to-lowest-level)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.delegation_code_scanner.DelegationCodeScanner`
- 🟩 **[Detect Legacy Unused Code](#detect-legacy-unused-code)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.dead_code_scanner.DeadCodeScanner`
- 🟩 **[Eliminate Duplication](#eliminate-duplication)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.duplication_scanner.DuplicationScanner`
- 🟩 **[Enforce Encapsulation](#enforce-encapsulation)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.encapsulation_scanner.EncapsulationScanner`
- 🟩 **[Favor Code Representation](#favor-code-representation)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.code_representation_code_scanner.CodeRepresentationCodeScanner`
- 🟩 **[Group By Domain](#group-by-domain)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.domain_grouping_code_scanner.DomainGroupingCodeScanner`
- 🟩 **[Hide Business Logic Behind Properties](#hide-business-logic-behind-properties)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.calculation_timing_code_scanner.CalculationTimingCodeScanner`
- 🟩 **[Hide Calculation Timing](#hide-calculation-timing)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.calculation_timing_code_scanner.CalculationTimingCodeScanner`
- 🟩 **[Keep Classes Small With Single Responsibility](#keep-classes-small-with-single-responsibility)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.class_size_scanner.ClassSizeScanner`
- 🟩 **[Keep Functions Single Responsibility](#keep-functions-single-responsibility)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.single_responsibility_scanner.SingleResponsibilityScanner`
- 🟩 **[Keep Functions Small Focused](#keep-functions-small-focused)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.function_size_scanner.FunctionSizeScanner`
- 🟩 **[Maintain Vertical Density](#maintain-vertical-density)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.vertical_density_scanner.VerticalDensityScanner`
- 🟩 **[Never Swallow Exceptions](#never-swallow-exceptions)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.swallowed_exceptions_scanner.SwallowedExceptionsScanner`
- 🟩 **[Place Imports At Top](#place-imports-at-top)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.import_placement_scanner.ImportPlacementScanner`
- 🟩 **[Prefer Object Model Over Config](#prefer-object-model-over-config)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.prefer_object_model_over_config_scanner.PreferObjectModelOverConfigScanner`
- 🟩 **[Provide Meaningful Context](#provide-meaningful-context)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.meaningful_context_scanner.MeaningfulContextScanner`
- 🟩 **[Refactor Completely Not Partially](#refactor-completely-not-partially)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.complete_refactoring_scanner.CompleteRefactoringScanner`
- 🟩 **[Simplify Control Flow](#simplify-control-flow)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.simplify_control_flow_scanner.SimplifyControlFlowScanner`
- 🟩 **[Stop Writing Useless Comments](#stop-writing-useless-comments)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.useless_comments_scanner.UselessCommentsScanner`
- 🟩 **[Use Clear Function Parameters](#use-clear-function-parameters)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.clear_parameters_scanner.ClearParametersScanner`
- 🟩 **[Use Consistent Indentation](#use-consistent-indentation)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.consistent_indentation_scanner.ConsistentIndentationScanner`
- 🟩 **[Use Consistent Naming](#use-consistent-naming)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.consistent_naming_scanner.ConsistentNamingScanner`
- 🟩 **[Use Domain Language](#use-domain-language)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.domain_language_code_scanner.DomainLanguageCodeScanner`
- 🟩 **[Use Exceptions Properly](#use-exceptions-properly)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.exception_handling_scanner.ExceptionHandlingScanner`
- 🟩 **[Use Explicit Dependencies](#use-explicit-dependencies)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.explicit_dependencies_scanner.ExplicitDependenciesScanner`
- 🟩 **[Use Natural English](#use-natural-english)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.natural_english_code_scanner.NaturalEnglishCodeScanner`
- 🟩 **[Use Resource Oriented Design](#use-resource-oriented-design)** - 0 violations (EXECUTION_SUCCESS)
  - Scanner: `agile_bot.src.scanners.resource_oriented_code_scanner.ResourceOrientedCodeScanner`

### <span style="color: gray;">[i] Rules Without Scanners</span>

- <span style="color: gray;">[i]</span> **[Refactor Tests With Production Code](#refactor-tests-with-production-code)** - No scanner configured

## Validation Rules Checked

### 🟩 Rule: <span id="avoid-excessive-guards">Avoid Excessive Guards</span> - CLEAN (0 violations)
**Description:** Excessive guard clauses add to cyclomatic complexity and make code harder to read. Centralize error handling in one place rather than scattering defensive checks throughout the code. Let code fail fast with clear errors rather than silently handling missing components.
**Scanner:** `agile_bot.src.scanners.excessive_guards_scanner.ExcessiveGuardsScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="avoid-unnecessary-parameter-passing">Avoid Unnecessary Parameter Passing</span> - CLEAN (0 violations)
**Description:** Don't pass parameters to internal methods when the value is already accessible through instance variables. Access instance properties directly instead of passing them around unnecessarily.
**Scanner:** `agile_bot.src.scanners.unnecessary_parameter_passing_scanner.UnnecessaryParameterPassingScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="chain-dependencies-properly">Chain Dependencies Properly</span> - CLEAN (0 violations)
**Description:** CRITICAL: Code must chain dependencies properly with constructor injection. Map dependencies in a chain: highest-level object → collaborator → sub-collaborator. Inject collaborators at construction time so methods can use them without passing them as parameters. Access sub-collaborators through their owning objects.
**Scanner:** `agile_bot.src.scanners.dependency_chaining_code_scanner.DependencyChainingCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="classify-exceptions-by-caller-needs">Classify Exceptions By Caller Needs</span> - CLEAN (0 violations)
**Description:** Design exceptions based on how callers will handle them. Create exception types based on caller's needs, use special case objects for predictable failures, and wrap third-party exceptions at boundaries.
**Scanner:** `agile_bot.src.scanners.exception_classification_scanner.ExceptionClassificationScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="delegate-to-lowest-level">Delegate To Lowest Level</span> - CLEAN (0 violations)
**Description:** CRITICAL: Code must delegate responsibilities to the lowest-level object that can handle them. If a collection class can do something, delegate to it rather than implementing it in the parent.
**Scanner:** `agile_bot.src.scanners.delegation_code_scanner.DelegationCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="detect-legacy-unused-code">Detect Legacy Unused Code</span> - CLEAN (0 violations)
**Description:** CRITICAL: Legacy code that is not used by any other code or front-end interfaces (CLI, MCP, web) should be removed. Unused code increases maintenance burden, creates confusion, and violates YAGNI (You Aren't Gonna Need It) principle.
**Scanner:** `agile_bot.src.scanners.dead_code_scanner.DeadCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="eliminate-duplication">Eliminate Duplication</span> - CLEAN (0 violations)
**Description:** CRITICAL: Every piece of knowledge should have a single, authoritative representation (DRY principle). Extract repeated logic into reusable functions and use abstraction to capture common patterns.
**Scanner:** `agile_bot.src.scanners.duplication_scanner.DuplicationScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="enforce-encapsulation">Enforce Encapsulation</span> - CLEAN (0 violations)
**Description:** CRITICAL: Hide implementation details and expose minimal interface. Make fields private by default, expose behavior not data. NEVER pass raw dicts/lists that expose internal structure - use typed objects that encapsulate the data. Follow Law of Demeter (principle of least knowledge).
**Scanner:** `agile_bot.src.scanners.encapsulation_scanner.EncapsulationScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="favor-code-representation">Favor Code Representation</span> - CLEAN (0 violations)
**Description:** CRITICAL: Code should represent domain concepts directly. Domain models should match code. If code doesn't match domain concepts, refactor the code rather than creating abstract domain models.
**Scanner:** `agile_bot.src.scanners.code_representation_code_scanner.CodeRepresentationCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="group-by-domain">Group By Domain</span> - CLEAN (0 violations)
**Description:** CRITICAL: Code must be organized by domain area and relationships, not by technical layers, object types, or architectural concerns.
**Scanner:** `agile_bot.src.scanners.domain_grouping_code_scanner.DomainGroupingCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="hide-business-logic-behind-properties">Hide Business Logic Behind Properties</span> - CLEAN (0 violations)
**Description:** CRITICAL: Hide business logic behind properties. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.
**Scanner:** `agile_bot.src.scanners.calculation_timing_code_scanner.CalculationTimingCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="hide-calculation-timing">Hide Calculation Timing</span> - CLEAN (0 violations)
**Description:** CRITICAL: Code must hide calculations. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.
**Scanner:** `agile_bot.src.scanners.calculation_timing_code_scanner.CalculationTimingCodeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="keep-classes-small-with-single-responsibility">Keep Classes Small With Single Responsibility</span> - CLEAN (0 violations)
**Description:** CRITICAL: Classes should be small (under 200-300 lines) with a single responsibility. Keep classes cohesive (methods/data interdependent), eliminate dead code, and favor many small focused classes over few large ones.
**Scanner:** `agile_bot.src.scanners.class_size_scanner.ClassSizeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="keep-functions-single-responsibility">Keep Functions Single Responsibility</span> - CLEAN (0 violations)
**Description:** CRITICAL: Functions should do one thing and do it well, with no hidden side effects. Each function must have a single, well-defined responsibility.
**Scanner:** `agile_bot.src.scanners.single_responsibility_scanner.SingleResponsibilityScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="keep-functions-small-focused">Keep Functions Small Focused</span> - CLEAN (0 violations)
**Description:** Functions should be small enough to understand at a glance. Keep functions under 20 lines when possible and extract complex logic into named helper functions.
**Scanner:** `agile_bot.src.scanners.function_size_scanner.FunctionSizeScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="maintain-vertical-density">Maintain Vertical Density</span> - CLEAN (0 violations)
**Description:** Related code should be visually close. Group related concepts together, declare variables close to usage, and keep files under 500 lines when possible.
**Scanner:** `agile_bot.src.scanners.vertical_density_scanner.VerticalDensityScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="never-swallow-exceptions">Never Swallow Exceptions</span> - CLEAN (0 violations)
**Description:** CRITICAL: Never swallow exceptions silently. Empty catch blocks hide failures and make debugging impossible. Always log, handle, or rethrow exceptions with context.
**Scanner:** `agile_bot.src.scanners.swallowed_exceptions_scanner.SwallowedExceptionsScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="place-imports-at-top">Place Imports At Top</span> - CLEAN (0 violations)
**Description:** Place all import statements at the top of the file, after module docstrings and comments, but before any executable code. This improves readability and makes dependencies clear.
**Scanner:** `agile_bot.src.scanners.import_placement_scanner.ImportPlacementScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="prefer-object-model-over-config">Prefer Object Model Over Config</span> - CLEAN (0 violations)
**Description:** Use existing object model to access information instead of directly accessing configuration files
**Scanner:** `agile_bot.src.scanners.prefer_object_model_over_config_scanner.PreferObjectModelOverConfigScanner`
**Execution Status:** EXECUTION_SUCCESS

### 🟩 Rule: <span id="provide-meaningful-context">Provide Meaningful Context</span> - CLEAN (0 violations)
**Description:** Names should provide appropriate context without redundancy. Use longer names for longer scopes and replace magic numbers with named constants.
**Scanner:** `agile_bot.src.scanners.meaningful_context_scanner.MeaningfulContextScanner`
**Execution Status:** EXECUTION_SUCCESS

*... and 12 more rules*

## Violations Found

🟩 **No violations found.** All rules passed validation.

## Validation Instructions

The following validation steps were performed:

1. ## Step 1: Scanner Violation Review
2. 
3. {{scanner_output}}
4. 
5. Carefully review all scanner-reported violations as follows:
6. 1. For each violation message, locate the corresponding element in the story graph.
7. 2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
8. 3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
9. 4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
10. 5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
*... and 49 more instructions*

## Report Location

This report was automatically generated and saved to:
`C:\dev\agile_bots\docs\stories\reports\code-validation-report-2026-01-16_16-50-23.md`

