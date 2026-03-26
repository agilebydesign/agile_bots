
import json
from cli.adapters import JSONAdapter
from actions.strategy.strategy_action import StrategyAction

class JSONStrategyAction(JSONAdapter):
    
    def __init__(self, action: StrategyAction, is_current: bool = False, is_completed: bool = False):
        self.action = action
        self.is_current = is_current
        self.is_completed = is_completed
    
    @property
    def action_name(self):
        return self.action.action_name
    
    @property
    def description(self):
        return self.action.description
    
    @property
    def order(self):
        return self.action.order
    
    @property
    def next_action(self):
        return self.action.next_action
    
    @property
    def workflow(self):
        return self.action.workflow
    
    @property
    def auto_confirm(self):
        return self.action.auto_confirm
    
    @property
    def skip_confirm(self):
        return self.action.skip_confirm
    
    @property
    def behavior(self):
        return self.action.behavior
    
    @property
    def strategy(self):
        return self.action.strategy
    
    @property
    def strategy_criteria(self):
        return self.action.strategy_criteria
    
    @property
    def typical_assumptions(self):
        return self.action.typical_assumptions
    
    def to_dict(self) -> dict:
        result = {
            'action_name': self.action.action_name,
            'description': self.action.description,
            'order': self.action.order,
            'next_action': self.action.next_action,
            'workflow': self.action.workflow,
            'auto_confirm': self.action.auto_confirm,
            'skip_confirm': self.action.skip_confirm,
            'behavior': self.action.behavior.name if self.action.behavior else None,
        }
        
        if self.action.strategy:
            from actions.strategy.strategy_decision import StrategyDecision
            saved_data = StrategyDecision.load_all(self.action.behavior.bot_paths)
            
            behavior_data = saved_data.get(self.action.behavior.name, {}) if saved_data else {}
            saved_decisions = behavior_data.get('decisions', {})
            saved_assumptions = behavior_data.get('additional_strategies') or behavior_data.get('assumptions', [])
            
            serialized_criteria = {}
            
            if self.action.strategy_criteria:
                for key, criteria in self.action.strategy_criteria.items():
                    if hasattr(criteria, 'to_dict'):
                        serialized_criteria[key] = criteria.to_dict()
                    else:
                        serialized_criteria[key] = {
                            'question': criteria.question if hasattr(criteria, 'question') else '',
                            'options': criteria.options if hasattr(criteria, 'options') else [],
                            'outcome': criteria.outcome if hasattr(criteria, 'outcome') else None
                        }
            
            result['strategy'] = {
                'criteria_count': len(self.action.strategy_criteria) if self.action.strategy_criteria else 0,
                'assumptions_count': len(self.action.typical_assumptions) if self.action.typical_assumptions else 0,
                'strategy_criteria': {
                    'criteria': serialized_criteria,
                    'decisions_made': saved_decisions
                },
                'assumptions': {
                    'assumptions_made': saved_assumptions
                }
            }
            
            if self.action.strategy_criteria:
                criteria_dict = self.action.strategy_criteria
                if isinstance(criteria_dict, dict):
                    result['strategy_criteria'] = [
                        {
                            'id': key,
                            'question': criteria.question if hasattr(criteria, 'question') else '',
                            'options': getattr(criteria, 'options', []) if hasattr(criteria, 'options') else [],
                            'criteria': getattr(criteria, 'question', '') if hasattr(criteria, 'question') else '',
                            'selected': saved_decisions.get(key)
                        }
                        for key, criteria in criteria_dict.items()
                    ]
            
            if self.action.typical_assumptions:
                result['typical_assumptions'] = self.action.typical_assumptions
        
        return result
    
    def deserialize(self, data: str) -> dict:
        return json.loads(data)
