from pathlib import Path
from typing import Dict, Any
from .strategy_criterias import StrategyCriterias
from .assumptions import Assumptions

class Strategy:

    def __init__(self, behavior_folder: Path):
        strategy_dir = behavior_folder / 'guardrails' / 'strategy'
        self.strategy_criterias = StrategyCriterias(strategy_dir)
        self.assumptions = Assumptions(strategy_dir)

    @property
    def instructions(self) -> Dict[str, Any]:
        strategy_criteria_dict = {}
        for key, criteria in self.strategy_criterias.strategy_criterias.items():
            strategy_criteria_dict[key] = {'question': criteria.question, 'options': criteria.options, 'outcome': criteria.outcome}
        return {'strategy_criteria': strategy_criteria_dict, 'assumptions': self.assumptions.assumptions}