
import json
from cli.adapters import JSONAdapter
from cli.base_hierarchical_adapter import BaseBotAdapter
from bot.bot import Bot

class JSONBot(BaseBotAdapter, JSONAdapter):
    
    def __init__(self, bot: Bot):
        BaseBotAdapter.__init__(self, bot, 'json')
        self.bot = bot
    
    @property
    def name(self):
        return self.bot.name
    
    @property
    def bot_name(self):
        return self.bot.bot_name
    
    @property
    def bot_directory(self):
        return self.bot.bot_directory
    
    @property
    def workspace_directory(self):
        return self.bot.workspace_directory
    
    @property
    def bot_paths(self):
        return self.bot.bot_paths
    
    @property
    def behaviors(self):
        return self.bot.behaviors
    
    def format_header(self) -> str:
        return ""
    
    def format_bot_info(self) -> str:
        return ""
    
    def format_footer(self) -> str:
        return ""
    
    def serialize(self) -> str:
        from utils import sanitize_for_json
        try:
            data = self.to_dict()
            sanitized_data = sanitize_for_json(data)
            return json.dumps(sanitized_data, indent=2, ensure_ascii=True)
        except (ValueError, TypeError) as e:
            # If serialization fails, try to provide more context
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"[JSONBot] Error serializing bot data: {str(e)}")
            # Fallback: try without sanitization (shouldn't happen but just in case)
            return json.dumps(self.to_dict(), indent=2, ensure_ascii=True)
    
    def to_dict(self) -> dict:
        result = {
            'name': self.bot.name,
            'bot_directory': str(self.bot.bot_directory),
            'workspace_directory': str(self.bot.workspace_directory),
            'behavior_names': self.bot.behaviors.names if self.bot.behaviors else [],
            'current_behavior': self.bot.behaviors.current.name if self.bot.behaviors and self.bot.behaviors.current else None,
            'current_action': self.bot.current_action_name if hasattr(self.bot, 'current_action_name') else None,
            'available_bots': self.bot.bots,
            'registered_bots': self.bot.bots
        }
        if self._behaviors_adapter:
            result['behaviors'] = self._behaviors_adapter.to_dict() if hasattr(self._behaviors_adapter, 'to_dict') else {}
        if hasattr(self.bot, 'get_execution_settings'):
            settings = self.bot.get_execution_settings()
            if settings:
                result['execution'] = settings  # e.g. {"shape.clarify": "auto"} for Panel toggles

        if hasattr(self.bot, 'get_special_instructions_settings'):
            si_settings = self.bot.get_special_instructions_settings()
            if si_settings:
                result['special_instructions'] = si_settings

        if hasattr(self.bot, '_scope') and self.bot._scope:
            import time
            # Reload scope from file to ensure we have the latest persisted state
            t0 = time.perf_counter()
            self.bot._scope.load()
            t1 = time.perf_counter()
            from cli.adapter_factory import AdapterFactory
            scope_adapter = AdapterFactory.create(self.bot._scope, 'json')
            result['scope'] = scope_adapter.to_dict(apply_include_level=False)  # Panel/status: fast, no trace
            t2 = time.perf_counter()
            import sys
            msg = f"[PERF] json_bot scope.load: {(t1-t0)*1000:.0f}ms | scope.to_dict: {(t2-t1)*1000:.0f}ms"
            print(msg, file=sys.stderr, flush=True)
            try:
                wp = getattr(self.bot, 'bot_paths', None) and self.bot.bot_paths.workspace_directory
                if wp:
                    (wp / '.cursor').mkdir(parents=True, exist_ok=True)
                    log_file = wp / '.cursor' / 'panel-perf.log'
                    from datetime import datetime
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"{datetime.now().isoformat()} {msg}\n")
            except Exception:
                pass
        
        return result
    
    def deserialize(self, data: str) -> dict:
        from utils import sanitize_json_string
        try:
            # Try parsing as-is first
            return json.loads(data)
        except ValueError as e:
            # If parsing fails due to control characters, sanitize and retry
            if 'control character' in str(e).lower() or 'Invalid' in str(e):
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"[JSONBot] JSON parse error, sanitizing and retrying: {str(e)}")
                sanitized = sanitize_json_string(data)
                return json.loads(sanitized)
            raise
