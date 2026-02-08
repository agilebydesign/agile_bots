"""
Scenario scanners package.

All scanners related to validating Gherkin scenarios in the story graph.

Domain-aware scanners (inherit ScenarioScannerBase):
- ExampleTableScanner: validates example tables match domain structure
- ScenarioLanguageScanner: validates scenario language uses domain terms

Structural scanners (inherit StoryScanner):
- ScenarioSpecificGivenScanner: scenarios must start with Given
- ScenarioOutlineScanner: Scenario Outlines must have Examples
- ScenariosCoverAllCasesScanner: ensure happy/edge/error cases
- ScenariosOnStoryDocsScanner: stories must have scenarios
- PlainEnglishScenariosScanner: scenarios should be plain English
- BackgroundCommonSetupScanner: background usage validation
- GivenStateNotActionsScanner: Given describes state, not actions
"""

from scanners.scenarios.scenario_scanner_base import ScenarioScannerBase
from scanners.scenarios.example_table_scanner import ExampleTableScanner
from scanners.scenarios.scenario_language_scanner import ScenarioLanguageScanner
from scanners.scenarios.scenario_specific_given_scanner import ScenarioSpecificGivenScanner
from scanners.scenarios.scenario_outline_scanner import ScenarioOutlineScanner
from scanners.scenarios.scenarios_cover_all_cases_scanner import ScenariosCoverAllCasesScanner
from scanners.scenarios.scenarios_on_story_docs_scanner import ScenariosOnStoryDocsScanner
from scanners.scenarios.plain_english_scenarios_scanner import PlainEnglishScenariosScanner
from scanners.scenarios.background_common_setup_scanner import BackgroundCommonSetupScanner
from scanners.scenarios.given_state_not_actions_scanner import GivenStateNotActionsScanner

__all__ = [
    'ScenarioScannerBase',
    'ExampleTableScanner',
    'ScenarioLanguageScanner',
    'ScenarioSpecificGivenScanner',
    'ScenarioOutlineScanner',
    'ScenariosCoverAllCasesScanner',
    'ScenariosOnStoryDocsScanner',
    'PlainEnglishScenariosScanner',
    'BackgroundCommonSetupScanner',
    'GivenStateNotActionsScanner',
]
