from pathlib import Path
from typing import Dict
from ...utils import read_json_file
from .strategy_criteria import StrategyCriteria

class StrategyCriterias:

    def __init__(self, strategy_dir: Path):
        self._strategy_dir = strategy_dir
        self._strategy_criterias: Dict[str, StrategyCriteria] = {}
        self._load_strategy_criterias()

    def _load_strategy_criterias(self):
        criteria_dir = self._strategy_dir / 'decision_criteria'
        if not criteria_dir.exists():
            return
        for criteria_file in criteria_dir.glob('*.json'):
            criteria_data = read_json_file(criteria_file)
            criteria_key = criteria_file.stem
            self._strategy_criterias[criteria_key] = StrategyCriteria(criteria_data)

    @property
    def strategy_criterias(self) -> Dict[str, StrategyCriteria]:
        return self._strategy_criterias