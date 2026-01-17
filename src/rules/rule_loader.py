import logging
from pathlib import Path
from typing import List
from rules.rule import Rule

logger = logging.getLogger(__name__)

class RuleLoader:

    def __init__(self, bot_name: str, behavior_name: str, bot_paths, behavior=None):
        self.bot_name = bot_name
        self.behavior_name = behavior_name
        self.bot_paths = bot_paths
        self.behavior = behavior

    def load_bot_rules(self) -> List[Rule]:
        bot_rules_dir = self.bot_paths.bot_directory / 'rules'
        bot_rules = []
        if not bot_rules_dir.exists():
            logger.debug(f'Bot rules directory does not exist: {bot_rules_dir}')
            return bot_rules
        
        for rule_file in bot_rules_dir.glob('*.json'):
            if self._is_in_disabled_folder(rule_file):
                logger.debug(f'Skipping disabled rule: {rule_file.name}')
                continue
            bot_rules.append(self._create_rule(rule_file))
        
        logger.info(f'Loaded {len(bot_rules)} bot-level rules')
        return sorted(bot_rules, key=lambda r: r.priority)

    def load_behavior_rules(self) -> List[Rule]:
        behavior_folder = self.bot_paths.bot_directory / 'behaviors' / self.behavior_name
        behavior_rules_dir = behavior_folder / 'rules'
        behavior_rules = []
        for rule_file in behavior_rules_dir.glob('*.json'):
            if self._is_in_disabled_folder(rule_file):
                logger.debug(f'Skipping disabled rule: {rule_file.name}')
                continue
            behavior_rules.append(self._create_rule(rule_file))
        for subdir_name in ['3_rules', 'rules']:
            subdir = behavior_folder / subdir_name
            if subdir != behavior_rules_dir:
                behavior_rules.extend(self._load_rules_from_subdir(subdir, behavior_rules_dir))
        logger.info(f'Loaded {len(behavior_rules)} behavior rules for {self.behavior_name}')
        return sorted(behavior_rules, key=lambda r: r.priority)

    def _create_rule(self, rule_file: Path) -> Rule:
        return Rule(rule_file_path=rule_file, behavior_name=self.behavior_name, bot_name=self.bot_name)

    def _load_rules_from_subdir(self, subdir: Path, behavior_rules_dir: Path) -> List[Rule]:
        rules = []
        for rule_file in subdir.rglob('*.json'):
            if self._is_in_disabled_folder(rule_file):
                logger.debug(f'Skipping disabled rule: {rule_file.name}')
                continue
            if behavior_rules_dir.exists() and rule_file.is_relative_to(behavior_rules_dir):
                continue
            try:
                rules.append(self._create_rule(rule_file))
            except Exception as e:
                logger.warning(f'Failed to load rule from {rule_file}: {e}')
                continue
        return rules

    def _is_in_disabled_folder(self, file_path: Path) -> bool:
        return 'disabled' in file_path.parts

