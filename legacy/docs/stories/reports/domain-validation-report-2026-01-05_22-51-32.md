# Validation Report - Domain

**Generated:** 2026-01-05 22:51:32
**Project:** base_bot
**Behavior:** domain
**Action:** validate

## Summary

Validated story map and domain model and 262 code file(s) and 31 test file(s) against **8 validation rules**.

## Content Validated

- **Rendered Outputs:**
  - `story-graph.json`
- **Test Files Scanned:**
  - `test\conftest.py`
  - `test\test_build_agile_bots.py`
  - `test\test_build_knowledge.py`
  - `test\test_current_initialize_repl_session.py`
  - `test\test_decide_strategy_criteria_action.py`
  - `test\test_display_bot_state_using_cli.py`
  - `test\test_display_bot_state_using_cli_current.py`
  - `test\test_document_headless_mode_requirements.py`
  - `test\test_execute_action_operation_through_cli.py`
  - `test\test_execute_action_operation_through_cli_current.py`
  - `test\test_execute_behavior_actions.py`
  - `test\test_execute_in_headless_mode.py`
  - `test\test_formatters.py`
  - `test\test_gather_context.py`
  - `test\test_generate_mcp_tools.py`
  - `test\test_generate_repl_cli.py`
  - `test\test_get_help_using_cli_current.py`
  - `test\test_helpers.py`
  - `test\test_initialize_repl_session.py`
  - `test\test_initialize_repl_session_current.py`
  - `test\test_invoke_bot.py`
  - `test\test_invoke_mcp.py`
  - `test\test_manage_bot_scope_through_cli.py`
  - `test\test_manage_bot_scope_through_cli_current.py`
  - `test\test_monitor_session.py`
  - `test\test_navigate_bot_behaviors_and_actions_with_cli.py`
  - `test\test_navigate_bot_behaviors_and_actions_with_cli_current.py`
  - `test\test_perform_behavior_action.py`
  - `test\test_render_output.py`
  - `test\test_resources.py`
  - `test\test_validation_scope_and_file_filtering.py`
  - **Total:** 31 test file(s)
- **Code Files Scanned:**
  - `src\actions\action.py`
  - `src\actions\action_context.py`
  - `src\actions\action_factory.py`
  - `src\actions\action_scope.py`
  - `src\actions\action_state_manager.py`
  - `src\actions\actions.py`
  - `src\actions\activity_tracker.py`
  - `src\actions\build\build_action.py`
  - `src\actions\build\build_scope.py`
  - `src\actions\build\knowledge.py`
  - `src\actions\build\knowledge_graph_spec.py`
  - `src\actions\build\knowledge_graph_template.py`
  - `src\actions\clarify\clarify_action.py`
  - `src\actions\clarify\evidence.py`
  - `src\actions\clarify\key_questions.py`
  - `src\actions\clarify\required_context.py`
  - `src\actions\clarify\requirements_clarifications.py`
  - `src\actions\content.py`
  - `src\actions\context_data_injector.py`
  - `src\actions\guardrails.py`
  - `src\actions\help_action.py`
  - `src\actions\instructions.py`
  - `src\actions\render\evidence.py`
  - `src\actions\render\render_action.py`
  - `src\actions\render\render_config_loader.py`
  - `src\actions\render\render_instruction_builder.py`
  - `src\actions\render\render_spec.py`
  - `src\actions\render\synchronizer.py`
  - `src\actions\render\template.py`
  - `src\actions\rules\rule.py`
  - `src\actions\rules\rule_filter.py`
  - `src\actions\rules\rule_loader.py`
  - `src\actions\rules\rules.py`
  - `src\actions\rules\rules_action.py`
  - `src\actions\rules\rules_digest_guidance.py`
  - `src\actions\scope_matcher.py`
  - `src\actions\scoping_parameter.py`
  - `src\actions\strategy\assumptions.py`
  - `src\actions\strategy\json_persistent.py`
  - `src\actions\strategy\strategy.py`
  - `src\actions\strategy\strategy_action.py`
  - `src\actions\strategy\strategy_criteria.py`
  - `src\actions\strategy\strategy_criterias.py`
  - `src\actions\strategy\strategy_decision.py`
  - `src\actions\validate\background_validation_handler.py`
  - `src\actions\validate\file_discovery.py`
  - `src\actions\validate\file_link_builder.py`
  - `src\actions\validate\knowledge_graph.py`
  - `src\actions\validate\path_resolver.py`
  - `src\actions\validate\story_graph.py`
  - `src\actions\validate\validate_action.py`
  - `src\actions\validate\validation_executor.py`
  - `src\actions\validate\validation_report_builder.py`
  - `src\actions\validate\validation_report_formatter.py`
  - `src\actions\validate\validation_report_writer.py`
  - `src\actions\validate\validation_scope.py`
  - `src\actions\validate\validation_stats.py`
  - `src\actions\validate\validation_violations_builder.py`
  - `src\actions\validate\violation_formatter.py`
  - `src\actions\workflow_status_builder.py`
  - `src\bot\behavior.py`
  - `src\bot\behaviors.py`
  - `src\bot\bot.py`
  - `src\bot\bot_paths.py`
  - `src\bot\merged_instructions.py`
  - `src\bot\reminders.py`
  - `src\bot\workspace.py`
  - `src\ext\behavior_matcher.py`
  - `src\ext\bot_matcher.py`
  - `src\ext\trigger_domain.py`
  - `src\ext\trigger_router.py`
  - `src\ext\trigger_router_entry.py`
  - `src\ext\trigger_words.py`
  - `src\generator\action_data_collector.py`
  - `src\generator\help_context.py`
  - `src\generator\orchestrator.py`
  - `src\generator\visitor.py`
  - `src\mcp\mcp_code_generator.py`
  - `src\mcp\mcp_code_visitor.py`
  - `src\mcp\mcp_config_generator.py`
  - `src\mcp\mcp_server.py`
  - `src\mcp\mcp_server_generator.py`
  - `src\mcp\server_deployer.py`
  - `src\mcp\server_restart.py`
  - `src\repl_cli\cli_base.py`
  - `src\repl_cli\cli_bot\cli_actions\build_cli_action.py`
  - `src\repl_cli\cli_bot\cli_actions\clarify_cli_action.py`
  - `src\repl_cli\cli_bot\cli_actions\cli_action.py`
  - `src\repl_cli\cli_bot\cli_actions\cli_action_factory.py`
  - `src\repl_cli\cli_bot\cli_actions\cli_actions.py`
  - `src\repl_cli\cli_bot\cli_actions\render_cli_action.py`
  - `src\repl_cli\cli_bot\cli_actions\strategy_cli_action.py`
  - `src\repl_cli\cli_bot\cli_actions\validate_cli_action.py`
  - `src\repl_cli\cli_bot\cli_behavior.py`
  - `src\repl_cli\cli_bot\cli_behaviors.py`
  - `src\repl_cli\cli_bot\cli_bot.py`
  - `src\repl_cli\cli_command_router.py`
  - `src\repl_cli\cli_context_builder.py`
  - `src\repl_cli\cli_scope.py`
  - `src\repl_cli\command_parser.py`
  - `src\repl_cli\description_extractor.py`
  - `src\repl_cli\formatter.py`
  - `src\repl_cli\formatters\formatter_factory.py`
  - `src\repl_cli\formatters\json_formatter.py`
  - `src\repl_cli\formatters\markdown_formatter.py`
  - `src\repl_cli\formatters\output_formatter.py`
  - `src\repl_cli\formatters\terminal_formatter.py`
  - `src\repl_cli\generators\generate_repl_commands.py`
  - `src\repl_cli\generators\repl_cursor_command_generator.py`
  - `src\repl_cli\generators\repl_cursor_command_visitor.py`
  - `src\repl_cli\headless\context_injector.py`
  - `src\repl_cli\headless\cursor_api.py`
  - `src\repl_cli\headless\error_recovery.py`
  - `src\repl_cli\headless\execution_context.py`
  - `src\repl_cli\headless\execution_result.py`
  - `src\repl_cli\headless\headless_config.py`
  - `src\repl_cli\headless\headless_session.py`
  - `src\repl_cli\headless\non_recoverable_error.py`
  - `src\repl_cli\headless\recoverable_error.py`
  - `src\repl_cli\headless\session_log.py`
  - `src\repl_cli\headless\supervised_session.py`
  - `src\repl_cli\headless\task_supervisor.py`
  - `src\repl_cli\message_parser.py`
  - `src\repl_cli\repl_help.py`
  - `src\repl_cli\repl_main.py`
  - `src\repl_cli\repl_results.py`
  - `src\repl_cli\repl_session.py`
  - `src\repl_cli\repl_status.py`
  - `src\repl_cli\status_display.py`
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
  - `src\scanners\simplify_control_flow_scanner.py`
  - `src\scanners\single_responsibility_scanner.py`
  - `src\scanners\specification_match_scanner.py`
  - `src\scanners\specificity_scanner.py`
  - `src\scanners\spine_optional_scanner.py`
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
  - `src\story_graph\domain.py`
  - `src\story_graph\nodes.py`
  - `src\utils.py`
  - **Total:** 262 src file(s)

## Scanner Execution Status

### 🟩 Overall Status: ALL CLEAN

| Status | Count | Description |
|--------|-------|-------------|
| [i] No Scanner | 8 | Rule has no scanner configured |

**Total Rules:** 8
- **Rules with Scanners:** 0
  - 🟩 **Executed Successfully:** 0
- [i] **Rules without Scanners:** 8

### <span style="color: gray;">[i] Rules Without Scanners</span>

- <span style="color: gray;">[i]</span> **[Integrate And Organize Concepts](#integrate-and-organize-concepts)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Use Module For Folder Structure](#use-module-for-folder-structure)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Use Domain Language](#use-domain-language)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Favor Code Representation](#favor-code-representation)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Scope Concepts Correctly](#scope-concepts-correctly)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Use Natural English](#use-natural-english)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Use Resource Oriented Design](#use-resource-oriented-design)** - No scanner configured
- <span style="color: gray;">[i]</span> **[Shape Relationships From Story Map](#shape-relationships-from-story-map)** - No scanner configured

## Validation Rules Checked

### [i] Rule: <span id="favor-code-representation">Favor Code Representation</span> - NO SCANNER
**Description:** Keep domain model tightly aligned to code it represents, use actual class names and method signatures, not prose descriptions. Show collaborators as types, not descriptions. Avoid over conceptualization.
**Scanner:** Not configured

### [i] Rule: <span id="integrate-and-organize-concepts">Integrate And Organize Concepts</span> - NO SCANNER
**Description:** Integrate related capabilities under parent concepts and organize by business domain. Avoid noun redundancy by nesting related capabilities together, group by business capabilities not technical layers.
**Scanner:** Not configured

### [i] Rule: <span id="scope-concepts-correctly">Scope Concepts Correctly</span> - NO SCANNER
**Description:** Scope domain concepts correctly - place at the most specific level where relevant and ensure they represent complete functional capabilities. Use 'local' scope for single sub-epic concepts, 'global' for shared concepts. Concepts should be complete functional units, not fragments.
**Scanner:** Not configured

### [i] Rule: <span id="shape-relationships-from-story-map">Shape Relationships From Story Map</span> - NO SCANNER
**Description:** Shape domain concept relationships from the story map. Collaborators should come from stories showing how concepts work together to accomplish user goals.
**Scanner:** Not configured

### [i] Rule: <span id="use-domain-language">Use Domain Language</span> - NO SCANNER
**Description:** Use domain-specific language rooted in core business concepts. Avoid generic terms, technical patterns (Manager, Service, Handler, Factory), and capability verbs (Exposes, Provides, Contains). Name concepts and responsibilities using the ubiquitous language of the business domain.
**Scanner:** Not configured

### [i] Rule: <span id="use-module-for-folder-structure">Use Module For Folder Structure</span> - NO SCANNER
**Description:** Use module field to map domain concepts to source code folder structure. Module names MUST exactly match folder paths where they exist using dot notation for nesting.
**Scanner:** Not configured

### [i] Rule: <span id="use-natural-english">Use Natural English</span> - NO SCANNER
**Description:** Use natural English for responsibility names. Responsibilities should read like natural language method calls, using proper grammar and clear intent.
**Scanner:** Not configured

### [i] Rule: <span id="use-resource-oriented-design">Use Resource Oriented Design</span> - NO SCANNER
**Description:** Use resource-oriented design where concepts represent resources with properties and behaviors. Focus on what the resource IS and HAS, not implementation operations.
**Scanner:** Not configured

## Violations Found

🟩 **No violations found.** All rules passed validation.

## Validation Instructions

The following validation steps were performed:

1. ## Step 1: Scanner Violation Review
2. 
3. {{scanner_output}}
4. 
5. Carefully review all scanner-reported violations as follows:
6. 1. For each violation message, locate the corresponding element in the knowledge graph.
7. 2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
8. 3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
9. 4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
10. 5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
*... and 49 more instructions*

## Report Location

This report was automatically generated and saved to:
`c:\dev\augmented-teams\agile_bot\bots\base_bot\docs\stories\reports\domain-validation-report-2026-01-05_22-51-32.md`

