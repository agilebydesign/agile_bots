from typing import Dict, Any
from ...bot_path import BotPath
from .json_persistent import JsonPersistent
from .strategy import Strategy

class StrategyDecision(JsonPersistent):
    
    @staticmethod
    def get_decisions_parameter_description() -> str:
        """Get description for decisions_made/decisions/choices parameter."""
        return "Dict mapping decision criteria keys to selected options/values"
    
    @staticmethod
    def get_assumptions_parameter_description() -> str:
        """Get description for assumptions_made/assumptions parameter."""
        return "List of assumption strings"

    def __init__(self, behavior_name: str, bot_paths: BotPath, strategy: Strategy, decisions_made: Dict[str, Any]=None, assumptions_made: list=None):
        super().__init__(bot_paths, 'strategy.json')
        self.behavior_name = behavior_name
        self.strategy = strategy
        self.decisions_made = decisions_made or {}
        self.assumptions_made = assumptions_made or []

    def save(self):
        existing_data = self.load()
        
        behavior_data = existing_data.get(self.behavior_name, {})
        existing_decisions = behavior_data.get('decisions', {})
        existing_assumptions = behavior_data.get('assumptions', [])
        
        merged_decisions = {**existing_decisions, **self.decisions_made}
        
        merged_assumptions = self.assumptions_made if self.assumptions_made else existing_assumptions
        
        new_data = {
            'decisions': merged_decisions,
            'assumptions': merged_assumptions
        }
        merged_data = self.merge(existing_data, new_data, self.behavior_name)
        super().save(merged_data)

    @classmethod
    def load_all(cls, bot_paths: BotPath) -> Dict[str, Any]:
        instance = cls.__new__(cls)
        instance.bot_paths = bot_paths
        instance.filename = 'strategy.json'
        return instance.load()