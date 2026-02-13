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


@dataclass
class IncrementChange:
    """Delta for a single increment: stories added or removed."""
    name: str
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)


@dataclass
class IncrementMove:
    """A story that moved from one increment to another."""
    story: str
    from_increment: str   # '' means previously unassigned (orphan)
    to_increment: str     # '' means now unassigned (orphan)


class UpdateReport:

    def __init__(self):
        self._renames: List[MatchEntry] = []
        self._new_stories: List[StoryEntry] = []
        self._new_sub_epics: List[StoryEntry] = []
        self._new_epics: List[StoryEntry] = []
        self._removed_stories: List[StoryEntry] = []
        self._removed_sub_epics: List[StoryEntry] = []
        self._removed_epics: List[StoryEntry] = []
        self._large_deletions = LargeDeletions()
        self._matched_count = 0
        self._increment_changes: List[IncrementChange] = []
        self._increment_moves: List[IncrementMove] = []

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
    def new_sub_epics(self) -> List[StoryEntry]:
        return list(self._new_sub_epics)

    @property
    def new_epics(self) -> List[StoryEntry]:
        return list(self._new_epics)

    @property
    def removed_stories(self) -> List[StoryEntry]:
        return list(self._removed_stories)

    @property
    def removed_sub_epics(self) -> List[StoryEntry]:
        return list(self._removed_sub_epics)

    @property
    def removed_epics(self) -> List[StoryEntry]:
        return list(self._removed_epics)

    @property
    def large_deletions(self) -> LargeDeletions:
        return self._large_deletions

    @property
    def matched_count(self) -> int:
        return self._matched_count

    @property
    def increment_changes(self) -> List[IncrementChange]:
        return list(self._increment_changes)

    @property
    def increment_moves(self) -> List[IncrementMove]:
        return list(self._increment_moves)

    def set_increment_changes(self, changes: List[IncrementChange],
                               moves: List[IncrementMove]):
        self._increment_changes = list(changes)
        self._increment_moves = list(moves)

    @property
    def has_changes(self) -> bool:
        return (len(self._renames) > 0 or len(self._new_stories) > 0
                or len(self._new_sub_epics) > 0 or len(self._new_epics) > 0
                or len(self._removed_stories) > 0
                or len(self._removed_sub_epics) > 0 or len(self._removed_epics) > 0
                or len(self._large_deletions.missing_epics) > 0
                or len(self._large_deletions.missing_sub_epics) > 0
                or len(self._increment_changes) > 0
                or len(self._increment_moves) > 0)

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

    def add_new_sub_epic(self, name: str, parent: str = ''):
        self._new_sub_epics.append(StoryEntry(name=name, parent=parent))

    def add_new_epic(self, name: str, parent: str = ''):
        self._new_epics.append(StoryEntry(name=name, parent=parent))

    def add_removed_story(self, name: str, parent: str = ''):
        self._removed_stories.append(StoryEntry(name=name, parent=parent))

    def add_removed_sub_epic(self, name: str, parent: str = ''):
        self._removed_sub_epics.append(StoryEntry(name=name, parent=parent))

    def add_removed_epic(self, name: str, parent: str = ''):
        self._removed_epics.append(StoryEntry(name=name, parent=parent))

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
        if self._new_epics:
            result['new_epics'] = [{'name': s.name, 'parent': s.parent} for s in self._new_epics]
        if self._new_sub_epics:
            result['new_sub_epics'] = [{'name': s.name, 'parent': s.parent} for s in self._new_sub_epics]
        if self._new_stories:
            result['new_stories'] = [{'name': s.name, 'parent': s.parent} for s in self._new_stories]
        if self._removed_epics:
            result['removed_epics'] = [{'name': s.name, 'parent': s.parent} for s in self._removed_epics]
        if self._removed_sub_epics:
            result['removed_sub_epics'] = [{'name': s.name, 'parent': s.parent} for s in self._removed_sub_epics]
        if self._removed_stories:
            result['removed_stories'] = [{'name': s.name, 'parent': s.parent} for s in self._removed_stories]
        if self._large_deletions.missing_epics or self._large_deletions.missing_sub_epics:
            result['large_deletions'] = {
                'missing_epics': self._large_deletions.missing_epics,
                'missing_sub_epics': self._large_deletions.missing_sub_epics
            }
        if self._increment_changes:
            result['increment_changes'] = [
                {k: v for k, v in
                 [('name', c.name),
                  ('added', c.added if c.added else None),
                  ('removed', c.removed if c.removed else None)]
                 if v is not None}
                for c in self._increment_changes
            ]
        if self._increment_moves:
            result['increment_moves'] = [
                {'story': m.story,
                 'from': m.from_increment or '(unassigned)',
                 'to': m.to_increment or '(unassigned)'}
                for m in self._increment_moves
            ]
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
        for s in data.get('new_epics', []):
            report.add_new_epic(s['name'], s.get('parent', ''))
        for s in data.get('new_sub_epics', []):
            report.add_new_sub_epic(s['name'], s.get('parent', ''))
        for s in data.get('new_stories', []):
            report.add_new_story(s['name'], s.get('parent', ''))
        for s in data.get('removed_epics', []):
            report.add_removed_epic(s['name'], s.get('parent', ''))
        for s in data.get('removed_sub_epics', []):
            report.add_removed_sub_epic(s['name'], s.get('parent', ''))
        for s in data.get('removed_stories', []):
            report.add_removed_story(s['name'], s.get('parent', ''))
        large = data.get('large_deletions', {})
        for e in large.get('missing_epics', []):
            report.add_missing_epic(e)
        for se in large.get('missing_sub_epics', []):
            report.add_missing_sub_epic(se)
        for c in data.get('increment_changes', []):
            report._increment_changes.append(
                IncrementChange(
                    name=c['name'],
                    added=c.get('added', []),
                    removed=c.get('removed', [])))
        for m in data.get('increment_moves', []):
            from_inc = m.get('from', '')
            if from_inc == '(unassigned)':
                from_inc = ''
            to_inc = m.get('to', '')
            if to_inc == '(unassigned)':
                to_inc = ''
            report._increment_moves.append(
                IncrementMove(
                    story=m['story'],
                    from_increment=from_inc,
                    to_increment=to_inc))
        return report
