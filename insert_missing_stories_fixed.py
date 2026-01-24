"""
Insert missing test class stories into story-graph.json
This version properly handles CLI/JSON/TTY acronyms and preserves existing test_file fields
"""
import json
import re
from pathlib import Path

# Load story-graph.json
with open('docs/stories/story-graph.json', 'r', encoding='utf-8') as f:
    story_graph = json.load(f)

# Extract all test_class values from story-graph
def find_test_classes_in_graph(obj, classes=None):
    if classes is None:
        classes = set()
    
    if isinstance(obj, dict):
        if 'test_class' in obj and obj['test_class']:
            classes.add(obj['test_class'])
        for value in obj.values():
            find_test_classes_in_graph(value, classes)
    elif isinstance(obj, list):
        for item in obj:
            find_test_classes_in_graph(item, classes)
    
    return classes

graph_test_classes = find_test_classes_in_graph(story_graph)

# Find sub-epics with their test_file
def find_sub_epics_with_test_files(obj, parent_path="", sub_epics=None):
    if sub_epics is None:
        sub_epics = []
    
    if isinstance(obj, dict):
        if 'name' in obj and 'test_file' in obj and obj.get('test_file'):
            sub_epics.append({
                'name': obj['name'],
                'test_file': obj['test_file'],
                'path': parent_path,
                'object': obj
            })
        for key, value in obj.items():
            new_path = f"{parent_path}/{obj.get('name', '')}" if 'name' in obj else parent_path
            find_sub_epics_with_test_files(value, new_path, sub_epics)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            find_sub_epics_with_test_files(item, f"{parent_path}[{idx}]", sub_epics)
    
    return sub_epics

sub_epics_map = {}
for se in find_sub_epics_with_test_files(story_graph):
    sub_epics_map[se['test_file']] = se

print(f"Found {len(sub_epics_map)} sub-epics with test_file")

# Parse test files to find missing test classes
test_class_pattern = re.compile(r'^class (Test\w+):', re.MULTILINE)

missing_count = 0
added_count = 0

for test_file, sub_epic_info in sorted(sub_epics_map.items()):
    file_path = Path('test') / test_file
    if not file_path.exists():
        continue
    
    content = file_path.read_text(encoding='utf-8')
    file_test_classes = test_class_pattern.findall(content)
    
    for test_class in file_test_classes:
        if test_class in graph_test_classes:
            continue
        
        missing_count += 1
        
        # Extract story info
        class_match = re.search(
            rf'^class {test_class}:.*?(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')?',
            content,
            re.MULTILINE | re.DOTALL
        )
        
        story_name = None
        if class_match:
            docstring = class_match.group(1) or class_match.group(2)
            if docstring:
                story_match = re.search(r'Story:\s*(.+?)(?:\n|$)', docstring, re.IGNORECASE)
                if story_match:
                    story_name = story_match.group(1).strip()
        
        # If no story name in docstring, derive from class name
        if not story_name:
            # Convert TestClarifyRequirementsUsingCLI -> Clarify Requirements Using CLI
            # Handle acronyms like CLI, JSON, TTY properly
            name_parts = re.findall(r'[A-Z][a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', test_class[4:])  # Skip "Test"
            
            # Fix common acronyms
            result_parts = []
            for part in name_parts:
                if part == 'CLI' or part == 'C':
                    # Check if we have L I following
                    if len(result_parts) >= 2 and result_parts[-2:] == ['L', 'I']:
                        result_parts[-2:] = ['CLI']
                        continue
                if part == 'JSON' or part == 'J':
                    if len(result_parts) >= 3 and result_parts[-3:] == ['S', 'O', 'N']:
                        result_parts[-3:] = ['JSON']
                        continue
                if part == 'TTY' or part == 'T':
                    if len(result_parts) >= 2 and result_parts[-2:] == ['T', 'Y']:
                        result_parts[-2:] = ['TTY']
                        continue
                result_parts.append(part)
            
            # Final pass: look for separated acronyms
            final_parts = []
            i = 0
            while i < len(result_parts):
                if i + 2 < len(result_parts) and result_parts[i:i+3] == ['C', 'L', 'I']:
                    final_parts.append('CLI')
                    i += 3
                elif i + 3 < len(result_parts) and result_parts[i:i+4] == ['J', 'S', 'O', 'N']:
                    final_parts.append('JSON')
                    i += 4
                elif i + 2 < len(result_parts) and result_parts[i:i+3] == ['T', 'T', 'Y']:
                    final_parts.append('TTY')
                    i += 3
                else:
                    final_parts.append(result_parts[i])
                    i += 1
            
            story_name = ' '.join(final_parts)
        
        # Find test methods and scenarios
        class_start = content.find(f'class {test_class}:')
        if class_start == -1:
            continue
            
        # Find next class or end of file
        next_class = re.search(r'\nclass \w+:', content[class_start + 1:])
        if next_class:
            class_end = class_start + 1 + next_class.start()
        else:
            class_end = len(content)
        
        class_content = content[class_start:class_end]
        
        # Find all test methods with docstrings
        test_methods = re.findall(
            r'def (test_\w+)\(self.*?\):\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')?',
            class_content,
            re.DOTALL
        )
        
        scenarios = []
        for idx, (method_name, docstring1, docstring2) in enumerate(test_methods, 1):
            docstring = (docstring1 or docstring2 or "").strip()
            
            scenario_name = None
            scenario_steps = ""
            
            if docstring:
                # Extract SCENARIO
                scenario_match = re.search(r'SCENARIO:\s*(.+?)(?:\n|$)', docstring, re.IGNORECASE)
                if scenario_match:
                    scenario_name = scenario_match.group(1).strip()
                
                # Extract GIVEN/WHEN/THEN steps
                steps_lines = []
                for line in docstring.split('\n'):
                    line = line.strip()
                    if re.match(r'^(GIVEN|WHEN|THEN|AND):', line, re.IGNORECASE):
                        steps_lines.append(line)
                scenario_steps = '\n'.join(steps_lines)
            
            # If no scenario name, derive from method name
            if not scenario_name:
                # Convert test_clarify_action_shows_questions -> Clarify action shows questions
                name_parts = method_name.replace('test_', '').replace('_', ' ')
                scenario_name = name_parts.capitalize()
            
            scenarios.append({
                "name": scenario_name,
                "sequential_order": float(idx),
                "type": "happy_path" if not any(x in method_name.lower() for x in ['error', 'invalid', 'fail']) else "error",
                "background": [],
                "test_method": method_name,
                "steps": scenario_steps
            })
        
        # Determine story type and user
        story_type = "user"
        users = ["User"] if "CLI" in story_name or "Panel" in story_name else ["Bot Behavior"]
        
        # Get existing stories count for sequential_order
        story_groups = sub_epic_info['object'].get('story_groups', [])
        if story_groups and len(story_groups) > 0 and 'stories' in story_groups[0]:
            existing_stories = story_groups[0].get('stories', [])
            next_order = len(existing_stories)
        else:
            next_order = 0
        
        # Create story structure - DON'T override test_file, leave as None
        # The sub-epic already has test_file set, stories inherit from parent
        story_json = {
            "name": story_name,
            "sequential_order": float(next_order),
            "connector": "or" if "Bot Behavior" in users else None,
            "story_type": story_type,
            "users": users,
            "test_file": None,  # Stories don't have test_file, they inherit from sub-epic
            "test_class": test_class,
            "scenarios": scenarios,
            "scenario_outlines": [],
            "acceptance_criteria": []
        }
        
        # Add story to the sub-epic
        if 'story_groups' not in sub_epic_info['object']:
            sub_epic_info['object']['story_groups'] = [{"name": "", "sequential_order": 0.0, "type": "and", "connector": None, "stories": []}]
        
        if not sub_epic_info['object']['story_groups']:
            sub_epic_info['object']['story_groups'].append({"name": "", "sequential_order": 0.0, "type": "and", "connector": None, "stories": []})
        
        if 'stories' not in sub_epic_info['object']['story_groups'][0]:
            sub_epic_info['object']['story_groups'][0]['stories'] = []
        
        sub_epic_info['object']['story_groups'][0]['stories'].append(story_json)
        added_count += 1
        
        print(f"Added: {story_name} ({test_class}) to {sub_epic_info['name']}")

# Save updated story-graph.json
with open('docs/stories/story-graph.json', 'w', encoding='utf-8') as f:
    json.dump(story_graph, f, indent=2, ensure_ascii=False)

print()
print("=" * 80)
print(f"Total missing test classes found: {missing_count}")
print(f"Total stories added: {added_count}")
print("=" * 80)
print("\nstory-graph.json has been updated!")
