from typing import Dict, Any, List, Optional

class StrategyCriteria:

    def __init__(self, criteria_data: Dict[str, Any]):
        self.question = criteria_data.get('question', '')
        self.options = self._format_options(criteria_data.get('options', []))
        self.outcome = criteria_data.get('outcome', None)

    def _format_options(self, options: List[Any]) -> List[Any]:
        formatted_options = []
        for option in options:
            if isinstance(option, dict):
                formatted_option = option.copy()
                if 'example' in formatted_option and isinstance(formatted_option['example'], list):
                    formatted_option['example'] = self._format_example(formatted_option['example'])
                formatted_options.append(formatted_option)
            else:
                formatted_options.append(option)
        return formatted_options

    def _format_example(self, example_lines: List[str]) -> str:
        return '\n'.join(example_lines)

    @property
    def question(self) -> str:
        return self._question

    @question.setter
    def question(self, value: str):
        self._question = value

    @property
    def options(self) -> List[Any]:
        return self._options

    @options.setter
    def options(self, value: List[Any]):
        self._options = value

    @property
    def outcome(self) -> Optional[Any]:
        return self._outcome

    @outcome.setter
    def outcome(self, value: Optional[Any]):
        self._outcome = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            'question': self.question,
            'options': self.options,
            'outcome': self.outcome
        }