from typing import List


class GuidanceLineCollection:
    """Collection class for guidance lines"""
    def __init__(self, lines: List[str]):
        self._lines = lines
    
    def add_to_instructions(self, instructions) -> None:
        for line in self._lines:
            instructions.add(line)


class RulesDigestGuidance:
    
    @property
    def lines(self) -> List[str]:
        return [
            'CRITICAL: The rules digest above contains everything you need to get started.',
            '',
            'WORKFLOW:',
            '1. Read the rules digest above (descriptions + key principles)',
            "2. Apply rules to the user's request",
            '3. IF you need clarity on a specific rule (examples, edge cases, detailed patterns):',
            '   - Use read_file tool to read that specific rule file',
            '   - The full rule has detailed examples and detection patterns',
            '4. Cite rule names when making decisions',
            '',
            'The digest gives you 80% of what you need. Only read full rule files when you need the remaining 20%.',
            '',
            'When analyzing code, focus on finding violations and cite the specific rule names.'
        ]
    
    def add_to(self, instructions) -> None:
        # Delegate to collection class
        collection = GuidanceLineCollection(self.lines)
        collection.add_to_instructions(instructions)



