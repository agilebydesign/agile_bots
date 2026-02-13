import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class MatchEntry:
    extracted_name: str
    original_name: str
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
        self._renames: List[MatchEntry] = []
        self._new_stories: List[StoryEntry] = []
        self._removed_stories: List[StoryEntry] = []
        self._large_deletions = LargeDeletions()
        self._matched_count = 0

    @property
    def renames(self) -> List[MatchEntry]:
        return list(self._renames)

    @property
    def fuzzy_matches(self) -> List[MatchEntry]:
        return self.renames

    @property
    def new_stories(self) -> List[StoryEntry]:
        return list(self._new_stories)

    @property
    def removed_stories(self) -> List[StoryEntry]:
        return list(self._removed_stories)

    @property
    def large_deletions(self) -> LargeDeletions:
        return self._large_deletions

    @property
    def matched_count(self) -> int:
        return self._matched_count

    @property
    def has_changes(self) -> bool:
        return len(self._renames) > 0 or len(self._new_stories) > 0 or len(self._removed_stories) > 0 or len(self._large_deletions.missing_epics) > 0 or len(self._large_deletions.missing_sub_epics) > 0

    def add_exact_match(self, extracted_name: str, original_name: str, parent: str = ''):
        self._matched_count += 1

    def add_rename(self, extracted_name: str, original_name: str,
                   confidence: float, parent: str = ''):
        self._renames.append(
            MatchEntry(extracted_name=extracted_name, original_name=original_name,
                       confidence=confidence, parent=parent))

    def add_fuzzy_match(self, extracted_name: str, original_name: str,
                        confidence: float, parent: str = ''):
        self.add_rename(extracted_name, original_name, confidence, parent)

    def add_new_story(self, name: str, parent: str = ''):
        self._new_stories.append(StoryEntry(name=name, parent=parent))

    def add_removed_story(self, name: str, parent: str = ''):
        self._removed_stories.append(StoryEntry(name=name, parent=parent))

    def add_missing_epic(self, epic_name: str):
        self._large_deletions.missing_epics.append(epic_name)

    def add_missing_sub_epic(self, sub_epic_name: str):
        self._large_deletions.missing_sub_epics.append(sub_epic_name)

    def to_dict(self) -> Dict[str, Any]:
        result = {'matched_count': self._matched_count}
        if self._renames:
            result['renames'] = [{'extracted': m.extracted_name, 'original': m.original_name,
                                  'confidence': m.confidence, 'parent': m.parent}
                                 for m in self._renames]
        if self._new_stories:
            result['new_stories'] = [{'name': s.name, 'parent': s.parent} for s in self._new_stories]
        if self._removed_stories:
            result['removed_stories'] = [{'name': s.name, 'parent': s.parent} for s in self._removed_stories]
        if self._large_deletions.missing_epics or self._large_deletions.missing_sub_epics:
            result['large_deletions'] = {
                'missing_epics': self._large_deletions.missing_epics,
                'missing_sub_epics': self._large_deletions.missing_sub_epics
            }
        if not self.has_changes:
            result['status'] = 'no_changes'
        return result

    def save(self, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(self.to_dict(), indent=2), encoding='utf-8')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UpdateReport':
        report = cls()
        report._matched_count = data.get('matched_count', 0)
        for m in data.get('renames', []):
            report.add_rename(m['extracted'], m['original'], m['confidence'], m.get('parent', ''))
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
