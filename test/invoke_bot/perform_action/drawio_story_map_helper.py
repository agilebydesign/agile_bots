"""
DrawIO Story Map Test Helper
Handles DrawIO rendering, extraction, layout data, and update report testing
"""
import json
from pathlib import Path
from helpers.base_helper import BaseHelper


class DrawIOStoryMapTestHelper(BaseHelper):

    def create_simple_story_map_data(self):
        return {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sequential_order": 1.0,
                    "sub_epics": [
                        {
                            "name": "Initialize Bot",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {"name": "Load Config", "sequential_order": 1.0, "story_type": "user", "users": [], "acceptance_criteria": []},
                                        {"name": "Register Behaviors", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def create_story_map_data_with_counts(self, epic_count, sub_epic_count, story_count):
        epics = []
        se_created = 0
        story_created = 0
        for e in range(epic_count):
            se_for_this_epic = (sub_epic_count - se_created) // (epic_count - e)
            sub_epics = []
            for s in range(se_for_this_epic):
                stories_for_this_se = (story_count - story_created) // (sub_epic_count - se_created)
                stories = []
                for st in range(stories_for_this_se):
                    story_created += 1
                    stories.append({"name": f"Story {story_created}", "sequential_order": float(st + 1), "story_type": "user", "users": [], "acceptance_criteria": []})
                se_created += 1
                sub_epics.append({"name": f"SubEpic {se_created}", "sequential_order": float(s + 1), "sub_epics": [], "story_groups": [{"type": "and", "connector": None, "stories": stories}]})
            epics.append({"name": f"Epic {e+1}", "sequential_order": float(e + 1), "sub_epics": sub_epics})
        return {"epics": epics}

    def create_story_map_data_with_nested_sub_epics(self, depth=3):
        """Create story map data with sub-epics nested to the specified depth.
        
        depth=2: Epic -> SubEpic -> Stories (standard)
        depth=3: Epic -> SubEpic -> SubEpic -> Stories
        depth=4: Epic -> SubEpic -> SubEpic -> SubEpic -> Stories
        """
        def build_sub_epic(name, order, remaining_depth):
            if remaining_depth <= 1:
                # Leaf: contains stories
                return {
                    "name": name,
                    "sequential_order": order,
                    "sub_epics": [],
                    "story_groups": [{
                        "type": "and",
                        "connector": None,
                        "stories": [
                            {"name": f"{name} Story A", "sequential_order": 1.0, "story_type": "user", "users": [], "acceptance_criteria": []},
                            {"name": f"{name} Story B", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                        ]
                    }]
                }
            # Branch: contains nested sub-epics
            return {
                "name": name,
                "sequential_order": order,
                "sub_epics": [
                    build_sub_epic(f"{name} Child 1", 1.0, remaining_depth - 1),
                    build_sub_epic(f"{name} Child 2", 2.0, remaining_depth - 1)
                ],
                "story_groups": []
            }

        return {
            "epics": [{
                "name": "Nested Epic",
                "sequential_order": 1.0,
                "sub_epics": [
                    build_sub_epic("Top SubEpic", 1.0, depth - 1)
                ]
            }]
        }

    def create_story_map_data_with_users(self):
        """Story map where stories have assigned users (actors).

        Used to verify that actor elements are rendered in the correct
        position relative to their story card.
        """
        return {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sequential_order": 1.0,
                    "sub_epics": [
                        {
                            "name": "Initialize Bot",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {"name": "Load Config", "sequential_order": 1.0, "story_type": "user",
                                         "users": ["Developer", "Admin"],
                                         "acceptance_criteria": []},
                                        {"name": "Register Behaviors", "sequential_order": 2.0, "story_type": "system",
                                         "users": ["Bot Engine"],
                                         "acceptance_criteria": []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def create_story_map_data_with_story_type(self, story_type):
        data = self.create_simple_story_map_data()
        data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'] = [
            {"name": "Typed Story", "sequential_order": 1.0, "story_type": story_type, "users": [], "acceptance_criteria": []}
        ]
        return data

    def create_story_map_data_with_acceptance_criteria(self):
        return {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sequential_order": 1.0,
                    "sub_epics": [
                        {
                            "name": "Initialize Bot",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {"name": "Load Config", "sequential_order": 1.0, "story_type": "user", "users": [],
                                         "acceptance_criteria": [
                                             {"name": "When config file exists then system loads settings", "text": "When config file exists then system loads settings", "sequential_order": 1.0},
                                             {"name": "When config file missing then system uses defaults", "text": "When config file missing then system uses defaults", "sequential_order": 2.0}
                                         ]},
                                        {"name": "Register Behaviors", "sequential_order": 2.0, "story_type": "system", "users": [], "acceptance_criteria": []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def create_story_map_data_with_increments(self):
        return {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sequential_order": 1.0,
                    "sub_epics": [
                        {
                            "name": "Initialize Bot",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {"name": "Load Config", "sequential_order": 1.0, "story_type": "user", "users": ["Bot Behavior"], "acceptance_criteria": []},
                                        {"name": "Register Behaviors", "sequential_order": 2.0, "story_type": "system", "users": ["Bot Behavior"], "acceptance_criteria": []},
                                        {"name": "Validate Input", "sequential_order": 3.0, "story_type": "user", "users": ["Developer"], "acceptance_criteria": []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            "increments": [
                {"name": "MVP", "priority": 1, "stories": ["Load Config"]},
                {"name": "Phase 2", "priority": 2, "stories": ["Register Behaviors"]}
            ]
        }

    def create_story_map_data_with_renamed_story(self):
        data = self.create_simple_story_map_data()
        data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]['name'] = 'Load Configuration'
        return data

    def create_drawio_xml_with_renamed_story(self):
        return self.create_minimal_drawio_xml(story_names=['Load Config Settings', 'Register Behaviors'])

    def create_drawio_xml_with_deleted_story(self):
        return self.create_minimal_drawio_xml(story_names=['Load Config'])

    def create_drawio_xml_with_new_story(self):
        return self.create_minimal_drawio_xml(story_names=['Load Config', 'Register Behaviors', 'Validate Config'],
                                               sub_epic_width=500, epic_width=520)

    def create_drawio_xml_without_sub_epic(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="epic-1" value="Invoke Bot" style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="20" y="120" width="300" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="story-1" value="Load Config" style="fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="35" y="270" width="120" height="50" as="geometry"/>
        </mxCell>
    </root></mxGraphModel>
  </diagram>
</mxfile>'''

    def create_drawio_xml_without_epic(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
    </root></mxGraphModel>
  </diagram>
</mxfile>'''

    def create_empty_drawio_xml(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
    </root></mxGraphModel>
  </diagram>
</mxfile>'''

    def create_story_graph_file(self, graph_data=None, filename='story-graph.json'):
        if graph_data is None:
            graph_data = self.create_simple_story_map_data()
        docs_dir = self.workspace / 'docs' / 'story'
        docs_dir.mkdir(parents=True, exist_ok=True)
        story_graph_file = docs_dir / filename
        story_graph_file.write_text(json.dumps(graph_data, indent=2), encoding='utf-8')
        return story_graph_file

    def create_minimal_drawio_xml(self, epic_name='Invoke Bot', sub_epic_name='Initialize Bot',
                                   story_names=None, epic_width=None, sub_epic_width=None):
        if story_names is None:
            story_names = ['Load Config', 'Register Behaviors']
        total_stories_width = len(story_names) * 130 + 20
        ew = epic_width or max(300, total_stories_width + 20)
        sw = sub_epic_width or max(280, total_stories_width)
        story_cells = []
        x_pos = 35
        for idx, story_name in enumerate(story_names):
            story_cells.append(
                f'<mxCell id="story-{idx+1}" value="{story_name}" style="fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;" vertex="1" parent="1">'
                f'<mxGeometry x="{x_pos}" y="270" width="120" height="50" as="geometry"/></mxCell>')
            x_pos += 130
        stories_xml = '\n        '.join(story_cells)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Story Map" id="test-diagram">
    <mxGraphModel><root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="epic-1" value="{epic_name}" style="rounded=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="20" y="120" width="{ew}" height="300" as="geometry"/></mxCell>
        <mxCell id="sub-epic-1" value="{sub_epic_name}" style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="30" y="180" width="{sw}" height="200" as="geometry"/></mxCell>
        {stories_xml}
    </root></mxGraphModel>
  </diagram>
</mxfile>'''

    def create_drawio_file(self, xml_content=None, filename='story-map.drawio'):
        if xml_content is None:
            xml_content = self.create_minimal_drawio_xml()
        docs_dir = self.workspace / 'docs' / 'story'
        docs_dir.mkdir(parents=True, exist_ok=True)
        drawio_file = docs_dir / filename
        drawio_file.write_text(xml_content, encoding='utf-8')
        return drawio_file

    def create_rendered_increments_drawio_file(self, data=None, filename='story-map-increments.drawio'):
        """Render an increments diagram from story map data and save to disk.

        Returns (drawio_file_path, story_map, data_dict).
        """
        from synchronizers.story_io.drawio_story_map import DrawIOStoryMap
        from story_graph.nodes import StoryMap
        if data is None:
            data = self.create_story_map_data_with_increments()
        story_map = StoryMap(data)
        drawio_story_map = DrawIOStoryMap(diagram_type='increments')
        drawio_story_map.render_increments_from_story_map(
            story_map, data.get('increments', []), layout_data=None)
        docs_dir = self.workspace / 'docs' / 'story'
        docs_dir.mkdir(parents=True, exist_ok=True)
        drawio_file = docs_dir / filename
        drawio_story_map.save(drawio_file)
        return drawio_file, story_map, data

    def create_story_map_data_with_three_increments(self):
        """Story map with 3 stories across 3 increment lanes."""
        return {
            "epics": [
                {
                    "name": "Invoke Bot",
                    "sequential_order": 1.0,
                    "sub_epics": [
                        {
                            "name": "Initialize Bot",
                            "sequential_order": 1.0,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {"name": "Load Config", "sequential_order": 1.0, "story_type": "user", "users": ["Bot Behavior"], "acceptance_criteria": []},
                                        {"name": "Register Behaviors", "sequential_order": 2.0, "story_type": "system", "users": ["Bot Behavior"], "acceptance_criteria": []},
                                        {"name": "Validate Input", "sequential_order": 3.0, "story_type": "user", "users": ["Developer"], "acceptance_criteria": []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            "increments": [
                {"name": "MVP", "priority": 1, "stories": ["Load Config"]},
                {"name": "Phase 2", "priority": 2, "stories": ["Register Behaviors"]},
                {"name": "Phase 3", "priority": 3, "stories": ["Validate Input"]}
            ]
        }

    def create_layout_data(self):
        return {
            "EPIC|Invoke Bot": {"x": 20, "y": 120, "width": 300, "height": 50},
            "SUB_EPIC|Initialize Bot": {"x": 30, "y": 180, "width": 280, "height": 50},
            "STORY|Invoke Bot|Initialize Bot|Load Config": {"x": 35, "y": 270, "width": 120, "height": 50},
            "STORY|Invoke Bot|Initialize Bot|Register Behaviors": {"x": 165, "y": 270, "width": 120, "height": 50}
        }

    def create_layout_data_file(self, layout_data=None, filename='story-map-layout.json'):
        if layout_data is None:
            layout_data = self.create_layout_data()
        docs_dir = self.workspace / 'docs' / 'story'
        docs_dir.mkdir(parents=True, exist_ok=True)
        layout_file = docs_dir / filename
        layout_file.write_text(json.dumps(layout_data, indent=2), encoding='utf-8')
        return layout_file

    def assert_cell_style(self, node, expected_fill, expected_stroke, expected_font_color):
        assert node.fill == expected_fill, f"Expected fill {expected_fill}, got {node.fill}"
        assert node.stroke == expected_stroke, f"Expected stroke {expected_stroke}, got {node.stroke}"
        assert node.font_color == expected_font_color, f"Expected font_color {expected_font_color}, got {node.font_color}"

    def assert_render_summary(self, summary, expected_epics, expected_sub_epic_count, expected_diagram_generated=True):
        assert summary.get('epics') == expected_epics, f"Expected epics {expected_epics}, got {summary.get('epics')}"
        assert summary.get('sub_epic_count') == expected_sub_epic_count, f"Expected sub_epic_count {expected_sub_epic_count}, got {summary.get('sub_epic_count')}"
        assert summary.get('diagram_generated') == expected_diagram_generated, f"Expected diagram_generated {expected_diagram_generated}, got {summary.get('diagram_generated')}"

    def assert_update_report(self, report, expected_exact=None, expected_fuzzy=None, expected_new=None, expected_removed=None):
        if expected_exact is not None:
            assert len(report.get('exact_matches', [])) == expected_exact, f"Expected {expected_exact} exact matches"
        if expected_fuzzy is not None:
            assert len(report.get('fuzzy_matches', [])) == expected_fuzzy, f"Expected {expected_fuzzy} fuzzy matches"
        if expected_new is not None:
            assert len(report.get('new_stories', [])) == expected_new, f"Expected {expected_new} new stories"
        if expected_removed is not None:
            assert len(report.get('removed_stories', [])) == expected_removed, f"Expected {expected_removed} removed stories"
