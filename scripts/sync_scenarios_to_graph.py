"""
Sync scenario markdown files back into story-graph.json.
Reads fixed markdown files, extracts steps, examples tables, and background,
then updates the corresponding scenarios in story-graph.json.
"""
import json
import re
import sys
from pathlib import Path

STORY_GRAPH_PATH = Path(__file__).parent.parent / "docs" / "story" / "story-graph.json"
SCENARIOS_DIR = Path(__file__).parent.parent / "docs" / "story" / "scenarios"


def parse_markdown_tables(text):
    """Extract markdown tables from text. Returns list of {name, columns, rows}."""
    tables = []
    lines = text.split('\n')
    i = 0
    current_table_name = None
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Table header bold name like **DrawIOEpic:** or **DrawIOSubEpic:**
        if line.startswith('**') and line.endswith(':**'):
            current_table_name = line.strip('*').strip(':').strip()
            i += 1
            continue
        
        # Table header row (starts with |)
        if line.startswith('|') and '---' not in line:
            # Check if next line is separator
            if i + 1 < len(lines) and '---' in lines[i + 1]:
                columns = [c.strip() for c in line.strip('|').split('|')]
                columns = [c for c in columns if c]
                i += 2  # skip header and separator
                
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    row_line = lines[i].strip()
                    if '---' in row_line:
                        i += 1
                        continue
                    row_values = [c.strip() for c in row_line.strip('|').split('|')]
                    row_values = [c for c in row_values if c != '']
                    if row_values:
                        rows.append(row_values)
                    i += 1
                
                table = {
                    "name": current_table_name or "",
                    "columns": columns,
                    "rows": rows
                }
                tables.append(table)
                current_table_name = None
                continue
        
        i += 1
    
    return tables


def parse_gherkin_steps(gherkin_block):
    """Extract steps from a gherkin code block."""
    steps = []
    order = 1.0
    for line in gherkin_block.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('```'):
            steps.append({
                "text": line,
                "sequential_order": order
            })
            order += 1.0
    return steps


def parse_scenario_section(section_text):
    """Parse a single scenario section into steps and examples."""
    result = {
        "steps": [],
        "examples": []
    }
    
    # Extract gherkin block
    gherkin_match = re.search(r'```gherkin\n(.*?)```', section_text, re.DOTALL)
    if gherkin_match:
        result["steps"] = parse_gherkin_steps(gherkin_match.group(1))
    
    # Extract tables (everything after the gherkin block)
    if gherkin_match:
        after_gherkin = section_text[gherkin_match.end():]
        result["examples"] = parse_markdown_tables(after_gherkin)
    
    return result


def parse_background(md_content):
    """Extract background section from markdown."""
    bg_match = re.search(r'## Background\s*\n(.*?)## Scenarios', md_content, re.DOTALL)
    if not bg_match:
        return None, []
    
    bg_text = bg_match.group(1)
    
    # Extract gherkin steps
    gherkin_match = re.search(r'```gherkin\n(.*?)```', bg_text, re.DOTALL)
    bg_steps = []
    if gherkin_match:
        for line in gherkin_match.group(1).strip().split('\n'):
            line = line.strip()
            if line:
                bg_steps.append(line)
    
    # Extract tables
    bg_tables = parse_markdown_tables(bg_text)
    
    return bg_steps, bg_tables


def parse_story_md(md_path):
    """Parse a story markdown file into structured data."""
    content = md_path.read_text(encoding='utf-8')
    
    # Parse background
    bg_steps, bg_tables = parse_background(content)
    
    # Split into scenario sections
    scenario_sections = re.split(r'<a id="scenario-[^"]*"></a>\n### Scenario:', content)
    
    scenarios = {}
    for section in scenario_sections[1:]:  # skip first split (before first scenario)
        # Extract scenario name from the link
        name_match = re.match(r'\s*\[([^\]]+)\]', section)
        if not name_match:
            continue
        scenario_name = name_match.group(1)
        
        parsed = parse_scenario_section(section)
        scenarios[scenario_name] = parsed
    
    return {
        "background": bg_steps,
        "background_tables": bg_tables,
        "scenarios": scenarios
    }


def find_story_in_graph(graph_data, story_name):
    """Find a story dict in the graph by name, recursively."""
    for epic in graph_data.get("epics", []):
        result = _find_story_recursive(epic, story_name)
        if result:
            return result
    return None


def _find_story_recursive(node, story_name):
    for sg in node.get("story_groups", []):
        for story in sg.get("stories", []):
            if story.get("name") == story_name:
                return story
    for se in node.get("sub_epics", []):
        result = _find_story_recursive(se, story_name)
        if result:
            return result
    return None


def update_scenario_in_graph(graph_scenario, md_scenario, bg_steps, bg_tables):
    """Update a single scenario in the graph with data from markdown."""
    # Update steps
    if md_scenario["steps"]:
        graph_scenario["steps"] = md_scenario["steps"]
    
    # Update examples
    all_tables = bg_tables + md_scenario.get("examples", [])
    if all_tables:
        graph_scenario["examples"] = all_tables
    
    # Update background
    if bg_steps:
        graph_scenario["background"] = bg_steps


def get_story_name_from_md(md_path):
    """Extract story name from markdown file path."""
    # Filename is like "📄 Story Name.md"
    name = md_path.stem
    if name.startswith("📄 "):
        name = name[2:]
    return name.strip()


def main():
    # Load story graph
    graph_data = json.loads(STORY_GRAPH_PATH.read_text(encoding='utf-8'))
    
    # Find all fixed markdown files in the Synchronize Diagram by Domain scope
    sync_dir = SCENARIOS_DIR / "🎯 Invoke Bot" / "⚙️ Perform Action" / "⚙️ Synchronize Diagram by Domain"
    
    if not sync_dir.exists():
        print(f"Directory not found: {sync_dir}")
        sys.exit(1)
    
    md_files = list(sync_dir.rglob("📄 *.md"))
    print(f"Found {len(md_files)} story files to process")
    
    updated_count = 0
    
    for md_path in sorted(md_files):
        story_name = get_story_name_from_md(md_path)
        print(f"\nProcessing: {story_name}")
        
        # Find story in graph
        story = find_story_in_graph(graph_data, story_name)
        if not story:
            print(f"  WARNING: Story not found in graph: {story_name}")
            continue
        
        # Parse markdown
        md_data = parse_story_md(md_path)
        
        # Update each scenario
        graph_scenarios = story.get("scenarios", [])
        for graph_scenario in graph_scenarios:
            scenario_name = graph_scenario.get("name", "")
            
            if scenario_name in md_data["scenarios"]:
                md_scenario = md_data["scenarios"][scenario_name]
                update_scenario_in_graph(
                    graph_scenario,
                    md_scenario,
                    md_data["background"],
                    md_data["background_tables"]
                )
                print(f"  Updated: {scenario_name}")
                updated_count += 1
            else:
                print(f"  SKIPPED (not in md): {scenario_name}")
    
    # Write updated graph
    STORY_GRAPH_PATH.write_text(
        json.dumps(graph_data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    
    print(f"\n{'='*60}")
    print(f"Updated {updated_count} scenarios in story-graph.json")


if __name__ == "__main__":
    main()
