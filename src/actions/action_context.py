
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum

from ..scope import Scope, ScopeType, StoryGraphFilter, FileFilter

@dataclass
class ActionContext:
    pass

@dataclass
class ScopeActionContext(ActionContext):
    scope: Optional[Scope] = None

@dataclass
class ClarifyActionContext(ActionContext):
    answers: Optional[Dict[str, Any]] = None
    evidence_provided: Optional[Dict[str, Any]] = None
    context: Optional[str] = None

@dataclass
class StrategyActionContext(ActionContext):
    decisions_made: Optional[Dict[str, Any]] = None
    assumptions: Optional[List[str]] = None
    assumptions_made: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.decisions_made is None:
            object.__setattr__(self, 'decisions_made', {})
        if self.assumptions_made is None:
            object.__setattr__(self, 'assumptions_made', self.assumptions or [])
        if self.assumptions is None:
            object.__setattr__(self, 'assumptions', self.assumptions_made)
    
    def get_decisions(self) -> Dict[str, Any]:
        excluded = {'assumptions', 'assumptions_made', 'decisions_made'}
        decisions = dict(self.decisions_made or {})
        for key, value in self.__dict__.items():
            if key.startswith('_') or key in excluded or value is None:
                continue
            decisions[key] = value
        return decisions
    
    @property
    def assumptions_list(self) -> Optional[List[str]]:
        return self.assumptions or self.assumptions_made
    
    @assumptions_list.setter
    def assumptions_list(self, value: Optional[List[str]]):
        object.__setattr__(self, 'assumptions_made', value)
        object.__setattr__(self, 'assumptions', value)

@dataclass
class ValidateActionContext(ScopeActionContext):
    background: Optional[bool] = None
    skip_cross_file: bool = False
    all_files: bool = False
    force_full: bool = False
    max_cross_file_comparisons: int = 20
    
    def __post_init__(self):
        if self.force_full:
            object.__setattr__(self, 'all_files', True)
        elif self.all_files:
            object.__setattr__(self, 'force_full', True)

@dataclass
class RulesActionContext(ActionContext):
    message: Optional[str] = None

ContextClass = type

