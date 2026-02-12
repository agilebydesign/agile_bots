"""
UpdateReport - Structured report comparing extracted diagram to original story graph.

Lists exact matches, fuzzy matches, new stories, removed stories, and large deletions.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class MatchEntry:
    extracted_name: str
    original_name: str
    match_type: str
    confidence: float = 1.0
    parent: str = ''


@dataclass
class StoryEntry:
    name: str
    parent: str = ''


@dataclass
class LargeDeletions:
    missing_epics: List[str] = field(default_factory=list)
    missing_sub_epics: List[str] = field(default_factory=list)


class UpdateReport:

    def __init__(self):
        self._exact_matches: List[MatchEntry] = []
        self._fuzzy_matches: List[MatchEntry] = []
        self._new_stories: List[StoryEntry] = []
        self._removed_stories: List[StoryEntry] = []
        self._large_deletions = LargeDeletions()

    @property
    def exact_matches(self) -> List[MatchEntry]:
        return list(self._exact_matches)

    @property
    def fuzzy_matches(self) -> List[MatchEntry]:
        return list(self._fuzzy_matches)

    @property
    def new_stories(self) -> List[StoryEntry]:
        return list(self._new_stories)

    @property
    def removed_stories(self) -> List[StoryEntry]:
        return list(self._removed_stories)

    @property
    def large_deletions(self) -> LargeDeletions:
        return self._large_deletions

    def add_exact_match(self, extracted_name: str, original_name: str, parent: str = ''):
        self._exact_matches.append(
            MatchEntry(extracted_name=extracted_name, original_name=original_name,
                       match_type='exact', confidence=1.0, parent=parent))

    def add_fuzzy_match(self, extracted_name: str, original_name: str,
                        confidence: float, parent: str = ''):
        self._fuzzy_matches.append(
            MatchEntry(extracted_name=extracted_name, original_name=original_name,
                       match_type='fuzzy', confidence=confidence, parent=parent))

    def add_new_story(self, name: str, parent: str = ''):
        self._new_stories.append(StoryEntry(name=name, parent=parent))

    def add_removed_story(self, name: str, parent: str = ''):
        self._removed_stories.append(StoryEntry(name=name, parent=parent))

    def add_missing_epic(self, epic_name: str):
        self._large_deletions.missing_epics.append(epic_name)

    def add_missing_sub_epic(self, sub_epic_name: str):
        self._large_deletions.missing_sub_epics.append(sub_epic_name)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'exact_matches': [{'extracted': m.extracted_name, 'original': m.original_name,
                               'confidence': m.confidence, 'parent': m.parent}
                              for m in self._exact_matches],
            'fuzzy_matches': [{'extracted': m.extracted_name, 'original': m.original_name,
                               'confidence': m.confidence, 'parent': m.parent}
                              for m in self._fuzzy_matches],
            'new_stories': [{'name': s.name, 'parent': s.parent} for s in self._new_stories],
            'removed_stories': [{'name': s.name, 'parent': s.parent} for s in self._removed_stories],
            'large_deletions': {
                'missing_epics': self._large_deletions.missing_epics,
                'missing_sub_epics': self._large_deletions.missing_sub_epics
            }
        }

    def save(self, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(self.to_dict(), indent=2), encoding='utf-8')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateReport':
        report = cls()
        for m in data.get('exact_matches', []):
            report.add_exact_match(m['extracted'], m['original'], m.get('parent', ''))
        for m in data.get('fuzzy_matches', []):
            report.add_fuzzy_match(m['extracted'], m['original'], m['confidence'], m.get('parent', ''))
        for s in data.get('new_stories', []):
            report.add_new_story(s['name'], s.get('parent', ''))
        for s in data.get('removed_stories', []):
            report.add_removed_story(s['name'], s.get('parent', ''))
        large = data.get('large_deletions', {})
        for e in large.get('missing_epics', []):
            report.add_missing_epic(e)
        for se in large.get('missing_sub_epics', []):
            report.add_missing_sub_epic(se)
        return report
