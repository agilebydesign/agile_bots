
from typing import Any

class AdapterFactory:
    
    _registry = {
        ('Instructions', 'json'): ('instructions.json_instructions', 'JSONInstructions'),
        ('Instructions', 'tty'): ('instructions.tty_instructions', 'TTYInstructions'),
        ('Instructions', 'markdown'): ('instructions.markdown_instructions', 'MarkdownInstructions'),
        
        ('Guardrails', 'tty'): ('actions.guardrails.tty_guardrails', 'TTYGuardrails'),
        ('RequiredContext', 'tty'): ('actions.guardrails.tty_required_context', 'TTYRequiredContext'),
        ('Strategy', 'tty'): ('actions.guardrails.tty_strategy', 'TTYStrategy'),
        
        ('Scope', 'json'): ('scope.json_scope', 'JSONScope'),
        ('Scope', 'tty'): ('scope.tty_scope', 'TTYScope'),
        ('Scope', 'markdown'): ('scope.markdown_scope', 'MarkdownScope'),
        
        ('ScopeCommandResult', 'json'): ('scope.json_scope_command_result', 'JSONScopeCommandResult'),
        ('ScopeCommandResult', 'tty'): ('scope.tty_scope_command_result', 'TTYScopeCommandResult'),
        ('ScopeCommandResult', 'markdown'): ('scope.markdown_scope_command_result', 'MarkdownScopeCommandResult'),
        
        ('NavigationResult', 'json'): ('navigation.json_navigation', 'JSONNavigation'),
        ('NavigationResult', 'tty'): ('navigation.tty_navigation', 'TTYNavigation'),
        ('NavigationResult', 'markdown'): ('navigation.markdown_navigation', 'MarkdownNavigation'),
        
        ('BotPath', 'json'): ('bot_path.json_bot_path', 'JSONBotPath'),
        ('BotPath', 'tty'): ('bot_path.tty_bot_path', 'TTYBotPath'),
        ('BotPath', 'markdown'): ('bot_path.markdown_bot_path', 'MarkdownBotPath'),
        ('BotPaths', 'json'): ('bot_path.json_bot_path', 'JSONBotPath'),
        ('BotPaths', 'tty'): ('bot_path.tty_bot_path', 'TTYBotPath'),
        ('BotPaths', 'markdown'): ('bot_path.markdown_bot_path', 'MarkdownBotPath'),
        
        ('Help', 'json'): ('help.json_help', 'JSONHelp'),
        ('Help', 'tty'): ('help.tty_help', 'TTYHelp'),
        ('Help', 'markdown'): ('help.markdown_help', 'MarkdownHelp'),
        
        ('ExitResult', 'json'): ('exit_result.json_exit_result', 'JSONExitResult'),
        ('ExitResult', 'tty'): ('exit_result.tty_exit_result', 'TTYExitResult'),
        ('ExitResult', 'markdown'): ('exit_result.markdown_exit_result', 'MarkdownExitResult'),
        
        ('Bot', 'json'): ('bot.json_bot', 'JSONBot'),
        ('Bot', 'tty'): ('bot.tty_bot', 'TTYBot'),
        ('Bot', 'markdown'): ('bot.markdown_bot', 'MarkdownBot'),
        
        ('Behavior', 'json'): ('behaviors.json_behavior', 'JSONBehavior'),
        ('Behavior', 'tty'): ('behaviors.tty_behavior', 'TTYBehavior'),
        ('Behavior', 'markdown'): ('behaviors.markdown_behavior', 'MarkdownBehavior'),
        
        ('Behaviors', 'json'): ('behaviors.json_behavior', 'JSONBehaviors'),
        ('Behaviors', 'tty'): ('behaviors.tty_behavior', 'TTYBehaviors'),
        ('Behaviors', 'markdown'): ('behaviors.markdown_behavior', 'MarkdownBehaviors'),
        
        ('Actions', 'json'): ('actions.json_actions', 'JSONActions'),
        ('Actions', 'tty'): ('actions.tty_actions', 'TTYActions'),
        ('Actions', 'markdown'): ('actions.markdown_actions', 'MarkdownActions'),
        
        ('ValidateRulesAction', 'json'): ('actions.validate.json_validate_action', 'JSONValidateAction'),
        ('ValidateRulesAction', 'tty'): ('actions.validate.tty_validate_action', 'TTYValidateAction'),
        ('ValidateRulesAction', 'markdown'): ('actions.validate.markdown_validate_action', 'MarkdownValidateAction'),
        
        ('BuildStoryGraphAction', 'json'): ('actions.build.json_build_action', 'JSONBuildAction'),
        ('BuildStoryGraphAction', 'tty'): ('actions.build.tty_build_action', 'TTYBuildAction'),
        ('BuildStoryGraphAction', 'markdown'): ('actions.build.markdown_build_action', 'MarkdownBuildAction'),
        
        ('ClarifyContextAction', 'json'): ('actions.clarify.json_clarify_action', 'JSONClarifyAction'),
        ('ClarifyContextAction', 'tty'): ('actions.clarify.tty_clarify_action', 'TTYClarifyAction'),
        ('ClarifyContextAction', 'markdown'): ('actions.clarify.markdown_clarify_action', 'MarkdownClarifyAction'),
        
        ('StrategyAction', 'json'): ('actions.strategy.json_strategy_action', 'JSONStrategyAction'),
        ('StrategyAction', 'tty'): ('actions.strategy.tty_strategy_action', 'TTYStrategyAction'),
        ('StrategyAction', 'markdown'): ('actions.strategy.markdown_strategy_action', 'MarkdownStrategyAction'),
        
        ('RenderOutputAction', 'json'): ('actions.render.json_render_action', 'JSONRenderAction'),
        ('RenderOutputAction', 'tty'): ('actions.render.tty_render_action', 'TTYRenderAction'),
        ('RenderOutputAction', 'markdown'): ('actions.render.markdown_render_action', 'MarkdownRenderAction'),
        
        ('StoryGraph', 'json'): ('story_graph.json_story_graph', 'JSONStoryGraph'),
        ('StoryGraph', 'tty'): ('story_graph.tty_story_graph', 'TTYStoryGraph'),
        ('StoryGraph', 'markdown'): ('story_graph.markdown_story_graph', 'MarkdownStoryGraph'),
    }
    
    @classmethod
    def create(cls, domain_object: Any, channel: str, **kwargs):
        domain_type = type(domain_object).__name__
        
        if domain_type in ('dict', 'list', 'str'):
            if channel == 'json':
                from cli.adapters import GenericJSONAdapter
                return GenericJSONAdapter(domain_object)
            elif channel == 'tty':
                from cli.adapters import GenericTTYAdapter
                return GenericTTYAdapter(domain_object)
            elif channel == 'markdown':
                from cli.adapters import GenericMarkdownAdapter
                return GenericMarkdownAdapter(domain_object)
            else:
                from cli.adapters import GenericJSONAdapter
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
