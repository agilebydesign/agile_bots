"""
Test Prepare Common Instructions For Behavior, Action, and Scope

SubEpic: Prepare Common Instructions For Behavior, Action, and Scope
Parent Epic: Invoke Bot > Perform Action

Domain tests verify guardrails (clarifications, evidence, strategies) are saved correctly.
CLI tests verify guardrails commands and error handling.
"""
import pytest
from pathlib import Path
import json
import os
from helpers.bot_test_helper import BotTestHelper
from helpers import TTYBotTestHelper, PipeBotTestHelper, JsonBotTestHelper


# ============================================================================
# DOMAIN TESTS - Guardrails (Clarifications, Evidence, Strategies)
# ============================================================================

class TestSaveClarificationAnswers:
    """Story: Save Clarification Answers"""
    
    def test_save_new_clarification_answers(self, tmp_path):
        """
        SCENARIO: Save new clarification answers
        GIVEN: Bot with no existing clarifications
        WHEN: User saves answers via Bot.save()
        THEN: Answers saved to clarification.json in test workspace
        """
        # Create isolated test bot
        helper = BotTestHelper(tmp_path)
        
        # Navigate to a behavior
        helper.bot.behaviors.navigate_to('shape')
        
        # Save new answers
        test_answers = {
            "What is the scope?": "Test project scope",
            "Who are the users?": "Test users"
        }
        
        helper.bot.save(
            answers=test_answers,
            evidence_provided=None,
            decisions=None,
            assumptions=None
        )
        
        # Verify answers saved to TEST workspace (not production)
        clarification_file = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        assert clarification_file.exists(), "clarification.json should be created in test workspace"
        
        saved_data = json.loads(clarification_file.read_text())
        assert 'shape' in saved_data
        assert 'key_questions' in saved_data['shape']
        assert saved_data['shape']['key_questions']['answers'] == test_answers
    
    def test_save_merges_with_existing_clarification_answers(self, tmp_path):
        """
        SCENARIO: Save merges with existing clarification answers
        GIVEN: Bot with existing clarification answers
        WHEN: User saves additional/modified answers
        THEN: New answers merged with existing, new overrides existing for same question
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        # Create existing clarification data
        existing_answers = {
            "What is the scope?": "Original scope",
            "Who are the users?": "Original users"
        }
        helper.bot.save(answers=existing_answers, evidence_provided=None, decisions=None, assumptions=None)
        
        # Save new/modified answers
        new_answers = {
            "What is the scope?": "Updated scope",  # Override existing
            "What is the timeline?": "New timeline"  # Add new question
        }
        helper.bot.save(answers=new_answers, evidence_provided=None, decisions=None, assumptions=None)
        
        # Verify merge behavior
        clarification_file = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        saved_data = json.loads(clarification_file.read_text())
        
        merged_answers = saved_data['shape']['key_questions']['answers']
        assert merged_answers["What is the scope?"] == "Updated scope"  # Updated
        assert merged_answers["Who are the users?"] == "Original users"  # Preserved
        assert merged_answers["What is the timeline?"] == "New timeline"  # Added


class TestSaveClarificationEvidence:
    """Story: Save Clarification Evidence"""
    
    def test_save_evidence_provided(self, tmp_path):
        """
        SCENARIO: Save evidence provided
        GIVEN: Bot with clarification requirements
        WHEN: User provides evidence via Bot.save()
        THEN: Evidence saved to clarification.json
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        test_evidence = {
            "Requirements doc": ["requirements.md", "specs.pdf"],
            "User interviews": ["interview1.txt"]
        }
        
        helper.bot.save(
            answers=None,
            evidence_provided=test_evidence,
            decisions=None,
            assumptions=None
        )
        
        clarification_file = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        saved_data = json.loads(clarification_file.read_text())
        
        assert 'shape' in saved_data
        assert 'evidence' in saved_data['shape']
        assert saved_data['shape']['evidence']['provided'] == test_evidence


class TestSaveStrategyDecisions:
    """Story: Save Strategy Decisions"""
    
    def test_save_strategy_decisions(self, tmp_path):
        """
        SCENARIO: Save strategy decisions
        GIVEN: Bot with strategy decision criteria
        WHEN: User makes decisions via Bot.save()
        THEN: Only chosen decisions saved (not entire criteria template)
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        test_decisions = {
            "Approach": "Incremental development",
            "Architecture": "Microservices"
        }
        
        helper.bot.save(
            answers=None,
            evidence_provided=None,
            decisions=test_decisions,
            assumptions=None
        )
        
        strategy_file = tmp_path / 'workspace' / 'docs' / 'story' / 'strategy.json'
        assert strategy_file.exists()
        
        saved_data = json.loads(strategy_file.read_text())
        assert 'shape' in saved_data
        # Actual format: behavior_data['decisions'] = {...}
        assert 'decisions' in saved_data['shape']
        assert saved_data['shape']['decisions'] == test_decisions
    
    def test_save_strategy_assumptions(self, tmp_path):
        """
        SCENARIO: Save strategy assumptions
        GIVEN: Bot with strategy context
        WHEN: User saves assumptions via Bot.save()
        THEN: Assumptions saved to strategy.json
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        test_assumptions = [
            "Users have basic tech literacy",
            "System will scale to 1000 users"
        ]
        
        helper.bot.save(
            answers=None,
            evidence_provided=None,
            decisions=None,
            assumptions=test_assumptions
        )
        
        strategy_file = tmp_path / 'workspace' / 'docs' / 'story' / 'strategy.json'
        saved_data = json.loads(strategy_file.read_text())
        
        assert 'shape' in saved_data
        # Actual format: behavior_data['assumptions'] = [...]
        assert 'assumptions' in saved_data['shape']
        assert saved_data['shape']['assumptions'] == test_assumptions


class TestSaveMultipleGuardrails:
    """Story: Save Multiple Guardrails Together"""
    
    def test_save_all_guardrails_at_once(self, tmp_path):
        """
        SCENARIO: Save all guardrails at once
        GIVEN: Bot with current behavior
        WHEN: User saves answers, evidence, decisions, and assumptions together
        THEN: All data saved to respective files
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        helper.bot.save(
            answers={"What is scope?": "Full scope"},
            evidence_provided={"Requirements doc": ["req.md"]},
            decisions={"Approach": "Agile"},
            assumptions=["Team has agile experience"]
        )
        
        # Verify clarifications
        clarification_file = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        clarification_data = json.loads(clarification_file.read_text())
        assert clarification_data['shape']['key_questions']['answers']['What is scope?'] == "Full scope"
        assert clarification_data['shape']['evidence']['provided']['Requirements doc'] == ["req.md"]
        
        # Verify strategy
        strategy_file = tmp_path / 'workspace' / 'docs' / 'story' / 'strategy.json'
        strategy_data = json.loads(strategy_file.read_text())
        # Actual format: behavior_data['decisions'] and behavior_data['assumptions']
        assert strategy_data['shape']['decisions']['Approach'] == "Agile"
        assert strategy_data['shape']['assumptions'] == ["Team has agile experience"]
    
    def test_save_preserves_data_across_behaviors(self, tmp_path):
        """
        SCENARIO: Save preserves data across behaviors
        GIVEN: Multiple behaviors with saved guardrails
        WHEN: Switching between behaviors and saving
        THEN: Each behavior's data is preserved independently
        """
        helper = BotTestHelper(tmp_path)
        
        # Save data for 'shape' behavior
        helper.bot.behaviors.navigate_to('shape')
        helper.bot.save(
            answers={"Shape question": "Shape answer"},
            evidence_provided=None,
            decisions=None,
            assumptions=None
        )
        
        # Save data for 'exploration' behavior
        helper.bot.behaviors.navigate_to('exploration')
        helper.bot.save(
            answers={"Exploration question": "Exploration answer"},
            evidence_provided=None,
            decisions=None,
            assumptions=None
        )
        
        # Verify both behaviors' data exists
        clarification_file = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        saved_data = json.loads(clarification_file.read_text())
        
        assert 'shape' in saved_data
        assert saved_data['shape']['key_questions']['answers']['Shape question'] == "Shape answer"
        
        assert 'exploration' in saved_data
        assert saved_data['exploration']['key_questions']['answers']['Exploration question'] == "Exploration answer"


class TestSaveFileIsolation:
    """Verify tests do NOT pollute production workspace"""
    
    def test_save_uses_test_workspace_not_production(self, tmp_path):
        """
        SCENARIO: Save uses test workspace not production
        GIVEN: Bot initialized with tmp_path workspace
        WHEN: Saving any data
        THEN: Data saved to tmp_path workspace, NOT production agile_bots/docs/story
        """
        helper = BotTestHelper(tmp_path)
        helper.bot.behaviors.navigate_to('shape')
        
        helper.bot.save(
            answers={"Test question": "Test answer"},
            evidence_provided=None,
            decisions=None,
            assumptions=None
        )
        
        # Verify saved to TEST workspace
        test_clarification = tmp_path / 'workspace' / 'docs' / 'story' / 'clarification.json'
        assert test_clarification.exists(), "Should save to test workspace"
        
        # Verify NOT saved to production workspace
        production_clarification = Path(__file__).parent.parent.parent / 'docs' / 'story' / 'clarification.json'
        if production_clarification.exists():
            prod_data = json.loads(production_clarification.read_text())
            # If production file exists, ensure our test data is NOT in it
            for behavior_data in prod_data.values():
                if isinstance(behavior_data, dict) and 'key_questions' in behavior_data:
                    answers = behavior_data['key_questions'].get('answers', {})
                    assert "Test question" not in answers, "Test data should NOT appear in production file"


class TestSubmitScopeInstructions:
    """Story: Submit Scope Instructions"""
    
    def test_scope_appears_in_instructions_display_content(self, tmp_path):
        """
        SCENARIO: Scope appears in instructions display_content markdown
        GIVEN: Build action with story scope set
        WHEN: Instructions are retrieved via action.get_instructions()
        THEN: instructions.display_content contains "## Scope" section
        AND: instructions.display_content contains story_graph markdown from scope.results
        AND: bot.submit_instructions() can use display_content to submit scope instructions
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph with test stories
        story_graph = helper.story.given_story_graph_dict(epic='TestEpic')
        
        # Set up sub_epics structure with Story1 for scope filtering
        epic = story_graph['epics'][0]
        epic['sub_epics'] = [
            {
                "name": "SubEpic1",
                "sequential_order": 1,
                "story_groups": [
                    {
                        "stories": [
                            {
                                "name": "Story1",
                                "sequential_order": 1,
                                "scenarios": []
                            }
                        ]
                    }
                ]
            }
        ]
        
        stories_dir = helper.workspace / 'docs' / 'story'
        helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        
        # Set scope to a specific story - apply it to the bot first
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        scope.apply_to_bot()
        context = ScopeActionContext(scope=scope)
        
        # Get instructions - this calls _build_display_content() which uses MarkdownInstructions.serialize()
        instructions = action.get_instructions(context)
        
        # Verify scope appears in display_content
        helper.instructions.verify_scope_in_display_content(instructions)
    
    def test_domain_concepts_serialized_in_json_story_graph(self, tmp_path):
        """
        SCENARIO: Domain concepts are properly serialized in JSON story graph
        GIVEN: Build action with story scope set and story graph containing domain_concepts
        WHEN: Instructions are retrieved via action.get_instructions()
        THEN: instructions.display_content contains "## Scope" section
        AND: instructions.display_content contains story_graph markdown with domain_concepts from scope.results
        AND: Domain concepts from both epic and sub-epic levels are included in JSON
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph with test stories - same as previous test
        story_graph = helper.story.given_story_graph_dict(epic='TestEpic')
        
        # Add domain_concepts to epic
        epic = story_graph['epics'][0]
        epic['domain_concepts'] = [
            {
                "name": "EpicDomainConcept",
                "responsibilities": [
                    {
                        "name": "Manages epic-level responsibilities",
                        "collaborators": ["EpicCollaborator1", "EpicCollaborator2"]
                    }
                ],
                "realization": [
                    {
                        "scope": "TestEpic.EpicDomainConcept.Manages epic-level responsibilities",
                        "scenario": "EpicDomainConcept manages responsibilities",
                        "walks": [
                            {
                                "covers": "Steps 1-2",
                                "object_flow": [
                                    "concept: EpicDomainConcept = EpicDomainConcept.create(name: 'EpicDomainConcept')"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        
        # Set up sub_epics structure with Story1 for scope filtering
        epic['sub_epics'] = [
            {
                "name": "SubEpic1",
                "sequential_order": 1,
                "story_groups": [
                    {
                        "stories": [
                            {
                                "name": "Story1",
                                "sequential_order": 1,
                                "scenarios": []
                            }
                        ]
                    }
                ]
            }
        ]
        
        # Add domain_concepts to first sub-epic
        sub_epic = epic['sub_epics'][0]
        sub_epic['domain_concepts'] = [
            {
                "name": "SubEpicDomainConcept",
                "responsibilities": [
                    {
                        "name": "Manages sub-epic responsibilities",
                        "collaborators": ["SubEpicCollaborator"]
                    }
                ],
                "realization": [
                    {
                        "scope": "TestEpic.SubEpic1.SubEpicDomainConcept.Manages sub-epic responsibilities",
                        "scenario": "SubEpicDomainConcept manages responsibilities",
                        "walks": [
                            {
                                "covers": "Steps 1-2",
                                "object_flow": [
                                    "concept: SubEpicDomainConcept = SubEpicDomainConcept.create(name: 'SubEpicDomainConcept')"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        
        stories_dir = helper.workspace / 'docs' / 'story'
        helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        
        # Set scope to a specific story - apply it to the bot first
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        scope.apply_to_bot()
        context = ScopeActionContext(scope=scope)
        
        # Get instructions - this calls _build_display_content() which uses MarkdownInstructions.serialize()
        instructions = action.get_instructions(context)
        
        # Verify scope appears in display_content and get parsed JSON
        parsed_json = helper.instructions.verify_scope_in_display_content(instructions)
        
        # Verify domain_concepts are present and properly structured
        helper.instructions.verify_domain_concepts_in_json(parsed_json)
    
    def test_include_level_persisted_in_scope_json(self, tmp_path):
        """
        SCENARIO: Scope with include_level persists in scope.json
        GIVEN: User sets include_level to 'code'
        WHEN: Scope is saved
        THEN: include_level='code' persisted to scope.json
        AND: Reloading scope restores include_level='code'
        """
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        
        # Set include_level
        scope.include_level = 'code'
        scope.save()
        
        # Verify persisted
        scope_file = helper.workspace / 'scope.json'
        scope_data = json.loads(scope_file.read_text())
        assert scope_data['include_level'] == 'code'
        
        # Verify restored
        new_scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        new_scope.load()
        assert new_scope.include_level == 'code'
    
    def test_scope_with_include_level_stories_only(self, tmp_path):
        """
        SCENARIO: Scope with include_level='stories' filters to structure
        GIVEN: Story graph with domain concepts, acceptance criteria, scenarios, examples
        WHEN: include_level='stories' and instructions retrieved
        THEN: Scope content contains only epic/sub-epic/story names
        AND: No domain concepts, acceptance criteria, scenarios, examples, tests, or code
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create full story graph with domain concepts, acceptance criteria, scenarios
        story_graph = {
            'epics': [{
                'name': 'TestEpic',
                'sequential_order': 1,
                'domain_concepts': [{
                    'name': 'TestDomainConcept',
                    'responsibilities': [{'name': 'Does something', 'collaborators': ['OtherClass']}]
                }],
                'sub_epics': [{
                    'name': 'TestSubEpic',
                    'sequential_order': 1,
                    'story_groups': [{
                        'stories': [{
                            'name': 'TestStory',
                            'sequential_order': 1,
                            'acceptance_criteria': [{'name': 'Criteria 1', 'text': 'Criteria 1'}, {'name': 'Criteria 2', 'text': 'Criteria 2'}],
                            'scenarios': [{
                                'name': 'Happy path',
                                'steps': [{'text': 'Given... When... Then...', 'sequential_order': 1}],
                                'examples': [{'input': 'test'}]
                            }]
                        }]
                    }]
                }]
            }]
        }
        helper.files.given_file_created(
            helper.workspace / 'docs' / 'story',
            'story-graph.json',
            story_graph
        )
        
        # Set scope with include_level='stories'
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['TestStory'])
        scope.include_level = 'stories'
        scope.apply_to_bot()
        
        # Get instructions
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        context = ScopeActionContext(scope=scope)
        instructions = action.get_instructions(context)
        
        # Verify only structure included
        content = '\n'.join(instructions.display_content)
        assert 'TestEpic' in content
        assert 'TestSubEpic' in content
        assert 'TestStory' in content
        
        # Verify filtered out
        assert 'TestDomainConcept' not in content
        assert 'Criteria 1' not in content
        assert 'Happy path' not in content
        assert 'Given... When... Then...' not in content
    
    def test_scope_with_include_level_domain_concepts(self, tmp_path):
        """
        SCENARIO: Scope with include_level='domain_concepts' includes CRC cards
        GIVEN: Story graph with domain concepts at epic and sub-epic levels
        WHEN: include_level='domain_concepts'
        THEN: Scope includes structure + domain concepts with responsibilities/collaborators
        AND: No acceptance criteria, scenarios, examples, tests, or code
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph with domain concepts
        story_graph = {
            'epics': [{
                'name': 'TestEpic',
                'sequential_order': 1,
                'domain_concepts': [{
                    'name': 'TestDomainConcept',
                    'responsibilities': [{
                        'name': 'Processes test data',
                        'collaborators': ['DataStore', 'Validator']
                    }],
                    'module': 'test_module',
                    'inherits_from': 'BaseClass'
                }],
                'sub_epics': [{
                    'name': 'TestSubEpic',
                    'sequential_order': 1,
                    'story_groups': [{
                        'stories': [{
                            'name': 'TestStory',
                            'sequential_order': 1,
                            'acceptance_criteria': [{'name': 'Criteria 1', 'text': 'Criteria 1'}],
                            'scenarios': [{'name': 'Happy path', 'steps': [{'text': 'Given...', 'sequential_order': 1}]}]
                        }]
                    }]
                }]
            }]
        }
        helper.files.given_file_created(
            helper.workspace / 'docs' / 'story',
            'story-graph.json',
            story_graph
        )
        
        # Set scope with include_level='domain_concepts'
        scope = Scope(workspace_directory=helper.workspace, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['TestStory'])
        scope.include_level = 'domain_concepts'
        scope.apply_to_bot()
        
        # Get instructions
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        context = ScopeActionContext(scope=scope)
        instructions = action.get_instructions(context)
        
        # Verify domain concepts included
        content = '\n'.join(instructions.display_content)
        assert 'TestDomainConcept' in content
        assert 'Processes test data' in content
        assert 'DataStore' in content
        assert 'Validator' in content
        
        # Verify acceptance/scenarios filtered out
        assert 'Criteria 1' not in content
        assert 'Happy path' not in content


# ============================================================================
# CLI TESTS - Guardrails Commands and Error Handling
# ============================================================================

class TestSaveGuardrailsUsingCLI:
    """
    Story: Save Guardrails Using CLI Commands
    
    Domain logic: test_perform_action.py::TestSaveGuardrailsViaCLI
    CLI focus: Execute save commands with parameters and verify output
    """
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_save_answers_via_cli_command(self, tmp_path, helper_class):
        """
        SCENARIO: Save answers via CLI command
        GIVEN: CLI is at shape.clarify
        WHEN: user runs 'save --answers {"What is the scope?": "Bot system"}'
        THEN: CLI shows success message
        AND: clarification.json is updated
        
        Domain: test_save_guardrail_data_answers
        """
        # Given
        helper = helper_class(tmp_path)
        helper.domain.bot.behaviors.navigate_to('shape')
        
        # When - Execute save command (simulated via action context)
        from actions.action_context import ClarifyActionContext
        action = helper.domain.bot.behaviors.current.actions.find_by_name('clarify')
        answers_data = {"What is the scope?": "Bot system"}
        context = ClarifyActionContext(answers=answers_data, evidence_provided=None)
        action.do_execute(context)
        
        # Then - File exists with saved data
        helper.domain.clarify.assert_clarification_file_exists()
        helper.domain.clarify.assert_clarification_contains_answers('shape', answers_data)
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_save_decisions_via_cli_command(self, tmp_path, helper_class):
        """
        SCENARIO: Save decisions via CLI command
        GIVEN: CLI is at shape.strategy
        WHEN: user runs 'save --decisions {"drill_down": "Deep"}'
        THEN: CLI shows success message
        AND: strategy.json is updated
        
        Domain: test_save_guardrail_data_decisions
        """
        # Given
        helper = helper_class(tmp_path)
        helper.domain.bot.behaviors.navigate_to('shape')
        
        # When - Execute save command
        from actions.action_context import StrategyActionContext
        action = helper.domain.bot.behaviors.current.actions.find_by_name('strategy')
        decisions_data = {"drill_down": "Deep"}
        context = StrategyActionContext(decisions_made=decisions_data, assumptions_made=None)
        action.do_execute(context)
        
        # Then - File exists with saved data
        helper.domain.strategy.assert_strategy_file_exists()
        helper.domain.strategy.assert_strategy_contains_behavior('shape', expected_decisions=decisions_data)


# ============================================================================
# STORY: Handle Errors
# ============================================================================

class TestHandleErrorsUsingCLI:
    """
    Story: Handle Errors Using CLI
    
    CLI focus: Error display and validation messages
    """
    
    @pytest.mark.parametrize("helper_class", [
        TTYBotTestHelper,
        PipeBotTestHelper,
        JsonBotTestHelper
    ])
    def test_invalid_command_shows_error(self, tmp_path, helper_class):
        """
        SCENARIO: Invalid command shows error (all channels)
        GIVEN: CLI is at shape.build
        WHEN: user enters 'invalid_command'
        THEN: CLI displays error message in appropriate channel format
        """
        # Given
        helper = helper_class(tmp_path)
        helper.domain.state.set_state('shape', 'build')
        
        # When
        cli_response = helper.cli_session.execute_command('invalid_command')
        
        # Then - Error message shown
        assert 'error' in cli_response.output.lower() or 'unknown' in cli_response.output.lower()


# ============================================================================
# STORY: Display Status Tree with behavior.action Commands
# ============================================================================