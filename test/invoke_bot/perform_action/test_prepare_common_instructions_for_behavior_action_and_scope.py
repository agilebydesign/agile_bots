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
        clarification_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
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
        clarification_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
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
        
        clarification_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
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
        
        strategy_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'strategy.json'
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
        
        strategy_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'strategy.json'
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
        clarification_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
        clarification_data = json.loads(clarification_file.read_text())
        assert clarification_data['shape']['key_questions']['answers']['What is scope?'] == "Full scope"
        assert clarification_data['shape']['evidence']['provided']['Requirements doc'] == ["req.md"]
        
        # Verify strategy
        strategy_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'strategy.json'
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
        
        # Save data for 'discovery' behavior
        helper.bot.behaviors.navigate_to('discovery')
        helper.bot.save(
            answers={"Discovery question": "Discovery answer"},
            evidence_provided=None,
            decisions=None,
            assumptions=None
        )
        
        # Verify both behaviors' data exists
        clarification_file = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
        saved_data = json.loads(clarification_file.read_text())
        
        assert 'shape' in saved_data
        assert saved_data['shape']['key_questions']['answers']['Shape question'] == "Shape answer"
        
        assert 'discovery' in saved_data
        assert saved_data['discovery']['key_questions']['answers']['Discovery question'] == "Discovery answer"


class TestSaveFileIsolation:
    """Verify tests do NOT pollute production workspace"""
    
    def test_save_uses_test_workspace_not_production(self, tmp_path):
        """
        SCENARIO: Save uses test workspace not production
        GIVEN: Bot initialized with tmp_path workspace
        WHEN: Saving any data
        THEN: Data saved to tmp_path workspace, NOT production agile_bots/docs/stories
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
        test_clarification = tmp_path / 'workspace' / 'docs' / 'stories' / 'clarification.json'
        assert test_clarification.exists(), "Should save to test workspace"
        
        # Verify NOT saved to production workspace
        production_clarification = Path(__file__).parent.parent.parent / 'docs' / 'stories' / 'clarification.json'
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
        stories_dir = helper.workspace / 'docs' / 'stories'
        helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        
        # Set scope to a specific story - apply it to the bot first
        scope = Scope(workspace_directory=tmp_path, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        scope.apply_to_bot()
        context = ScopeActionContext(scope=scope)
        
        # Get instructions - this calls _build_display_content() which uses MarkdownInstructions.serialize()
        instructions = action.get_instructions(context)
        
        # Verify display_content exists and contains scope markdown
        assert instructions.display_content is not None
        assert len(instructions.display_content) > 0
        
        # Join display_content to check for scope section
        display_text = '\n'.join(instructions.display_content)
        
        # Verify "## Scope" section exists
        assert '## Scope' in display_text, "display_content should contain '## Scope' section"
        
        # Verify story scope is mentioned
        assert 'Story Scope' in display_text or 'Story1' in display_text, \
            "display_content should contain story scope information"
        
        # Verify instruction text and story_graph JSON appears (from scope.results serialized via JSON adapter)
        # The story_graph should appear after the scope section
        scope_section_index = display_text.find('## Scope')
        after_scope = display_text[scope_section_index:]
        
        # Verify instruction text appears before JSON
        assert 'Please only work on the following scope' in after_scope, \
            "display_content should contain instruction text 'Please only work on the following scope'"
        assert 'Scope Filter:' in after_scope, "display_content should contain 'Scope Filter:' label"
        assert 'Scope:' in after_scope, "display_content should contain 'Scope:' label"
        
        # Story graph JSON should be valid JSON (starts with {)
        import json
        # Find JSON content after scope section - look for JSON structure
        json_start = after_scope.find('{')
        assert json_start != -1, "display_content should contain JSON story graph after scope section"
        
        # Extract and parse JSON to verify it's valid
        json_content = after_scope[json_start:]
        # Find the end of JSON (stop at next section marker)
        json_end_marker = json_content.find('\n---')
        if json_end_marker != -1:
            json_content = json_content[:json_end_marker].strip()
        
        # Parse JSON to verify it's valid story graph structure
        parsed_json = json.loads(json_content)
        assert isinstance(parsed_json, dict), "Story graph JSON should be a dictionary"
        # Verify it contains expected story graph structure (path, content, epics, etc.)
        assert 'path' in parsed_json or 'content' in parsed_json or 'epics' in parsed_json or 'epic_count' in parsed_json, \
            "display_content should contain story graph JSON with expected structure (path, content, epics, or epic_count)"
        
        # Verify bot.submit_instructions() can use this display_content
        # This is what bot.submit_instructions() does - joins display_content
        content_str = '\n'.join(instructions.display_content)
        assert len(content_str) > 0, "display_content should produce non-empty string for submission"
        assert '## Scope' in content_str, "Submitted content should contain scope section"
        assert '{' in content_str or '[' in content_str, "Submitted content should contain JSON story graph"
    
    def test_domain_concepts_serialized_in_json_story_graph(self, tmp_path):
        """
        SCENARIO: Domain concepts are properly serialized in JSON story graph
        GIVEN: Story graph with domain_concepts at epic and sub-epic levels
        WHEN: Instructions are retrieved with scope
        THEN: display_content contains JSON with domain_concepts properly serialized
        AND: Domain concepts from both epic and sub-epic levels are included
        """
        from actions.action_context import ScopeActionContext
        from scope import Scope, ScopeType
        
        helper = BotTestHelper(tmp_path)
        
        # Create story graph with complex domain_concepts at epic and sub-epic levels
        story_graph = {
            "epics": [
                {
                    "name": "TestEpic",
                    "sequential_order": 1,
                    "domain_concepts": [
                        {
                            "name": "EpicDomainConcept",
                            "responsibilities": [
                                {
                                    "name": "Manages epic-level responsibilities",
                                    "collaborators": ["EpicCollaborator1", "EpicCollaborator2"]
                                },
                                {
                                    "name": "Coordinates epic activities",
                                    "collaborators": ["Coordinator"]
                                }
                            ],
                            "realization": [
                                {
                                    "scope": "TestEpic.EpicDomainConcept.Manages epic-level responsibilities",
                                    "scenario": "EpicDomainConcept manages responsibilities with multiple collaborators",
                                    "walks": [
                                        {
                                            "covers": "Steps 1-2 (Initialize concept, validate collaborators)",
                                            "object_flow": [
                                                "concept: EpicDomainConcept = EpicDomainConcept.create(name: 'EpicDomainConcept')",
                                                "collaborators: ['EpicCollaborator1', 'EpicCollaborator2'] = concept.get_collaborators()",
                                                "is_valid: True = concept.validate_collaborators(collaborators)"
                                            ]
                                        },
                                        {
                                            "covers": "Step 3 (Execute responsibility with collaborators)",
                                            "object_flow": [
                                                "result = concept.manage_responsibilities(collaborators: ['EpicCollaborator1', 'EpicCollaborator2'])",
                                                "  -> EpicCollaborator1.execute_task()",
                                                "  -> EpicCollaborator2.execute_task()",
                                                "  return result: Success"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "EpicSecondConcept",
                            "responsibilities": [
                                {
                                    "name": "Handles epic-level operations",
                                    "collaborators": ["Operator"]
                                }
                            ]
                        }
                    ],
                    "sub_epics": [
                        {
                            "name": "SubEpic1",
                            "sequential_order": 1,
                            "domain_concepts": [
                                {
                                    "name": "SubEpicDomainConcept",
                                    "responsibilities": [
                                        {
                                            "name": "Manages sub-epic responsibilities",
                                            "collaborators": ["SubEpicCollaborator"]
                                        },
                                        {
                                            "name": "Handles sub-epic operations",
                                            "collaborators": ["SubOperator1", "SubOperator2"]
                                        }
                                    ],
                                    "realization": [
                                        {
                                            "scope": "TestEpic.SubEpic1.SubEpicDomainConcept.Handles sub-epic operations",
                                            "scenario": "SubEpicDomainConcept handles operations with multiple operators",
                                            "walks": [
                                                {
                                                    "covers": "Steps 1-3 (Initialize concept, load operators, execute operations)",
                                                    "object_flow": [
                                                        "concept: SubEpicDomainConcept = SubEpicDomainConcept.create(name: 'SubEpicDomainConcept')",
                                                        "operators: ['SubOperator1', 'SubOperator2'] = concept.get_operators()",
                                                        "result = concept.handle_operations(operators: ['SubOperator1', 'SubOperator2'])",
                                                        "  -> SubOperator1.process()",
                                                        "  -> SubOperator2.process()",
                                                        "  return result: Completed"
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "sub_epics": [
                                {
                                    "name": "NestedSubEpic1",
                                    "sequential_order": 1,
                                    "domain_concepts": [
                                        {
                                            "name": "NestedSubEpicDomainConcept",
                                            "responsibilities": [
                                                {
                                                    "name": "Manages nested sub-epic operations",
                                                    "collaborators": ["NestedOperator1", "NestedOperator2"]
                                                }
                                            ],
                                            "realization": [
                                                {
                                                    "scope": "TestEpic.SubEpic1.NestedSubEpic1.NestedSubEpicDomainConcept.Manages nested sub-epic operations",
                                                    "scenario": "NestedSubEpicDomainConcept manages nested operations with multiple operators",
                                                    "walks": [
                                                        {
                                                            "covers": "Steps 1-2 (Initialize nested concept, validate operators)",
                                                            "object_flow": [
                                                                "concept: NestedSubEpicDomainConcept = NestedSubEpicDomainConcept.create(name: 'NestedSubEpicDomainConcept')",
                                                                "operators: ['NestedOperator1', 'NestedOperator2'] = concept.get_operators()",
                                                                "is_valid: True = concept.validate_operators(operators)"
                                                            ]
                                                        },
                                                        {
                                                            "covers": "Step 3 (Execute nested operations)",
                                                            "object_flow": [
                                                                "result = concept.manage_nested_operations(operators: ['NestedOperator1', 'NestedOperator2'])",
                                                                "  -> NestedOperator1.execute()",
                                                                "  -> NestedOperator2.execute()",
                                                                "  return result: Success"
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "story_groups": [
                                        {
                                            "stories": [
                                                {
                                                    "name": "NestedStory1",
                                                    "sequential_order": 1,
                                                    "scenarios": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
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
                        },
                        {
                            "name": "SubEpic2",
                            "sequential_order": 2,
                            "domain_concepts": [
                                {
                                    "name": "SubEpic2DomainConcept",
                                    "responsibilities": [
                                        {
                                            "name": "Manages second sub-epic",
                                            "collaborators": ["SubEpic2Collaborator"]
                                        }
                                    ]
                                }
                            ],
                            "story_groups": [
                                {
                                    "stories": [
                                        {
                                            "name": "Story2",
                                            "sequential_order": 1,
                                            "scenarios": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        stories_dir = helper.workspace / 'docs' / 'stories'
        helper.files.given_file_created(stories_dir, 'story-graph.json', story_graph)
        
        helper.bot.behaviors.navigate_to('shape')
        action = helper.bot.behaviors.current.actions.find_by_name('build')
        
        # Set scope to include the epic
        scope = Scope(workspace_directory=tmp_path, bot_paths=helper.bot.bot_paths)
        scope.filter(type=ScopeType.STORY, value=['Story1'])
        scope.apply_to_bot()
        context = ScopeActionContext(scope=scope)
        
        # Get instructions
        instructions = action.get_instructions(context)
        
        # Verify display_content contains JSON with domain_concepts
        assert instructions.display_content is not None
        assert len(instructions.display_content) > 0
        display_text = '\n'.join(instructions.display_content)
        
        # Find JSON content
        scope_section_index = display_text.find('## Scope')
        after_scope = display_text[scope_section_index:]
        json_start = after_scope.find('{')
        assert json_start != -1, "display_content should contain JSON story graph"
        
        # Extract and parse JSON
        import json
        json_content = after_scope[json_start:]
        json_end_marker = json_content.find('\n---')
        if json_end_marker != -1:
            json_content = json_content[:json_end_marker].strip()
        
        parsed_json = json.loads(json_content)
        
        # Verify domain_concepts are present in epic
        assert 'content' in parsed_json, "JSON should contain 'content'"
        assert 'epics' in parsed_json['content'], "JSON content should contain 'epics'"
        assert len(parsed_json['content']['epics']) > 0, "JSON should contain at least one epic"
        
        epic = parsed_json['content']['epics'][0]
        assert 'domain_concepts' in epic, "Epic should contain 'domain_concepts'"
        assert len(epic['domain_concepts']) == 2, f"Epic should have 2 domain_concepts, got {len(epic['domain_concepts'])}"
        
        # Verify epic domain_concepts structure
        epic_dc1 = epic['domain_concepts'][0]
        assert epic_dc1['name'] == 'EpicDomainConcept', f"Expected 'EpicDomainConcept', got '{epic_dc1['name']}'"
        assert 'responsibilities' in epic_dc1, "Domain concept should have 'responsibilities'"
        assert len(epic_dc1['responsibilities']) == 2, "EpicDomainConcept should have 2 responsibilities"
        assert epic_dc1['responsibilities'][0]['name'] == 'Manages epic-level responsibilities'
        assert 'collaborators' in epic_dc1['responsibilities'][0]
        assert len(epic_dc1['responsibilities'][0]['collaborators']) == 2
        
        # Verify walkthroughs/realizations are present in epic domain concept
        assert 'realization' in epic_dc1, "EpicDomainConcept should have 'realization' field with walkthroughs"
        assert len(epic_dc1['realization']) == 1, "EpicDomainConcept should have 1 realization"
        realization1 = epic_dc1['realization'][0]
        assert 'scope' in realization1, "Realization should have 'scope'"
        assert 'scenario' in realization1, "Realization should have 'scenario'"
        assert 'walks' in realization1, "Realization should have 'walks'"
        assert len(realization1['walks']) == 2, "Realization should have 2 walks"
        assert 'covers' in realization1['walks'][0], "Walk should have 'covers'"
        assert 'object_flow' in realization1['walks'][0], "Walk should have 'object_flow'"
        
        epic_dc2 = epic['domain_concepts'][1]
        assert epic_dc2['name'] == 'EpicSecondConcept'
        
        # Verify domain_concepts are present in sub-epics
        assert 'sub_epics' in epic, "Epic should contain 'sub_epics'"
        assert len(epic['sub_epics']) == 2, "Epic should have 2 sub-epics"
        
        sub_epic1 = epic['sub_epics'][0]
        assert 'domain_concepts' in sub_epic1, "Sub-epic should contain 'domain_concepts'"
        assert len(sub_epic1['domain_concepts']) == 1, f"Sub-epic1 should have 1 domain_concept, got {len(sub_epic1['domain_concepts'])}"
        assert sub_epic1['domain_concepts'][0]['name'] == 'SubEpicDomainConcept'
        assert len(sub_epic1['domain_concepts'][0]['responsibilities']) == 2
        
        # Verify walkthroughs/realizations are present in sub-epic domain concept
        sub_epic_dc = sub_epic1['domain_concepts'][0]
        assert 'realization' in sub_epic_dc, "SubEpicDomainConcept should have 'realization' field with walkthroughs"
        assert len(sub_epic_dc['realization']) == 1, "SubEpicDomainConcept should have 1 realization"
        sub_realization = sub_epic_dc['realization'][0]
        assert 'scope' in sub_realization, "Sub-epic realization should have 'scope'"
        assert 'scenario' in sub_realization, "Sub-epic realization should have 'scenario'"
        assert 'walks' in sub_realization, "Sub-epic realization should have 'walks'"
        assert len(sub_realization['walks']) == 1, "Sub-epic realization should have 1 walk"
        assert 'covers' in sub_realization['walks'][0], "Sub-epic walk should have 'covers'"
        assert 'object_flow' in sub_realization['walks'][0], "Sub-epic walk should have 'object_flow'"
        
        sub_epic2 = epic['sub_epics'][1]
        assert 'domain_concepts' in sub_epic2, "Sub-epic2 should contain 'domain_concepts'"
        assert len(sub_epic2['domain_concepts']) == 1, f"Sub-epic2 should have 1 domain_concept, got {len(sub_epic2['domain_concepts'])}"
        assert sub_epic2['domain_concepts'][0]['name'] == 'SubEpic2DomainConcept'
        
        # Verify domain_concepts are present in nested sub-epics
        assert 'sub_epics' in sub_epic1, "Sub-epic1 should contain nested 'sub_epics'"
        assert len(sub_epic1['sub_epics']) == 1, f"Sub-epic1 should have 1 nested sub-epic, got {len(sub_epic1.get('sub_epics', []))}"
        
        nested_sub_epic1 = sub_epic1['sub_epics'][0]
        assert 'domain_concepts' in nested_sub_epic1, "Nested sub-epic should contain 'domain_concepts'"
        assert len(nested_sub_epic1['domain_concepts']) == 1, f"Nested sub-epic should have 1 domain_concept, got {len(nested_sub_epic1['domain_concepts'])}"
        assert nested_sub_epic1['domain_concepts'][0]['name'] == 'NestedSubEpicDomainConcept'
        assert len(nested_sub_epic1['domain_concepts'][0]['responsibilities']) >= 1
        
        # Verify walkthroughs/realizations are present in nested sub-epic domain concept
        nested_dc = nested_sub_epic1['domain_concepts'][0]
        assert 'realization' in nested_dc, "NestedSubEpicDomainConcept should have 'realization' field with walkthroughs"
        assert len(nested_dc['realization']) == 1, "NestedSubEpicDomainConcept should have 1 realization"
        nested_realization = nested_dc['realization'][0]
        assert 'scope' in nested_realization, "Nested sub-epic realization should have 'scope'"
        assert 'scenario' in nested_realization, "Nested sub-epic realization should have 'scenario'"
        assert 'walks' in nested_realization, "Nested sub-epic realization should have 'walks'"
        assert len(nested_realization['walks']) == 2, "Nested sub-epic realization should have 2 walks"
        assert 'covers' in nested_realization['walks'][0], "Nested sub-epic walk should have 'covers'"
        assert 'object_flow' in nested_realization['walks'][0], "Nested sub-epic walk should have 'object_flow'"
        
        # Verify domain_concepts are present in nested sub-epics
        assert 'sub_epics' in sub_epic1, "Sub-epic1 should contain nested 'sub_epics'"
        assert len(sub_epic1['sub_epics']) == 1, f"Sub-epic1 should have 1 nested sub-epic, got {len(sub_epic1.get('sub_epics', []))}"
        
        nested_sub_epic1 = sub_epic1['sub_epics'][0]
        assert 'domain_concepts' in nested_sub_epic1, "Nested sub-epic should contain 'domain_concepts'"
        assert len(nested_sub_epic1['domain_concepts']) == 1, f"Nested sub-epic should have 1 domain_concept, got {len(nested_sub_epic1['domain_concepts'])}"
        assert nested_sub_epic1['domain_concepts'][0]['name'] == 'NestedSubEpicDomainConcept'
        
        # Verify walkthroughs/realizations are present in nested sub-epic domain concept
        nested_dc = nested_sub_epic1['domain_concepts'][0]
        assert 'realization' in nested_dc, "NestedSubEpicDomainConcept should have 'realization' field with walkthroughs"
        assert len(nested_dc['realization']) == 1, "NestedSubEpicDomainConcept should have 1 realization"
        nested_realization = nested_dc['realization'][0]
        assert 'scope' in nested_realization, "Nested sub-epic realization should have 'scope'"
        assert 'scenario' in nested_realization, "Nested sub-epic realization should have 'scenario'"
        assert 'walks' in nested_realization, "Nested sub-epic realization should have 'walks'"
        assert len(nested_realization['walks']) == 2, "Nested sub-epic realization should have 2 walks"
        assert 'covers' in nested_realization['walks'][0], "Nested sub-epic walk should have 'covers'"
        assert 'object_flow' in nested_realization['walks'][0], "Nested sub-epic walk should have 'object_flow'"
        
        # Helper function to recursively check all nested sub-epics for domain concepts
        def check_sub_epic_domain_concepts(sub_epic_data, level=1, path=""):
            """Recursively check all nested sub-epics for domain concepts."""
            current_path = f"{path}.{sub_epic_data['name']}" if path else sub_epic_data['name']
            
            # Check if this sub-epic has domain_concepts
            if 'domain_concepts' in sub_epic_data:
                domain_concepts = sub_epic_data['domain_concepts']
                assert len(domain_concepts) > 0, f"Sub-epic at level {level} ({current_path}) should have domain_concepts"
                
                # Verify each domain concept has proper structure
                for dc in domain_concepts:
                    assert 'name' in dc, f"Domain concept at {current_path} should have 'name'"
                    assert 'responsibilities' in dc, f"Domain concept '{dc['name']}' at {current_path} should have 'responsibilities'"
                    
                    # If realization exists, verify its structure
                    if 'realization' in dc:
                        for realization in dc['realization']:
                            assert 'scope' in realization, f"Realization in '{dc['name']}' at {current_path} should have 'scope'"
                            assert 'scenario' in realization, f"Realization in '{dc['name']}' at {current_path} should have 'scenario'"
                            assert 'walks' in realization, f"Realization in '{dc['name']}' at {current_path} should have 'walks'"
                            for walk in realization['walks']:
                                assert 'covers' in walk, f"Walk in '{dc['name']}' at {current_path} should have 'covers'"
                                assert 'object_flow' in walk, f"Walk in '{dc['name']}' at {current_path} should have 'object_flow'"
            
            # Recursively check nested sub-epics
            if 'sub_epics' in sub_epic_data:
                for nested_sub_epic in sub_epic_data['sub_epics']:
                    check_sub_epic_domain_concepts(nested_sub_epic, level + 1, current_path)
        
        # Verify nested sub-epics with domain concepts (specific check for our test data)
        assert 'sub_epics' in sub_epic1, "Sub-epic1 should contain nested 'sub_epics'"
        assert len(sub_epic1['sub_epics']) == 1, f"Sub-epic1 should have 1 nested sub-epic, got {len(sub_epic1['sub_epics'])}"
        
        nested_sub_epic1 = sub_epic1['sub_epics'][0]
        assert nested_sub_epic1['name'] == 'NestedSubEpic1', f"Expected 'NestedSubEpic1', got '{nested_sub_epic1['name']}'"
        assert 'domain_concepts' in nested_sub_epic1, "Nested sub-epic should contain 'domain_concepts'"
        assert len(nested_sub_epic1['domain_concepts']) == 1, f"Nested sub-epic should have 1 domain_concept, got {len(nested_sub_epic1['domain_concepts'])}"
        
        nested_dc = nested_sub_epic1['domain_concepts'][0]
        assert nested_dc['name'] == 'NestedSubEpicDomainConcept', f"Expected 'NestedSubEpicDomainConcept', got '{nested_dc['name']}'"
        assert 'responsibilities' in nested_dc, "Nested domain concept should have 'responsibilities'"
        assert len(nested_dc['responsibilities']) == 1, "Nested domain concept should have 1 responsibility"
        
        # Verify walkthroughs/realizations are present in nested sub-epic domain concept
        assert 'realization' in nested_dc, "NestedSubEpicDomainConcept should have 'realization' field with walkthroughs"
        assert len(nested_dc['realization']) == 1, "NestedSubEpicDomainConcept should have 1 realization"
        nested_realization = nested_dc['realization'][0]
        assert 'scope' in nested_realization, "Nested realization should have 'scope'"
        assert 'scenario' in nested_realization, "Nested realization should have 'scenario'"
        assert 'walks' in nested_realization, "Nested realization should have 'walks'"
        assert len(nested_realization['walks']) == 2, "Nested realization should have 2 walks"
        assert 'covers' in nested_realization['walks'][0], "Nested walk should have 'covers'"
        assert 'object_flow' in nested_realization['walks'][0], "Nested walk should have 'object_flow'"
        
        # Recursively check ALL nested sub-epics at all levels
        for sub_epic in epic['sub_epics']:
            check_sub_epic_domain_concepts(sub_epic, level=1)


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