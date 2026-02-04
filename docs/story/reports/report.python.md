Validation Report - Code
Generated: 2026-01-28 00:17:39 Project: agile_bots Behavior: code Action: validate

Summary
Validated story map and domain model and 378 code file(s) against 32 validation rules.

Content Validated
Clarification: clarification.json
Rendered Outputs:
story-graph.json
Code Files Scanned:
src\actions\action.py
src\actions\action_context.py
src\actions\action_factory.py
src\actions\action_state_manager.py
src\actions\actions.py
src\actions\activity_tracker.py
src\actions\behavior_action_status_builder.py
src\actions\build\build_action.py
src\actions\build\json_build_action.py
src\actions\build\markdown_build_action.py
src\actions\build\story_graph_data.py
src\actions\build\story_graph_spec.py
src\actions\build\story_graph_template.py
src\actions\build\tty_build_action.py
src\actions\clarify\clarify_action.py
src\actions\clarify\evidence.py
src\actions\clarify\json_clarify_action.py
src\actions\clarify\key_questions.py
src\actions\clarify\markdown_clarify_action.py
src\actions\clarify\required_context.py
src\actions\clarify\requirements_clarifications.py
src\actions\clarify\tty_clarify_action.py
src\actions\content.py
src\actions\guardrails\guardrails.py
src\actions\guardrails\tty_guardrails.py
src\actions\guardrails\tty_required_context.py
src\actions\guardrails\tty_strategy.py
src\actions\json_actions.py
src\actions\markdown_action.py
src\actions\markdown_actions.py
src\actions\render\evidence.py
src\actions\render\json_render_action.py
src\actions\render\markdown_render_action.py
src\actions\render\render_action.py
src\actions\render\render_config_loader.py
src\actions\render\render_instruction_builder.py
src\actions\render\render_spec.py
src\actions\render\synchronizer.py
src\actions\render\template.py
src\actions\render\tty_render_action.py
src\actions\strategy\assumptions.py
src\actions\strategy\json_persistent.py
src\actions\strategy\json_strategy_action.py
src\actions\strategy\markdown_strategy_action.py
src\actions\strategy\strategy.py
src\actions\strategy\strategy_action.py
src\actions\strategy\strategy_criteria.py
src\actions\strategy\strategy_criterias.py
src\actions\strategy\strategy_decision.py
src\actions\strategy\tty_strategy_action.py
src\actions\tty_action.py
src\actions\tty_actions.py
src\actions\validate\background_validation_handler.py
src\actions\validate\file_discovery.py
src\actions\validate\file_link_builder.py
src\actions\validate\json_validate_action.py
src\actions\validate\markdown_validate_action.py
src\actions\validate\story_graph.py
src\actions\validate\tty_validate_action.py
src\actions\validate\validate_action.py
src\actions\validate\validation_executor.py
src\actions\validate\validation_report_builder.py
src\actions\validate\validation_report_formatter.py
src\actions\validate\validation_report_writer.py
src\actions\validate\validation_scope.py
src\actions\validate\validation_stats.py
src\actions\validate\validation_type.py
src\actions\validate\validation_violations_builder.py
src\actions\validate\violation_formatter.py
src\actions\workflow_status_builder.py
src\behaviors\behavior.py
src\behaviors\behaviors.py
src\behaviors\json_behavior.py
src\behaviors\markdown_behavior.py
src\behaviors\tty_behavior.py
src\bot\behavior.py
src\bot\behaviors.py
src\bot\bot.py
src\bot\json_bot.py
src\bot\markdown_bot.py
src\bot\tty_bot.py
src\bot\workspace.py
src\bot_path\bot_path.py
src\bot_path\json_bot_path.py
src\bot_path\markdown_bot_path.py
src\bot_path\path_resolver.py
src\bot_path\tty_bot_path.py
src\cli\action_data_collector.py
src\cli\adapter_factory.py
src\cli\adapters.py
src\cli\base_hierarchical_adapter.py
src\cli\cli_generator.py
src\cli\cli_main.py
src\cli\cli_results.py
src\cli\cli_session.py
src\cli\cursor\cursor_command_visitor.py
src\cli\description_extractor.py
src\cli\formatter.py
src\cli\help_context.py
src\cli\orchestrator.py
src\cli\visitor.py
src\exit_result\exit_result.py
src\exit_result\json_exit_result.py
src\exit_result\markdown_exit_result.py
src\exit_result\tty_exit_result.py
src\ext\behavior_matcher.py
src\ext\bot_matcher.py
src\ext\trigger_domain.py
src\ext\trigger_router.py
src\ext\trigger_router_entry.py
src\ext\trigger_words.py
src\help\help.py
src\help\help_action.py
src\help\json_help.py
src\help\markdown_help.py
src\help\tty_help.py
src\instructions\context_data_injector.py
src\instructions\instructions.py
src\instructions\json_instructions.py
src\instructions\markdown_instructions.py
src\instructions\reminders.py
src\instructions\tty_instructions.py
src\navigation\domain_navigator.py
src\navigation\json_navigation.py
src\navigation\markdown_navigation.py
src\navigation\navigation.py
src\navigation\tty_navigation.py
src\rules\rule.py
src\rules\rule_filter.py
src\rules\rule_loader.py
src\rules\rules.py
src\rules\rules_action.py
src\rules\rules_digest_guidance.py
src\rules\scan_config.py
src\scanners\ac_consolidation_scanner.py
src\scanners\active_language_scanner.py
src\scanners\actor_alternation_scanner.py
src\scanners\background_common_setup_scanner.py
src\scanners\behavioral_ac_scanner.py
src\scanners\code\javascript\abstraction_levels_scanner.py
src\scanners\code\javascript\arrange_act_assert_scanner.py
src\scanners\code\javascript\ascii_only_scanner.py
src\scanners\code\javascript\bad_comments_scanner.py
src\scanners\code\javascript\business_readable_test_names_scanner.py
src\scanners\code\javascript\calculation_timing_code_scanner.py
src\scanners\code\javascript\class_based_organization_scanner.py
src\scanners\code\javascript\class_size_scanner.py
src\scanners\code\javascript\clear_parameters_scanner.py
src\scanners\code\javascript\complete_refactoring_scanner.py
src\scanners\code\javascript\consistent_indentation_scanner.py
src\scanners\code\javascript\consistent_naming_scanner.py
src\scanners\code\javascript\consistent_vocabulary_scanner.py
src\scanners\code\javascript\cover_all_paths_scanner.py
src\scanners\code\javascript\dead_code_scanner.py
src\scanners\code\javascript\descriptive_function_names_scanner.py
src\scanners\code\javascript\domain_grouping_code_scanner.py
src\scanners\code\javascript\domain_language_code_scanner.py
src\scanners\code\javascript\duplication_scanner.py
src\scanners\code\javascript\error_handling_isolation_scanner.py
src\scanners\code\javascript\exact_variable_names_scanner.py
src\scanners\code\javascript\exception_handling_scanner.py
src\scanners\code\javascript\excessive_guards_scanner.py
src\scanners\code\javascript\explicit_dependencies_scanner.py
src\scanners\code\javascript\fixture_placement_scanner.py
src\scanners\code\javascript\full_result_assertions_scanner.py
src\scanners\code\javascript\function_size_scanner.py
src\scanners\code\javascript\given_when_then_helpers_scanner.py
src\scanners\code\javascript\import_placement_scanner.py
src\scanners\code\javascript\intention_revealing_names_scanner.py
src\scanners\code\javascript\js_code_scanner.py
src\scanners\code\javascript\js_regex_analyzer.py
src\scanners\code\javascript\js_test_scanner.py
src\scanners\code\javascript\meaningful_context_scanner.py
src\scanners\code\javascript\minimize_mutable_state_scanner.py
src\scanners\code\javascript\mock_boundaries_scanner.py
src\scanners\code\javascript\natural_english_code_scanner.py
src\scanners\code\javascript\no_fallbacks_scanner.py
src\scanners\code\javascript\no_guard_clauses_scanner.py
src\scanners\code\javascript\object_oriented_helpers_scanner.py
src\scanners\code\javascript\observable_behavior_scanner.py
src\scanners\code\javascript\one_concept_per_test_scanner.py
src\scanners\code\javascript\open_closed_principle_scanner.py
src\scanners\code\javascript\prefer_object_model_over_config_scanner.py
src\scanners\code\javascript\primitive_vs_object_scanner.py
src\scanners\code\javascript\property_encapsulation_code_scanner.py
src\scanners\code\javascript\real_implementations_scanner.py
src\scanners\code\javascript\resource_oriented_code_scanner.py
src\scanners\code\javascript\separate_concerns_scanner.py
src\scanners\code\javascript\setup_similarity_scanner.py
src\scanners\code\javascript\simplify_control_flow_scanner.py
src\scanners\code\javascript\single_responsibility_scanner.py
src\scanners\code\javascript\specification_match_scanner.py
src\scanners\code\javascript\standard_data_reuse_scanner.py
src\scanners\code\javascript\story_graph_match_scanner.py
src\scanners\code\javascript\swallowed_exceptions_scanner.py
src\scanners\code\javascript\technical_abstraction_code_scanner.py
src\scanners\code\javascript\test_boundary_behavior_scanner.py
src\scanners\code\javascript\test_file_naming_scanner.py
src\scanners\code\javascript\test_quality_scanner.py
src\scanners\code\javascript\third_party_isolation_scanner.py
src\scanners\code\javascript\type_safety_scanner.py
src\scanners\code\javascript\ubiquitous_language_scanner.py
src\scanners\code\javascript\unnecessary_parameter_passing_scanner.py
src\scanners\code\javascript\useless_comments_scanner.py
src\scanners\code\javascript\vertical_density_scanner.py
src\scanners\code\python\abstraction_levels_scanner.py
src\scanners\code\python\arrange_act_assert_scanner.py
src\scanners\code\python\ascii_only_scanner.py
src\scanners\code\python\bad_comments_scanner.py
src\scanners\code\python\business_readable_test_names_scanner.py
src\scanners\code\python\calculation_timing_code_scanner.py
src\scanners\code\python\class_based_organization_scanner.py
src\scanners\code\python\class_size_scanner.py
src\scanners\code\python\clear_parameters_scanner.py
src\scanners\code\python\code_scanner.py
src\scanners\code\python\complete_refactoring_scanner.py
src\scanners\code\python\consistent_indentation_scanner.py
src\scanners\code\python\consistent_naming_scanner.py
src\scanners\code\python\consistent_vocabulary_scanner.py
src\scanners\code\python\cover_all_paths_scanner.py
src\scanners\code\python\dead_code_scanner.py
src\scanners\code\python\descriptive_function_names_scanner.py
src\scanners\code\python\domain_grouping_code_scanner.py
src\scanners\code\python\domain_language_code_scanner.py
src\scanners\code\python\duplication_scanner.py
src\scanners\code\python\error_handling_isolation_scanner.py
src\scanners\code\python\exact_variable_names_scanner.py
src\scanners\code\python\exception_handling_scanner.py
src\scanners\code\python\excessive_guards_scanner.py
src\scanners\code\python\explicit_dependencies_scanner.py
src\scanners\code\python\fixture_placement_scanner.py
src\scanners\code\python\full_result_assertions_scanner.py
src\scanners\code\python\function_size_scanner.py
src\scanners\code\python\given_when_then_helpers_scanner.py
src\scanners\code\python\import_placement_scanner.py
src\scanners\code\python\intention_revealing_names_scanner.py
src\scanners\code\python\meaningful_context_scanner.py
src\scanners\code\python\minimize_mutable_state_scanner.py
src\scanners\code\python\mock_boundaries_scanner.py
src\scanners\code\python\natural_english_code_scanner.py
src\scanners\code\python\no_fallbacks_scanner.py
src\scanners\code\python\no_guard_clauses_scanner.py
src\scanners\code\python\object_oriented_helpers_scanner.py
src\scanners\code\python\observable_behavior_scanner.py
src\scanners\code\python\one_concept_per_test_scanner.py
src\scanners\code\python\open_closed_principle_scanner.py
src\scanners\code\python\prefer_object_model_over_config_scanner.py
src\scanners\code\python\primitive_vs_object_scanner.py
src\scanners\code\python\property_encapsulation_code_scanner.py
src\scanners\code\python\real_implementations_scanner.py
src\scanners\code\python\resource_oriented_code_scanner.py
src\scanners\code\python\separate_concerns_scanner.py
src\scanners\code\python\setup_similarity_scanner.py
src\scanners\code\python\simplify_control_flow_scanner.py
src\scanners\code\python\single_responsibility_scanner.py
src\scanners\code\python\specification_match_scanner.py
src\scanners\code\python\standard_data_reuse_scanner.py
src\scanners\code\python\story_graph_match_scanner.py
src\scanners\code\python\swallowed_exceptions_scanner.py
src\scanners\code\python\technical_abstraction_code_scanner.py
src\scanners\code\python\test_boundary_behavior_scanner.py
src\scanners\code\python\test_file_naming_scanner.py
src\scanners\code\python\test_quality_scanner.py
src\scanners\code\python\test_scanner.py
src\scanners\code\python\third_party_isolation_scanner.py
src\scanners\code\python\type_safety_scanner.py
src\scanners\code\python\ubiquitous_language_scanner.py
src\scanners\code\python\unnecessary_parameter_passing_scanner.py
src\scanners\code\python\useless_comments_scanner.py
src\scanners\code\python\vertical_density_scanner.py
src\scanners\code_representation_scanner.py
src\scanners\communication_verb_scanner.py
src\scanners\complexity_metrics.py
src\scanners\crc_delegation_scanner.py
src\scanners\delegation_scanner.py
src\scanners\dependency_chaining_scanner.py
src\scanners\domain_concept_node.py
src\scanners\domain_grouping_scanner.py
src\scanners\domain_language_scanner.py
src\scanners\domain_scanner.py
src\scanners\enumerate_ac_permutations_scanner.py
src\scanners\enumerate_stories_scanner.py
src\scanners\exhaustive_decomposition_scanner.py
src\scanners\generic_capability_scanner.py
src\scanners\given_precondition_scanner.py
src\scanners\given_state_not_actions_scanner.py
src\scanners\implementation_details_scanner.py
src\scanners\increment_folder_structure_scanner.py
src\scanners\invest_principles_scanner.py
src\scanners\natural_english_scanner.py
src\scanners\noun_redundancy_scanner.py
src\scanners\parameterized_tests_scanner.py
src\scanners\plain_english_scenarios_scanner.py
src\scanners\present_ac_consolidation_scanner.py
src\scanners\property_encapsulation_scanner.py
src\scanners\reaction_chaining_scanner.py
src\scanners\resource_oriented_design_scanner.py
src\scanners\resources\ast_elements.py
src\scanners\resources\block.py
src\scanners\resources\block_extractor.py
src\scanners\resources\file.py
src\scanners\resources\line.py
src\scanners\resources\scan.py
src\scanners\resources\scan_context.py
src\scanners\resources\scope.py
src\scanners\resources\violation.py
src\scanners\scanner.py
src\scanners\scanner_execution_error.py
src\scanners\scanner_loader.py
src\scanners\scanner_orchestrator.py
src\scanners\scanner_registry.py
src\scanners\scanner_status_formatter.py
src\scanners\scenario_outline_scanner.py
src\scanners\scenario_specific_given_scanner.py
src\scanners\scenarios_cover_all_cases_scanner.py
src\scanners\scenarios_on_story_docs_scanner.py
src\scanners\specificity_scanner.py
src\scanners\spine_optional_scanner.py
src\scanners\story_enumeration_scanner.py
src\scanners\story_filename_scanner.py
src\scanners\story_map.py
src\scanners\story_scanner.py
src\scanners\story_sizing_scanner.py
src\scanners\technical_abstraction_scanner.py
src\scanners\technical_language_scanner.py
src\scanners\validation_scanner_status_builder.py
src\scanners\verb_noun_scanner.py
src\scanners\vertical_slice_scanner.py
src\scanners\violation.py
src\scanners\vocabulary_helper.py
src\scope\action_scope.py
src\scope\json_scope.py
src\scope\json_scope_command_result.py
src\scope\markdown_scope.py
src\scope\markdown_scope_command_result.py
src\scope\scope.py
src\scope\scope_action_context.py
src\scope\scope_command_result.py
src\scope\scope_matcher.py
src\scope\scoping_parameter.py
src\scope\tty_scope.py
src\scope\tty_scope_command_result.py
src\story_graph\domain.py
src\story_graph\json_story_graph.py
src\story_graph\markdown_story_graph.py
src\story_graph\nodes.py
src\story_graph\story_graph.py
src\story_graph\test_class_mover.py
src\story_graph\tty_story_graph.py
src\synchronizers\domain_model\domain_model_synchronizer.py
src\synchronizers\story_io\examples\add_gm_user.py
src\synchronizers\story_io\examples\add_user_example.py
src\synchronizers\story_io\examples\example_load_and_render.py
src\synchronizers\story_io\examples\load_and_render_example.py
src\synchronizers\story_io\examples\render_example.py
src\synchronizers\story_io\extract_layout.py
src\synchronizers\story_io\render_story_graph.py
src\synchronizers\story_io\story_io_cli.py
src\synchronizers\story_io\story_io_component.py
src\synchronizers\story_io\story_io_diagram.py
src\synchronizers\story_io\story_io_epic.py
src\synchronizers\story_io\story_io_feature.py
src\synchronizers\story_io\story_io_increment.py
src\synchronizers\story_io\story_io_mcp_server.py
src\synchronizers\story_io\story_io_position.py
src\synchronizers\story_io\story_io_renderer.py
src\synchronizers\story_io\story_io_story.py
src\synchronizers\story_io\story_io_synchronizer.py
src\synchronizers\story_io\story_io_user.py
src\synchronizers\story_io\story_map_drawio_synchronizer.py
src\synchronizers\story_io\test_increment_full_cycle.py
src\synchronizers\story_io\test_increment_priority.py
src\synchronizers\story_scenarios\story_scenarios_synchronizer.py
src\synchronizers\story_tests\create_tree_view.py
src\synchronizers\story_tests\extract_scenario_steps_from_tests.py
src\synchronizers\story_tests\extract_scenarios_from_tests.py
src\synchronizers\story_tests\story_tests_synchronizer.py
src\utils.py
Total: 378 src file(s)
Scanner Execution Status
🟥 Overall Status: CRITICAL ISSUES
Status	Count	Description
🟩 Executed Successfully	16	Scanners ran without errors
🟩 Clean Rules	9	No violations found
🟨 Rules with Warnings	4	Found 49 warning violation(s)
🟥 Rules with Errors	3	Found 809 error violation(s)
🟥 Load Failed	15	Scanner could not be loaded
[i] No Scanner	1	Rule has no scanner configured
Total Rules: 32

Rules with Scanners: 31
🟩 Executed Successfully: 16
🟥 Load Failed: 15
[i] Rules without Scanners: 1
🟩 Successfully Executed Scanners
🟥 Stop Writing Useless Comments - 741 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.useless_comments_scanner.UselessCommentsScanner
🟥 Eliminate Duplication - 54 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.duplication_scanner.DuplicationScanner
🟨 Refactor Completely Not Partially - 36 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.complete_refactoring_scanner.CompleteRefactoringScanner
🟥 Place Imports At Top - 14 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.import_placement_scanner.ImportPlacementScanner
🟨 Provide Meaningful Context - 11 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.meaningful_context_scanner.MeaningfulContextScanner
🟨 Avoid Unnecessary Parameter Passing - 1 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.unnecessary_parameter_passing_scanner.UnnecessaryParameterPassingScanner
🟨 Use Explicit Dependencies - 1 violation(s) (EXECUTION_SUCCESS) - View Details
Scanner: scanners.code.python.explicit_dependencies_scanner.ExplicitDependenciesScanner
🟩 Detect Legacy Unused Code - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.dead_code_scanner.DeadCodeScanner
🟩 Group By Domain - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.domain_grouping_code_scanner.DomainGroupingCodeScanner
🟩 Hide Business Logic Behind Properties - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.calculation_timing_code_scanner.CalculationTimingCodeScanner
🟩 Hide Calculation Timing - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.calculation_timing_code_scanner.CalculationTimingCodeScanner
🟩 Keep Functions Single Responsibility - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.single_responsibility_scanner.SingleResponsibilityScanner
🟩 Keep Functions Small Focused - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.function_size_scanner.FunctionSizeScanner
🟩 Maintain Vertical Density - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.vertical_density_scanner.VerticalDensityScanner
🟩 Prefer Object Model Over Config - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.prefer_object_model_over_config_scanner.PreferObjectModelOverConfigScanner
🟩 Use Consistent Indentation - 0 violations (EXECUTION_SUCCESS)
Scanner: scanners.code.python.consistent_indentation_scanner.ConsistentIndentationScanner
🟥 Scanner Load Failures
🟥 Avoid Excessive Guards - LOAD FAILED
Scanner Path: scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner
Error: Scanner not found at scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner
🟥 Chain Dependencies Properly - LOAD FAILED
Scanner Path: scanners.dependency_chaining_scanner.DependencyChainingScanner
Error: Scanner class not found in any language: scanners.dependency_chaining_scanner.DependencyChainingScanner
🟥 Classify Exceptions By Caller Needs - LOAD FAILED
Scanner Path: scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner
Error: Scanner not found at scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner
🟥 Delegate To Lowest Level - LOAD FAILED
Scanner Path: scanners.delegation_scanner.DelegationScanner
Error: Scanner class not found in any language: scanners.delegation_scanner.DelegationScanner
🟥 Enforce Encapsulation - LOAD FAILED
Scanner Path: scanners.property_encapsulation_scanner.PropertyEncapsulationScanner
Error: Scanner class not found in any language: scanners.property_encapsulation_scanner.PropertyEncapsulationScanner
🟥 Favor Code Representation - LOAD FAILED
Scanner Path: scanners.code_representation_scanner.CodeRepresentationScanner
Error: Scanner class not found in any language: scanners.code_representation_scanner.CodeRepresentationScanner
🟥 Keep Classes Small With Single Responsibility - LOAD FAILED
Scanner Path: scanners.code.python.class_size_scanner.ClassSizeScanner
Error: Scanner not found at scanners.code.python.class_size_scanner.ClassSizeScanner
🟥 Never Swallow Exceptions - LOAD FAILED
Scanner Path: scanners.code.python.swallowed_exceptions_scanner.SwallowedExceptionsScanner
Error: Scanner not found at scanners.code.python.swallowed_exceptions_scanner.SwallowedExceptionsScanner
🟥 Simplify Control Flow - LOAD FAILED
Scanner Path: scanners.code.python.simplify_control_flow_scanner.SimplifyControlFlowScanner
Error: Scanner not found at scanners.code.python.simplify_control_flow_scanner.SimplifyControlFlowScanner
🟥 Use Clear Function Parameters - LOAD FAILED
Scanner Path: scanners.code.python.clear_parameters_scanner.ClearParametersScanner
Error: Scanner not found at scanners.code.python.clear_parameters_scanner.ClearParametersScanner
🟥 Use Consistent Naming - LOAD FAILED
Scanner Path: scanners.code.python.consistent_naming_scanner.ConsistentNamingScanner
Error: Scanner not found at scanners.code.python.consistent_naming_scanner.ConsistentNamingScanner
🟥 Use Domain Language - LOAD FAILED
Scanner Path: scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner
Error: Scanner not found at scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner
🟥 Use Exceptions Properly - LOAD FAILED
Scanner Path: scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner
Error: Scanner not found at scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner
🟥 Use Natural English - LOAD FAILED
Scanner Path: scanners.code.python.natural_english_code_scanner.NaturalEnglishCodeScanner
Error: Scanner not found at scanners.code.python.natural_english_code_scanner.NaturalEnglishCodeScanner
🟥 Use Resource Oriented Design - LOAD FAILED
Scanner Path: scanners.code.python.resource_oriented_code_scanner.ResourceOrientedCodeScanner
Error: Scanner not found at scanners.code.python.resource_oriented_code_scanner.ResourceOrientedCodeScanner
[i] Rules Without Scanners
[i] Refactor Tests With Production Code - No scanner configured
Validation Rules Checked
🟥 Rule: Avoid Excessive Guards - FAILED
Description: Excessive guard clauses add to cyclomatic complexity and make code harder to read. Centralize error handling in one place rather than scattering defensive checks throughout the code. Let code fail fast with clear errors rather than silently handling missing components. Scanner: scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner Error: Scanner not found at scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner

🟥 Rule: Chain Dependencies Properly - FAILED
Description: CRITICAL: Code must chain dependencies properly with constructor injection. Map dependencies in a chain: highest-level object → collaborator → sub-collaborator. Inject collaborators at construction time so methods can use them without passing them as parameters. Access sub-collaborators through their owning objects. Scanner: scanners.dependency_chaining_scanner.DependencyChainingScanner Error: Scanner class not found in any language: scanners.dependency_chaining_scanner.DependencyChainingScanner

🟥 Rule: Classify Exceptions By Caller Needs - FAILED
Description: Design exceptions based on how callers will handle them. Create exception types based on caller's needs, use special case objects for predictable failures, and wrap third-party exceptions at boundaries. Scanner: scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner Error: Scanner not found at scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner

🟥 Rule: Delegate To Lowest Level - FAILED
Description: CRITICAL: Code must delegate responsibilities to the lowest-level object that can handle them. If a collection class can do something, delegate to it rather than implementing it in the parent. Scanner: scanners.delegation_scanner.DelegationScanner Error: Scanner class not found in any language: scanners.delegation_scanner.DelegationScanner

🟥 Rule: Enforce Encapsulation - FAILED
Description: CRITICAL: Hide implementation details and expose minimal interface. Make fields private by default, expose behavior not data. NEVER pass raw dicts/lists that expose internal structure - use typed objects that encapsulate the data. Follow Law of Demeter (principle of least knowledge). Scanner: scanners.property_encapsulation_scanner.PropertyEncapsulationScanner Error: Scanner class not found in any language: scanners.property_encapsulation_scanner.PropertyEncapsulationScanner

🟥 Rule: Favor Code Representation - FAILED
Description: CRITICAL: Code should represent domain concepts directly. Domain models should match code. If code doesn't match domain concepts, refactor the code rather than creating abstract domain models. Scanner: scanners.code_representation_scanner.CodeRepresentationScanner Error: Scanner class not found in any language: scanners.code_representation_scanner.CodeRepresentationScanner

🟥 Rule: Keep Classes Small With Single Responsibility - FAILED
Description: CRITICAL: Classes should be small (under 200-300 lines) with a single responsibility. Keep classes cohesive (methods/data interdependent), eliminate dead code, and favor many small focused classes over few large ones. Scanner: scanners.code.python.class_size_scanner.ClassSizeScanner Error: Scanner not found at scanners.code.python.class_size_scanner.ClassSizeScanner

🟥 Rule: Never Swallow Exceptions - FAILED
Description: CRITICAL: Never swallow exceptions silently. Empty catch blocks hide failures and make debugging impossible. Always log, handle, or rethrow exceptions with context. Scanner: scanners.code.python.swallowed_exceptions_scanner.SwallowedExceptionsScanner Error: Scanner not found at scanners.code.python.swallowed_exceptions_scanner.SwallowedExceptionsScanner

🟥 Rule: Simplify Control Flow - FAILED
Description: Keep nesting minimal and control flow straightforward. Use guard clauses to reduce nesting and extract nested blocks into separate functions. Scanner: scanners.code.python.simplify_control_flow_scanner.SimplifyControlFlowScanner Error: Scanner not found at scanners.code.python.simplify_control_flow_scanner.SimplifyControlFlowScanner

🟥 Rule: Use Clear Function Parameters - FAILED
Description: CRITICAL: Function signatures must be simple and intention-revealing. Prefer 0-2 parameters. NEVER pass Dict[str, Any] or List[str] for complex data - create typed objects instead. Examples: parameters dict → ParametersObject, files dict → FilesCollection, exclude list → ExcludePatterns. Scanner: scanners.code.python.clear_parameters_scanner.ClearParametersScanner Error: Scanner not found at scanners.code.python.clear_parameters_scanner.ClearParametersScanner

🟥 Rule: Use Consistent Naming - FAILED
Description: Use one word per concept across the entire codebase. Pick consistent terms (get/fetch/retrieve → choose one) and follow domain language for business concepts. Scanner: scanners.code.python.consistent_naming_scanner.ConsistentNamingScanner Error: Scanner not found at scanners.code.python.consistent_naming_scanner.ConsistentNamingScanner

🟥 Rule: Use Domain Language - FAILED
Description: CRITICAL: Code must use domain-specific language, not generic terms. NEVER use Dict[str, Any], List[str], or generic 'data'/'config'/'parameters' - use typed domain objects. Objects should expose properties representing what they contain (e.g., recommended_trades), not methods that 'generate' or 'calculate' things. Scanner: scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner Error: Scanner not found at scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner

🟥 Rule: Use Exceptions Properly - FAILED
Description: Prefer exceptions over error codes for exceptional conditions. Use exceptions for truly exceptional situations, provide informative error messages, and create domain-specific exception types. Scanner: scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner Error: Scanner not found at scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner

🟥 Rule: Use Natural English - FAILED
Description: CRITICAL: Code must use natural English for method names, variable names, and relationships. Use 'many' for collections, 'may' for optional, 'will' for required. Don't use technical notation or abbreviations. Scanner: scanners.code.python.natural_english_code_scanner.NaturalEnglishCodeScanner Error: Scanner not found at scanners.code.python.natural_english_code_scanner.NaturalEnglishCodeScanner

🟥 Rule: Use Resource Oriented Design - FAILED
Description: CRITICAL: Code must use resource-oriented, object-oriented design. Use object-oriented classes (singular or collection) with responsibilities that encapsulate logic over manager/doer/loader patterns. Maximize encapsulation through collaborator relationships. Scanner: scanners.code.python.resource_oriented_code_scanner.ResourceOrientedCodeScanner Error: Scanner not found at scanners.code.python.resource_oriented_code_scanner.ResourceOrientedCodeScanner

🟥 Rule: Stop Writing Useless Comments - 741 ERROR(S) - View Details
Description: CRITICAL: DO NOT WRITE COMMENTS. Delete all comments written by the AI chat. Code must be self-explanatory through clear naming and structure. ONLY exception: legal/license requirements. If you think a comment is needed, the code is wrong - fix the code instead. Scanner: scanners.code.python.useless_comments_scanner.UselessCommentsScanner Execution Status: EXECUTION_SUCCESS

🟥 Rule: Eliminate Duplication - 54 ERROR(S) - View Details
Description: CRITICAL: Every piece of knowledge should have a single, authoritative representation (DRY principle). Extract repeated logic into reusable functions and use abstraction to capture common patterns. Scanner: scanners.code.python.duplication_scanner.DuplicationScanner Execution Status: EXECUTION_SUCCESS

🟥 Rule: Place Imports At Top - 14 ERROR(S) - View Details
Description: Place all import statements at the top of the file, after module docstrings and comments, but before any executable code. This improves readability and makes dependencies clear. Scanner: scanners.code.python.import_placement_scanner.ImportPlacementScanner Execution Status: EXECUTION_SUCCESS

🟨 Rule: Refactor Completely Not Partially - 36 WARNING(S) - View Details
Description: CRITICAL: When refactoring, replace old code completely - don't try to support both legacy and new patterns. Write new code, delete old code, fix tests. Clean breaks are better than compatibility bridges that create technical debt. Scanner: scanners.code.python.complete_refactoring_scanner.CompleteRefactoringScanner Execution Status: EXECUTION_SUCCESS

🟨 Rule: Provide Meaningful Context - 11 WARNING(S) - View Details
Description: Names should provide appropriate context without redundancy. Use longer names for longer scopes and replace magic numbers with named constants. Scanner: scanners.code.python.meaningful_context_scanner.MeaningfulContextScanner Execution Status: EXECUTION_SUCCESS

... and 12 more rules

Violations Found
Total Violations: 858

File-by-File Violations: 858
Cross-File Violations: 0
File-by-File Violations (Pass 1)
These violations were detected by scanning each file individually.

Avoid Unnecessary Parameter Passing: 1 violation(s)
[!] WARNING - src\story_graph\nodes.py: Method "_set_bot_on_all_nodes" in Test class StoryMap receives parameter "bot" that matches instance variable "self._bot". Access self._bot directly instead of passing as parameter.
            self._bot._story_graph = None

    def _set_bot_on_all_nodes(self, bot: Any) -> None:
        for epic in self._epics_list:
            epic._bot = bot
            for node in self.walk(epic):
                node._bot = bot

Eliminate Duplication: 54 violation(s)
[X] ERROR - src\utils.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (find_js_test_class_line:340-349):

content = test_file_path.read_text(encoding='utf-8')
lines = content.split('\n')
pattern = re.compile(f"""test\\s*\\(\\s*['\\"]({re.escape(test_class_name)})['\\"]""")
for i, line in enumerate(lines, ...
Location (find_js_test_method_line:359-368):

content = test_file_path.read_text(encoding='utf-8')
lines = content.split('\n')
pattern = re.compile(f"""(?:await\\s+)?t\\.test\\s*\\(\\s*['\\"]({re.escape(test_method_name)})['\\"]""")
for i, line i...
[X] ERROR - src\utils.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (find_js_file_with_test_class:388-406):

if not py_test_file_path.exists():
    return (None, None)
test_dir = py_test_file_path.parent
js_path = py_test_file_path.with_suffix('.js')
if js_path.exists():
    line_number = find_js_test_class_...
Location (find_js_file_with_test_method:415-433):

if not py_test_file_path.exists():
    return (None, None)
test_dir = py_test_file_path.parent
js_path = py_test_file_path.with_suffix('.js')
if js_path.exists():
    line_number = find_js_test_method...
[X] ERROR - src\cli\adapters.py: Duplicate code detected: functions serialize, parse_command_text, serialize, to_dict, serialize have identical bodies - extract to shared function

[X] ERROR - src\cli\adapters.py: Duplicate code detected: functions parse_command_text, parse_command_text, parse_command_text, parse_command_text have identical bodies - extract to shared function

[X] ERROR - src\cli\cli_session.py: Duplicate code blocks detected (3 locations) - extract to helper function.

Location (_build_response:271-277):

import logging
logger = logging.getLogger(__name__)
logger.warning(f'[CLISession] JSON parse error in bot data, sanitizing: {str(e)}')
bot_data = json.loads(sanitize_json_string(adapter.serialize()))
Location (_build_json_instructions_response:313-319):

import logging
logger = logging.getLogger(__name__)
logger.warning(f'[CLISession] JSON parse error in status, sanitizing: {str(e)}')
status_data = json.loads(sanitize_json_string(status_adapter.serial...
Location (_append_json_navigation_context:355-361):

import logging
logger = logging.getLogger(__name__)
logger.warning(f'[CLISession] JSON parse error in status, sanitizing: {str(e)}')
unified['bot'] = json.loads(sanitize_json_string(status_adapter.ser...
[X] ERROR - src\cli\cli_session.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_build_json_instructions_response:301-307):

import logging
logger = logging.getLogger(__name__)
logger.warning(f'[CLISession] JSON parse error in instructions, sanitizing: {str(e)}')
instructions_data = json.loads(sanitize_json_string(output)) ...
Location (_append_json_navigation_context:338-344):

import logging
logger = logging.getLogger(__name__)
logger.warning(f'[CLISession] JSON parse error in navigation context, sanitizing: {str(e)}')
result_data = json.loads(sanitize_json_string(output)) ...
[X] ERROR - src\story_graph\nodes.py: Duplicate code detected: functions _generate_unique_child_name, _generate_unique_child_name have identical bodies - extract to shared function

[X] ERROR - src\story_graph\nodes.py: Duplicate code detected: functions getitem, getitem have identical bodies - extract to shared function

[X] ERROR - src\story_graph\nodes.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (delete:186-205):

if not hasattr(self, '_parent') or not self._parent:
    raise ValueError('Cannot delete node without parent')
node_type = type(self).__name__
node_name = self.name
parent = self._parent
children_coun...
Location (delete:208-219):

self._children.clear()
parent._children.remove(self)
self._resequence_siblings()
parent.save()
elapsed = time.time() - start_time
print(f"[DELETE TIMING] Deleted {node_type} '{node_name}' in {elapsed:...
[X] ERROR - src\story_graph\nodes.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (move_to:256-263):

actual_parent._children.remove(self)
adjusted_position = min(position, len(actual_parent._children))
actual_parent._children.insert(adjusted_position, self)
actual_parent._resequence_children()
self.s...
Location (move_to:271-278):

self._parent._children.remove(self)
adjusted_position = min(position, len(self._parent.children))
self._parent._children.insert(adjusted_position, self)
self._resequence_siblings()
self.save()
[X] ERROR - src\story_graph\nodes.py: Duplicate code blocks detected (4 locations) - extract to helper function.

Location (_generate_unique_child_name:760-764):

name = f'{child_type}{counter}'
if not any((child.name == name for child in self.children)):
    return name
counter += 1
Location (_generate_unique_child_name:977-981):

name = f'{child_type}{counter}'
if not any((child.name == name for child in story_group.children)):
    return name
counter += 1
Location (_generate_unique_child_name:984-988):

name = f'{child_type}{counter}'
if not any((child.name == name for child in self.children)):
    return name
counter += 1
Location (_generate_unique_child_name:1213-1217):

name = f'{child_type}{counter}'
if not any((child.name == name for child in self.children)):
    return name
counter += 1
[X] ERROR - src\story_graph\nodes.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (all_scenarios_have_tests:1125-1131):

from pathlib import Path
workspace_dir = Path(self._bot.bot_paths.workspace_directory if hasattr(self._bot.bot_paths, 'workspace_directory') else '.')
test_dir = workspace_dir / self._bot.bot_paths.te...
Location (behavior_needed:1325-1334):

if not test_file or not test_class:
    return 'tests'
from pathlib import Path
workspace_dir = Path(self._bot.bot_paths.workspace_directory if hasattr(self._bot.bot_paths, 'workspace_directory') else...
[X] ERROR - src\story_graph\nodes.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (find_node:1528-1534):

if child.name == node_name:
    return child
if hasattr(child, 'children'):
    result = self._find_in_children(child, node_name)
    if result:
        return result
Location (_find_in_children:1538-1544):

if child.name == name:
    return child
if hasattr(child, 'children'):
    result = self._find_in_children(child, name)
    if result:
        return result
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_load_domain_concepts:25-33):

name = concept['name']
if name not in domain_concepts:
    concept_with_metadata = concept.copy()
    if 'module' not in concept_with_metadata:
        concept_with_metadata['module'] = epic_namespace...
Location (_load_domain_concepts:40-46):

concept_with_metadata = concept.copy()
if 'module' not in concept_with_metadata:
    concept_with_metadata['module'] = sub_epic_name
concept_with_metadata['namespace'] = sub_epic_name
domain_concepts[...
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Duplicate code blocks detected (3 locations) - extract to helper function.

Location (render:243-262):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
solution_name, solution_name_slug, solution_purpose = _get_so...
Location (render:138-154):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
solution_name, solution_name_slug, solution_purpose = _get_so...
Location (render:357-372):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
domain_concepts = _load_domain_concepts(input_path)
concepts_...
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Duplicate code blocks detected (3 locations) - extract to helper function.

Location (render:138-146):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
solution_name, solution_name_slug, solution_purpose = _get_so...
Location (render:243-251):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
solution_name, solution_name_slug, solution_purpose = _get_so...
Location (render:357-364):

input_path = Path(input_path)
project_path = kwargs.get('project_path', input_path.parent.parent.parent)
project_path = Path(project_path)
domain_concepts = _load_domain_concepts(input_path)
concepts_...
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render:318-336):

output_path = Path(output_path)
if output_path.is_dir() or not output_path.suffix:
    output_path = output_path / f'{solution_name_slug}-domain-model-diagram.mmd'
elif output_path.suffix == '.md':
  ...
Location (render:391-406):

output_path = Path(output_path)
if output_path.is_dir() or not output_path.suffix:
    output_path = output_path / 'domain_outline.md'
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(o...
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (convert_behavioral_ac_to_steps:22-35):

step_type = 'Given'
step_lower = step_text.lower()
if step_lower.startswith('when'):
    step_type = 'When'
elif step_lower.startswith('then'):
    step_type = 'Then'
elif step_lower.startswith('and')...
Location (adapt_story_in_story_groups:48-62):

step_type = 'Given'
ac_lower = ac.lower()
if ac_lower.startswith('when'):
    step_type = 'When'
elif ac_lower.startswith('then'):
    step_type = 'Then'
elif ac_lower.startswith('and'):
    step_type...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (synchronize_outline_command:99-103):

report = result.get('sync_report', {})
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f'Synchronization report saved to: {report_path}...
Location (synchronize_increments_command:131-135):

report = result.get('sync_report', {})
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(f'Synchronization report saved to: {report_path}...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (synchronize_outline_command:78-91):

diagram = StoryIODiagram(drawio_file=args.drawio_file)
original_path = None
if args.original:
    original_path = Path(args.original)
generate_report = getattr(args, 'generate_report', False)
report_p...
Location (synchronize_increments_command:110-124):

diagram = StoryIODiagram(drawio_file=args.drawio_file)
original_path = None
if args.original:
    original_path = Path(args.original)
generate_report = getattr(args, 'generate_report', False)
report_p...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (4 locations) - extract to helper function.

Location (main:432-445):

parser = argparse.ArgumentParser(description='Story IO CLI - Manage story maps')
subparsers = parser.add_subparsers(dest='command', help='Command to execute')
render_outline_parser = subparsers.add_pa...
Location (main:456-467):

sync_parser.add_argument('--type', choices=['auto', 'outline', 'increments'], default='auto', help='Sync type: auto (detect from filename), outline, or increments')
sync_parser.add_argument('--origina...
Location (main:477-487):

sync_inc_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_inc_parser.add_argument('--original', type=Path, help='Original story graph for comparison')
sync_...
Location (main:520-528):

sync_discovery_parser.add_argument('--original', type=Path, help='Original story graph for comparison')
sync_discovery_parser.add_argument('--output', type=Path, help='Output story graph JSON file')
s...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (7 locations) - extract to helper function.

Location (main:450-466):

render_inc_parser.add_argument('--layout', type=Path, help='Layout JSON file')
sync_parser = subparsers.add_parser('synchronize', aliases=['sync'], help='Synchronize from DrawIO file (auto-detects out...
Location (main:468-483):

sync_outline_parser.add_argument('--original', type=Path, help='Original story graph for comparison')
sync_outline_parser.add_argument('--output', type=Path, help='Output story graph JSON file')
sync_...
Location (main:531-546):

render_exploration_parser.add_argument('--layout', type=Path, help='Layout JSON file to preserve positions')
sync_exploration_parser = subparsers.add_parser('sync-exploration', help='Synchronize explo...
Location (main:499-512):

add_user_parser.add_argument('--epic-name', help='Epic name (optional - to narrow story search)')
add_user_parser.add_argument('--sub-epic-name', help='Sub-epic name (optional - to narrow story search...
Location (main:514-527):

render_discovery_parser.add_argument('--increment-names', nargs='+', help='Increment name(s) to render')
render_discovery_parser.add_argument('--layout', type=Path, help='Layout JSON file to preserve ...
Location (main:439-449):

render_outline_parser.add_argument('--drawio-file', type=Path, help='DrawIO file path')
render_outline_parser.add_argument('--output', type=Path, required=True, help='Output DrawIO file')
render_outli...
Location (main:487-495):

search_parser.add_argument('--story-graph', type=Path, help='Story graph JSON file')
search_parser.add_argument('--json', type=Path, help='Story graph JSON file (alias)')
search_parser.add_argument('q...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (4 locations) - extract to helper function.

Location (main:459-476):

sync_parser.add_argument('--output', type=Path, help='Output story graph JSON file')
sync_parser.add_argument('--generate-report', action='store_true', help='Generate synchronization report')
sync_par...
Location (main:477-488):

sync_inc_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_inc_parser.add_argument('--original', type=Path, help='Original story graph for comparison')
sync_...
Location (main:519-527):

sync_discovery_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_discovery_parser.add_argument('--original', type=Path, help='Original story graph for compar...
Location (main:535-539):

sync_exploration_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_exploration_parser.add_argument('--original', type=Path, help='Original story graph for co...
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (main:535-546):

sync_exploration_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_exploration_parser.add_argument('--original', type=Path, help='Original story graph for co...
Location (main:519-524):

sync_discovery_parser.add_argument('--drawio-file', type=Path, required=True, help='DrawIO file path')
sync_discovery_parser.add_argument('--original', type=Path, help='Original story graph for compar...
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render_outline_from_graph:526-545):

import json
if isinstance(story_graph, (str, Path)):
    story_graph_path = Path(story_graph)
    with open(story_graph_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
else:
    g...
Location (render_increments_from_graph:733-751):

import json
if isinstance(story_graph, (str, Path)):
    story_graph_path = Path(story_graph)
    with open(story_graph_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
else:
    g...
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render_increments:612-617):

import json
with open(self._source_path, 'r', encoding='utf-8') as f:
    raw_graph_data = json.load(f)
graph_data = raw_graph_data
Location (render_discovery:656-661):

import json
with open(self._source_path, 'r', encoding='utf-8') as f:
    raw_graph_data = json.load(f)
graph_data = raw_graph_data
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render_exploration:357-364):

story_name = story.get('name', '')
if story_name:
    epic_name, sub_epic_name = self._find_story_path(story_name, all_epics_for_lookup)
    if epic_name and sub_epic_name:
        story_key = f'{epic...
Location (render_discovery:497-504):

story_name = story.get('name', '')
if story_name:
    epic_name, sub_epic_name = self._find_story_path(story_name, all_epics_for_lookup)
    if epic_name and sub_epic_name:
        story_key = f'{epic...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render_exploration:383-387):

story_name = story.get('name', '')
story_key = f'{epic_name}|{sub_epic_name}|{story_name}'
if story_key in stories_in_increment:
    filtered_stories.append(story)
Location (render_discovery:523-527):

story_name = story.get('name', '')
story_key = f'{epic_name}|{sub_epic_name}|{story_name}'
if story_key in stories_in_increments:
    filtered_stories.append(story)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (render_increments:442-458):

output_path.parent.mkdir(parents=True, exist_ok=True)
xml_output = self._generate_diagram(story_graph, layout_data, is_increments=True)
output_path.write_text(xml_output, encoding='utf-8')
increments_...
Location (render_discovery:583-599):

output_path.parent.mkdir(parents=True, exist_ok=True)
xml_output = self._generate_diagram(filtered_graph, layout_data, is_increments=True)
output_path.write_text(xml_output, encoding='utf-8')
incremen...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (5 locations) - extract to helper function.

Location (_generate_exploration_diagram:858-864):

ac_x = ac_layout['x']
ac_y = ac_layout['y']
ac_width = ac_layout.get('width', ac_width)
Location (_generate_diagram:2188-2196):

ac_x = layout_data[ac_key]['x']
ac_y = layout_data[ac_key]['y']
ac_width = layout_data[ac_key].get('width', ac_width)
Location (_generate_diagram:1920-1926):

ac_x = layout_data[ac_key]['x']
ac_y = layout_data[ac_key]['y']
ac_width = layout_data[ac_key].get('width', ac_width)
Location (_generate_increments_diagram:4453-4461):

ac_x = layout_data[ac_key]['x']
ac_y = layout_data[ac_key]['y']
ac_width = layout_data[ac_key].get('width', ac_width)
Location (_generate_increments_diagram:4185-4191):

ac_x = layout_data[ac_key]['x']
ac_y = layout_data[ac_key]['y']
ac_width = layout_data[ac_key].get('width', ac_width)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1043-1060):

story_groups = normalize_story_groups(feature)
if not story_groups:
    continue
has_story_with_ac = False
for group in story_groups:
    for story in group.get('stories', []):
        if story.get('a...
Location (_generate_increments_diagram:3308-3325):

story_groups = normalize_story_groups(feature)
if not story_groups:
    continue
has_story_with_ac = False
for group in story_groups:
    for story in group.get('stories', []):
        if story.get('a...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1070-1083):

epic_x = layout_data[epic_key]['x']
epic_y = layout_data[epic_key]['y']
epic_width = layout_data[epic_key].get('width', 0)
epic_height = 60
use_epic_layout = True
Location (_generate_increments_diagram:3335-3348):

epic_x = layout_data[epic_key]['x']
epic_y = layout_data[epic_key]['y']
epic_width = layout_data[epic_key].get('width', 0)
epic_height = 60
use_epic_layout = True
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1090-1096):

stories = feature.get('stories', [])
has_ac = any((s.get('acceptance_criteria') for s in stories))
feature_has_ac[feature['name']] = has_ac
Location (_generate_increments_diagram:3355-3361):

stories = feature.get('stories', [])
has_ac = any((s.get('acceptance_criteria') for s in stories))
feature_has_ac[feature['name']] = has_ac
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1111-1119):

sub_story_groups = normalize_story_groups(sub_epic)
sub_nested = sub_epic.get('sub_epics', [])
if sub_story_groups and len(sub_story_groups) > 0:
    collected.append(sub_epic)
elif sub_nested:
    co...
Location (_generate_increments_diagram:3376-3384):

sub_story_groups = normalize_story_groups(sub_epic)
sub_nested = sub_epic.get('sub_epics', [])
if sub_story_groups and len(sub_story_groups) > 0:
    collected.append(sub_epic)
elif sub_nested:
    co...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1182-1190):

group_stories = group.get('stories', [])
if is_exploration:
    group_stories = [s for s in group_stories if s.get('acceptance_criteria')]
stories.extend(group_stories)
Location (_generate_increments_diagram:3447-3455):

group_stories = group.get('stories', [])
if is_exploration:
    group_stories = [s for s in group_stories if s.get('acceptance_criteria')]
stories.extend(group_stories)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1215-1222):

stories_in_seq = stories_by_seq[seq_order]
for story in stories_in_seq:
    if story.get('flag', False):
        has_optional = True
    elif seq_order not in sequential_orders:
        sequential_ord...
Location (_generate_increments_diagram:3480-3487):

stories_in_seq = stories_by_seq[seq_order]
for story in stories_in_seq:
    if story.get('flag', False):
        has_optional = True
    elif seq_order not in sequential_orders:
        sequential_ord...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1339-1344):

has_estimated_stories = True
estimated_stories_count = epic['estimated_stories']
epic_story_text = f"""<span style="border-color: rgb(218, 220, 224); flex: 1 1 0%;">{epic['name']}</span><div style="bo...
Location (_generate_increments_diagram:3604-3609):

has_estimated_stories = True
estimated_stories_count = epic['estimated_stories']
epic_story_text = f"""<span style="border-color: rgb(218, 220, 224); flex: 1 1 0%;">{epic['name']}</span><div style="bo...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1377-1388):

user_x = layout_data[user_key]['x']
layout_user_y = layout_data[user_key]['y']
if layout_user_y < self.EPIC_Y + 50:
    user_y = layout_user_y
else:
    user_x = epic_x + epic_user_x_offset
    user_y...
Location (_generate_increments_diagram:3642-3653):

user_x = layout_data[user_key]['x']
layout_user_y = layout_data[user_key]['y']
if layout_user_y < self.EPIC_Y + 50:
    user_y = layout_user_y
else:
    user_x = epic_x + epic_user_x_offset
    user_y...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1589-1604):

filtered_story_groups = []
for group in feature_story_groups:
    group_stories = group.get('stories', [])
    filtered_group_stories = [s for s in group_stories if s.get('acceptance_criteria')]
    i...
Location (_generate_increments_diagram:3854-3869):

filtered_story_groups = []
for group in feature_story_groups:
    group_stories = group.get('stories', [])
    filtered_group_stories = [s for s in group_stories if s.get('acceptance_criteria')]
    i...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (4 locations) - extract to helper function.

Location (_generate_diagram:1837-1846):

collision_detected = False
for rx, ry, rw, rh in rendered_positions:
    if user_x < rx + rw and user_x + user_width > rx and (user_y < ry + rh) and (user_y + user_height > ry):
        collision_dete...
Location (_generate_diagram:1759-1767):

collision_detected = False
for rx, ry, rw, rh in rendered_positions:
    if group_start_x < rx + rw and group_start_x + user_width > rx and (test_user_y < ry + rh) and (test_user_y + user_height > ry)...
Location (_generate_increments_diagram:4102-4111):

collision_detected = False
for rx, ry, rw, rh in rendered_positions:
    if user_x < rx + rw and user_x + user_width > rx and (user_y < ry + rh) and (user_y + user_height > ry):
        collision_dete...
Location (_generate_increments_diagram:4024-4032):

collision_detected = False
for rx, ry, rw, rh in rendered_positions:
    if group_start_x < rx + rw and group_start_x + user_width > rx and (test_user_y < ry + rh) and (test_user_y + user_height > ry)...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1771-1777):

new_user_bottom = test_user_y + user_height
new_story_y = new_user_bottom + 10
story_adjustment = new_story_y - story_y
max_group_adjustment = max(max_group_adjustment, story_adjustment)
Location (_generate_increments_diagram:4036-4042):

new_user_bottom = test_user_y + user_height
new_story_y = new_user_bottom + 10
story_adjustment = new_story_y - story_y
max_group_adjustment = max(max_group_adjustment, story_adjustment)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1780-1786):

group_start_y += max_group_adjustment
if group_type == 'and':
    group_bottom_y = group_start_y
else:
    group_bottom_y = group_start_y + (len(sorted_group_stories) - 1) * self.STORY_SPACING_Y
Location (_generate_increments_diagram:4045-4051):

group_start_y += max_group_adjustment
if group_type == 'and':
    group_bottom_y = group_start_y
else:
    group_bottom_y = group_start_y + (len(sorted_group_stories) - 1) * self.STORY_SPACING_Y
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1821-1831):

user_x = layout_data[user_key]['x']
layout_user_y = layout_data[user_key]['y']
if layout_user_y < 50:
    user_x = story_x
    user_y = initial_user_y
else:
    user_y = layout_user_y
Location (_generate_increments_diagram:4086-4096):

user_x = layout_data[user_key]['x']
layout_user_y = layout_data[user_key]['y']
if layout_user_y < 50:
    user_x = story_x
    user_y = initial_user_y
else:
    user_y = layout_user_y
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:1978-1994):

previous_group_bottom_y = group_bottom_y
previous_group_rightmost_x = group_rightmost_x
previous_group_start_x = group_start_x
previous_group_has_users = group_has_users
Location (_generate_increments_diagram:4243-4259):

previous_group_bottom_y = group_bottom_y
previous_group_rightmost_x = group_rightmost_x
previous_group_start_x = group_start_x
previous_group_has_users = group_has_users
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2106-2119):

feature_x = feature_min_x
actual_feature_width = actual_feature_rightmost - feature_min_x
if feat_idx == 1:
    feature_x = feature_min_x - self.FIRST_SUB_EPIC_LEFT_SHIFT
    actual_feature_width = ac...
Location (_generate_increments_diagram:4371-4384):

feature_x = feature_min_x
actual_feature_width = actual_feature_rightmost - feature_min_x
if feat_idx == 1:
    feature_x = feature_min_x - self.FIRST_SUB_EPIC_LEFT_SHIFT
    actual_feature_width = ac...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2156-2164):

if cell.get('id') == next_feat_cell_id:
    geom = cell.find('mxGeometry')
    if geom is not None:
        geom.set('x', str(next_feature_x))
        next_feat_data['x'] = next_feature_x
    break
Location (_generate_increments_diagram:4421-4429):

if cell.get('id') == next_feat_cell_id:
    geom = cell.find('mxGeometry')
    if geom is not None:
        geom.set('x', str(next_feature_x))
        next_feat_data['x'] = next_feature_x
    break
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2319-2325):

if fg.get('geom'):
    final_feat_x = float(fg['geom'].get('x', 0))
    final_feat_width = float(fg['geom'].get('width', 0))
    if final_feat_width > 0:
        epic_min_x = min(epic_min_x, final_fea...
Location (_generate_increments_diagram:4584-4590):

if fg.get('geom'):
    final_feat_x = float(fg['geom'].get('x', 0))
    final_feat_width = float(fg['geom'].get('width', 0))
    if final_feat_width > 0:
        epic_min_x = min(epic_min_x, final_fea...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (4 locations) - extract to helper function.

Location (_generate_diagram:2355-2359):

feat_x = float(fg['geom'].get('x', 0))
feat_width = float(fg['geom'].get('width', 0))
if feat_width > 0:
    feature_rights.append(feat_x + feat_width)
Location (_generate_diagram:2370-2374):

feat_x = float(geom.get('x', 0))
feat_width = float(geom.get('width', 0))
if feat_width > 0:
    feature_rights.append(feat_x + feat_width)
Location (_generate_increments_diagram:4620-4624):

feat_x = float(fg['geom'].get('x', 0))
feat_width = float(fg['geom'].get('width', 0))
if feat_width > 0:
    feature_rights.append(feat_x + feat_width)
Location (_generate_increments_diagram:4635-4639):

feat_x = float(geom.get('x', 0))
feat_width = float(geom.get('width', 0))
if feat_width > 0:
    feature_rights.append(feat_x + feat_width)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2376-2386):

calculated_epic_max_x = max(feature_rights)
epic_padding = 30 if epic_idx == 1 else 6
actual_epic_width = calculated_epic_max_x - epic_x + epic_padding
actual_epic_x = epic_x
Location (_generate_increments_diagram:4641-4651):

calculated_epic_max_x = max(feature_rights)
epic_padding = 30 if epic_idx == 1 else 6
actual_epic_width = calculated_epic_max_x - epic_x + epic_padding
actual_epic_x = epic_x
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2475-2479):

spacing = available_width / (len(middle_features) + 1)
for idx, (feat_cell, feat_geom, old_feat_x, feat_width) in enumerate(middle_features):
    new_feat_x = first_feat_right + (idx + 1) * spacing
  ...
Location (_generate_increments_diagram:4740-4744):

spacing = available_width / (len(middle_features) + 1)
for idx, (feat_cell, feat_geom, old_feat_x, feat_width) in enumerate(middle_features):
    new_feat_x = first_feat_right + (idx + 1) * spacing
  ...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2486-2491):

story_geom = story_cell.find('mxGeometry')
if story_geom is not None:
    story_x = float(story_geom.get('x', 0))
    new_story_x = story_x + feat_x_offset
    story_geom.set('x', str(new_story_x))
Location (_generate_increments_diagram:4751-4756):

story_geom = story_cell.find('mxGeometry')
if story_geom is not None:
    story_x = float(story_geom.get('x', 0))
    new_story_x = story_x + feat_x_offset
    story_geom.set('x', str(new_story_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2497-2502):

epic_geom = epic_cell.find('mxGeometry')
if epic_geom is not None:
    epic_x = float(epic_geom.get('x', 0))
    epic_width = float(epic_geom.get('width', 0))
    epic_group_rightmost = max(epic_group...
Location (_generate_increments_diagram:4762-4767):

epic_geom = epic_cell.find('mxGeometry')
if epic_geom is not None:
    epic_x = float(epic_geom.get('x', 0))
    epic_width = float(epic_geom.get('width', 0))
    epic_group_rightmost = max(epic_group...
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (_generate_diagram:2640-2645):

geom = cell.find('mxGeometry')
if geom is not None:
    y = float(geom.get('y', 0))
    height = float(geom.get('height', 0))
    max_y = max(max_y, y + height)
Location (_generate_increments_diagram:4871-4876):

geom = cell.find('mxGeometry')
if geom is not None:
    y = float(geom.get('y', 0))
    height = float(geom.get('height', 0))
    max_y = max(max_y, y + height)
[X] ERROR - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Duplicate code blocks detected (2 locations) - extract to helper function.

Location (main:156-162):

if test_method in test_methods_map:
    method_info = test_methods_map[test_method]
    if method_info['steps']:
        scenario['steps'] = method_info['steps']
        updated_count += 1
        pri...
Location (main:172-178):

if test_method in test_methods_map:
    method_info = test_methods_map[test_method]
    if method_info['steps']:
        scenario['steps'] = method_info['steps']
        updated_count += 1
        pri...
Place Imports At Top: 14 violation(s)
[X] ERROR - src\utils.py: Import statement found after non-import code. Move all imports to the top of the file.

    return _find_ast_node_line(test_file_path, test_method_name, ast.FunctionDef)

import re

[X] ERROR - src\scanners\vocabulary_helper.py: Import statement found after non-import code. Move all imports to the top of the file.

        nltk.download('wordnet', quiet=True)
    except Exception as e:
        import sys
        print(f"Warning: Failed to download NLTK wordnet: {e}", file=sys.stderr)
[X] ERROR - src\scanners\vocabulary_helper.py: Import statement found after non-import code. Move all imports to the top of the file.

        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        import sys
        print(f"Warning: Failed to download NLTK punkt_tab: {e}", file=sys.stderr)
[X] ERROR - src\scanners\vocabulary_helper.py: Import statement found after non-import code. Move all imports to the top of the file.

        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
    except Exception as e:
        import sys
        print(f"Warning: Failed to download NLTK averaged_perceptron_tagger_eng: {e}", file=sys.stderr)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Import statement found after non-import code. Move all imports to the top of the file.

if __name__ == "__main__":
    """Command-line interface for synchronizing story maps from DrawIO."""
    import argparse
    import tempfile
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Import statement found after non-import code. Move all imports to the top of the file.

    """Command-line interface for synchronizing story maps from DrawIO."""
    import argparse
    import tempfile
    
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Import statement found after non-import code. Move all imports to the top of the file.

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
[X] ERROR - src\synchronizers\story_io\examples\add_gm_user.py: Import statement found after non-import code. Move all imports to the top of the file.

args = parser.parse_args()

from bots.base_bot.src.state.workspace import get_workspace_directory
workspace_root = get_workspace_directory()
[X] ERROR - src\synchronizers\story_io\examples\add_user_example.py: Import statement found after non-import code. Move all imports to the top of the file.

args = parser.parse_args()

from bots.base_bot.src.state.workspace import get_workspace_directory
workspace_root = get_workspace_directory()
[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Import statement found after non-import code. Move all imports to the top of the file.

sys.path.insert(0, str(_src_dir))

from synchronizers.story_io.story_io_diagram import StoryIODiagram
from synchronizers.story_io.examples.render_example import adapt_story_graph
[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Import statement found after non-import code. Move all imports to the top of the file.


from synchronizers.story_io.story_io_diagram import StoryIODiagram
from synchronizers.story_io.examples.render_example import adapt_story_graph
import json
[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Import statement found after non-import code. Move all imports to the top of the file.

from synchronizers.story_io.story_io_diagram import StoryIODiagram
from synchronizers.story_io.examples.render_example import adapt_story_graph
import json

[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Import statement found after non-import code. Move all imports to the top of the file.


# Resolve workspace from environment (WORKING_AREA preferred)
from bots.base_bot.src.state.workspace import get_workspace_directory
workspace_root = get_workspace_directory()
[X] ERROR - src\synchronizers\story_io\examples\load_and_render_example.py: Import statement found after non-import code. Move all imports to the top of the file.

args = parser.parse_args()

from bots.base_bot.src.state.workspace import get_workspace_directory
workspace_root = get_workspace_directory()
Provide Meaningful Context: 11 violation(s)
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Line 1281 contains magic number - replace with named constant

                        # Estimate width based on story count (will be updated after rendering)
                        estimated_width = max(200, len(stories) * self.STORY_SPACING_X + 20)
                        current_feature_x = feat_x + estimated_width + self.FEATURE_SPACING_X
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Line 1358 contains magic number - replace with named constant

                estimated_text = f"~{estimated_stories_count} stories"
                estimated_cell = ET.SubElement(root_elem, 'mxCell', id=str(epic_idx + 200), 
                                              value=f"<span style=\"font-family: Helvetica; font-size: 8px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;\">{estimated_text}</span>",
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Line 3546 contains magic number - replace with named constant

                        # Estimate width based on story count (will be updated after rendering)
                        estimated_width = max(200, len(stories) * self.STORY_SPACING_X + 20)
                        current_feature_x = feat_x + estimated_width + self.FEATURE_SPACING_X
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Line 3623 contains magic number - replace with named constant

                estimated_text = f"~{estimated_stories_count} stories"
                estimated_cell = ET.SubElement(root_elem, 'mxCell', id=str(epic_idx + 200), 
                                              value=f"<span style=\"font-family: Helvetica; font-size: 8px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;\">{estimated_text}</span>",
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 434 contains magic number - replace with named constant

            # Check if sub-epic is not too far below (within reasonable distance, max 200px)
            max_distance_below = parent_bottom + 200
            is_within_range = sub_epic_y < max_distance_below
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 629 contains magic number - replace with named constant

                    sub_epic_x = best_match['x']
                    sub_epic_width = best_match.get('width', 200)
                    sub_epic_right = sub_epic_x + sub_epic_width
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 639 contains magic number - replace with named constant

                        sub_epic_x = sub_epic['x']
                        sub_epic_width = sub_epic.get('width', 200)
                        sub_epic_right = sub_epic_x + sub_epic_width
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 680 contains magic number - replace with named constant

            if (sub_epic_x <= story_center_x <= sub_epic_right and 
                sub_epic_y - tolerance <= story_y <= sub_epic_bottom + 200):
                containing_sub_epics.append(sub_epic)
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 1035 contains magic number - replace with named constant

        opt_story_y = 402
        or_story_y_start = 404.75
        
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 1105 contains magic number - replace with named constant

        opt_story_y = 402  # Optional stories start at y=402
        or_story_y_start = 404.75  # Alternative stories start at y=404.75+
        y_tolerance = 10  # pixels tolerance for base row
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Line 1231 contains magic number - replace with named constant

                    # Check if AC is not too far below (within reasonable distance, max 500px)
                    max_distance_below = story_y + story_height + 500
                    is_within_range = ac_y < max_distance_below
Refactor Completely Not Partially: 36 violation(s)
[!] WARNING - src\bot\json_bot.py: Fallback/legacy support code found (comment at line 57, code at line 58) - complete refactoring by removing old pattern support
[!] WARNING - src\bot_path\bot_path.py: Fallback/legacy support code found (comment at line 57, code at line 58) - complete refactoring by removing old pattern support
[!] WARNING - src\scanners\story_map.py: Fallback/legacy support code found (comment at line 203, code at line 204) - complete refactoring by removing old pattern support
[!] WARNING - src\story_graph\nodes.py: Fallback/legacy support code found (comment at line 1246, code at line 1247) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 764, code at line 765) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 1024, code at line 1025) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 1502, code at line 1503) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 1727, code at line 1728) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2080, code at line 2081) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2117, code at line 2118) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2125, code at line 2126) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2262, code at line 2264) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2383, code at line 2384) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2422, code at line 2423) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2520, code at line 2521) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2754, code at line 2756) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 2799, code at line 2800) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 3289, code at line 3290) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 3767, code at line 3768) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 3992, code at line 3993) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4345, code at line 4346) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4382, code at line 4383) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4390, code at line 4391) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4527, code at line 4529) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4648, code at line 4649) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4687, code at line 4688) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_renderer.py: Fallback/legacy support code found (comment at line 4785, code at line 4786) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_story.py: Fallback/legacy support code found (comment at line 158, code at line 159) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_io_story.py: Fallback/legacy support code found (comment at line 219, code at line 220) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Fallback/legacy support code found (comment at line 371, code at line 372) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Fallback/legacy support code found (comment at line 544, code at line 545) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Fallback/legacy support code found (comment at line 695, code at line 696) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Fallback/legacy support code found (comment at line 838, code at line 839) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Fallback/legacy support code found (comment at line 265, code at line 266) - complete refactoring by removing old pattern support
[!] WARNING - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Fallback/legacy support code found (comment at line 94, code at line 95) - complete refactoring by removing old pattern support
[!] WARNING - src\scanners\code\javascript\js_code_scanner.py: Fallback/legacy support code found (comment at line 52, code at line 53) - complete refactoring by removing old pattern support
Stop Writing Useless Comments: 741 violation(s)
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def sanitize_json_string(text: str) -> str:
    """Remove invalid control characters from a string before JSON serialization.
    
    JSON only allows \n (0x0A), \r (0x0D), and \t (0x09) as control characters.
    All other control characters (0x00-0x1F) are invalid and will cause parse errors.
    
    Args:
        text: String that may contain invalid control characters
        
    Returns:
        Sanitized string with invalid control characters removed
    """
    if not isinstance(text, str):
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def sanitize_for_json(obj: Any) -> Any:
    """Recursively sanitize an object for JSON serialization by removing invalid control characters.
    
    Also handles objects with to_dict() methods by converting them to dictionaries first.
    
    Args:
        obj: Object to sanitize (dict, list, str, etc.)
        
    Returns:
        Sanitized object safe for JSON serialization
    """
    if isinstance(obj, str):
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def parse_command_text(text: str) -> tuple[str, str]:
    """Parse command text into verb and arguments.
    
    Args:
        text: Command text to parse (e.g., "scope --filter=story")
        
    Returns:
        Tuple of (verb, args) where verb is lowercase and args is the rest
    """
    parts = text.split(maxsplit=1)
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _find_ast_node_line(file_path: Path, node_name: str, node_type: type) -> Optional[int]:
    """Generic helper to find AST node line number by name and type.
    
    Args:
        file_path: Path to Python file to parse
        node_name: Name of the node to find
        node_type: Type of AST node to look for (ast.ClassDef, ast.FunctionDef, etc.)
        
    Returns:
        Line number where node is defined, or None if not found
    """
    if not file_path.exists() or not node_name or node_name == '?':
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_test_class_line(test_file_path: Path, test_class_name: str) -> Optional[int]:
    """Find line number where a test class is defined."""
    return _find_ast_node_line(test_file_path, test_class_name, ast.ClassDef)
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_test_method_line(test_file_path: Path, test_method_name: str) -> Optional[int]:
    """Find line number where a test method/function is defined."""
    return _find_ast_node_line(test_file_path, test_method_name, ast.FunctionDef)
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_js_test_class_line(test_file_path: Path, test_class_name: str) -> Optional[int]:
    """Find line number where a JavaScript test class is defined.
    
    Looks for patterns like: test('TestClassName', ...)
    """
    if not test_file_path.exists() or not test_class_name or test_class_name == '?':
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_js_test_method_line(test_file_path: Path, test_method_name: str) -> Optional[int]:
    """Find line number where a JavaScript test method is defined.
    
    Looks for patterns like: await t.test('test_method_name', ...) or t.test('test_method_name', ...)
    """
    if not test_file_path.exists() or not test_method_name or test_method_name == '?':
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_js_test_file_path(py_test_file_path: Path) -> Optional[Path]:
    """Get the corresponding JavaScript test file for a Python test file.
    
    Example: test_edit_story_nodes.py -> test_edit_story_nodes.js
    """
    if not py_test_file_path.suffix == '.py':
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_js_file_with_test_class(py_test_file_path: Path, test_class_name: str) -> tuple[Optional[Path], Optional[int]]:
    """Search all JS files in the same directory for a test class.
    
    Returns tuple of (js_file_path, line_number) or (None, None) if not found.
    """
    if not py_test_file_path.exists():
[X] ERROR - src\utils.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_js_file_with_test_method(py_test_file_path: Path, test_method_name: str) -> tuple[Optional[Path], Optional[int]]:
    """Search all JS files in the same directory for a test method.
    
    Returns tuple of (js_file_path, line_number) or (None, None) if not found.
    """
    if not py_test_file_path.exists():
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_parameter_description(self, param_name: str) -> str:
        """Get meaningful description for a parameter by delegating to domain objects."""
        from .clarify.requirements_clarifications import RequirementsClarifications
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def __call__(self, **kwargs) -> Dict[str, Any]:
        """
        Make Action objects callable so DomainNavigator can execute them directly.
        Example: bot.behaviors.shape.build() or bot.behaviors.shape.build(**params)
        """
        # If context is provided in kwargs, use it; otherwise create default
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_behavior_section(self, output_lines: list):
        """Format behavior instructions section."""
        if not self.behavior:
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_action_section(self, output_lines: list):
        """Format action instructions section."""
        action_name = self.action_name if hasattr(self, 'action_name') else 'unknown'
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_key_questions(self, key_questions, output_lines: list):
        """Format key questions section."""
        if not key_questions:
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_evidence(self, evidence, output_lines: list):
        """Format evidence section."""
        if not evidence:
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_guardrails_section(self, guardrails_dict: dict, output_lines: list):
        """Format guardrails section with required context."""
        if not guardrails_dict:
[X] ERROR - src\actions\action.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_instructions_for_display(self, instructions) -> str:
        """Format instructions for display by building sections."""
        instructions_dict = instructions.to_dict()
[X] ERROR - src\behaviors\behavior.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getattr__(self, name: str):
        """
        Dynamically resolve action names as attributes.
        This allows DomainNavigator to access actions like: behavior.build, behavior.clarify, etc.
        """
        # Avoid infinite recursion by checking if _actions exists
[X] ERROR - src\behaviors\behavior.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def submitRules(self) -> Dict[str, Any]:
        """Submit behavior rules instructions to AI chat.
        
        Executes the rules action to get instructions, then submits them to chat.
        
        Returns:
            Status dict with success message and submission details
        """
        if not self.bot:
[X] ERROR - src\behaviors\behavior.py: Useless comment: "# Return the action object, not the navigation result" - delete it or improve the code instead

            # Navigate to the action when accessed
            self.actions.navigate_to(name)
            # Return the action object, not the navigation result
            return action
[X] ERROR - src\bot\behavior.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getattr__(self, name: str):
        """
        Dynamically resolve action names as attributes.
        This allows DomainNavigator to access actions like: behavior.build, behavior.clarify, etc.
        """
        # Avoid infinite recursion by checking if _actions exists
[X] ERROR - src\bot\bot.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_map(self) -> StoryMap:
        """Lazy-load and return the story map from workspace.
        
        Returns:
            StoryMap: The loaded story map with Epic/SubEpic/Story hierarchy
            
        Raises:
            FileNotFoundError: If story-graph.json doesn't exist in workspace
        """
        story_graph_path = self.bot_paths.workspace_directory / 'docs' / 'stories' / 'story-graph.json'
[X] ERROR - src\bot\bot.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def reload_story_graph(self) -> dict:
        """Clear the cached story graph to force reload on next access.
        
        Returns:
            dict: Status message indicating the cache was cleared
        """
        self._story_graph = None
[X] ERROR - src\bot\bot.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_graph(self) -> StoryMap:
        """Deprecated: Use story_map instead."""
        return self.story_map
[X] ERROR - src\bot_path\bot_path.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def _load_workspace_from_config(self) -> Optional[Path]:
        """Load workspace directory from bot_config.json (mcp.env.WORKING_AREA)"""
        if not self._bot_directory:
[X] ERROR - src\bot_path\bot_path.py: Useless comment: "# Update instance variable only - don't mutate global enviro" - delete it or improve the code instead

        resolved_path = Path(new_path).expanduser().resolve()
        previous = getattr(self, '_workspace_directory', None)
        # Update instance variable only - don't mutate global environment variable
        # This prevents tests from accidentally affecting other instances
[X] ERROR - src\cli\cli_session.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _execute_domain_object_command(self, command: str) -> tuple:
        """Execute commands on domain objects like story_graph.create_epic"""
        from navigation.domain_navigator import DomainNavigator
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainNavigator:
    """Navigate and execute methods on domain objects via dot notation"""
    
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def navigate(self, command: str) -> Any:
        """Parse and execute a domain object command
        
        Examples:
            story_graph.create_epic name:"User Management"
            story_graph."Epic Name".create_sub_epic name:"Auth"
        """
        import logging
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _split_command_and_params(self, command: str) -> tuple:
        """Split command into dot notation part and parameters part
        
        Example: 
            'story_graph.create_epic name:"User" at_position:1'
            -> ('story_graph.create_epic', 'name:"User" at_position:1')
            
            'story_graph."Invoke Bot".create name:"Test"'
            -> ('story_graph."Invoke Bot".create', 'name:"Test"')
        """
        # Split by finding where the parameters start (looking for param_name:)
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _parse_dot_notation(self, path: str) -> list:
        """Parse dot notation into parts, handling quoted strings
        
        Example:
            'story_graph."Epic Name".create_sub_epic'
            -> ['story_graph', 'Epic Name', 'create_sub_epic']
        """
        parts = []
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _parse_parameters(self, params_str: str) -> dict:
        """Parse parameters from string like: name:"User Management" at_position:1
        Also handles dotted paths like: target:"Epic1"."Child1"
        
        Returns:
            dict with parameter names and values
        """
        if not params_str:
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_result(self, method_name: str, result: Any, params: dict) -> dict:
        """Format domain object method result as serializable dict"""
        if result is None:
[X] ERROR - src\navigation\domain_navigator.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_object_result(self, obj: Any) -> dict:
        """Format a domain object (like StoryMap) as serializable dict"""
        # Handle Instructions objects - return them directly so CLI adapter can format them
[X] ERROR - src\navigation\domain_navigator.py: Useless comment: "# Get the first parameter name from the method signature" - delete it or improve the code instead

                    # If the next part looks like a value (not a method/property), treat it as a parameter
                    if not hasattr(attr, next_part): 
                        # Get the first parameter name from the method signature
                        try:
[X] ERROR - src\navigation\domain_navigator.py: Useless comment: "# Get first parameter (excluding 'self')" - delete it or improve the code instead

                        try:
                            sig = inspect.signature(attr)
                            # Get first parameter (excluding 'self')
                            param_names = [p for p in sig.parameters.keys() if p != 'self']
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass
class Responsibility:
    """Represents a single responsibility on a CRC card."""
    text: str
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass
class CRCCard:
    """Represents a CRC (Class-Responsibility-Collaborator) card."""
    name: str
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass
class Violation:
    """Represents a detected delegation violation."""
    card_name: str
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def parse_crc_file(file_path: str) -> List[CRCCard]:
    """Parse CRC model outline file into CRC cards."""
    cards = []
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_verb(responsibility_text: str) -> str:
    """Extract the action verb from a responsibility."""
    # Handle patterns like "Get/Set name" or "Get/Update name"
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_target(responsibility_text: str) -> str:
    """Extract the target object from 'Get X' or 'Set X' patterns."""
    # Handle "Get scenarios", "Get children", etc.
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_domain_verbs(collaborator_name: str) -> Set[str]:
    """Get domain verbs for a collaborator based on its type."""
    collab_lower = collaborator_name.lower()
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def is_implementation_detail(responsibility_text: str) -> bool:
    """Check if responsibility describes implementation (HOW) vs responsibility (WHAT)."""
    lower_text = responsibility_text.lower()
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def is_business_constraint(responsibility_text: str) -> bool:
    """Check if this is a unique business rule/constraint."""
    lower_text = responsibility_text.lower()
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def count_collaborators_in_responsibility(responsibility: Responsibility) -> int:
    """Count how many collaborators are involved in this responsibility."""
    return len(responsibility.collaborators)
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def check_delegation_violation(card: CRCCard, responsibility: Responsibility) -> Optional[Violation]:
    """
    Check if a responsibility violates delegation patterns.
    Returns None if no violation, otherwise returns a Violation object.
    """
    resp_text = responsibility.text
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def scan_crc_file(file_path: str) -> List[Violation]:
    """Scan a CRC file for delegation violations."""
    cards = parse_crc_file(file_path)
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_violation_report(violations: List[Violation]) -> str:
    """Format violations into a readable report."""
    if not violations:
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def main():
    """Main entry point."""
    import sys
[X] ERROR - src\scanners\crc_delegation_scanner.py: Useless comment: "# Get all collaborator names from ALL responsibilities" - delete it or improve the code instead

        target = extract_target(resp_text)
        if target:
            # Get all collaborator names from ALL responsibilities
            all_collabs = set()
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class LanguageAgnosticScanner(Scanner):
    """Wrapper scanner that delegates to language-specific scanner based on file extension."""
    
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_scanner_for_file(self, file_path: Path) -> Optional[Scanner]:
        """Get the appropriate scanner based on file extension."""
        if not file_path:
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context):
        """Delegate to appropriate scanner based on file extension."""
        scanner = self._get_scanner_for_file(context.path)
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_with_context(self, context):
        """Delegate to appropriate scanner based on file extensions in context."""
        # Group files by extension
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _load_single_scanner(self, module_path: str, class_name: str) -> tuple[Optional[Type[Scanner]], Optional[str]]:
        """Load a scanner from a specific path."""
        try:
[X] ERROR - src\scanners\scanner_registry.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _load_both_languages(self, module_path: str, class_name: str) -> tuple[Optional[Type[Scanner]], Optional[Type[Scanner]]]:
        """Load both Python and JavaScript versions of a scanner."""
        scanner_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower().replace('_scanner', '').replace('scanner', '')
[X] ERROR - src\scanners\story_map.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def has_examples(self) -> bool:
        """Check if this scenario has examples (data-driven testing)."""
        return self.examples is not None and len(self.examples.get('columns', [])) > 0
[X] ERROR - src\scope\scope.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def copy(self) -> 'Scope':
        """Create a copy of this scope."""
        new_scope = Scope(self.workspace_directory, self.bot_paths)
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_epic(self, epic) -> dict:
        """Serialize Epic object to dict by reading its properties."""
        return {
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_sub_epic(self, sub_epic) -> dict:
        """Serialize SubEpic object to dict by reading its properties."""
        from story_graph.nodes import SubEpic, Story, StoryGroup
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_story_group(self, story_group) -> dict:
        """Serialize StoryGroup object to dict."""
        return {
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_story(self, story) -> dict:
        """Serialize Story object to dict by reading its properties."""
        return {
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_ac(self, ac) -> dict:
        """Serialize AcceptanceCriteria object."""
        return {
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_scenario(self, scenario) -> dict:
        """Serialize Scenario object to dict by reading its properties."""
        # Serialize background steps
[X] ERROR - src\story_graph\json_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _serialize_step(self, step) -> dict:
        """Serialize Step object to dict."""
        return {
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _log(message: str):
    """Write log message to file."""
    log_file = Path(__file__).parent.parent.parent / 'logs' / 'test_class_mover.log'
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getitem__(self, child_name: str) -> 'StoryNode':
        """Access child by name"""
        for child in self.children:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def save(self) -> None:
        """Save this node's changes to the story graph and persist to disk."""
        if not self._bot:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def save_all(self) -> None:
        """Save this node and all children's changes to the story graph and persist to disk."""
        # Same as save() since updating the parent updates all children
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def _scope_command_for_node(self) -> str:
        """Get scope command string for this node type."""
        if isinstance(self, Story):
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def submit_instructions(self, behavior: str, action: str):
        """Submit instructions with scope set to this node, then restore original scope.
        
        Args:
            behavior: The behavior name to execute
            action: The action name to execute
        
        Returns:
            Instructions object containing the generated instructions
        """
        scope_file = self._bot.workspace_directory / 'scope.json'
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def submit_required_behavior_instructions(self, action: str):
        """Submit the required behavior instructions. Behavior from node; action passed in (e.g. build)."""
        behavior_needed = self.behavior_needed
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def submit_current_instructions(self):
        """Submit instructions using bot's current behavior and action with scope set to this node."""
        current_behavior = self._bot.behaviors.current.name
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def rename(self, name: str = None) -> dict:
        """Rename the node. Parameter 'name' for CLI compatibility."""
        if name is None or not name:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def delete(self, cascade: bool = True) -> dict:
        """Delete this node. Always cascades to delete all children."""
        import time
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def move_to(self, target: Union[str, 'StoryNode'] = None, position: Optional[int] = None, at_position: Optional[int] = None) -> dict:
        """Move node to a different parent or reorder within same parent. Parameters 'target' and 'at_position' for CLI compatibility."""
        # Handle CLI parameter alias
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _resolve_target_from_string(self, target_name: str) -> 'StoryNode':
        """Resolve a target node name to an actual node by searching from root.
        Supports both simple names and dotted paths like \"Epic1\".\"Child1\"
        """
        import re
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _search_node_recursive(self, node: 'StoryNode', name: str) -> Optional['StoryNode']:
        """Recursively search for a node by name"""
        for child in node.children:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def move_to_position(self, position: int) -> dict:
        """Alias for move_to with only position (moves within same parent)"""
        return self.move_to(position=position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def move_after(self, sibling: Union[str, 'StoryNode']) -> dict:
        """Move this node to be positioned after the specified sibling.
        
        Args:
            sibling: Either the name of a sibling node or a StoryNode instance
            
        Returns:
            Dict with operation details including new position
        """
        # Handle Epic nodes (no _parent, managed by StoryMap)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def create(self, name: Optional[str] = None, child_type: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Alias for create_child"""
        return self.create_child(name, child_type, position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_sub_epic(self, name: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Create SubEpic child"""
        return self.create_child(name, 'SubEpic', position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def delete(self, cascade: bool = True) -> dict:
        """Delete this epic from the story map. Always cascades to delete all children."""
        if not self._bot:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def children(self) -> List['StoryNode']:
        """Return children, transparently exposing Stories from StoryGroups."""
        if self.has_stories and not self.has_subepics:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getitem__(self, child_name: str) -> 'StoryNode':
        """Access child by name"""
        for child in self.children:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getitem__(self, child_name: str) -> 'StoryNode':
        """Access child by name"""
        for child in self.children:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def create(self, name: Optional[str] = None, child_type: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Alias for create_child"""
        return self.create_child(name, child_type, position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_story(self, name: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Create Story child"""
        return self.create_child(name, 'Story', position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_sub_epic(self, name: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Create SubEpic child"""
        return self.create_child(name, 'SubEpic', position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[StoryNode]=None, bot: Optional[Any]=None) -> 'StoryGroup':
        """Create StoryGroup from dictionary data."""
        sequential_order = data.get('sequential_order', 0.0)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getitem__(self, child_name: str) -> 'StoryNode':
        """Access child by name"""
        for child in self.children:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def create(self, name: Optional[str] = None, child_type: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Alias for create_child"""
        return self.create_child(name, child_type, position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_scenario(self, name: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Create Scenario child"""
        return self.create_child(name, 'Scenario', position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_acceptance_criteria(self, name: Optional[str] = None, position: Optional[int] = None) -> StoryNode:
        """Create AcceptanceCriteria child"""
        return self.create_child(name, 'AcceptanceCriteria', position)
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def examples_columns(self) -> List[str]:
        """Return columns from examples table, or empty list if no examples."""
        if self.examples:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def examples_rows(self) -> List[List[str]]:
        """Return rows from examples table, or empty list if no examples."""
        if self.examples:
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def has_examples(self) -> bool:
        """Check if this scenario has examples (data-driven testing)."""
        return self.examples is not None and len(self.examples.get('columns', [])) > 0
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


    def save(self) -> None:
        """Save the story graph to disk."""
        if not self._bot or not hasattr(self._bot, 'bot_paths'):
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __getitem__(self, epic_name: str) -> Epic:
        """Allow epic access by name: story_map['Epic Name']"""
        return self._epics[epic_name]
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def create_epic(self, name: Optional[str] = None, position: Optional[int] = None) -> Epic:
        """Create a new Epic at the root level of the story map.
        
        Args:
            name: Name for the new Epic. If None, generates unique name (Epic1, Epic2, etc.)
            position: Position to insert the Epic. If None, adds to end. If exceeds count, adjusts to last position.
            
        Returns:
            The newly created Epic instance
            
        Raises:
            ValueError: If an Epic with the same name already exists or name is empty
        """
        # Validate name is not empty
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def delete_epic(self, name: str) -> Dict[str, Any]:
        """Delete an epic from the story map. Always cascades to delete all children.
        
        Args:
            name: Name of the epic to delete
            
        Returns:
            Dict with operation details
            
        Raises:
            ValueError: If epic not found
        """
        # Find the epic
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _generate_unique_epic_name(self) -> str:
        """Generate a unique Epic name (Epic1, Epic2, etc.)"""
        counter = 1
[X] ERROR - src\story_graph\nodes.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _calculate_story_file_link(self, story: Story) -> str:
        """Calculate the file path for a story's markdown file."""
        if not self._bot or not hasattr(self._bot, 'bot_paths'):
[X] ERROR - src\story_graph\nodes.py: Useless comment: "# Create a new StoryGroup" - delete it or improve the code instead

                actual_target = story_groups[0]
            else:
                # Create a new StoryGroup
                story_group = StoryGroup(
[X] ERROR - src\story_graph\nodes.py: Useless comment: "# Perform the move" - delete it or improve the code instead

                _log(f"[move_to] Target SubEpic: None")
        
        # Perform the move
        _log(f"[move_to] BEFORE MOVE - actual_target type: {type(actual_target).__name__}, name: {actual_target.name}, children count: {len(actual_target._children)}")
[X] ERROR - src\story_graph\nodes.py: Useless comment: "# Handle already-quoted paths from parameter parsing (e.g., " - delete it or improve the code instead

        _log(f"[_resolve_target_from_string] RECEIVED target_name: '{target_name}' (type: {type(target_name)})")
        
        # Handle already-quoted paths from parameter parsing (e.g., "Epic1"."Child1")
        path_str = target_name
[X] ERROR - src\story_graph\nodes.py: Useless comment: "# Load story graph with error handling for control character" - delete it or improve the code instead

            raise FileNotFoundError(f'Story graph not found at {story_graph_path}')
        
        # Load story graph with error handling for control characters
        try:
[X] ERROR - src\story_graph\nodes.py: Useless comment: "# Create Epic instance" - delete it or improve the code instead

            name = self._generate_unique_epic_name()
        
        # Create Epic instance
        epic = Epic(name=name, domain_concepts=[], _bot=self._bot)
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _log(message: str):
    """Write log message to file."""
    log_file = Path(__file__).parent.parent.parent / 'logs' / 'test_class_mover.log'
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TestClassMover:
    """Handles extraction and movement of test classes between files."""
    
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def extract_class(file_path: Path, class_name: str) -> Optional[str]:
        """Extract a test class from a Python file.
        
        Args:
            file_path: Path to the source test file
            class_name: Name of the class to extract
            
        Returns:
            The class code as a string, or None if not found
        """
        _log(f"[TestClassMover] Extracting Test class [{class_name}](vscode://file/C:/dev/agile_bots/src/story_graph/test_class_mover.py:22) from {file_path}")
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT
    @staticmethod
    def remove_class(file_path: Path, class_name: str) -> bool:
        """Remove a test class from a Python file.
        
        Args:
            file_path: Path to the source test file
            class_name: Name of the class to remove
            
        Returns:
            True if class was found and removed, False otherwise
        """
        _log(f"[TestClassMover] Removing Test class [{class_name}](vscode://file/C:/dev/agile_bots/src/story_graph/test_class_mover.py:70) from {file_path}")
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def add_class(file_path: Path, class_code: str) -> bool:
        """Add a test class to a Python file.
        
        Args:
            file_path: Path to the target test file
            class_code: The class code to add
            
        Returns:
            True if class was added successfully
        """
        _log(f"[TestClassMover] Adding class to {file_path}")
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def move_class(source_file: Path, target_file: Path, class_name: str) -> bool:
        """Move a test class from source file to target file.
        
        Args:
            source_file: Path to the source test file
            target_file: Path to the target test file
            class_name: Name of the class to move
            
        Returns:
            True if class was moved successfully, False otherwise
        """
        _log(f"[TestClassMover] ========================================")
[X] ERROR - src\story_graph\test_class_mover.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def get_test_file_for_subepic(subepic: 'SubEpic') -> Optional[Path]:
        """Get the test file path for a SubEpic.
        
        Args:
            subepic: The SubEpic node
            
        Returns:
            Path to the test file, or None if not found
        """
        if not hasattr(subepic, 'test_file') or not subepic.test_file:
[X] ERROR - src\story_graph\test_class_mover.py: Useless comment: "# Get the source lines" - delete it or improve the code instead

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                # Get the source lines
                lines = content.splitlines(keepends=True)
[X] ERROR - src\story_graph\test_class_mover.py: Useless comment: "# Get the source lines" - delete it or improve the code instead

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                # Get the source lines
                lines = content.splitlines(keepends=True)
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _load_domain_concepts(input_path: Path) -> Dict[str, Dict]:
    """Load and deduplicate domain concepts from story graph, tracking module and namespace."""
    with open(input_path, 'r', encoding='utf-8') as f:
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _normalize_namespace(namespace: str, class_names: list) -> str:
    """
    Normalize namespace/module name to avoid conflicts with class names.
    If namespace/module matches a class name, add underscore prefix.
    
    Args:
        namespace: Original namespace/module name
        class_names: List of all class names in the domain
    
    Returns:
        Normalized namespace/module name
    """
    normalized = namespace
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _get_solution_info(project_path: Path, kwargs: Dict) -> tuple:
    """Extract solution name, slug, and purpose from project or kwargs."""
    solution_name = kwargs.get('solution_name')
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _get_source_material(project_path: Path) -> str:
    """Generate source material section."""
    input_file = project_path / 'input.txt'
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainModelDescriptionSynchronizer:
    """Synchronizer for rendering domain model description markdown."""
    
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainModelDiagramSynchronizer:
    """Synchronizer for rendering domain model diagram markdown with Mermaid."""
    
[X] ERROR - src\synchronizers\domain_model\domain_model_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainModelOutlineSynchronizer:
    """Synchronizer for rendering domain outline markdown for src/ directory."""
    
[X] ERROR - src\synchronizers\story_io\extract_layout.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_layout(drawio_path: Path, output_dir: Path = None):
    """Extract layout data from DrawIO file."""
    # Resolve to absolute paths
[X] ERROR - src\synchronizers\story_io\extract_layout.py: Useless comment: "# Create output path (ensure it's absolute)" - delete it or improve the code instead

    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output path (ensure it's absolute)
    output_path = (output_dir / f"{drawio_path.stem}-extracted.json").resolve()
[X] ERROR - src\synchronizers\story_io\extract_layout.py: Useless comment: "# Load diagram and synchronize to extract layout" - delete it or improve the code instead

    print(f"Output path: {output_path}")
    
    # Load diagram and synchronize to extract layout
    diagram = StoryIODiagram(drawio_file=drawio_path)
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def convert_behavioral_ac_to_steps(story_data):
    """Convert behavioral_ac array to Steps format."""
    if 'behavioral_ac' in story_data and story_data['behavioral_ac']:
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_story_in_story_groups(story_data, epic_users=None):
    """Adapt a single story, converting acceptance_criteria to Steps."""
    adapted_story = story_data.copy()
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_sub_epic(sub_epic_data, epic_users=None):
    """Recursively adapt a sub_epic, preserving structure and converting stories."""
    adapted_sub_epic = {
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_story_graph(data):
    """
    Adapt story graph to our expected format.
    Preserves sub_epics structure and converts acceptance_criteria/behavioral_ac to Steps.
    """
    adapted = {}
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
[X] ERROR - src\synchronizers\story_io\render_story_graph.py: Useless comment: "# Get input file" - delete it or improve the code instead

        sys.exit(1)
    
    # Get input file
    input_path = Path(sys.argv[1])
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def render_outline_command(args):
    """Render story graph as outline DrawIO diagram."""
    if args.story_graph:
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def render_increments_command(args):
    """Render story graph with increments as DrawIO diagram."""
    if args.story_graph:
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def synchronize_outline_command(args):
    """Synchronize story graph from DrawIO outline file."""
    diagram = StoryIODiagram(drawio_file=args.drawio_file)
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def synchronize_increments_command(args):
    """Synchronize story graph from DrawIO increments file."""
    diagram = StoryIODiagram(drawio_file=args.drawio_file)
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def synchronize_command(args):
    """Synchronize story graph from DrawIO file (auto-detects outline or increments)."""
    drawio_path = Path(args.drawio_file)
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def search_command(args):
    """Search for components in story graph."""
    if args.story_graph:
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def add_user_command(args):
    """Add user to story or all stories."""
    # Load diagram
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def merge_command(args):
    """Merge extracted story graph with original."""
    if not args.extracted or not args.extracted.exists():
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def render_discovery_command(args):
    """
    Render discovery increment(s) DrawIO diagram.
    """
    if args.story_graph:
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def sync_discovery_command(args):
    """
    Synchronize discovery increment(s) from DrawIO.
    
    Placeholder - implementation to be added.
    """
    print("Error: sync-discovery command not yet implemented", file=sys.stderr)
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def render_exploration_command(args):
    """Render exploration acceptance criteria DrawIO diagram."""
    story_graph_data = None
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def sync_exploration_command(args):
    """
    Synchronize exploration acceptance criteria from DrawIO.
    
    Placeholder - implementation to be added.
    """
    print("Error: sync-exploration command not yet implemented", file=sys.stderr)
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _load_from_json(json_path: Path) -> StoryIODiagram:
    """Load diagram from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
[X] ERROR - src\synchronizers\story_io\story_io_cli.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Story IO CLI - Manage story maps')
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass
class StoryIOComponent(ABC):
    """
    Base class for all story map components.
    
    Provides common functionality for hierarchy management, position tracking,
    synchronization, and rendering.
    """
    
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @parent.setter
    def parent(self, value: Optional['StoryIOComponent']) -> None:
        """Set the parent component and update relationships."""
        # Remove from old parent if exists
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __post_init__(self):
        """Initialize component after dataclass initialization."""
        if self._parent:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _add_child(self, child: 'StoryIOComponent') -> None:
        """Internal method to add a child component."""
        if child not in self._children:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _remove_child(self, child: 'StoryIOComponent') -> None:
        """Internal method to remove a child component."""
        if child in self._children:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def children(self) -> List['StoryIOComponent']:
        """Get all direct children of this component."""
        return list(self._children)
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def children_at_level(self, level: int) -> List['StoryIOComponent']:
        """Get all children at a specific depth level."""
        if level < 0:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def leafs(self) -> List['StoryIOComponent']:
        """Get all leaf nodes (components with no children)."""
        if not self._children:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def determine_children(self, level: int) -> List['StoryIOComponent']:
        """Determine children at a specific level of the hierarchy."""
        return self.children_at_level(level)
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_all_children(self, query: str) -> List['StoryIOComponent']:
        """Search for all children matching a query string."""
        results = []
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def move_before(self, target: 'StoryIOComponent') -> None:
        """
        Move this component before the target component.
        
        Both components must be at the same level in the hierarchy.
        Pushes other components at the same level to the right.
        """
        if not self._parent or self._parent != target._parent:
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _reorder_siblings(self, siblings: List['StoryIOComponent']) -> None:
        """Update sequential_order for sibling components."""
        for idx, sibling in enumerate(siblings, 1):
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @abstractmethod
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize component from external source (e.g., DrawIO file)."""
        pass
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @abstractmethod
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate a synchronization report."""
        pass
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @abstractmethod
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this component with another."""
        pass
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @abstractmethod
    def render(self) -> Any:
        """Render component to output format (XML, JSON, etc.)."""
        pass
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StoryIOComponent':
        """Create component from dictionary representation."""
        # Subclasses should override this
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless comment: "# Set new parent" - delete it or improve the code instead

            self._parent._remove_child(self)
        
        # Set new parent
        self._parent = value
[X] ERROR - src\synchronizers\story_io\story_io_component.py: Useless comment: "# Update sequential orders" - delete it or improve the code instead

        parent._children.insert(target_index, self)
        
        # Update sequential orders
        self._reorder_siblings(parent._children)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class StoryIODiagram(StoryIOComponent):
    """
    Main diagram class representing a complete story map.
    
    Supports both outline mode (epics/features/stories) and increments mode
    (with marketable releases).
    """
    
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def drawio_file(self) -> Optional[Path]:
        """Get the DrawIO file path."""
        return self._drawio_file
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_graph_file(self) -> Optional[Path]:
        """Get the story graph JSON file path."""
        return self._story_graph_file
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def epics(self) -> List[Epic]:
        """Get all epics in this diagram."""
        return [child for child in self.children if isinstance(child, Epic)]
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def sub_epics(self) -> List[Feature]:
        """Get all sub-epics directly in this diagram (not through epics)."""
        return [child for child in self.children if isinstance(child, Feature)]
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def features(self) -> List[Feature]:
        """Deprecated: Use sub_epics instead."""
        return self.sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def stories(self) -> List[Story]:
        """Get all stories directly in this diagram."""
        return [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def increments(self) -> List[Increment]:
        """Get all increments in this diagram."""
        return [child for child in self.children if isinstance(child, Increment)]
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_any(self, query: str) -> List[StoryIOComponent]:
        """Search for any component matching the query."""
        return self.search_for_all_children(query)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_epics(self, query: str) -> List[Epic]:
        """Search for epics matching the query."""
        results = self.search_for_any(query)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_sub_epics(self, query: str) -> List[Feature]:
        """Search for sub-epics matching the query."""
        results = self.search_for_any(query)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_features(self, query: str) -> List[Feature]:
        """Deprecated: Use search_for_sub_epics instead."""
        return self.search_for_sub_epics(query)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def search_for_stories(self, query: str) -> List[Story]:
        """Search for stories matching the query."""
        results = self.search_for_any(query)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _to_story_graph_format(self, include_increments: bool = False) -> Dict[str, Any]:
        """Convert diagram to story graph JSON format."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _load_from_story_graph_format(self, data: Dict[str, Any]) -> None:
        """Load diagram from story graph JSON format."""
        # Clear existing children
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _create_epic_from_data(self, data: Dict[str, Any]) -> Epic:
        """Create epic from dictionary data."""
        from .story_io_position import Position, Boundary
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _create_feature_from_sub_epic_data(self, data: Dict[str, Any], parent_epic: Epic) -> Feature:
        """Create feature from sub_epic data (new format, supports nested sub_epics)."""
        # Support both story_count (legacy) and estimated_stories (new)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _create_feature_from_data(self, data: Dict[str, Any]) -> Feature:
        """Create feature from dictionary data."""
        # Support both story_count (legacy) and estimated_stories (new)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _create_story_from_data(self, data: Dict[str, Any]) -> Story:
        """Create Story from data dictionary, handling story_type."""
        from .story_io_position import Position
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _create_increment_from_data(self, data: Dict[str, Any]) -> Increment:
        """Create increment from dictionary data."""
        # Preserve priority as-is (can be string like "NOW" or int)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize diagram from external source."""
        if self._drawio_file and self._drawio_file.exists():
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for current diagram state."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this diagram with another."""
        if not isinstance(other, StoryIODiagram):
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render diagram to JSON representation."""
        return self._to_story_graph_format(include_increments=True)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagram to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def save_story_graph(self, output_path: Optional[Union[str, Path]] = None) -> Path:
        """Save diagram as story graph JSON."""
        if output_path is None:
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Create temporary diagram instance just for rendering" - delete it or improve the code instead

        output_path = Path(output_path)
        
        # Create temporary diagram instance just for rendering
        diagram = StoryIODiagram()
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Create renderer and render" - delete it or improve the code instead

                story_graph = json.load(f)
        
        # Create renderer and render
        renderer = DrawIORenderer()
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Create temporary diagram instance just for rendering" - delete it or improve the code instead

        output_path = Path(output_path)
        
        # Create temporary diagram instance just for rendering
        diagram = StoryIODiagram()
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Load into diagram structure" - delete it or improve the code instead

        )
        
        # Load into diagram structure
        self._load_from_story_graph_format(extracted_data)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Load into diagram structure" - delete it or improve the code instead

        )
        
        # Load into diagram structure
        self._load_from_story_graph_format(extracted_data)
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Handle story_groups in sub_epic (new format)" - delete it or improve the code instead

            nested_feature.change_parent(feature)
        
        # Handle story_groups in sub_epic (new format)
        story_groups_data = data.get('story_groups', [])
[X] ERROR - src\synchronizers\story_io\story_io_diagram.py: Useless comment: "# Handle Steps (from structured.json) or steps (from story g" - delete it or improve the code instead

        from .story_io_position import Position
        
        # Handle Steps (from structured.json) or steps (from story graph)
        steps = data.get('Steps', []) or data.get('steps', [])
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class Epic(StoryIOComponent):
    """Represents an epic containing sub-epics and stories."""
    
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def sub_epics(self) -> List[Feature]:
        """Get all sub-epics in this epic."""
        return [child for child in self.children if isinstance(child, Feature)]
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def features(self) -> List[Feature]:
        """Deprecated: Use sub_epics instead."""
        return self.sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def stories(self) -> List[Story]:
        """Get all stories directly in this epic (not through features)."""
        return [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def estimated_stories(self) -> Optional[int]:
        """Get estimated story count if stories are not fully enumerated."""
        return self._estimated_stories
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def total_stories(self) -> int:
        """Get total stories: actual stories + estimated stories from features."""
        actual_stories = len(self.stories)
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def add_sub_epic(self, sub_epic: Feature, target: Optional[Feature] = None) -> None:
        """Add a sub-epic to this epic."""
        if target:
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def remove_sub_epic(self, sub_epic: Feature) -> None:
        """Remove a sub-epic from this epic."""
        if sub_epic in self.sub_epics:
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def add_feature(self, feature: Feature, target: Optional[Feature] = None) -> None:
        """Deprecated: Use add_sub_epic instead."""
        self.add_sub_epic(feature, target)
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def remove_feature(self, feature: Feature) -> None:
        """Deprecated: Use remove_sub_epic instead."""
        self.remove_sub_epic(feature)
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize epic from external source (new format: sub_epics)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for this epic."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this epic with another component."""
        if not isinstance(other, Epic):
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render epic to JSON representation (new format: sub_epics)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_epic.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert epic to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class Feature(StoryIOComponent):
    """Represents a sub-epic containing stories."""
    
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def stories(self) -> List[Story]:
        """Get all stories in this sub-epic."""
        return [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_count(self) -> Optional[int]:
        """Get estimated story count if stories are not fully enumerated."""
        return self._story_count
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def estimated_stories(self) -> Optional[int]:
        """Get estimated story count (alias for story_count)."""
        return self._story_count
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def total_stories(self) -> int:
        """Get total stories: actual stories + estimated stories."""
        actual_stories = len(self.stories)
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize sub-epic from external source."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_as_sub_epic(self) -> Dict[str, Any]:
        """Synchronize sub-epic as sub_epic (new format: supports nested sub_epics)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for this sub-epic."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this sub-epic with another component."""
        if not isinstance(other, Feature):
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render sub-epic to JSON representation."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render_as_sub_epic(self) -> Dict[str, Any]:
        """Render sub-epic as sub_epic (new format: supports nested sub_epics)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def sub_epics(self) -> List['Feature']:
        """Get nested sub-epics."""
        return [child for child in self.children if isinstance(child, Feature)]
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def features(self) -> List['Feature']:
        """Deprecated: Use sub_epics instead."""
        return self.sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_feature.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sub-epic to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class Increment(StoryIOComponent):
    """Represents an increment containing epics, sub-epics, and stories."""
    
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _priority_to_int(priority: Union[int, str]) -> int:
        """Convert priority to integer for ordering."""
        if isinstance(priority, str):
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def priority(self) -> Union[int, str]:
        """Get the priority of this increment (original value, can be int or string like 'NOW')."""
        return self._priority_value
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def priority_int(self) -> int:
        """Get the numeric priority value for ordering."""
        return self._priority_int
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def epics(self) -> List[Epic]:
        """Get all epics in this increment."""
        return [child for child in self.children if isinstance(child, Epic)]
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def sub_epics(self) -> List[Feature]:
        """Get all sub-epics directly in this increment (not through epics)."""
        return [child for child in self.children if isinstance(child, Feature)]
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def features(self) -> List[Feature]:
        """Deprecated: Use sub_epics instead."""
        return self.sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def stories(self) -> List[Story]:
        """Get all stories directly in this increment (not through epics/sub-epics)."""
        return [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_names(self) -> List[str]:
        """Get story names referenced by this increment (for JSON format)."""
        return self._story_names if hasattr(self, '_story_names') else []
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @story_names.setter
    def story_names(self, names: List[str]) -> None:
        """Set story names referenced by this increment (for JSON format)."""
        self._story_names = names
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def add_story(self, story: Story) -> None:
        """
        Add a story to this increment.
        Pushes down other stories and increases increment height if needed.
        Handles user placement if story has different users than previous stories.
        """
        # Calculate position below existing stories
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize increment from external source."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for this increment."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this increment with another component."""
        if not isinstance(other, Increment):
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render increment to JSON representation."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_increment.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert increment to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_io_mcp_server.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def main():
    """Main entry point for MCP server."""
    if not mcp:
[X] ERROR - src\synchronizers\story_io\story_io_mcp_server.py: Useless comment: "# Load from DrawIO (sync from diagram)" - delete it or improve the code instead

    """Load diagram from file path."""
    if drawio_path:
        # Load from DrawIO (sync from diagram)
        return StoryIODiagram.sync_from_drawio(Path(drawio_path))
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass(frozen=True)
class Position:
    """Represents a 2D position with x and y coordinates."""
    
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __add__(self, other: 'Position') -> 'Position':
        """Add two positions component-wise."""
        return Position(self.x + other.x, self.y + other.y)
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def __sub__(self, other: 'Position') -> 'Position':
        """Subtract two positions component-wise."""
        return Position(self.x - other.x, self.y - other.y)
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        dx = self.x - other.x
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def is_within_tolerance(self, other: 'Position', tolerance: float) -> bool:
        """Check if this position is within tolerance of another."""
        return self.distance_to(other) <= tolerance
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

@dataclass(frozen=True)
class Boundary:
    """Represents a rectangular boundary with position and dimensions."""
    
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def position(self) -> Position:
        """Get the top-left position of this boundary."""
        return Position(self.x, self.y)
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def center(self) -> Position:
        """Get the center position of this boundary."""
        return Position(self.x + self.width / 2, self.y + self.height / 2)
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def right(self) -> float:
        """Get the right edge x coordinate."""
        return self.x + self.width
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def bottom(self) -> float:
        """Get the bottom edge y coordinate."""
        return self.y + self.height
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def contains_position(self, pos: Position) -> bool:
        """Check if a position is within this boundary."""
        return (self.x <= pos.x <= self.right and
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def contains_boundary(self, other: 'Boundary') -> bool:
        """Check if another boundary is fully contained within this one."""
        return (self.x <= other.x and
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def overlaps(self, other: 'Boundary') -> bool:
        """Check if this boundary overlaps with another."""
        return not (self.right < other.x or
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def expand(self, padding: float) -> 'Boundary':
        """Create a new boundary expanded by padding on all sides."""
        return Boundary(
[X] ERROR - src\synchronizers\story_io\story_io_position.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def union(self, other: 'Boundary') -> 'Boundary':
        """Create a boundary that contains both this and another boundary."""
        min_x = min(self.x, other.x)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DrawIORenderer:
    """
    Renderer for converting story diagrams to DrawIO XML format.
    
    Handles both outline mode (epics/sub-epics/stories) and increments mode.
    """
    
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _get_story_style(story: Dict[str, Any]) -> str:
        """
        Get DrawIO style for story based on story_type.
        
        - user (default): yellow fill (#fff2cc)
        - system: dark blue fill (#1a237e), white text
        - technical: black fill (#000000), white text
        """
        story_type = story.get('story_type', 'user')
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _calculate_total_stories_for_epic_in_increment(epic: Dict[str, Any]) -> int:
        """
        Calculate total stories for an epic within an increment scope.
        Counts only stories in story_groups within sub_epics (no direct stories on epics or sub_epics).
        """
        # Helper to get sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _calculate_total_stories_for_feature_in_increment(feature: Dict[str, Any]) -> int:
        """
        Calculate total stories for a sub-epic within an increment scope.
        Counts only stories in story_groups (no direct stories on sub-epics).
        """
        story_groups = feature.get('story_groups', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _find_story_path(story_name: str, epics: List[Dict[str, Any]]) -> tuple:
        """
        Find the epic and sub_epic path for a story by name.
        Returns (epic_name, sub_epic_name) or (None, None) if not found.
        """
        def get_sub_epics(epic):
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _traverse_all_stories(story: Dict[str, Any], collected: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Simple algorithm to collect a story (no nested stories - stories are flat).
        Legacy method kept for compatibility but no longer traverses nested stories.
        
        Args:
            story: Story dictionary
            collected: List to collect stories
        
        Returns:
            List containing only the story (no nested traversal)
        """
        if collected is None:
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def _get_story_count_display_html(count: int, position: str = 'bottom') -> str:
        """
        Get HTML for displaying story count.
        
        Args:
            count: Story count to display
            position: 'bottom' (default, below name) or 'top-right' (absolute positioned in top right)
        """
        if position == 'top-right':
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _calculate_text_width(self, text: str, font_size: int = 8, padding: int = 10) -> int:
        """
        Calculate approximate width needed for text at given font size.
        Accounts for word wrapping - uses max characters per line (typically 30-40 chars).
        
        Args:
            text: Text content (HTML will be stripped)
            font_size: Font size in pixels
            padding: Additional padding (left + right)
        
        Returns:
            Width in pixels
        """
        import re
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _format_steps_as_acceptance_criteria(self, steps: List[Union[str, dict]], step_idx: int) -> Tuple[str, int]:
        """
        Format steps as acceptance criteria text for display.
        Each AC entry gets its own box: Box 0 = first entry, Box 1 = second entry
        
        Args:
            steps: List of acceptance criteria (dictionaries with 'description', or strings)
            step_idx: Index of the current box (0 = first box, 1 = second box)
        
        Returns:
            Tuple of (HTML formatted text, calculated width)
        """
        if step_idx < len(steps):
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

        # Recursively count all sub_epics at all nesting levels
        def count_all_sub_epics(epic_or_sub_epic):
            """Recursively count all sub_epics, including nested ones."""
            count = 0
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _generate_exploration_diagram(self, story_graph: Dict[str, Any], layout_data: Dict[str, Dict[str, float]], root_elem: ET.Element, root: ET.Element) -> str:
        """
        Generate DrawIO XML for exploration mode (acceptance criteria below stories).
        This is a clean, separate implementation that doesn't intermingle with non-exploration logic.
        
        Args:
            story_graph: Story graph JSON data
            layout_data: Optional layout data with story coordinates
            root_elem: Root XML element for the diagram
            root: Root XML element for the file
        
        Returns:
            XML string for the DrawIO file
        """
        # Helper to get sub_epics
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _generate_diagram(self, story_graph: Dict[str, Any], layout_data: Dict[str, Dict[str, float]] = None, is_increments: bool = False, is_exploration: bool = False) -> str:
        """
        Generate DrawIO XML from story graph.
        
        Args:
            story_graph: Story graph JSON data
            layout_data: Optional layout data with story coordinates (key: "epic_name|sub_epic_name|story_name")
            is_increments: If True, render in increments mode (story counts in top right for epics/sub-epics)
            is_exploration: If True, render in exploration mode (acceptance criteria below stories)
        """
        if layout_data is None:
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

        # Helper to normalize story_groups (supports legacy 'stories' format)
        def normalize_story_groups(feature_or_sub_epic):
            """Convert legacy 'stories' format to 'story_groups' format if needed."""
            story_groups = feature_or_sub_epic.get('story_groups', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

            # Helper function to recursively collect nested sub-epics with story_groups, maintaining order
            def collect_nested_with_stories(sub_epics, collected):
                """Recursively collect all nested sub-epics that have story_groups, in order"""
                # Sort by sequential_order to maintain order
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _generate_increments_diagram(self, story_graph: Dict[str, Any], layout_data: Dict[str, Any], root_elem: ET.Element, xml_root: ET.Element) -> str:
        """
        Generate DrawIO XML for increments mode.
        Uses exact outline rendering code.
        """
        # Set flags for outline code
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

        # Helper to normalize story_groups (supports legacy 'stories' format)
        def normalize_story_groups(feature_or_sub_epic):
            """Convert legacy 'stories' format to 'story_groups' format if needed."""
            story_groups = feature_or_sub_epic.get('story_groups', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

            # Helper function to recursively collect nested sub-epics with story_groups, maintaining order
            def collect_nested_with_stories(sub_epics, collected):
                """Recursively collect all nested sub-epics that have story_groups, in order"""
                # Sort by sequential_order to maintain order
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create epic group" - delete it or improve the code instead

            return filtered
        
        # Create epic group
        epic_group = ET.SubElement(root_elem, 'mxCell', id='epic-group', value='', 
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get filtered story groups (already filtered to only those " - delete it or improve the code instead

            for feat_idx, feature in enumerate(filtered_features, 1):
                feature_x = current_feature_x  # Each feature gets its own x position
                # Get filtered story groups (already filtered to only those with AC in filtered_features)
                story_groups = feature.get('story_groups', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update rightmost AC position for this story's AC boxes" - delete it or improve the code instead

                                    ac_y = acceptance_criteria_y + ac_box_idx * self.ACCEPTANCE_CRITERIA_SPACING_Y
                                
                                # Update rightmost AC position for this story's AC boxes
                                current_ac_rightmost_x = max(current_ac_rightmost_x or 0, ac_x + ac_width)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update group x to align with leftmost story" - delete it or improve the code instead

                            group_geom = group_cell.find('mxGeometry')
                            if group_geom is not None:
                                # Update group x to align with leftmost story
                                group_geom.set('x', str(feature_min_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update group width to match feature width" - delete it or improve the code instead

                                # Update group x to align with leftmost story
                                group_geom.set('x', str(feature_min_x))
                                # Update group width to match feature width
                                group_geom.set('width', str(actual_feature_width + 5))  # +5 for padding
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update epic bounds" - delete it or improve the code instead

                    feature_max_x = feature_min_x + actual_feature_width
                
                # Update epic bounds
                epic_max_x = max(epic_max_x, feature_max_x)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update current_group_x for next feature" - delete it or improve the code instead

                feature_x = feature_max_x + self.FEATURE_SPACING_X
                
                # Update current_group_x for next feature
                current_group_x = feature_x + 2
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get story_groups (supports legacy 'stories' format)" - delete it or improve the code instead

                    use_feature_layout = False
                
                # Get story_groups (supports legacy 'stories' format)
                story_groups = normalize_story_groups(feature)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Process story groups - flatten stories from all groups" - delete it or improve the code instead

                story_groups = normalize_story_groups(feature)
                
                # Process story groups - flatten stories from all groups
                stories = []
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feat_x to use actual position for story rendering" - delete it or improve the code instead

                    feature_geom.set('as', 'geometry')
                
                # Update feat_x to use actual position for story rendering
                feat_x = actual_feat_x
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create a copy of the group with filtered stories" - delete it or improve the code instead

                            # Only include group if it has stories with AC
                            if filtered_group_stories:
                                # Create a copy of the group with filtered stories
                                filtered_group = group.copy()
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update group bottom Y (track the bottommost story in this " - delete it or improve the code instead

                            story_idx += 1
                            
                            # Update group bottom Y (track the bottommost story in this group)
                            group_bottom_y = max(group_bottom_y, story_y + self.STORY_HEIGHT)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update actual feature bottom (for nested sub-epic position" - delete it or improve the code instead

                            feature_bottom_y[feat_idx] = max(feature_bottom_y[feat_idx], group_bottom_y + 20)
                        
                        # Update actual feature bottom (for nested sub-epic positioning)
                        # This tracks the bottommost story group - group_bottom_y already includes story height
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create grey background rectangle element" - delete it or improve the code instead

                            rect_height = max_y - min_y
                            
                            # Create grey background rectangle element
                            bg_rect = ET.Element('mxCell',
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feature geometry position and width" - delete it or improve the code instead

                                actual_feature_width = actual_feature_rightmost - feat_x
                            
                            # Update feature geometry position and width
                            feature_geom.set('x', str(feature_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feat_data so next iteration uses correct position" - delete it or improve the code instead

                        else:
                            actual_feature_rightmost = feat_x + actual_feature_width
                        # Update feat_data so next iteration uses correct position
                        feat_data['x'] = feature_x if feature_min_x < float('inf') else feat_x
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update current_feature_x for next feature (used in first l" - delete it or improve the code instead

                        feat_data['x'] = feature_x if feature_min_x < float('inf') else feat_x
                        feat_data['width'] = actual_feature_width  # Update width
                        # Update current_feature_x for next feature (used in first loop for next epic)
                        next_feature_x = actual_feature_rightmost + self.FEATURE_SPACING_X
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update next feature's X position in feature_positions" - delete it or improve the code instead

                        current_feature_x = next_feature_x
                        
                        # Update next feature's X position in feature_positions
                        # feat_idx is 1-based, so next feature is at index feat_idx in the list (0-based)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update next feature's X position in feat_data" - delete it or improve the code instead

                            next_feat_data = feature_positions[feat_idx]
                            if not next_feat_data.get('use_layout', False):
                                # Update next feature's X position in feat_data
                                # This will be used when we render that feature (it checks feat_data.get('x'))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create acceptance criteria box (rectangle, not square)" - delete it or improve the code instead

                                        ac_y = acceptance_criteria_y + ac_box_idx * self.ACCEPTANCE_CRITERIA_SPACING_Y
                                    
                                    # Create acceptance criteria box (rectangle, not square)
                                    ac_cell = ET.SubElement(root_elem, 'mxCell',
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x for next feature posit" - delete it or improve the code instead

                    epic_min_x = min(epic_min_x, feat_x)
                    epic_max_x = max(epic_max_x, feat_x + feat_width)
                    # Update previous_feature_rightmost_x for next feature positioning
                    feature_rightmost = feat_x + feat_width
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x with actual rightmost " - delete it or improve the code instead

                    feature_geometries[-1]['geom'].set('x', str(actual_feature_x))
                    
                    # Update previous_feature_rightmost_x with actual rightmost position (including AC cards)
                    # This will be used to position the next feature
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x for next feature posit" - delete it or improve the code instead

                    epic_min_x = min(epic_min_x, feat_x)
                    epic_max_x = max(epic_max_x, feat_x + feat_width)
                    # Update previous_feature_rightmost_x for next feature positioning
                    feature_rightmost = feat_x + feat_width
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update x_pos for next epic using stored epic width" - delete it or improve the code instead

            if use_epic_layout:
                # Use stored epic coordinates and dimensions - don't shrink
                # Update x_pos for next epic using stored epic width
                # In exploration mode, use 30px spacing between epics to match expected layout
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update x_pos for next epic using actual epic width" - delete it or improve the code instead

                # If epic is in a group (parent is like "101", "102"), don't set x - it's relative to group
                
                # Update x_pos for next epic using actual epic width
                # In exploration mode, use 30px spacing between epics to match expected layout
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get index of epic-group" - delete it or improve the code instead

            epic_group_elem = root_elem.find(".//mxCell[@id='epic-group']")
            if epic_group_elem is not None:
                # Get index of epic-group
                epic_group_index = list(root_elem).index(epic_group_elem)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get all epics and features to build mapping from cell IDs " - delete it or improve the code instead

            story_cells_to_move = []  # List of (cell, story_x, story_data, increment_indices, story_key, group_connector)
            
            # Get all epics and features to build mapping from cell IDs to story keys
            all_epics = story_graph.get('epics', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get group connector type (for flattening "or" groups in pr" - delete it or improve the code instead

                                                    story_data = increment_stories_map.get(story_key)
                                                    increment_indices = story_to_increments[story_key]
                                                    # Get group connector type (for flattening "or" groups in priority mode)
                                                    group_connector = story_to_group_connector.get(story_key)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create unique ID by including story name to avoid duplicat" - delete it or improve the code instead

                    current_story_y = story_y_positions[position_key]
                    
                    # Create unique ID by including story name to avoid duplicates
                    safe_story_name = story_data['name'].replace(' ', '_').replace('|', '_')
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update position and width" - delete it or improve the code instead

                        new_width = feature_widths[key]

                        # Update position and width
                        geom.set('x', str(current_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update user/actor cell positions to be directly below thei" - delete it or improve the code instead

                        current_x = current_x + new_width + feature_spacing
            
            # Update user/actor cell positions to be directly below their features
            # Collect all users per feature (deduplicate by user name)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update story positions to align with repositioned features" - delete it or improve the code instead

                            user_geom.set('y', str(user_y))
            
            # Update story positions to align with repositioned features
            # Build mapping of (epic_name, feature_name) -> new feature x position
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update background rectangles to align with repositioned fe" - delete it or improve the code instead

                    story_cell_geometries[position_key].set('x', str(new_story_x))
            
            # Update background rectangles to align with repositioned features
            # Map stories to their features
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get feature from first story (all stories in a bg should b" - delete it or improve the code instead

                        # Determine feature from stories in this background
                        if stories_in_bg:
                            # Get feature from first story (all stories in a bg should be from same feature)
                            first_story = stories_in_bg[0]
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update first background to match feature" - delete it or improve the code instead

                    for idx, (bg_cell, bg_geom) in enumerate(bg_cells):
                        if idx == 0:
                            # Update first background to match feature
                            bg_geom.set('x', str(feat_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Set flags for outline code" - delete it or improve the code instead

        Uses exact outline rendering code.
        """
        # Set flags for outline code
        is_increments = True
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get story_groups (supports legacy 'stories' format)" - delete it or improve the code instead

                    use_feature_layout = False
                
                # Get story_groups (supports legacy 'stories' format)
                story_groups = normalize_story_groups(feature)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Process story groups - flatten stories from all groups" - delete it or improve the code instead

                story_groups = normalize_story_groups(feature)
                
                # Process story groups - flatten stories from all groups
                stories = []
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feat_x to use actual position for story rendering" - delete it or improve the code instead

                    feature_geom.set('as', 'geometry')
                
                # Update feat_x to use actual position for story rendering
                feat_x = actual_feat_x
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create a copy of the group with filtered stories" - delete it or improve the code instead

                            # Only include group if it has stories with AC
                            if filtered_group_stories:
                                # Create a copy of the group with filtered stories
                                filtered_group = group.copy()
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update group bottom Y (track the bottommost story in this " - delete it or improve the code instead

                            story_idx += 1
                            
                            # Update group bottom Y (track the bottommost story in this group)
                            group_bottom_y = max(group_bottom_y, story_y + self.STORY_HEIGHT)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update actual feature bottom (for nested sub-epic position" - delete it or improve the code instead

                            feature_bottom_y[feat_idx] = max(feature_bottom_y[feat_idx], group_bottom_y + 20)
                        
                        # Update actual feature bottom (for nested sub-epic positioning)
                        # This tracks the bottommost story group - group_bottom_y already includes story height
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create grey background rectangle element" - delete it or improve the code instead

                            rect_height = max_y - min_y
                            
                            # Create grey background rectangle element
                            bg_rect = ET.Element('mxCell',
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feature geometry position and width" - delete it or improve the code instead

                                actual_feature_width = actual_feature_rightmost - feat_x
                            
                            # Update feature geometry position and width
                            feature_geom.set('x', str(feature_x))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update feat_data so next iteration uses correct position" - delete it or improve the code instead

                        else:
                            actual_feature_rightmost = feat_x + actual_feature_width
                        # Update feat_data so next iteration uses correct position
                        feat_data['x'] = feature_x if feature_min_x < float('inf') else feat_x
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update current_feature_x for next feature (used in first l" - delete it or improve the code instead

                        feat_data['x'] = feature_x if feature_min_x < float('inf') else feat_x
                        feat_data['width'] = actual_feature_width  # Update width
                        # Update current_feature_x for next feature (used in first loop for next epic)
                        next_feature_x = actual_feature_rightmost + self.FEATURE_SPACING_X
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update next feature's X position in feature_positions" - delete it or improve the code instead

                        current_feature_x = next_feature_x
                        
                        # Update next feature's X position in feature_positions
                        # feat_idx is 1-based, so next feature is at index feat_idx in the list (0-based)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update next feature's X position in feat_data" - delete it or improve the code instead

                            next_feat_data = feature_positions[feat_idx]
                            if not next_feat_data.get('use_layout', False):
                                # Update next feature's X position in feat_data
                                # This will be used when we render that feature (it checks feat_data.get('x'))
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create acceptance criteria box (rectangle, not square)" - delete it or improve the code instead

                                        ac_y = acceptance_criteria_y + ac_box_idx * self.ACCEPTANCE_CRITERIA_SPACING_Y
                                    
                                    # Create acceptance criteria box (rectangle, not square)
                                    ac_cell = ET.SubElement(root_elem, 'mxCell',
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x for next feature posit" - delete it or improve the code instead

                    epic_min_x = min(epic_min_x, feat_x)
                    epic_max_x = max(epic_max_x, feat_x + feat_width)
                    # Update previous_feature_rightmost_x for next feature positioning
                    feature_rightmost = feat_x + feat_width
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x with actual rightmost " - delete it or improve the code instead

                    feature_geometries[-1]['geom'].set('x', str(actual_feature_x))
                    
                    # Update previous_feature_rightmost_x with actual rightmost position (including AC cards)
                    # This will be used to position the next feature
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update previous_feature_rightmost_x for next feature posit" - delete it or improve the code instead

                    epic_min_x = min(epic_min_x, feat_x)
                    epic_max_x = max(epic_max_x, feat_x + feat_width)
                    # Update previous_feature_rightmost_x for next feature positioning
                    feature_rightmost = feat_x + feat_width
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update x_pos for next epic using stored epic width" - delete it or improve the code instead

            if use_epic_layout:
                # Use stored epic coordinates and dimensions - don't shrink
                # Update x_pos for next epic using stored epic width
                # In exploration mode, use 30px spacing between epics to match expected layout
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Update x_pos for next epic using actual epic width" - delete it or improve the code instead

                # If epic is in a group (parent is like "101", "102"), don't set x - it's relative to group
                
                # Update x_pos for next epic using actual epic width
                # In exploration mode, use 30px spacing between epics to match expected layout
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get index of epic-group" - delete it or improve the code instead

            epic_group_elem = root_elem.find(".//mxCell[@id='epic-group']")
            if epic_group_elem is not None:
                # Get index of epic-group
                epic_group_index = list(root_elem).index(epic_group_elem)
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Handle both 'stories' and 'story_groups' formats" - delete it or improve the code instead

                    feature_name = feature['name']
                    
                    # Handle both 'stories' and 'story_groups' formats
                    stories_list = []
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Get all epics and features to build mapping from cell IDs " - delete it or improve the code instead

        story_cells_to_move = []  # List of (cell, story_x, story_data, increment_indices)
        
        # Get all epics and features to build mapping from cell IDs to story keys
        all_epics = story_graph.get('epics', [])
[X] ERROR - src\synchronizers\story_io\story_io_renderer.py: Useless comment: "# Create unique ID by including story name to avoid duplicat" - delete it or improve the code instead

                current_story_x = story_x_positions[position_key]
                
                # Create unique ID by including story name to avoid duplicates
                safe_story_name = story_data['name'].replace(' ', '_').replace('|', '_')
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class Story(StoryIOComponent):
    """Represents a story with associated users."""
    
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def users(self) -> List[str]:
        """Get list of user names associated with this story."""
        return list(self._user_names)
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def user_components(self) -> List['User']:
        """Get user component objects associated with this story."""
        from .story_io_user import User
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def steps(self) -> List[Dict[str, Any]]:
        """Get acceptance criteria steps for this story."""
        return list(self._steps)
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def vertical_order(self) -> Optional[int]:
        """Get vertical ordering for stacked stories."""
        return self._vertical_order
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def story_type(self) -> str:
        """Get story type: 'user' (default), 'system', or 'technical'."""
        return self._story_type or 'user'
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def make_optional_to(self, target: 'Story') -> None:
        """
        Move this story below target story (for optional/alternative stories).
        Sets sequential_order to be a decimal of target's order.
        """
        if target.sequential_order is None:
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def add_user(self, user: str) -> None:
        """
        Add a user to this story.
        Places user above story and pushes stories and users below down.
        """
        if user not in self._user_names:
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def remove_user(self, user: str) -> None:
        """Remove a user from this story."""
        if user in self._user_names:
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def flag_story(self) -> None:
        """Flag this story (changes color in rendering)."""
        self.flag = True
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def unflag_story(self) -> None:
        """Unflag this story."""
        self.flag = False
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize story from external source (new format: acceptance_criteria, connector, nested stories)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for this story."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this story with another component."""
        if not isinstance(other, Story):
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render story to JSON representation (new format: acceptance_criteria, connector, nested stories)."""
        result = {
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert story to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless comment: "# Handle nested stories (new format)" - delete it or improve the code instead

            result['acceptance_criteria'] = []
        
        # Handle nested stories (new format)
        nested_stories = [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_story.py: Useless comment: "# Handle nested stories (new format)" - delete it or improve the code instead

            result['acceptance_criteria'] = []
        
        # Handle nested stories (new format)
        nested_stories = [child for child in self.children if isinstance(child, Story)]
[X] ERROR - src\synchronizers\story_io\story_io_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DrawIOSynchronizer:
    """Synchronizer for extracting story diagrams from DrawIO XML format."""
    
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class User(StoryIOComponent):
    """Represents a user associated with stories."""
    
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @property
    def stories(self) -> List['Story']:
        """Get all stories associated with this user."""
        from .story_io_story import Story
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def add_story(self, story: 'Story') -> None:
        """
        Add a story to this user.
        Same as story.add_user(user) - creates bidirectional relationship.
        """
        if story not in self._story_refs:
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def remove_story(self, story: 'Story') -> None:
        """Remove a story from this user."""
        if story in self._story_refs:
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize(self) -> Dict[str, Any]:
        """Synchronize user from external source."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def synchronize_report(self) -> Dict[str, Any]:
        """Generate synchronization report for this user."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def compare(self, other: 'StoryIOComponent') -> Dict[str, Any]:
        """Compare this user with another component."""
        if not isinstance(other, User):
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def render(self) -> Dict[str, Any]:
        """Render user to JSON representation."""
        return {
[X] ERROR - src\synchronizers\story_io\story_io_user.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        result = super().to_dict()
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_cell_value(cell) -> str:
    """Extract text value from a cell, handling HTML entities."""
    value = cell.get('value', '')
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_step_from_acceptance_criteria(ac_text: str) -> str:
    """
    Extract step text from acceptance criteria box.
    Handles "When ... Then ..." format, HTML formatting, and plain text.
    
    Args:
        ac_text: Text from acceptance criteria box (may contain HTML)
    
    Returns:
        Step text (description) - cleaned and formatted
    """
    if not ac_text:
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_story_count_from_value(cell) -> Optional[int]:
    """
    Extract story count/estimated_stories from cell HTML value.
    Checks both bottom position (outline mode) and top-right position (increments mode).
    """
    raw_value = cell.get('value', '')
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_story_type_from_style(style: str) -> str:
    """
    Extract story_type from DrawIO cell style based on fillColor.
    
    Returns:
        'user' (default), 'system', or 'technical'
    """
    if 'fillColor=#1a237e' in style:  # Dark blue - system story
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_geometry(cell) -> Optional[Dict[str, float]]:
    """Extract geometry information from a cell."""
    geom = cell.find('mxGeometry')
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_increments_and_boundaries(drawio_path: Path) -> List[Dict[str, Any]]:
    """
    Get all increment squares (white squares on the left) and their boundaries.
    
    Returns:
        List of increment dictionaries with id, name, x, y, width, height
    """
    tree = ET.parse(drawio_path)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_epics_features_and_boundaries(drawio_path: Path) -> Dict[str, Any]:
    """
    Get all epics and sub_epics with their boundaries (x, y, width, height).
    
    Returns:
        Dictionary with 'epics' and 'sub_epics' lists
    """
    tree = ET.parse(drawio_path)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _assign_sequential_order(all_stories: List[Dict]):
    """
    Assign sequential_order to stories based on left-to-right position.
    When a story is below another story (higher Y), use num.num format.
    Sequential order is global across all stories in the map.
    """
    # Sort all stories by X position (left to right), then by Y position (top to bottom)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

            # Recursively process sub_epics
            def process_sub_epic(sub_epic):
                """Recursively process sub_epic and return sub_epic with matching stories"""
                collected_stories = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    # Final cleanup: recursively remove empty sub_epics (no stories, no nested sub_epics)
    def cleanup_empty_sub_epics(sub_epics_list):
        """Recursively remove empty sub_epics"""
        cleaned = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _display_large_deletions(deletions: Dict[str, Any]) -> None:
    """Display large deletion warnings in a prominent format."""
    has_warnings = False
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _flatten_stories_from_original(original_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten all stories from original story graph into a list with context."""
    stories = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def _flatten_stories_from_extracted(extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten all stories from extracted story graph into a list with context."""
    stories = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    # Increments use direct stories arrays (no story_groups)
    def merge_sub_epic_stories(sub_epic, epic_name, sub_epic_name):
        """Recursively merge stories in sub_epic (handles both story_groups and direct stories)"""
        # Handle story_groups format (epics section)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def display_merge_report(report: Dict[str, Any]) -> None:
    """Display merge report in a human-readable format."""
    print("\n" + "="*80)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def is_exploration_mode(drawio_path: Path) -> bool:
    """
    Detect if DrawIO file is in exploration mode (has acceptance criteria boxes).
    
    Args:
        drawio_path: Path to DrawIO file
        
    Returns:
        True if exploration mode (has AC boxes), False otherwise
    """
    try:
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def generate_extract_report(data: Dict[str, Any], output_path: Optional[Path] = None) -> str:
    """
    Generate a plain English report of what was extracted from DrawIO.
    
    Args:
        data: The extracted story graph data
        output_path: Optional path to write the report to
        
    Returns:
        Plain English report as a string
    """
    lines = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Get all user cells that aren't already matched by ID" - delete it or improve the code instead

    y_tolerance = 50  # pixels - for checking if users are at same row level
    
    # Get all user cells that aren't already matched by ID
    unmatched_users = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Get stories for this sub_epic - only stories that belong t" - delete it or improve the code instead

            return sub_epic_data  # Return without processing stories
        
        # Get stories for this sub_epic - only stories that belong to this sub-epic
        # and are NOT contained within any child sub-epic
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Get stories for this sub_epic, sorted by sequential_order" - delete it or improve the code instead

                stories_for_this_sub_epic.append(story)
        
        # Get stories for this sub_epic, sorted by sequential_order
        feat_stories = stories_for_this_sub_epic
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create a default group for ungrouped top-level stories" - delete it or improve the code instead

            # Sort ungrouped stories by Y, then X
            ungrouped_stories.sort(key=lambda s: (s['y'], s['x']))
            # Create a default group for ungrouped top-level stories
            default_group_id = 'ungrouped'
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Process stories row by row" - delete it or improve the code instead

        first_row_y = sorted_rows[0][0] if sorted_rows else None
        
        # Process stories row by row
        # No nested stories - all stories are flat within story groups
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Return the completed sub_epic_data with nested sub_epics a" - delete it or improve the code instead

            del sub_epic_data['temp_stories']
        
        # Return the completed sub_epic_data with nested sub_epics and story_groups
        return sub_epic_data
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Get top-level sub-epics for this epic (sub-epics without a" - delete it or improve the code instead

        }
        
        # Get top-level sub-epics for this epic (sub-epics without a parent sub-epic)
        epic_sub_epics = sorted([f for f in sub_epics 
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create key: epic_name|sub_epic_name|story_name" - delete it or improve the code instead

        # Store story coordinates
        for story in all_stories:
            # Create key: epic_name|sub_epic_name|story_name
            epic = next((e for e in sorted_epics if e['epic_num'] == story['epic_num']), None)
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create new X group" - delete it or improve the code instead

        
        if not found_group:
            # Create new X group
            stories_by_x_group[story_x] = [story]
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Process all sub_epics in this epic" - delete it or improve the code instead

                return None
            
            # Process all sub_epics in this epic
            epic_sub_epics_with_stories = []
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create maps for matches: key -> extracted story and origin" - delete it or improve the code instead

        report = json.load(f)
    
    # Create maps for matches: key -> extracted story and original story
    # This allows us to update original stories with extracted data
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create a map of extracted stories by key for updating" - delete it or improve the code instead

    
    # Also need to get the actual extracted story objects (not just flattened data)
    # Create a map of extracted stories by key for updating
    extracted_full_story_map = {}
[X] ERROR - src\synchronizers\story_io\story_map_drawio_synchronizer.py: Useless comment: "# Create a map of existing increment names for quick lookup" - delete it or improve the code instead

    
    if 'increments' in extracted_data:
        # Create a map of existing increment names for quick lookup
        existing_increment_names = {inc.get('name') for inc in merged_data['increments']}
[X] ERROR - src\synchronizers\story_io\test_increment_full_cycle.py: Useless comment: "# Load story graph" - delete it or improve the code instead

from .story_io_diagram import StoryIODiagram

# Load story graph
story_graph_path = Path("demo/mm3e_animations/docs/story_graph.json")
[X] ERROR - src\synchronizers\story_io\test_increment_priority.py: Useless comment: "# Load story graph with increments" - delete it or improve the code instead

from .story_io_diagram import StoryIODiagram

# Load story graph with increments
story_graph_path = Path("demo/mm3e_animations/docs/story_graph.json")
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def create_scenario_anchor(scenario_name: str) -> str:
    """Create a markdown anchor ID from scenario name."""
    # Normalize for markdown anchor: lowercase, replace spaces/special chars with hyphens
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_acceptance_criteria(ac_list):
    """Format acceptance criteria list into markdown"""
    if not ac_list:
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_common_background(scenarios_list):
    """Extract common background steps shared across all scenarios"""
    if not scenarios_list:
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_scenarios(scenarios_list, common_background=None, story_test_file='', workspace_directory=None, story_file_path=None):
    """Format scenarios list into markdown"""
    if not scenarios_list:
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def build_folder_path_from_graph(epic_name, sub_epic_name, story_graph_data):
    """
    Build folder path dynamically from story graph structure.
    Traverses the graph to find the actual epic and sub_epic names.
    Uses emoji monikers: 🎯 for Epic, ⚙️ for Sub-Epic.
    Handles nested sub-epics by building full folder path.
    """
    # Find the epic in the graph
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def create_story_content(story, epic_name, sub_epic_name, workspace_directory, story_file_path=None):
    """Create markdown content for a story. sub_epic_name is the sub-epic name."""
    """Create markdown content for a story"""
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_stories_from_graph(epic, epic_path="", sub_epic_path="", parent_is_epic=True, parent_test_file=""):
    """
    Extract all stories from story graph recursively.
    Dynamically builds folder structure from the graph itself.
    Handles nested sub-epics (sub-subs) by building up the full path.
    Passes test_file from sub-epic level down to stories.
    """
    stories = []
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class StoryScenariosSynchronizer:
    """Synchronizer for rendering story markdown files from story graph JSON."""
    
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Get backgrounds from all scenarios" - delete it or improve the code instead

        return None
    
    # Get backgrounds from all scenarios
    backgrounds = [s.get('background', []) for s in scenarios_list if s.get('background')]
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Create anchor ID for scenario (normalized to match markdow" - delete it or improve the code instead

                )

        # Create anchor ID for scenario (normalized to match markdown auto-generated anchors)
        scenario_anchor = create_scenario_anchor(name)
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Get common background from all scenarios" - delete it or improve the code instead

    all_scenarios = scenarios_list + scenario_outlines_list
    
    # Get common background from all scenarios
    common_background = get_common_background(all_scenarios)
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Get test_file from this level (sub-epic) or inherit from p" - delete it or improve the code instead

    current_is_epic = parent_is_epic and not sub_epic_path
    
    # Get test_file from this level (sub-epic) or inherit from parent
    current_test_file = epic.get('test_file', '') or parent_test_file
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Get stories from story_groups" - delete it or improve the code instead

    current_test_file = epic.get('test_file', '') or parent_test_file
    
    # Get stories from story_groups
    # Exclude Human/AI Chat/AI Agent stories per render instructions
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Create story files and track which files were rendered in " - delete it or improve the code instead

        all_story_names_in_graph = {story['name'] for story in all_stories}
        
        # Create story files and track which files were rendered in correct locations
        created_files = []
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Create directory structure using names from the graph" - delete it or improve the code instead

            )
            
            # Create directory structure using names from the graph
            story_dir = base_dir / epic_folder / sub_epic_folder
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Create file (use 📄 emoji prefix) with sanitized name" - delete it or improve the code instead

            story_dir.mkdir(parents=True, exist_ok=True)
            
            # Create file (use 📄 emoji prefix) with sanitized name
            story_file = story_dir / f"📄 {sanitized_story_name}.md"
[X] ERROR - src\synchronizers\story_scenarios\story_scenarios_synchronizer.py: Useless comment: "# Delete files that exist but weren't rendered (wrong locati" - delete it or improve the code instead

                f.write(content)
        
        # Delete files that exist but weren't rendered (wrong location or obsolete)
        # This runs regardless of scope - we always clean up files that don't belong
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def normalize_name(name):
    """Normalize names for matching."""
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_scenarios_from_story_file(story_file_path):
    """Extract scenarios from a story markdown file."""
    try:
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_story_files(story_name, stories_dir):
    """Find story markdown files matching a story name."""
    story_files = []
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def parse_test_file(file_path):
    """Parse a test file and extract classes and methods."""
    try:
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_helper_file(test_file_name, test_dir):
    """Find helper file for a test file."""
    base_name = test_file_name.replace('test_', '').replace('.py', '')
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def match_test_to_story(test_name, story_names):
    """Match test class name to story name."""
    test_normalized = normalize_name(test_name.replace('Test', ''))
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def match_method_to_scenario(method_name, scenarios):
    """Match test method name to scenario name."""
    method_normalized = normalize_name(method_name.replace('test_', ''))
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_scenario_name(scenario):
    """Format scenario name for display."""
    # Remove (happy_path) or (edge_case) suffixes
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def print_tree(story_structure, test_mapping, stories_dir, test_dir, file_to_epic):
    """Print simple tree view with side-by-side format."""
    
[X] ERROR - src\synchronizers\story_tests\create_tree_view.py: Useless comment: "# Create mapping of methods to scenarios" - delete it or improve the code instead

                    # Match scenarios to methods
                    if test_class and scenarios:
                        # Create mapping of methods to scenarios
                        method_scenario_map = {}
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def normalize_name(name):
    """Normalize names for matching."""
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_scenario_from_docstring(docstring):
    """Extract scenario name and steps from docstring."""
    if not docstring:
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def generate_scenario_name_from_method(method_name):
    """Generate a readable scenario name from test method name."""
    # Remove 'test_' prefix
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def parse_test_file(file_path):
    """Parse a test file and extract classes and methods with docstrings."""
    try:
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def match_test_to_story(test_name, story_names):
    """Match test class name to story name."""
    test_normalized = normalize_name(test_name.replace('Test', ''))
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def find_story_in_graph(story_name, story_graph):
    """Find a story in the story graph by name."""
    for epic in story_graph.get('epics', []):
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def collect_all_stories(story_graph):
    """Collect all story names from the story graph."""
    stories = []
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def update_story_with_scenarios(story, test_methods):
    """Update a story with scenarios extracted from test methods."""
    if 'scenarios' not in story:
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless comment: "# Create a map of existing scenarios by test_method" - delete it or improve the code instead

        story['scenarios'] = []
    
    # Create a map of existing scenarios by test_method
    existing_scenarios = {s.get('test_method'): s for s in story['scenarios']}
[X] ERROR - src\synchronizers\story_tests\extract_scenarios_from_tests.py: Useless comment: "# Update existing scenario" - delete it or improve the code instead

        
        if test_method in existing_scenarios:
            # Update existing scenario
            scenario = existing_scenarios[test_method]
[X] ERROR - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def normalize_name(name):
    """Normalize names for matching."""
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())
[X] ERROR - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_steps_from_docstring(docstring):
    """Extract Gherkin steps from docstring."""
    if not docstring:
[X] ERROR - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def parse_test_file(file_path):
    """Parse a test file and extract test methods with their docstrings."""
    test_methods = {}
[X] ERROR - src\synchronizers\story_tests\extract_scenario_steps_from_tests.py: Useless comment: "# Update scenarios in story graph" - delete it or improve the code instead

                break
    
    # Update scenarios in story graph
    updated_count = 0
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_test_method_from_scenario(scenario, scenario_name, test_method_name, background_steps=None):
    """Format a test method from a scenario."""
    steps = scenario.get('steps', [])
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def format_test_method_from_scenario_outline(scenario_outline, scenario_name, test_method_name, background_steps=None):
    """Format a parametrized test method from a scenario outline."""
    steps = scenario_outline.get('steps', [])
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def get_common_background(scenarios_list):
    """Extract common background steps shared across all scenarios."""
    if not scenarios_list:
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def create_test_file_content(sub_epic, stories, epic_name):
    """Create test file content for a sub-epic."""
    sub_epic_name = sub_epic.get('name', '')
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def extract_stories_from_sub_epic(sub_epic):
    """Extract all stories from a sub-epic."""
    stories = []
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def process_sub_epic_for_tests(sub_epic, epic_name, output_dir):
    """Process a sub-epic and generate test file."""
    # Only process lowest-level sub_epics (those with test_file field)
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class StoryTestsSynchronizer:
    """Synchronizer for rendering pytest test files from story graph JSON."""
    
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

        
        def process_recursive(epic, epic_name):
            """Recursively process sub-epics."""
            for sub_epic in epic.get('sub_epics', []):
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless comment: "# Create parametrize string" - delete it or improve the code instead

    # Format parametrize decorator
    if columns and rows:
        # Create parametrize string
        param_names = ", ".join(columns)
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless comment: "# Get scenarios and scenario outlines" - delete it or improve the code instead

        test_class = story.get('test_class', f'Test{story_name.replace(" ", "")}')
        
        # Get scenarios and scenario outlines
        scenarios = story.get('scenarios', [])
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless comment: "# Get common background" - delete it or improve the code instead

        scenario_outlines = story.get('scenario_outlines', [])
        
        # Get common background
        all_scenarios = scenarios + scenario_outlines
[X] ERROR - src\synchronizers\story_tests\story_tests_synchronizer.py: Useless comment: "# Process all sub-epics" - delete it or improve the code instead

            data = json.load(f)
        
        # Process all sub-epics
        created_files = []
[X] ERROR - src\synchronizers\story_io\examples\add_user_example.py: Useless comment: "# Load into diagram" - delete it or improve the code instead

adapted_data = adapt_story_graph(original_data)

# Load into diagram
diagram = StoryIODiagram()
[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Useless comment: "# Load from the structured.json file" - delete it or improve the code instead



# Load from the structured.json file
# Determine Python import root for imports (examples folder layout).
[X] ERROR - src\synchronizers\story_io\examples\example_load_and_render.py: Useless comment: "# Create empty diagram and load adapted data" - delete it or improve the code instead

    print(f"  Epic {i}: {epic['name']} (sub_epics: {sub_epic_count}, features: {feature_count})")

# Create empty diagram and load adapted data
print("\nLoading diagram from adapted data...")
[X] ERROR - src\synchronizers\story_io\examples\load_and_render_example.py: Useless comment: "# Create diagram instance" - delete it or improve the code instead


# Now load into diagram (using adapted data)
# Create diagram instance
diagram = StoryIODiagram()
[X] ERROR - src\synchronizers\story_io\examples\load_and_render_example.py: Useless comment: "# Load the adapted data" - delete it or improve the code instead

diagram = StoryIODiagram()

# Load the adapted data
diagram._load_from_story_graph_format(adapted_data)
[X] ERROR - src\synchronizers\story_io\examples\render_example.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def convert_behavioral_ac_to_steps(story_data):
    """Convert behavioral_ac array to Steps format."""
    if 'behavioral_ac' in story_data and story_data['behavioral_ac']:
[X] ERROR - src\synchronizers\story_io\examples\render_example.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_story_in_story_groups(story_data, epic_users=None):
    """Adapt a single story, converting acceptance_criteria to Steps."""
    adapted_story = story_data.copy()
[X] ERROR - src\synchronizers\story_io\examples\render_example.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_sub_epic(sub_epic_data, epic_users=None):
    """Recursively adapt a sub_epic, preserving structure and converting stories."""
    adapted_sub_epic = {
[X] ERROR - src\synchronizers\story_io\examples\render_example.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def adapt_story_graph(data):
    """
    Adapt story graph to our expected format.
    Preserves sub_epics structure and converts acceptance_criteria/behavioral_ac to Steps.
    """
    adapted = {}
[X] ERROR - src\synchronizers\story_io\examples\render_example.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


def main():
    """Load structured.json and render to DrawIO."""
    # Path to the structured.json file (relative to workspace root)
[X] ERROR - src\scanners\code\javascript\abstraction_levels_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class AbstractionLevelsScanner(JSCodeScanner):
    """Detects abstraction levels scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\abstraction_levels_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\abstraction_levels_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\arrange_act_assert_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ArrangeActAssertScanner(JSTestScanner):
    """Detects arrange act assert scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\arrange_act_assert_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\arrange_act_assert_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\ascii_only_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class AsciiOnlyScanner(JSTestScanner):
    """Detects ascii only scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\ascii_only_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\ascii_only_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\bad_comments_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class BadCommentsScanner(JSCodeScanner):
    """Detects bad comments scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\bad_comments_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\bad_comments_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\business_readable_test_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class BusinessReadableTestNamesScanner(JSTestScanner):
    """Detects business readable test names scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\business_readable_test_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\business_readable_test_names_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\calculation_timing_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class CalculationTimingCodeScanner(JSCodeScanner):
    """Detects calculation timing code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\calculation_timing_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\calculation_timing_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\class_based_organization_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ClassBasedOrganizationScanner(JSTestScanner):
    """Detects class based organization scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\class_based_organization_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\class_based_organization_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\class_size_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ClassSizeScanner(JSCodeScanner):
    """Detects class size scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\class_size_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\class_size_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\clear_parameters_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ClearParametersScanner(JSCodeScanner):
    """Detects clear parameters scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\clear_parameters_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\clear_parameters_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\complete_refactoring_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class CompleteRefactoringScanner(JSCodeScanner):
    """Detects complete refactoring scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\complete_refactoring_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\complete_refactoring_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\consistent_indentation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ConsistentIndentationScanner(JSCodeScanner):
    """Detects consistent indentation scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\consistent_indentation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\consistent_indentation_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\consistent_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ConsistentNamingScanner(JSCodeScanner):
    """Ensures naming conventions are consistent across JavaScript code."""
    
[X] ERROR - src\scanners\code\javascript\consistent_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_identifiers(self, ast: Dict) -> Dict[str, List[Dict]]:
        """Extract all identifiers categorized by type."""
        identifiers = {
[X] ERROR - src\scanners\code\javascript\consistent_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _detect_naming_style(self, name: str) -> str:
        """Detect the naming convention used."""
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
[X] ERROR - src\scanners\code\javascript\consistent_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _check_naming_consistency(self, identifiers: Dict, file_path: Path) -> List[Dict[str, Any]]:
        """Check for naming convention violations."""
        violations = []
[X] ERROR - src\scanners\code\javascript\consistent_vocabulary_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ConsistentVocabularyScanner(JSTestScanner):
    """Detects consistent vocabulary scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\consistent_vocabulary_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\consistent_vocabulary_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\cover_all_paths_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class CoverAllPathsScanner(JSTestScanner):
    """Detects cover all paths scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\cover_all_paths_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\cover_all_paths_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\dead_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DeadCodeScanner(JSCodeScanner):
    """Detects dead code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\dead_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\dead_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\descriptive_function_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DescriptiveFunctionNamesScanner(JSTestScanner):
    """Detects descriptive function names scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\descriptive_function_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\descriptive_function_names_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\domain_grouping_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainGroupingCodeScanner(JSCodeScanner):
    """Detects domain grouping code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\domain_grouping_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\domain_grouping_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\domain_language_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DomainLanguageCodeScanner(JSCodeScanner):
    """Detects domain language code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\domain_language_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\domain_language_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class DuplicationScanner(JSCodeScanner):
    """Detects duplicate code blocks and functions in JavaScript files."""
    
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        """Scan all JavaScript files for duplicate code."""
        violations = []
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a single JavaScript file for internal duplication."""
        violations = []
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_functions_from_file(self, file_path: Path) -> List[Dict]:
        """Extract all functions from a JavaScript file."""
        parsed = self._parse_js_file(file_path)
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_functions_from_ast(self, ast: Dict, lines: List[str]) -> List[Dict]:
        """Extract function information from AST."""
        functions = []
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_function_info(self, node: Dict, node_type: str, parent_name: str, lines: List[str]) -> Dict:
        """Extract function name, location, and body."""
        if node_type == 'FunctionDeclaration':
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _find_duplicate_blocks(self, lines: List[str], file_path: Path) -> List[Dict[str, Any]]:
        """Find duplicate code blocks within a file."""
        violations = []
[X] ERROR - src\scanners\code\javascript\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two text blocks."""
        if not text1 or not text2:
[X] ERROR - src\scanners\code\javascript\error_handling_isolation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ErrorHandlingIsolationScanner(JSCodeScanner):
    """Detects error handling isolation scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\error_handling_isolation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\error_handling_isolation_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\exact_variable_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ExactVariableNamesScanner(JSTestScanner):
    """Detects exact variable names scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\exact_variable_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\exact_variable_names_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\exception_handling_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ExceptionHandlingScanner(JSCodeScanner):
    """Detects improper exception handling patterns in JavaScript code."""
    
[X] ERROR - src\scanners\code\javascript\exception_handling_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _find_try_catch_blocks(self, ast: Dict) -> List[Dict]:
        """Find all try-catch blocks in the AST."""
        try_blocks = []
[X] ERROR - src\scanners\code\javascript\exception_handling_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _analyze_catch_block(self, handler: Dict) -> Dict:
        """Analyze a catch block for common issues."""
        catch_line = handler.get('loc', {}).get('start', {}).get('line', 0)
[X] ERROR - src\scanners\code\javascript\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ExcessiveGuardsScanner(JSCodeScanner):
    """Detects excessive guards scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\excessive_guards_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\explicit_dependencies_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ExplicitDependenciesScanner(JSCodeScanner):
    """Detects explicit dependencies scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\explicit_dependencies_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\explicit_dependencies_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\fixture_placement_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class FixturePlacementScanner(JSTestScanner):
    """Detects fixture placement scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\fixture_placement_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\fixture_placement_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\full_result_assertions_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class FullResultAssertionsScanner(JSTestScanner):
    """Detects full result assertions scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\full_result_assertions_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\full_result_assertions_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\function_size_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class FunctionSizeScanner(JSCodeScanner):
    """Detects functions that exceed size limits in JavaScript code."""
    
[X] ERROR - src\scanners\code\javascript\function_size_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_all_functions(self, ast: Dict, lines: List[str]) -> List[tuple]:
        """Extract all function definitions from JavaScript AST.
        
        Returns:
            List of (name, start_line, end_line, type) tuples
        """
        functions = []
[X] ERROR - src\scanners\code\javascript\given_when_then_helpers_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class GivenWhenThenHelpersScanner(JSTestScanner):
    """Detects given when then helpers scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\given_when_then_helpers_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\given_when_then_helpers_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\import_placement_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ImportPlacementScanner(JSCodeScanner):
    """Detects import placement scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\import_placement_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\import_placement_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\intention_revealing_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class IntentionRevealingNamesScanner(JSCodeScanner):
    """Detects intention revealing names scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\intention_revealing_names_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\intention_revealing_names_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class JSCodeScanner(Scanner):
    """Base class for JavaScript code scanners.
    
    Uses esprima (via Node.js) to parse JavaScript and provide AST analysis.
    Subclasses implement specific validation rules.
    """
    
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _parse_js_file(self, file_path: Path) -> Optional[Tuple[str, Dict, List[str]]]:
        """Parse a JavaScript file and return (content, AST, lines).
        
        Returns:
            Tuple of (file_content, ast_dict, lines_list) or None if parsing fails
        """
        if not file_path.exists():
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _parse_js_with_esprima(self, content: str, filename: str) -> Optional[Dict]:
        """Use esprima (via Node.js) to parse JavaScript code.
        
        Returns:
            AST dictionary or None if parsing fails
        """
        import tempfile
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_domain_terms(self, story_graph: Dict[str, Any]) -> set:
        """Extract domain terminology from story graph."""
        domain_terms = self._get_common_domain_terms()
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_common_domain_terms(self) -> set:
        """Get common technical terms that aren't domain-specific."""
        return {
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_words_from_text(self, text: str) -> set:
        """Extract individual words from text."""
        import re
[X] ERROR - src\scanners\code\javascript\js_code_scanner.py: Useless comment: "# Create a Node.js script that reads from file" - delete it or improve the code instead

            
            try:
                # Create a Node.js script that reads from file
                js_script = f"""
[X] ERROR - src\scanners\code\javascript\js_regex_analyzer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class JSRegexAnalyzer:
    """Fallback analyzer using regex when AST parsing fails."""
    
[X] ERROR - src\scanners\code\javascript\js_regex_analyzer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def extract_functions(content: str, lines: List[str]) -> List[Tuple[str, int, int, str]]:
        """Extract functions using regex patterns.
        
        Returns:
            List of (name, start_line, end_line, type) tuples
        """
        functions = []
[X] ERROR - src\scanners\code\javascript\js_regex_analyzer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def find_try_catch_blocks(lines: List[str]) -> List[Dict]:
        """Find try-catch blocks using regex."""
        blocks = []
[X] ERROR - src\scanners\code\javascript\js_regex_analyzer.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    @staticmethod
    def find_comments(lines: List[str]) -> List[Tuple[int, str, str]]:
        """Find comments in JavaScript code.
        
        Returns:
            List of (line_number, comment_text, comment_type) tuples
        """
        comments = []
[X] ERROR - src\scanners\code\javascript\js_regex_analyzer.py: Useless comment: "# Update depth" - delete it or improve the code instead

                brace_stack.append((func_type, func_match, i, current_depth + 1))
            
            # Update depth
            current_depth += open_braces
[X] ERROR - src\scanners\code\javascript\js_test_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class JSTestScanner(JSCodeScanner):
    """Base class for JavaScript test file scanners.
    
    Inherits JavaScript parsing capabilities from JSCodeScanner.
    """
    
[X] ERROR - src\scanners\code\javascript\js_test_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _parse_test_file(self, test_file_path: Path) -> Optional[Tuple[str, Dict]]:
        """Parse a JavaScript test file and return (content, AST)."""
        if not test_file_path.exists():
[X] ERROR - src\scanners\code\javascript\meaningful_context_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class MeaningfulContextScanner(JSCodeScanner):
    """Detects meaningful context scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\meaningful_context_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\meaningful_context_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\minimize_mutable_state_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class MinimizeMutableStateScanner(JSCodeScanner):
    """Detects minimize mutable state scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\minimize_mutable_state_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\minimize_mutable_state_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\mock_boundaries_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class MockBoundariesScanner(JSTestScanner):
    """Detects mock boundaries scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\mock_boundaries_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\mock_boundaries_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\natural_english_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class NaturalEnglishCodeScanner(JSCodeScanner):
    """Detects natural english code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\natural_english_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\natural_english_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\no_fallbacks_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class NoFallbacksScanner(JSTestScanner):
    """Detects no fallbacks scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\no_fallbacks_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\no_fallbacks_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\no_guard_clauses_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class NoGuardClausesScanner(JSTestScanner):
    """Detects no guard clauses scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\no_guard_clauses_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\no_guard_clauses_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\object_oriented_helpers_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ObjectOrientedHelpersScanner(JSTestScanner):
    """Detects object oriented helpers scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\object_oriented_helpers_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\object_oriented_helpers_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\observable_behavior_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ObservableBehaviorScanner(JSTestScanner):
    """Detects observable behavior scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\observable_behavior_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\observable_behavior_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\one_concept_per_test_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class OneConceptPerTestScanner(JSTestScanner):
    """Detects one concept per test scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\one_concept_per_test_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\one_concept_per_test_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\open_closed_principle_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class OpenClosedPrincipleScanner(JSCodeScanner):
    """Detects open closed principle scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\open_closed_principle_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\open_closed_principle_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\prefer_object_model_over_config_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class PreferObjectModelOverConfigScanner(JSCodeScanner):
    """Detects prefer object model over config scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\prefer_object_model_over_config_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\prefer_object_model_over_config_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\primitive_vs_object_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class PrimitiveVsObjectScanner(JSCodeScanner):
    """Detects primitive vs object scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\primitive_vs_object_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\primitive_vs_object_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\property_encapsulation_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class PropertyEncapsulationCodeScanner(JSCodeScanner):
    """Detects property encapsulation code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\property_encapsulation_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\property_encapsulation_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\real_implementations_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class RealImplementationsScanner(JSTestScanner):
    """Detects real implementations scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\real_implementations_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\real_implementations_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\resource_oriented_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ResourceOrientedCodeScanner(JSCodeScanner):
    """Detects resource oriented code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\resource_oriented_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\resource_oriented_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\separate_concerns_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SeparateConcernsScanner(JSCodeScanner):
    """Detects separate concerns scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\separate_concerns_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\separate_concerns_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\setup_similarity_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SetupSimilarityScanner(JSTestScanner):
    """Detects setup similarity scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\setup_similarity_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\setup_similarity_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\simplify_control_flow_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SimplifyControlFlowScanner(JSCodeScanner):
    """Detects simplify control flow scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\simplify_control_flow_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\simplify_control_flow_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\single_responsibility_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SingleResponsibilityScanner(JSCodeScanner):
    """Detects single responsibility scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\single_responsibility_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\single_responsibility_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SpecificationMatchScanner(JSTestScanner):
    """Detects specification match scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\specification_match_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\standard_data_reuse_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class StandardDataReuseScanner(JSTestScanner):
    """Detects standard data reuse scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\standard_data_reuse_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\standard_data_reuse_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\story_graph_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class StoryGraphMatchScanner(JSTestScanner):
    """Detects story graph match scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\story_graph_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\story_graph_match_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\swallowed_exceptions_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class SwallowedExceptionsScanner(JSCodeScanner):
    """Detects swallowed exceptions scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\swallowed_exceptions_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\swallowed_exceptions_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\technical_abstraction_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TechnicalAbstractionCodeScanner(JSCodeScanner):
    """Detects technical abstraction code scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\technical_abstraction_code_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\technical_abstraction_code_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\test_boundary_behavior_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TestBoundaryBehaviorScanner(JSTestScanner):
    """Detects test boundary behavior scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\test_boundary_behavior_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\test_boundary_behavior_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\test_file_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TestFileNamingScanner(JSTestScanner):
    """Detects test file naming scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\test_file_naming_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\test_file_naming_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\test_quality_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TestQualityScanner(JSTestScanner):
    """Detects test quality scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\test_quality_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\test_quality_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\third_party_isolation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class ThirdPartyIsolationScanner(JSCodeScanner):
    """Detects third party isolation scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\third_party_isolation_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\third_party_isolation_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\type_safety_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class TypeSafetyScanner(JSCodeScanner):
    """Detects type safety scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\type_safety_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\type_safety_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\ubiquitous_language_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class UbiquitousLanguageScanner(JSTestScanner):
    """Detects ubiquitous language scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\ubiquitous_language_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\ubiquitous_language_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\unnecessary_parameter_passing_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class UnnecessaryParameterPassingScanner(JSCodeScanner):
    """Detects unnecessary parameter passing scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\unnecessary_parameter_passing_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\unnecessary_parameter_passing_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\javascript\useless_comments_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class UselessCommentsScanner(JSCodeScanner):
    """Detects comments that don't add value to the code."""
    
[X] ERROR - src\scanners\code\javascript\vertical_density_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT


class VerticalDensityScanner(JSCodeScanner):
    """Detects vertical density scanner violations in JavaScript code.
    
    TODO: Implement JavaScript-specific validation logic.
    This is a stub scanner that needs to be implemented.
    """
    
[X] ERROR - src\scanners\code\javascript\vertical_density_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def scan_file_with_context(self, context: FileScanContext) -> List[Dict[str, Any]]:
        """Scan a JavaScript file for violations.
        
        TODO: Implement scanning logic:
        1. Parse JavaScript file using _parse_js_file()
        2. Traverse AST to find violations
        3. Create violations using _create_violation()
        4. Return list of violations
        """
        violations = []
[X] ERROR - src\scanners\code\javascript\vertical_density_scanner.py: Useless comment: "# return violations" - delete it or improve the code instead

        # parsed = self._parse_js_file(context.file_path)
        # if not parsed:
        #     return violations
        # 
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_trivial_stub(self, func_node: ast.FunctionDef) -> bool:
        """Check if function is a trivial stub that just returns a simple constant."""
        executable_body = [stmt for stmt in func_node.body if not self._is_docstring_or_comment(stmt, func_node)]
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_property_attribute_decorator(self, decorator: ast.AST) -> bool:
        """Check if decorator is a property attribute decorator."""
        if not isinstance(decorator, ast.Attribute):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _calculate_block_similarities(self, block1: Dict, block2: Dict) -> Tuple[float, float, float]:
        """Calculate AST, normalized, and content similarities between two blocks."""
        try:
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _determine_max_similarity(self, ast_sim: float, content_sim: float, normalized_sim: float, threshold: float) -> float:
        """Determine the maximum similarity score based on multiple metrics."""
        if ast_sim >= 0.85 and content_sim >= 0.50:
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _should_skip_duplicate_pair(self, block1: Dict, block2: Dict) -> bool:
        """Check if a duplicate pair should be skipped based on various filters."""
        if self._is_interface_method(block1['func_name']) or self._is_interface_method(block2['func_name']):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _should_report_duplicate(self, block1: Dict, block2: Dict) -> bool:
        """Determine if a duplicate should be reported."""
        if block1['func_name'] != block2['func_name']:
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_from_node_children(self, node: ast.AST, extract_fn):
        """Recursively extract from child nodes."""
        if hasattr(node, 'body') and isinstance(node.body, list):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_if_end_line(self, stmt: ast.If) -> int:
        """Get end line for If statement."""
        end_line = stmt.lineno
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_loop_end_line(self, stmt) -> int:
        """Get end line for loop statement."""
        end_line = stmt.lineno
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_try_end_line(self, stmt: ast.Try) -> int:
        """Get end line for Try statement."""
        end_line = stmt.lineno
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_with_end_line(self, stmt) -> int:
        """Get end line for With statement."""
        end_line = stmt.lineno
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_helper_statements(self, statements: List[ast.stmt]) -> Tuple[int, int]:
        """Count helper calls vs total statements."""
        helper_count = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_helper_statement(self, stmt: ast.stmt, helper_patterns: List[str]) -> bool:
        """Check if statement is a helper call."""
        if isinstance(stmt, ast.Assert):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_valid_helper_only_statement(self, stmt: ast.stmt, helper_patterns: List[str]) -> bool:
        """Check if statement is valid for helper-only context."""
        if isinstance(stmt, ast.Assert):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_statement_and_children(self, stmt: ast.stmt) -> int:
        """Count a statement and recursively count its children."""
        if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr, ast.Return, 
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_control_flow_statement(self, stmt) -> int:
        """Count code in control flow statement."""
        count = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_async_statement(self, stmt) -> int:
        """Count code in async statement."""
        if hasattr(stmt, 'body'):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_string_operations(self, statements: List[ast.stmt]) -> Tuple[int, int]:
        """Count string operations vs total statements."""
        string_ops = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_call_statement(self, stmt: ast.stmt) -> bool:
        """Check if statement is a call (assign or expr)."""
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_helper_call_statement(self, stmt: ast.stmt) -> bool:
        """Check if call statement is a helper function."""
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _analyze_output_building(self, statements: List[ast.stmt]) -> Tuple[int, int, bool]:
        """Analyze statements for output building patterns."""
        append_count = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_append_statement(self, stmt: ast.stmt) -> bool:
        """Check if statement is an append/extend call."""
        if not isinstance(stmt, ast.Expr):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _loop_contains_appends(self, stmt: ast.For) -> bool:
        """Check if loop contains append operations."""
        for node in ast.walk(stmt):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_output_statements(self, statements: List[ast.stmt]) -> Tuple[float, int]:
        """Count output/logging statements vs total."""
        output_count = 0.0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_output_score(self, stmt: ast.stmt) -> float:
        """Get output score for statement (0, 0.5, or 1)."""
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_logging_call(self, call: ast.Call) -> bool:
        """Check if call is a logging/output operation."""
        if isinstance(call.func, ast.Attribute):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _analyze_list_building(self, statements: List[ast.stmt]) -> Tuple[int, int, bool, int]:
        """Analyze statements for list building patterns."""
        list_building_count = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_list_building_statement(self, stmt: ast.stmt) -> bool:
        """Check if statement is list building."""
        if self._is_append_or_extend_call(stmt):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_append_or_extend_call(self, stmt: ast.stmt) -> bool:
        """Check if statement is append/extend call."""
        if not isinstance(stmt, ast.Expr):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _if_contains_appends(self, stmt: ast.If) -> bool:
        """Check if If statement contains appends."""
        for substmt in ast.walk(stmt):
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _has_any_property_decorator(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has any property-related decorator."""
        for decorator in func_node.decorator_list:
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _count_constructor_statements(self, executable_body: List[ast.stmt]) -> Tuple[int, int]:
        """Count self assignments vs other statements in constructor."""
        self_assignments = 0
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _has_different_iteration_targets(self, block1: Dict, block2: Dict) -> bool:
        """Check if blocks iterate over different collections."""
        collections1 = self._extract_iteration_targets(block1.get('ast_nodes', []))
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _has_different_list_targets(self, block1: Dict, block2: Dict) -> bool:
        """Check if blocks build different lists."""
        list_targets1 = self._extract_list_building_targets(block1.get('ast_nodes', []))
[X] ERROR - src\scanners\code\python\duplication_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_call_name_from_node(self, node: ast.stmt) -> Optional[str]:
        """Extract call name from statement node."""
        call = None
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_guard_call_pattern(self, test_node: ast.AST) -> bool:
        """Check if test is a guard-related call (hasattr, isinstance, exists)."""
        if not isinstance(test_node, ast.Call):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _compare_checks_none(self, test_node: ast.Compare) -> bool:
        """Check if comparison checks for None."""
        for op in test_node.ops:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_file_exists_check_with_creation(self, test: ast.expr, guard_node: ast.If, source_lines: List[str]) -> bool:
        """Check if test is file.exists() followed by creation."""
        if not isinstance(test, ast.Call):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _returns_empty_value(self, guard_node: ast.If) -> bool:
        """Check if guard returns empty value."""
        if not guard_node.body:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _test_checks_optional_variable(self, test: ast.expr) -> bool:
        """Check if test checks an optional variable pattern."""
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _compare_checks_optional_variable(self, test: ast.Compare) -> bool:
        """Check if comparison checks optional variable."""
        for op in test.ops:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _comparator_is_none(self, comparator: ast.expr) -> bool:
        """Check if comparator is None."""
        if isinstance(comparator, ast.Constant) and comparator.value is None:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _call_is_creation_method(self, call: ast.Call, creation_methods: List[str]) -> bool:
        """Check if call is a creation method."""
        if isinstance(call.func, ast.Attribute):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_test_variable(self, test: ast.expr) -> Optional[str]:
        """Extract variable being tested in guard."""
        if isinstance(test, ast.Name):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _body_has_append_operations(self, guard_node: ast.If) -> bool:
        """Check if guard body contains append/extend/add/update operations."""
        for stmt in guard_node.body:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _variable_assigned_from_optional_source(self, var_name: str, func_node: ast.FunctionDef) -> bool:
        """Check if variable is assigned from a source that could return None/empty."""
        for node in ast.walk(func_node):
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _assignment_targets_variable(self, assign_node: ast.Assign, var_name: str) -> bool:
        """Check if assignment targets the given variable."""
        for target in assign_node.targets:
[X] ERROR - src\scanners\code\python\excessive_guards_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _assignment_value_could_be_empty(self, assign_node: ast.Assign) -> bool:
        """Check if assignment value could be None or empty."""
        value = assign_node.value
[X] ERROR - src\scanners\code\python\import_placement_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_bootstrap_file(self, lines: List[str]) -> bool:
        """Check if this is a bootstrap file that needs to configure environment before imports."""
        content = '\n'.join(lines)
[X] ERROR - src\scanners\code\python\real_implementations_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _get_attribute_root_name(self, attr_node: ast.Attribute) -> Optional[str]:
        """Get the root name from a chain of attributes."""
        root = attr_node
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_vague_test_name(self, test_node: ast.FunctionDef, vague_patterns: List[str], file_path: Path) -> bool:
        """Check if test name is vague and not a thin wrapper."""
        for pattern in vague_patterns:
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_test_methods(self, tree: ast.AST) -> List[ast.FunctionDef]:
        """Extract all test methods from AST."""
        test_methods = []
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_terms_from_story_group(self, story_group: dict, domain_terms: set):
        """Extract terms from all stories in a story group."""
        for story in story_group.get('stories', []):
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _iterate_all_stories(self, story_graph: Dict[str, Any]):
        """Iterate through all stories in the story graph."""
        for epic in story_graph.get('epics', []):
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _iterate_stories_in_epic(self, epic: dict):
        """Iterate through all stories in an epic."""
        for sub_epic in epic.get('sub_epics', []):
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _iterate_stories_in_sub_epic(self, sub_epic: dict):
        """Iterate through all stories in a sub-epic."""
        for story_group in sub_epic.get('story_groups', []):
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _extract_variable_names(self, test_method: ast.FunctionDef) -> List[Tuple[str, Optional[int]]]:
        """Extract variable names and line numbers from assignments."""
        variable_names = []
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_generic_name(self, var_name: str) -> bool:
        """Check if variable name is generic."""
        generic_names = {'self', 'result', 'value', 'data', 'item', 'obj', 'workspace', 'root', 'path', 'config'}
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _matches_any_domain_term(self, var_name: str, domain_terms: set) -> bool:
        """Check if variable name matches any domain term."""
        var_name_lower = var_name.lower()
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _analyze_test_assertions(self, test_method: ast.FunctionDef) -> Tuple[List[ast.Assert], bool, bool]:
        """Analyze test method for assertions and assertion patterns."""
        assertions = []
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _with_has_pytest_raises(self, with_node: ast.With) -> bool:
        """Check if With statement uses pytest.raises."""
        for item in with_node.items:
[X] ERROR - src\scanners\code\python\specification_match_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _is_helper_assertion_call(self, call_node: ast.Call) -> bool:
        """Check if call is a helper assertion function."""
        func = call_node.func
[X] ERROR - src\scanners\code\python\ubiquitous_language_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _to_class_name(self, concept_name: str) -> str:
        """
        Convert domain concept name to expected class name.
        'REPL Session' -> 'REPLSession'
        'Behavior Action State' -> 'BehaviorActionState'
        Preserves acronyms (all-caps words stay all-caps)
        """
        def convert_word(word: str) -> str:
[X] ERROR - src\scanners\code\python\unnecessary_parameter_passing_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _check_class_methods(self, class_node: ast.ClassDef, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Check for unnecessary parameter passing within a class."""
        violations = []
[X] ERROR - src\scanners\code\python\unnecessary_parameter_passing_scanner.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _has_semantic_difference(self, param_name: str, inst_var_name: str) -> bool:
        """Check if names suggest semantically different things."""
        # If one has '_name' suffix and the other doesn't, they're likely different
[X] ERROR - src\scanners\code\python\unnecessary_parameter_passing_scanner.py: Useless comment: "# Get all instance variable accesses in init" - delete it or improve the code instead

        violations = []
        
        # Get all instance variable accesses in __init__
        instance_vars = self._get_instance_variables(class_node)
[X] ERROR - src\scanners\code\python\unnecessary_parameter_passing_scanner.py: Useless comment: "# Get parameter names (excluding self, cls, args, kwargs)" - delete it or improve the code instead

            return violations
        
        # Get parameter names (excluding self, cls, args, kwargs)
        param_names = []
[X] ERROR - src\cli\cursor\cursor_command_visitor.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _build_wrapped_hierarchy(self):
        """Override to create CursorBehaviorWrapper instances instead of using factory"""
        current_behavior_name = (
[X] ERROR - src\cli\cursor\cursor_command_visitor.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _build_wrapped_hierarchy(self):
        """Override to skip building actions hierarchy - not needed for cursor commands"""
        pass
[X] ERROR - src\cli\cursor\cursor_command_visitor.py: Useless docstring that repeats function/class name - delete it or explain WHY, not WHAT

    
    def _empty_stub(self) -> str:
        """Stub method for interface compatibility - Cursor commands generate files, not text output."""
        return ""
[X] ERROR - src\cli\cursor\cursor_command_visitor.py: Useless comment: "# Set attributes BEFORE calling parent init (which calls" - delete it or improve the code instead

        if not bot:
            raise ValueError("bot is required")
        # Set attributes BEFORE calling parent __init__ (which calls _build_wrapped_hierarchy)
        self.workspace_root = workspace_root
Use Explicit Dependencies: 1 violation(s)
[!] WARNING - src\utils.py: Global variable usage detected - dependencies should be explicit (passed as parameters)
Validation Instructions
The following validation steps were performed:

Step 1: Scanner Violation Review
{{scanner_output}}
Carefully review all scanner-reported violations as follows:
For each violation message, locate the corresponding element in the story graph.
Open the relevant rule file and read all DO and DON'T examples thoroughly.
Decide if the violation is Valid (truly a rule breach per examples) or a False Positive (explain why if so).
Determine the Root Cause (e.g., 'incorrect concept naming', 'missing actor', etc.).
Assign a Theme grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria'). ... and 87 more instructions
Report Location
This report was automatically generated and saved to: C:\dev\agile_bots\docs\stories\reports\code-validation-report-2026-01-28_00-11-27.md

Some content has been disabled in this document