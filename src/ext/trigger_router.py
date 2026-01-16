from pathlib import Path
from typing import Dict, Optional
from ..bot.bot_paths import BotPath
from .bot_matcher import BotMatcher
from .behavior_matcher import BehaviorMatcher
from .trigger_domain import BotTriggers

class TriggerRouter:

    def __init__(self, bot_directory: Path, bot_name: Optional[str]=None, workspace_path: Path=None):
        self.bot_paths = BotPath(bot_directory=bot_directory, workspace_path=workspace_path)
        self.bot_name = bot_name
        self._bot_matcher = BotMatcher(self.bot_paths, bot_name)
        self._behavior_matcher = BehaviorMatcher(self.bot_paths, bot_name)
        if bot_name:
            self._behavior_matcher.load_triggers_for_bot()

    def match_trigger(self, message: str, current_behavior: Optional[str]=None, current_action: Optional[str]=None) -> Optional[Dict[str, str]]:
        message_lower = message.lower().strip()
        target_bot = self._resolve_target_bot(message_lower)
        self._behavior_matcher.bot_name = target_bot
        self._behavior_matcher.load_triggers_for_bot()
        return self._match_in_priority_order(message_lower, current_behavior, current_action, target_bot)

    def _resolve_target_bot(self, message_lower: str) -> str:
        return self.bot_name if self.bot_name else self._bot_matcher.match_bot_from_registry(message_lower)

    def _match_in_priority_order(self, message_lower: str, current_behavior: Optional[str], current_action: Optional[str], target_bot: str) -> Optional[Dict[str, str]]:
        matchers = [lambda: self._behavior_matcher.match_action_explicit(message_lower), lambda: self._behavior_matcher.match_behavior(message_lower, current_action), lambda: self._behavior_matcher.match_close(message_lower), lambda: self._match_bot_only(message_lower, current_behavior, current_action, target_bot)]
        for matcher in matchers:
            route = matcher()
            if route:
                return route
        return None

    def _match_bot_only(self, message: str, current_behavior: Optional[str], current_action: Optional[str], target_bot: str) -> Optional[Dict[str, str]]:
        self._bot_matcher.bot_name = target_bot
        bot_triggers = self._bot_matcher._load_bot_triggers()
        if not bot_triggers or not bot_triggers.patterns:
            return None
        if self._bot_matcher._message_matches_patterns(message, bot_triggers.patterns):
            return {'bot_name': target_bot, 'behavior_name': current_behavior, 'action_name': current_action, 'match_type': 'bot_only'}
        return None
