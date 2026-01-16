
from typing import Any

class AdapterFactory:
    
    _registry = {
        ('Instructions', 'json'): ('agile_bots.src.instructions.json_instructions', 'JSONInstructions'),
        ('Instructions', 'tty'): ('agile_bots.src.instructions.tty_instructions', 'TTYInstructions'),
        ('Instructions', 'markdown'): ('agile_bots.src.instructions.markdown_instructions', 'MarkdownInstructions'),
        
        ('Guardrails', 'tty'): ('agile_bots.src.actions.guardrails.tty_guardrails', 'TTYGuardrails'),
        ('RequiredContext', 'tty'): ('agile_bots.src.actions.guardrails.tty_required_context', 'TTYRequiredContext'),
        ('Strategy', 'tty'): ('agile_bots.src.actions.guardrails.tty_strategy', 'TTYStrategy'),
        
        ('Scope', 'json'): ('agile_bots.src.scope.json_scope', 'JSONScope'),
        ('Scope', 'tty'): ('agile_bots.src.scope.tty_scope', 'TTYScope'),
        ('Scope', 'markdown'): ('agile_bots.src.scope.markdown_scope', 'MarkdownScope'),
        
        ('ScopeCommandResult', 'json'): ('agile_bots.src.scope.json_scope_command_result', 'JSONScopeCommandResult'),
        ('ScopeCommandResult', 'tty'): ('agile_bots.src.scope.tty_scope_command_result', 'TTYScopeCommandResult'),
        ('ScopeCommandResult', 'markdown'): ('agile_bots.src.scope.markdown_scope_command_result', 'MarkdownScopeCommandResult'),
        
        ('NavigationResult', 'json'): ('agile_bots.src.navigation.json_navigation', 'JSONNavigation'),
        ('NavigationResult', 'tty'): ('agile_bots.src.navigation.tty_navigation', 'TTYNavigation'),
        ('NavigationResult', 'markdown'): ('agile_bots.src.navigation.markdown_navigation', 'MarkdownNavigation'),
        
        ('BotPath', 'json'): ('agile_bots.src.bot_path.json_bot_path', 'JSONBotPath'),
        ('BotPath', 'tty'): ('agile_bots.src.bot_path.tty_bot_path', 'TTYBotPath'),
        ('BotPath', 'markdown'): ('agile_bots.src.bot_path.markdown_bot_path', 'MarkdownBotPath'),
        ('BotPaths', 'json'): ('agile_bots.src.bot_path.json_bot_path', 'JSONBotPath'),
        ('BotPaths', 'tty'): ('agile_bots.src.bot_path.tty_bot_path', 'TTYBotPath'),
        ('BotPaths', 'markdown'): ('agile_bots.src.bot_path.markdown_bot_path', 'MarkdownBotPath'),
        
        ('Help', 'json'): ('agile_bots.src.help.json_help', 'JSONHelp'),
        ('Help', 'tty'): ('agile_bots.src.help.tty_help', 'TTYHelp'),
        ('Help', 'markdown'): ('agile_bots.src.help.markdown_help', 'MarkdownHelp'),
        
        ('ExitResult', 'json'): ('agile_bots.src.exit_result.json_exit_result', 'JSONExitResult'),
        ('ExitResult', 'tty'): ('agile_bots.src.exit_result.tty_exit_result', 'TTYExitResult'),
        ('ExitResult', 'markdown'): ('agile_bots.src.exit_result.markdown_exit_result', 'MarkdownExitResult'),
        
        ('Bot', 'json'): ('agile_bots.src.bot.json_bot', 'JSONBot'),
        ('Bot', 'tty'): ('agile_bots.src.bot.tty_bot', 'TTYBot'),
        ('Bot', 'markdown'): ('agile_bots.src.bot.markdown_bot', 'MarkdownBot'),
        
        ('Behavior', 'json'): ('agile_bots.src.behaviors.json_behavior', 'JSONBehavior'),
        ('Behavior', 'tty'): ('agile_bots.src.behaviors.tty_behavior', 'TTYBehavior'),
        ('Behavior', 'markdown'): ('agile_bots.src.behaviors.markdown_behavior', 'MarkdownBehavior'),
        
        ('Behaviors', 'json'): ('agile_bots.src.behaviors.json_behavior', 'JSONBehaviors'),
        ('Behaviors', 'tty'): ('agile_bots.src.behaviors.tty_behavior', 'TTYBehaviors'),
        ('Behaviors', 'markdown'): ('agile_bots.src.behaviors.markdown_behavior', 'MarkdownBehaviors'),
        
        ('Actions', 'json'): ('agile_bots.src.actions.json_actions', 'JSONActions'),
        ('Actions', 'tty'): ('agile_bots.src.actions.tty_actions', 'TTYActions'),
        ('Actions', 'markdown'): ('agile_bots.src.actions.markdown_actions', 'MarkdownActions'),
        
        ('ValidateRulesAction', 'json'): ('agile_bots.src.actions.validate.json_validate_action', 'JSONValidateAction'),
        ('ValidateRulesAction', 'tty'): ('agile_bots.src.actions.validate.tty_validate_action', 'TTYValidateAction'),
        ('ValidateRulesAction', 'markdown'): ('agile_bots.src.actions.validate.markdown_validate_action', 'MarkdownValidateAction'),
        
        ('BuildStoryGraphAction', 'json'): ('agile_bots.src.actions.build.json_build_action', 'JSONBuildAction'),
        ('BuildStoryGraphAction', 'tty'): ('agile_bots.src.actions.build.tty_build_action', 'TTYBuildAction'),
        ('BuildStoryGraphAction', 'markdown'): ('agile_bots.src.actions.build.markdown_build_action', 'MarkdownBuildAction'),
        
        ('ClarifyContextAction', 'json'): ('agile_bots.src.actions.clarify.json_clarify_action', 'JSONClarifyAction'),
        ('ClarifyContextAction', 'tty'): ('agile_bots.src.actions.clarify.tty_clarify_action', 'TTYClarifyAction'),
        ('ClarifyContextAction', 'markdown'): ('agile_bots.src.actions.clarify.markdown_clarify_action', 'MarkdownClarifyAction'),
        
        ('StrategyAction', 'json'): ('agile_bots.src.actions.strategy.json_strategy_action', 'JSONStrategyAction'),
        ('StrategyAction', 'tty'): ('agile_bots.src.actions.strategy.tty_strategy_action', 'TTYStrategyAction'),
        ('StrategyAction', 'markdown'): ('agile_bots.src.actions.strategy.markdown_strategy_action', 'MarkdownStrategyAction'),
        
        ('RenderOutputAction', 'json'): ('agile_bots.src.actions.render.json_render_action', 'JSONRenderAction'),
        ('RenderOutputAction', 'tty'): ('agile_bots.src.actions.render.tty_render_action', 'TTYRenderAction'),
        ('RenderOutputAction', 'markdown'): ('agile_bots.src.actions.render.markdown_render_action', 'MarkdownRenderAction'),
        
        ('StoryGraph', 'json'): ('agile_bots.src.story_graph.json_story_graph', 'JSONStoryGraph'),
        ('StoryGraph', 'tty'): ('agile_bots.src.story_graph.tty_story_graph', 'TTYStoryGraph'),
        ('StoryGraph', 'markdown'): ('agile_bots.src.story_graph.markdown_story_graph', 'MarkdownStoryGraph'),
    }
    
    @classmethod
    def create(cls, domain_object: Any, channel: str, **kwargs):
        domain_type = type(domain_object).__name__
        
        if domain_type in ('dict', 'list', 'str'):
            if channel == 'json':
                from agile_bots.src.cli.adapters import GenericJSONAdapter
                return GenericJSONAdapter(domain_object)
            elif channel == 'tty':
                from agile_bots.src.cli.adapters import GenericTTYAdapter
                return GenericTTYAdapter(domain_object)
            elif channel == 'markdown':
                from agile_bots.src.cli.adapters import GenericMarkdownAdapter
                return GenericMarkdownAdapter(domain_object)
            else:
                from agile_bots.src.cli.adapters import GenericJSONAdapter
                return GenericJSONAdapter(domain_object)
        
        key = (domain_type, channel)
        
        if key not in cls._registry:
            raise ValueError(f"No {channel} adapter registered for {domain_type}")
        
        module_path, class_name = cls._registry[key]
        
        import importlib
        module = importlib.import_module(module_path)
        adapter_class = getattr(module, class_name)
        
        return adapter_class(domain_object, **kwargs)
    
    @classmethod
    def register(cls, domain_type: str, channel: str, module_path: str, class_name: str):
        cls._registry[(domain_type, channel)] = (module_path, class_name)
