#!/usr/bin/env python3
"""
Story-Test Mapping Synchronization Tool

This script automatically maps stories in the story graph to their corresponding
test classes by analyzing story names and test class names. It generates a report
that can be reviewed before applying the mappings.

Usage:
    # Generate report only (dry run)
    python scripts/sync_story_test_mappings.py
    
    # Apply mappings after review
    python scripts/sync_story_test_mappings.py --apply
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class StoryTestMapper:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.test_dir = base_path / "test"
        self.story_graph_path = base_path / "docs" / "stories" / "story-graph.json"
        self.test_classes: Dict[str, Tuple[str, int]] = {}  # {class_name: (file_name, line_number)}
        self.mappings: List[Dict] = []
        self.unmapped_stories: List[Dict] = []
        self.unmapped_tests: List[str] = []
        
    def normalize_name(self, name: str) -> str:
        """Normalize a name for comparison by removing common words and formatting."""
        # Remove common prefixes/suffixes
        name = re.sub(r'^(test_|Test)', '', name, flags=re.IGNORECASE)
        # Convert from snake_case or PascalCase to space-separated lowercase
        name = re.sub(r'_', ' ', name)
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        # Remove common words
        common_words = ['for', 'the', 'a', 'an', 'to', 'from', 'with', 'and', 'or', 'as', 'part', 'of']
        words = [w.lower() for w in name.split() if w.lower() not in common_words]
        return ' '.join(words)
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)."""
        norm1 = self.normalize_name(str1)
        norm2 = self.normalize_name(str2)
        
        # Exact match after normalization
        if norm1 == norm2:
            return 1.0
        
        # Check if one contains the other
        if norm1 in norm2 or norm2 in norm1:
            return 0.9
        
        # Check word overlap
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0
    
    def scan_test_files(self):
        """Scan all test files and extract test class names and line numbers."""
        print(f"Scanning test directory: {self.test_dir}")
        
        test_files = list(self.test_dir.glob("test_*.py"))
        print(f"Found {len(test_files)} test files")
        
        for test_file in test_files:
            file_name = test_file.name
            print(f"  Scanning {file_name}...")
            
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, start=1):
                    # Match class definitions: "class TestSomething:"
                    match = re.match(r'^class (Test\w+):', line)
                    if match:
                        class_name = match.group(1)
                        self.test_classes[class_name] = (file_name, line_num)
                        
            except Exception as e:
                print(f"    Warning: Error reading {file_name}: {e}")
        
        print(f"\nFound {len(self.test_classes)} test classes")
    
    def find_best_match(self, story_name: str, test_file: Optional[str] = None) -> Optional[Tuple[str, str, int, float]]:
        """
        Find the best matching test class for a story.
        
        Returns: (test_class, test_file, line_number, similarity_score) or None
        """
        best_match = None
        best_score = 0.0
        
        for class_name, (file_name, line_num) in self.test_classes.items():
            # If test_file is specified, only consider classes from that file
            if test_file and file_name != test_file:
                continue
            
            score = self.calculate_similarity(story_name, class_name)
            
            if score > best_score and score >= 0.7:  # Minimum threshold
                best_score = score
                best_match = (class_name, file_name, line_num, score)
        
        return best_match
    
    def process_story_graph(self):
        """Process the story graph and find mappings."""
        print(f"\nLoading story graph: {self.story_graph_path}")
        
        with open(self.story_graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for epic in data.get('epics', []):
            self._process_epic(epic)
    
    def _process_epic(self, epic: Dict):
        """Process an epic and its sub-epics/stories."""
        epic_name = epic.get('name', 'Unknown')
        print(f"\n{'='*80}")
        print(f"Processing Epic: {epic_name}")
        print(f"{'='*80}")
        
        # Process sub-epics
        for sub_epic in epic.get('sub_epics', []):
            self._process_sub_epic(sub_epic, epic_name)
    
    def _process_sub_epic(self, sub_epic: Dict, epic_name: str):
        """Process a sub-epic and its stories."""
        sub_epic_name = sub_epic.get('name', 'Unknown')
        test_file = sub_epic.get('test_file')
        
        print(f"\n  Sub-Epic: {sub_epic_name}")
        if test_file:
            print(f"    Default test file: {test_file}")
        
        # Process all story groups
        for story_group in sub_epic.get('story_groups', []):
            for story in story_group.get('stories', []):
                self._process_story(story, epic_name, sub_epic_name, test_file)
    
    def _process_story(self, story: Dict, epic_name: str, sub_epic_name: str, default_test_file: Optional[str]):
        """Process a single story and find its test mapping."""
        story_name = story.get('name', 'Unknown')
        current_test_file = story.get('test_file')
        current_test_class = story.get('test_class')
        
        # Use story's test_file if available, otherwise use sub-epic's default
        test_file = current_test_file or default_test_file
        
        print(f"\n    Story: {story_name}")
        
        if current_test_class:
            print(f"      [OK] Already mapped: {current_test_class} in {current_test_file}")
            # Verify the mapping exists
            if current_test_class not in self.test_classes:
                print(f"        [WARNING] Test class {current_test_class} not found in codebase!")
            return
        
        # Try to find a match
        match = self.find_best_match(story_name, test_file)
        
        if match:
            test_class, matched_file, line_num, score = match
            print(f"      -> Suggested mapping: {test_class} in {matched_file} (line {line_num}, score: {score:.2f})")
            
            self.mappings.append({
                'epic': epic_name,
                'sub_epic': sub_epic_name,
                'story': story_name,
                'test_file': matched_file,
                'test_class': test_class,
                'line_number': line_num,
                'confidence': score,
                'story_object': story  # Keep reference for updating
            })
        else:
            print(f"      [X] No matching test class found")
            self.unmapped_stories.append({
                'epic': epic_name,
                'sub_epic': sub_epic_name,
                'story': story_name,
                'expected_test_file': test_file
            })
    
    def generate_report(self, output_file: Path):
        """Generate a detailed report of mappings."""
        print(f"\n{'='*80}")
        print("GENERATING REPORT")
        print(f"{'='*80}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Story-Test Mapping Report\n")
            f.write("=" * 80 + "\n\n")
            
            # Summary
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total test classes found: {len(self.test_classes)}\n")
            f.write(f"New mappings suggested: {len(self.mappings)}\n")
            f.write(f"Unmapped stories: {len(self.unmapped_stories)}\n")
            f.write("\n")
            
            # Suggested mappings
            if self.mappings:
                f.write("\nSUGGESTED MAPPINGS\n")
                f.write("-" * 80 + "\n")
                for mapping in sorted(self.mappings, key=lambda x: (x['epic'], x['sub_epic'], x['story'])):
                    f.write(f"\nEpic: {mapping['epic']}\n")
                    f.write(f"Sub-Epic: {mapping['sub_epic']}\n")
                    f.write(f"Story: {mapping['story']}\n")
                    f.write(f"  → Test Class: {mapping['test_class']}\n")
                    f.write(f"  → Test File: {mapping['test_file']}\n")
                    f.write(f"  → Line: {mapping['line_number']}\n")
                    f.write(f"  → Confidence: {mapping['confidence']:.2%}\n")
            
            # Unmapped stories
            if self.unmapped_stories:
                f.write("\n\nUNMAPPED STORIES (Need Test Implementation)\n")
                f.write("-" * 80 + "\n")
                for story in sorted(self.unmapped_stories, key=lambda x: (x['epic'], x['sub_epic'], x['story'])):
                    f.write(f"\nEpic: {story['epic']}\n")
                    f.write(f"Sub-Epic: {story['sub_epic']}\n")
                    f.write(f"Story: {story['story']}\n")
                    if story['expected_test_file']:
                        f.write(f"  Expected test file: {story['expected_test_file']}\n")
            
            # Identify test classes that aren't mapped to any story
            mapped_test_classes = set()
            # Load story graph to get all existing mappings
            with open(self.story_graph_path, 'r', encoding='utf-8') as sg:
                data = json.load(sg)
                self._collect_mapped_test_classes(data, mapped_test_classes)
            
            # Add newly mapped classes
            for mapping in self.mappings:
                mapped_test_classes.add(mapping['test_class'])
            
            unmapped_test_classes = set(self.test_classes.keys()) - mapped_test_classes
            
            if unmapped_test_classes:
                f.write("\n\nUNMAPPED TEST CLASSES (No Story Found)\n")
                f.write("-" * 80 + "\n")
                for test_class in sorted(unmapped_test_classes):
                    file_name, line_num = self.test_classes[test_class]
                    f.write(f"\nTest Class: {test_class}\n")
                    f.write(f"  File: {file_name}\n")
                    f.write(f"  Line: {line_num}\n")
        
        print(f"\nReport generated: {output_file}")
    
    def _collect_mapped_test_classes(self, data: Dict, mapped_classes: set):
        """Recursively collect all test classes that are already mapped."""
        for epic in data.get('epics', []):
            for sub_epic in epic.get('sub_epics', []):
                for story_group in sub_epic.get('story_groups', []):
                    for story in story_group.get('stories', []):
                        test_class = story.get('test_class')
                        if test_class:
                            mapped_classes.add(test_class)
    
    def apply_mappings(self):
        """Apply the suggested mappings to the story graph."""
        print(f"\n{'='*80}")
        print("APPLYING MAPPINGS")
        print(f"{'='*80}\n")
        
        with open(self.story_graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        applied_count = 0
        for mapping in self.mappings:
            # Update the story object
            story = mapping['story_object']
            story['test_file'] = mapping['test_file']
            story['test_class'] = mapping['test_class']
            applied_count += 1
            print(f"[OK] Applied: {mapping['story']} -> {mapping['test_class']}")
        
        # Save updated story graph
        with open(self.story_graph_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Applied {applied_count} mappings to story graph")
        print(f"[OK] Updated: {self.story_graph_path}")


def main():
    parser = argparse.ArgumentParser(description='Sync story-test mappings')
    parser.add_argument('--apply', action='store_true', 
                       help='Apply the suggested mappings (default: dry run)')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Auto-confirm without prompting')
    parser.add_argument('--output', type=str, default='story_test_mapping_report.txt',
                       help='Output report file name')
    args = parser.parse_args()
    
    # Determine base path (assuming script is in scripts/ directory)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent
    
    print(f"Base path: {base_path}")
    
    # Create mapper and run
    mapper = StoryTestMapper(base_path)
    
    # Step 1: Scan test files
    mapper.scan_test_files()
    
    # Step 2: Process story graph and find mappings
    mapper.process_story_graph()
    
    # Step 3: Generate report
    output_path = base_path / args.output
    mapper.generate_report(output_path)
    
    # Step 4: Apply mappings if requested
    if args.apply:
        print("\n[WARNING] This will modify the story graph file!")
        if not args.yes:
            response = input("Are you sure you want to apply these mappings? (yes/no): ")
            if response.lower() != 'yes':
                print("Mapping application cancelled.")
                return
        else:
            print("Auto-confirming with --yes flag")
        mapper.apply_mappings()
    else:
        print("\n" + "="*80)
        print("DRY RUN - No changes made")
        print("="*80)
        print(f"\nReview the report: {output_path}")
        print("To apply these mappings, run:")
        print(f"  python scripts/sync_story_test_mappings.py --apply")


if __name__ == "__main__":
    main()
