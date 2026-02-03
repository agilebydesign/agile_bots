"""
Story Test Helper
Handles story graph, story map, epics, scenarios testing
"""
import json
from pathlib import Path
from helpers.base_helper import BaseHelper


class StoryTestHelper(BaseHelper):
    """Helper for story graph and story map testing"""
    
    @property
    def bot(self):
        """Access bot instance for bot.story_graph API."""
        return self.parent.bot
    
    def create_story_graph(self, graph_data: dict = None, docs_path: str = 'docs/stories', filename: str = 'story-graph.json') -> Path:
        
        if graph_data is None:
            graph_data = {'epics': []}
        
        docs_dir = self.parent.workspace / docs_path
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        story_graph_file = docs_dir / filename
        story_graph_file.write_text(json.dumps(graph_data, indent=2), encoding='utf-8')
        
        self.load_story_graph_into_bot()
        
        return story_graph_file
    
    def simple_story_graph(self) -> dict:
        """Return simple story graph data for testing."""
        return {
            "epics": [
                {
                    "name": "Build Knowledge",
                    "sequential_order": 1,
                    "sub_epics": [
                        {
                            "name": "Load Story Graph",
                            "sequential_order": 1,
                            "sub_epics": [],
                            "story_groups": [
                                {
                                    "type": "and",
                                    "connector": None,
                                    "stories": [
                                        {
                                            "name": "Load Story Graph Into Memory",
                                            "sequential_order": 1,
                                            "connector": None,
                                            "users": ["Story Bot"],
                                            "story_type": "user",
                                            "sizing": "5 days",
                                            "scenarios": [
                                                {
                                                    "name": "Story graph file exists",
                                                    "type": "happy_path",
                                                    "background": ["Given story graph file exists"],
                                                    "steps": [
                                                        "When story graph is loaded",
                                                        "Then story map is created with epics"
                                                    ]
                                                },
                                                {
                                                    "name": "Story graph file missing",
                                                    "type": "error_case",
                                                    "background": [],
                                                    "steps": [
                                                        "When story graph file does not exist",
                                                        "Then FileNotFoundError is raised"
                                                    ]
                                                },
                                                {
                                                    "name": "Load story graph with different formats",
                                                    "type": "happy_path",
                                                    "background": ["Given story graph file exists"],
                                                    "steps": [
                                                        "When story graph is loaded from \"<file_path>\"",
                                                        "Then story map contains \"<expected_epics>\" epics"
                                                    ],
                                                    "examples": {
                                                        "columns": ["file_path", "expected_epics"],
                                                        "rows": [
                                                            ["story-graph.json", "2"],
                                                            ["story-graph-v2.json", "3"]
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "story_groups": []
                }
            ]
        }
    
    def create_story_map(self, story_graph_data: dict = None):
        """Create StoryMap from story graph data."""
        from scanners.story_map import StoryMap
        if story_graph_data is None:
            story_graph_data = self.simple_story_graph()
        return StoryMap(story_graph_data)
    
    def sample_story_graph(self) -> dict:
        """Return a reusable sample story graph for scope filtering tests."""
        return {
            'epics': [
                {
                    'name': 'Epic A',
                    'sub_epics': [
                        {
                            'name': 'Sub-Epic A1',
                            'story_groups': [
                                {
                                    'type': 'and',
                                    'connector': None,
                                    'stories': [
                                        {'name': 'Story A1'},
                                        {'name': 'Story A2'}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'Epic B',
                    'sub_epics': [
                        {
                            'name': 'Sub-Epic B1',
                            'story_groups': [
                                {
                                    'type': 'and',
                                    'connector': None,
                                    'stories': [
                                        {'name': 'Story B1'},
                                        {'name': 'Story B2'}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            'increments': [
                {
                    'name': 'Increment 1',
                    'priority': 1,
                    'epics': [
                        {
                            'name': 'Epic A',
                            'sub_epics': [
                                {
                                    'name': 'Sub-epic A1',
                                    'stories': [
                                        {'name': 'Story A1'},
                                        {'name': 'Story A2'}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'Increment 2',
                    'priority': 2,
                    'epics': [
                        {
                            'name': 'Epic B',
                            'sub_epics': [
                                {
                                    'name': 'Sub-epic B1',
                                    'stories': [
                                        {'name': 'Story B1'},
                                        {'name': 'Story B2'}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def story_graph_dict(self, minimal=False, scope_type=None, epic=None):
        """Return story graph dictionary for testing."""
        if minimal:
            return {
                "epics": [
                    {
                        "name": "Places Order",
                        "sub_epics": [
                            {
                                "name": "Validates Payment",
                                "story_groups": [
                                    {
                                        "stories": [
                                            {
                                                "name": "Place Order",
                                                "scenarios": []
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        elif scope_type == 'multiple_test_files':
            return {
                "epics": [
                    {
                        "name": "Manage Orders",
                        "sub_epics": [
                            {
                                "name": "Create Order",
                                "story_groups": [
                                    {
                                        "stories": [
                                            {
                                                "name": "Place Order",
                                                "scenarios": []
                                            },
                                            {
                                                "name": "Cancel Order",
                                                "scenarios": []
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        elif epic == 'mob':
            return {
                "epics": [
                    {
                        "name": "Manage Mobs",
                        "sequential_order": 1,
                        "estimated_stories": 6,
                        "domain_concepts": [
                            {
                                "name": "Mob",
                                "responsibilities": [
                                    {
                                        "name": "Groups minions together for coordinated action",
                                        "collaborators": ["Minion"]
                                    }
                                ]
                            }
                        ],
                        "sub_epics": []
                    }
                ]
            }
        else:
            return {
                "epics": [
                    {
                        "name": "Test Epic",
                        "sequential_order": 1,
                        "sub_epics": [],
                        "story_groups": []
                    }
                ]
            }
    
    def story_graph_with_epics_and_increments(self) -> dict:
        """Return test story graph with epics and increments."""
        return {
            'epics': [
                {
                    'name': 'Epic A',
                    'sub_epics': [
                        {
                            'name': 'Sub-epic A1',
                            'story_groups': [
                                {
                                    'stories': [
                                        {'name': 'Story A1'},
                                        {'name': 'Story A2'}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'Epic B',
                    'sub_epics': [
                        {
                            'name': 'Sub-epic B1',
                            'story_groups': [
                                {
                                    'stories': [
                                        {'name': 'Story B1'},
                                        {'name': 'Story B2'}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            'increments': [
                {
                    'name': 'Increment 1',
                    'priority': 1,
                    'epics': [
                        {
                            'name': 'Epic A',
                            'sub_epics': [
                                {
                                    'name': 'Sub-epic A1',
                                    'stories': [
                                        {'name': 'Story A1'},
                                        {'name': 'Story A2'}
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'Increment 2',
                    'priority': 2,
                    'epics': [
                        {
                            'name': 'Epic B',
                            'sub_epics': [
                                {
                                    'name': 'Sub-epic B1',
                                    'stories': [
                                        {'name': 'Story B1'},
                                        {'name': 'Story B2'}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def _get_epics(self, source):
        """Get epics from source, handling both method and property APIs."""
        epics_attr = source.epics
        # If epics is callable (method), call it; otherwise it's already a property
        return epics_attr() if callable(epics_attr) else epics_attr
    
    def access_story_item(self, item_type, source, **access_params):
        """Access item from story map source."""
        index = access_params.get('index', 0)
        name = access_params.get('name')
        
        if item_type == 'epics':
            return self._get_epics(source)
        elif item_type == 'epic':
            if hasattr(source, 'epics'):
                epics = self._get_epics(source)
            else:
                epics = source
            return epics[index] if index is not None else epics[0]
        elif item_type == 'sub_epic':
            epics = source if isinstance(source, list) else self._get_epics(source)
            return epics[0].children[0]
        elif item_type == 'story':
            if name:
                epic = source if hasattr(source, 'children') else self._get_epics(source)[0]
                for sub_epic in epic.children:
                    for story_group in sub_epic.children:
                        for story in story_group.children:
                            if story.name == name:
                                return story
                raise ValueError(f"Story '{name}' not found")
            elif hasattr(source, 'epics'):
                return self._get_epics(source)[0].children[0].children[0].children[0]
            elif hasattr(source, 'children'):
                return source.children[0].children[0].children[0]
            else:
                return source[0].children[0].children[0].children[0]
        elif item_type == 'scenario':
            if name:
                story = source if hasattr(source, 'scenarios') else self.access_story_item('story', source)
                for scenario in story.scenarios:
                    if scenario.name == name:
                        return scenario
                raise ValueError(f"Scenario '{name}' not found")
            elif hasattr(source, 'scenarios'):
                return source.scenarios[index]
            else:
                story = self.access_story_item('story', source)
                return story.scenarios[index]
        elif item_type == 'scenario_outline':
            # Legacy support: scenario_outline is now just a scenario with examples
            if name:
                story = source if hasattr(source, 'scenarios') else self.access_story_item('story', source)
                for scenario in story.scenarios:
                    if scenario.name == name and scenario.has_examples:
                        return scenario
                raise ValueError(f"Scenario with examples '{name}' not found")
            else:
                story = self.access_story_item('story', source)
                scenarios_with_examples = [s for s in story.scenarios if s.has_examples]
                if scenarios_with_examples and index < len(scenarios_with_examples):
                    return scenarios_with_examples[index]
                return story.scenarios[index] if index < len(story.scenarios) else None
        else:
            raise ValueError(f"Unknown item_type: {item_type}")
    
    def assert_nodes_match(self, nodes, expected_count=None, expected_names=None):
        """Assert nodes match expected count and names."""
        if expected_count is not None:
            assert len(nodes) == expected_count, f"Expected {expected_count} nodes, got {len(nodes)}"
        if expected_names is not None:
            actual_names = [node.name for node in nodes]
            assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"
    
    def assert_children_match(self, parent, expected_count=None, expected_names=None):
        """Assert children match expected count and names."""
        children = parent.children
        if expected_count is not None:
            assert len(children) == expected_count, f"Expected {expected_count} children, got {len(children)}"
        if expected_names is not None:
            actual_names = [child.name for child in children]
            assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"
    
    def assert_stories_match(self, expected, actual):
        """Assert stories match expected."""
        if isinstance(expected, set) and isinstance(actual, set):
            assert expected == actual, f"Expected {expected}, got {actual}"
        elif isinstance(expected, list) and isinstance(actual, list):
            assert set(expected) == set(actual), f"Expected {expected}, got {actual}"
        else:
            assert expected == actual, f"Expected {expected}, got {actual}"
    
    def assert_scenarios_match(self, story, expected_count=None, expected_names=None):
        """Assert scenarios match expected count and names."""
        scenarios = story.scenarios
        if expected_count is not None:
            assert len(scenarios) == expected_count, f"Expected {expected_count} scenarios, got {len(scenarios)}"
        if expected_names is not None:
            actual_names = [scenario.name for scenario in scenarios]
            assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"
    
    def assert_scenario_outlines_match(self, scenario, expected_count=None, expected_names=None):
        """Assert scenarios with examples match expected count and names (legacy method name)."""
        from scanners.story_map import Story
        if isinstance(scenario, Story):
            scenarios_with_examples = [s for s in scenario.scenarios if s.has_examples]
        else:
            scenarios_with_examples = [s for s in scenario.scenarios if s.has_examples] if hasattr(scenario, 'scenarios') else []
        if expected_count is not None:
            assert len(scenarios_with_examples) == expected_count, f"Expected {expected_count} scenarios with examples, got {len(scenarios_with_examples)}"
        if expected_names is not None:
            actual_names = [s.name for s in scenarios_with_examples]
            assert actual_names == expected_names, f"Expected names {expected_names}, got {actual_names}"
    
    def assert_story_map_matches(self, story_map_or_epics, epic_name=None):
        """Assert story map matches expected epic."""
        from scanners.story_map import Epic
        
        if isinstance(story_map_or_epics, list):
            epics = story_map_or_epics
            assert len(epics) == 1, f"Expected 1 epic, got {len(epics)}"
            assert isinstance(epics[0], Epic), f"Expected Epic instance, got {type(epics[0])}"
            expected_name = epic_name if epic_name is not None else "Build Knowledge"
            assert epics[0].name == expected_name, \
                f"Expected epic name '{expected_name}', got '{epics[0].name}'"
            return epics[0]
        else:
            epics_collection = self._get_epics(story_map_or_epics)
            epics_list = list(epics_collection)
            assert len(epics_list) == 1, f"Expected 1 epic, got {len(epics_list)}"
            expected_name = epic_name if epic_name is not None else "Test Epic"
            assert epics_list[0].name == expected_name, \
                f"Expected epic name '{expected_name}', got '{epics_list[0].name}'"
    
    def assert_map_location_matches(self, item, item_type=None, field=None):
        """Assert map location correctness for story map items."""
        from scanners.story_map import Epic, SubEpic, Story, Scenario
        
        if item_type is None:
            if isinstance(item, Epic):
                item_type = 'epic'
            elif isinstance(item, SubEpic):
                item_type = 'sub_epic'
            elif isinstance(item, Story):
                item_type = 'story'
            elif isinstance(item, Scenario):
                # Check if it's a scenario with examples (legacy scenario_outline)
                if item.has_examples:
                    item_type = 'scenario_outline'
                else:
                    item_type = 'scenario'
        
        expected_locations = {
            'epic': {
                None: "epics[0].name",
                'sequential_order': "epics[0].sequential_order"
            },
            'sub_epic': {
                None: "epics[0].sub_epics[0].name"
            },
            'story': {
                None: "epics[0].sub_epics[0].story_groups[0].stories[0].name",
                'sizing': "epics[0].sub_epics[0].story_groups[0].stories[0].sizing"
            },
            'scenario': {
                None: "epics[0].sub_epics[0].story_groups[0].stories[0].scenarios[0].name"
            },
            'scenario_outline': {
                None: "epics[0].sub_epics[0].story_groups[0].stories[0].scenarios[2].name"
            }
        }
        
        expected_default = expected_locations.get(item_type, {}).get(None)
        assert item.map_location() == expected_default, \
            f"Expected map_location() == '{expected_default}', got '{item.map_location()}'"
        
        if item_type == 'epic':
            expected_seq = expected_locations.get(item_type, {}).get('sequential_order')
            assert item.map_location('sequential_order') == expected_seq, \
                f"Expected map_location('sequential_order') == '{expected_seq}', got '{item.map_location('sequential_order')}'"
        elif item_type == 'story' and field == 'sizing':
            expected_sizing = expected_locations.get(item_type, {}).get('sizing')
            assert item.map_location('sizing') == expected_sizing, \
                f"Expected map_location('sizing') == '{expected_sizing}', got '{item.map_location('sizing')}'"
    
    def given_story_graph(self, story_graph: dict = None, docs_path: str = 'docs/stories', filename: str = 'story-graph.json') -> Path:
        """Create story graph file in workspace."""
        if story_graph is None:
            story_graph = {'epics': []}
        
        docs_dir = self.parent.workspace / docs_path
        docs_dir.mkdir(parents=True, exist_ok=True)
        story_graph_file = docs_dir / filename
        story_graph_file.write_text(json.dumps(story_graph, indent=2), encoding='utf-8')
        return story_graph_file
    
    def given_story_graph_dict(self, minimal=False, scope_type=None, epic=None):
        """Return story graph dictionary for testing (alias for story_graph_dict)."""
        return self.story_graph_dict(minimal, scope_type, epic)
    
    def when_item_accessed(self, item_type, source, **access_params):
        """Access item from source (alias for access_story_item)."""
        return self.access_story_item(item_type, source, **access_params)
    
    def create_story_graph_with_parent_and_children(self, parent_type, parent_name, existing_count, child_type):
        """Create story graph with parent node and existing children."""
        graph_data = {'epics': []}
        
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': []}
            for i in range(existing_count):
                epic['sub_epics'].append({
                    'name': f'SubEpic {chr(65 + i)}',
                    'sequential_order': i
                })
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0}
            if child_type == 'SubEpic':
                subepic['sub_epics'] = []
                for i in range(existing_count):
                    subepic['sub_epics'].append({
                        'name': f'SubEpic {chr(65 + i)}',
                        'sequential_order': i
                    })
            elif child_type == 'Story':
                subepic['story_groups'] = [{'type': 'and', 'stories': []}]
                for i in range(existing_count):
                    subepic['story_groups'][0]['stories'].append({
                        'name': f'Story {chr(65 + i)}',
                        'sequential_order': i,
                        'scenarios': []
                    })
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        elif parent_type == 'Story':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': 'Test SubEpic', 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            story = {'name': parent_name, 'sequential_order': 0, 'scenarios': []}
            for i in range(existing_count):
                story['scenarios'].append({
                    'name': f'Scenario {chr(65 + i)}',
                    'steps': []
                })
            subepic['story_groups'][0]['stories'].append(story)
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_named_children(self, parent_type, parent_name, existing_children_csv):
        """Create story graph with parent node and named children."""
        graph_data = {'epics': []}
        child_names = [name.strip() for name in existing_children_csv.split(',')] if existing_children_csv else []
        
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': []}
            for i, name in enumerate(child_names):
                epic['sub_epics'].append({
                    'name': name,
                    'sequential_order': i
                })
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0}
            
            has_nested_structure = any('Flow' in name or 'Reset' in name or 'OAuth' in name or 'Auth' in name for name in child_names)
            
            if has_nested_structure:
                subepic['sub_epics'] = []
                for i, name in enumerate(child_names):
                    subepic['sub_epics'].append({
                        'name': name,
                        'sequential_order': i
                    })
            else:
                subepic['story_groups'] = [{'type': 'and', 'stories': []}]
                for i, name in enumerate(child_names):
                    subepic['story_groups'][0]['stories'].append({
                        'name': name,
                        'sequential_order': i,
                        'scenarios': []
                    })
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        elif parent_type == 'Story':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': 'Test SubEpic', 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            story = {'name': parent_name, 'sequential_order': 0, 'scenarios': []}
            for i, name in enumerate(child_names):
                story['scenarios'].append({
                    'name': name,
                    'sequential_order': i,
                    'steps': []
                })
            subepic['story_groups'][0]['stories'].append(story)
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_existing_child(self, parent_type, parent_name, existing_child_name, child_type):
        """Create story graph with parent node and one existing child."""
        graph_data = {'epics': []}
        
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': []}
            epic['sub_epics'].append({
                'name': existing_child_name,
                'sequential_order': 0
            })
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0}
            if child_type == 'Story':
                subepic['story_groups'] = [{'type': 'and', 'stories': []}]
                subepic['story_groups'][0]['stories'].append({
                    'name': existing_child_name,
                    'sequential_order': 0,
                    'scenarios': []
                })
            else:
                subepic['sub_epics'] = []
                subepic['sub_epics'].append({
                    'name': existing_child_name,
                    'sequential_order': 0
                })
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        elif parent_type == 'Story':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': 'Test SubEpic', 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            story = {'name': parent_name, 'sequential_order': 0, 'scenarios': []}
            if child_type == 'Scenario':
                story['scenarios'].append({
                    'name': existing_child_name,
                    'sequential_order': 0,
                    'steps': []
                })
            subepic['story_groups'][0]['stories'].append(story)
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_subepic_with_existing_stories(self, subepic_name, existing_story_count):
        """Create SubEpic with existing Story count."""
        graph_data = {'epics': []}
        epic = {'name': 'Test Epic', 'sub_epics': []}
        subepic = {'name': subepic_name, 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
        for i in range(existing_story_count):
            subepic['story_groups'][0]['stories'].append({
                'name': f'Story {chr(65 + i)}',
                'sequential_order': i,
                'scenarios': []
            })
        epic['sub_epics'].append(subepic)
        graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_subepic_with_existing_story(self, subepic_name, existing_story):
        """Create SubEpic with one existing Story."""
        return self.create_subepic_with_existing_stories(subepic_name, 1)
    
    def create_subepic_with_existing_subepic(self, subepic_name, existing_subepic):
        """Create SubEpic with one existing SubEpic child."""
        graph_data = {'epics': []}
        epic = {'name': 'Test Epic', 'sub_epics': []}
        subepic = {'name': subepic_name, 'sequential_order': 0, 'sub_epics': []}
        subepic['sub_epics'].append({
            'name': existing_subepic,
            'sequential_order': 0
        })
        epic['sub_epics'].append(subepic)
        graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_in_graph(self, story_name):
        """Create Story in story graph."""
        graph_data = {'epics': []}
        epic = {'name': 'Test Epic', 'sub_epics': []}
        subepic = {'name': 'Test SubEpic', 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
        story = {'name': story_name, 'sequential_order': 0, 'scenarios': []}
        subepic['story_groups'][0]['stories'].append(story)
        epic['sub_epics'].append(subepic)
        graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def find_subepic_in_story_graph(self, name):
        """Find SubEpic by name in bot.story_graph."""
        from story_graph.nodes import SubEpic
        
        for epic in self.bot.story_graph.epics:
            for node in self.bot.story_graph.walk(epic):
                if isinstance(node, SubEpic) and node.name == name:
                    return node
        raise ValueError(f"SubEpic '{name}' not found in bot.story_graph")
    
    def find_story_in_story_graph(self, name):
        """Find Story by name in bot.story_graph."""
        from story_graph.nodes import Story
        
        for epic in self.bot.story_graph.epics:
            for node in self.bot.story_graph.walk(epic):
                if isinstance(node, Story) and node.name == name:
                    return node
        raise ValueError(f"Story '{name}' not found in bot.story_graph")
    
    def find_story_in_parent(self, parent, name):
        """Find Story by name within parent (handles StoryGroup)."""
        from story_graph.nodes import SubEpic, StoryGroup, Story
        
        if isinstance(parent, SubEpic):
            story_groups = [c for c in parent.children if isinstance(c, StoryGroup)]
            if story_groups:
                for story in story_groups[0].children:
                    if isinstance(story, Story) and story.name == name:
                        return story
        
        for child in parent.children:
            if child.name == name:
                return child
        return None
    
    def find_scenario_in_story_graph(self, name):
        """Find Scenario by name in bot.story_graph."""
        from story_graph.nodes import Scenario
        
        for epic in self.bot.story_graph.epics:
            for node in self.bot.story_graph.walk(epic):
                if isinstance(node, Scenario) and node.name == name:
                    return node
        raise ValueError(f"Scenario '{name}' not found in bot.story_graph")
    
    def load_story_graph_into_bot(self):
        """Load story graph into bot.story_graph for test access.
        
        Note: Bot now has a native story_graph property that loads from workspace.
        This method forces a reload by clearing the cached instance.
        """
        story_graph_path = self.bot.bot_paths.workspace_directory / 'docs' / 'stories' / 'story-graph.json'
        if not story_graph_path.exists():
            return None
        
        # Clear cached story_graph to force reload from file
        self.bot._story_graph = None
        
        # Access the property which will lazy-load it
        story_map = self.bot.story_graph
        
        return story_map
    
    def get_children_names(self, parent_name):
        """Get list of child names for a parent node - uses real domain objects from bot.story_graph."""
        if parent_name in self.bot.story_graph.epics:
            parent = self.bot.story_graph.epics[parent_name]
        else:
            parent = self.find_subepic_in_story_graph(parent_name) or self.find_story_in_story_graph(parent_name)
        return [child.name for child in parent.children]
    
    def get_child_count(self, parent_name):
        """Get count of children for a parent node."""
        return len(self.get_children_names(parent_name))
    
    def get_child_position(self, parent_name, child_name):
        """Get position of child in parent's children list."""
        children = self.get_children_names(parent_name)
        try:
            return children.index(child_name)
        except ValueError:
            raise ValueError(f"Child '{child_name}' not found under '{parent_name}'")
    
    def assert_story_is_in_storygroup_at_position(self, subepic_name, story_name, expected_position):
        """Verify Story is in StoryGroup at expected position - uses real domain objects from bot.story_graph."""
        from story_graph.nodes import StoryGroup, Story
        
        subepic = self.find_subepic_in_story_graph(subepic_name)
        # Check internal structure to verify StoryGroup exists
        story_groups = [child for child in subepic._children if isinstance(child, StoryGroup)]
        assert len(story_groups) > 0
        
        # Use public API to check stories (now transparent)
        stories = list(subepic.children)
        story_names = [s.name for s in stories if isinstance(s, Story)]
        assert story_name in story_names
        
        actual_position = story_names.index(story_name)
        assert actual_position == expected_position
    
    def assert_storygroup_exists(self, subepic_name):
        """Verify StoryGroup exists - uses real domain objects from bot.story_graph."""
        from story_graph.nodes import StoryGroup
        
        subepic = self.find_subepic_in_story_graph(subepic_name)
        # Check internal structure to verify StoryGroup exists
        story_groups = [child for child in subepic._children if isinstance(child, StoryGroup)]
        assert len(story_groups) > 0
    
    def assert_child_is_in_collection(self, story_name, child_name, collection_name):
        """Verify child is in target collection - uses real domain objects from bot.story_graph."""
        story = self.find_story_in_story_graph(story_name)
        
        if collection_name == 'scenarios':
            children = story.scenarios
        elif collection_name == 'scenario_outlines':
            # Legacy support: scenario_outlines are now scenarios with examples
            children = [s for s in story.scenarios if s.has_examples]
        elif collection_name == 'acceptance_criteria':
            children = story.acceptance_criteria
        else:
            raise ValueError(f"Unknown collection: {collection_name}")
        
        child_names = [c.name for c in children]
        assert child_name in child_names
    
    def assert_child_is_not_in_collection(self, story_name, child_name, excluded_collection):
        """Verify child is not in excluded collection - uses real domain objects from bot.story_graph."""
        story = self.find_story_in_story_graph(story_name)
        
        if excluded_collection == 'scenarios':
            children = story.scenarios
        elif excluded_collection == 'scenario_outlines':
            # Legacy support: scenario_outlines are now scenarios with examples
            children = [s for s in story.scenarios if s.has_examples]
        elif excluded_collection == 'acceptance_criteria':
            children = story.acceptance_criteria
        else:
            children = []
        
        child_names = [c.name for c in children]
        assert child_name not in child_names
    
    def create_story_graph_with_node_and_children(self, grandparent_type, grandparent, node_name, node_children, initial_child_count):
        """Create story graph with node that has children under grandparent."""
        graph_data = {'epics': []}
        epic = {'name': 'Test Epic' if grandparent_type != 'Epic' else grandparent, 'sub_epics': []}
        
        if grandparent_type == 'Epic':
            node = {'name': node_name, 'sequential_order': 0, 'sub_epics': []}
            for i, child in enumerate([n.strip() for n in node_children.split(',')]):
                node['sub_epics'].append({'name': child, 'sequential_order': i})
            for i in range(initial_child_count - 1):
                epic['sub_epics'].append({'name': f'Other {i}', 'sequential_order': i + 1})
            epic['sub_epics'].insert(0, node)
        elif grandparent_type == 'SubEpic':
            subepic = {'name': grandparent, 'sequential_order': 0, 'sub_epics': []}
            node = {'name': node_name, 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            for i, child in enumerate([n.strip() for n in node_children.split(',')]):
                node['story_groups'][0]['stories'].append({'name': child, 'sequential_order': i, 'scenarios': []})
            for i in range(initial_child_count - 1):
                subepic['sub_epics'].append({'name': f'Other {i}', 'sequential_order': i + 1})
            subepic['sub_epics'].insert(0, node)
            epic['sub_epics'].append(subepic)
        
        graph_data['epics'].append(epic)
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_descendants(self, parent_type, parent_name, initial_children, node_name, child_count, total_descendants):
        """Create story graph with node that has multiple descendant levels."""
        graph_data = {'epics': []}
        
        initial_child_list = [n.strip() for n in initial_children.split(',')]
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': []}
            for child_name in initial_child_list:
                if child_name == node_name:
                    subepic = {'name': node_name, 'sequential_order': len(epic['sub_epics']), 'sub_epics': []}
                    for i in range(child_count):
                        nested = {'name': f'Nested {i}', 'sequential_order': i, 'story_groups': [{'type': 'and', 'stories': []}]}
                        for j in range(2):
                            nested['story_groups'][0]['stories'].append({
                                'name': f'Story {i}-{j}',
                                'sequential_order': j,
                                'scenarios': []
                            })
                        subepic['sub_epics'].append(nested)
                    epic['sub_epics'].append(subepic)
                else:
                    epic['sub_epics'].append({'name': child_name, 'sequential_order': len(epic['sub_epics'])})
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            parent_subepic = {'name': parent_name, 'sequential_order': 0, 'sub_epics': []}
            for child_name in initial_child_list:
                if child_name == node_name:
                    subepic = {'name': node_name, 'sequential_order': len(parent_subepic['sub_epics']), 'sub_epics': []}
                    for i in range(child_count):
                        nested = {'name': f'Nested {i}', 'sequential_order': i, 'story_groups': [{'type': 'and', 'stories': []}]}
                        for j in range(2):
                            nested['story_groups'][0]['stories'].append({
                                'name': f'Story {i}-{j}',
                                'sequential_order': j,
                                'scenarios': []
                            })
                        subepic['sub_epics'].append(nested)
                    parent_subepic['sub_epics'].append(subepic)
                else:
                    parent_subepic['sub_epics'].append({'name': child_name, 'sequential_order': len(parent_subepic['sub_epics'])})
            epic['sub_epics'].append(parent_subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def assert_children_have_sequential_positions(self, parent_name):
        """Verify all children have sequential positions (0, 1, 2, ...)."""
        try:
            parent = self.bot.story_graph.epics[parent_name]
        except KeyError:
            try:
                parent = self.find_subepic_in_story_graph(parent_name)
            except ValueError:
                parent = self.find_story_in_story_graph(parent_name)
        
        children = list(parent.children)
        for i, child in enumerate(children):
            assert child.sequential_order is not None or i == 0
    
    def create_story_graph_with_node(self, node_type, parent_name, node_name):
        """Create story graph with single node."""
        graph_data = {'epics': []}
        
        if node_type == 'Epic':
            graph_data['epics'].append({'name': node_name, 'sub_epics': []})
        elif node_type == 'SubEpic':
            epic = {'name': parent_name if parent_name != 'root' else 'Root Epic', 'sub_epics': []}
            epic['sub_epics'].append({'name': node_name, 'sequential_order': 0})
            graph_data['epics'].append(epic)
        elif node_type == 'Story':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            subepic['story_groups'][0]['stories'].append({'name': node_name, 'sequential_order': 0, 'scenarios': []})
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        elif node_type == 'Scenario':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': 'Test SubEpic', 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': []}]}
            story = {'name': parent_name, 'sequential_order': 0, 'scenarios': []}
            story['scenarios'].append({'name': node_name, 'steps': []})
            subepic['story_groups'][0]['stories'].append(story)
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_for_move(self, source_parent_type, source_parent, node_name, target_parent_type, target_parent, target_child_count):
        """Create story graph for move operation tests."""
        graph_data = {'epics': []}
        
        if source_parent_type == 'Epic' and target_parent_type == 'Epic':
            source_epic = {'name': source_parent, 'sub_epics': []}
            source_epic['sub_epics'].append({'name': node_name, 'sequential_order': 0})
            
            target_epic = {'name': target_parent, 'sub_epics': []}
            for i in range(target_child_count):
                target_epic['sub_epics'].append({'name': f'Existing {i}', 'sequential_order': i})
            
            graph_data['epics'].extend([source_epic, target_epic])
        elif source_parent_type == 'SubEpic' and target_parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            
            # Create source SubEpic with node
            source_subepic = {'name': source_parent, 'sequential_order': 0, 'sub_epics': []}
            source_subepic['sub_epics'].append({'name': node_name, 'sequential_order': 0})
            
            # Create target SubEpic with existing children
            target_subepic = {'name': target_parent, 'sequential_order': 1, 'sub_epics': []}
            for i in range(target_child_count):
                target_subepic['sub_epics'].append({'name': f'Existing {i}', 'sequential_order': i})
            
            epic['sub_epics'].extend([source_subepic, target_subepic])
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_for_move_with_children(self, source_parent, node_name, target_parent, target_children):
        """Create story graph for move with specific target children."""
        graph_data = {'epics': []}
        
        source_epic = {'name': source_parent, 'sub_epics': []}
        source_epic['sub_epics'].append({'name': node_name, 'sequential_order': 0})
        
        target_epic = {'name': target_parent, 'sub_epics': []}
        for i, child in enumerate([n.strip() for n in target_children.split(',')]):
            target_epic['sub_epics'].append({'name': child, 'sequential_order': i})
        
        graph_data['epics'].extend([source_epic, target_epic])
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_child(self, parent_type, parent_name, node_name):
        """Create story graph with parent and single child."""
        graph_data = {'epics': []}
        
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': [{'name': node_name, 'sequential_order': 0}]}
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0, 'story_groups': [{'type': 'and', 'stories': [{'name': node_name, 'sequential_order': 0, 'scenarios': []}]}]}
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_for_hierarchy_move_test(self, source_parent, node_name, node_type, target_parent, existing_child, existing_type):
        """Create story graph for hierarchy violation move tests."""
        graph_data = {'epics': []}
        epic = {'name': 'Test Epic', 'sub_epics': []}
        
        source = {'name': source_parent, 'sequential_order': 0, 'sub_epics': []}
        if node_type == 'SubEpic':
            source['sub_epics'].append({'name': node_name, 'sequential_order': 0})
        else:
            source['story_groups'] = [{'type': 'and', 'stories': []}]
            source['story_groups'][0]['stories'].append({'name': node_name, 'sequential_order': 0, 'scenarios': []})
        
        target = {'name': target_parent, 'sequential_order': 1}
        if existing_type == 'SubEpic':
            target['sub_epics'] = [{'name': existing_child, 'sequential_order': 0}]
        else:
            target['story_groups'] = [{'type': 'and', 'stories': []}]
            target['story_groups'][0]['stories'].append({'name': existing_child, 'sequential_order': 0, 'scenarios': []})
        
        epic['sub_epics'].extend([source, target])
        graph_data['epics'].append(epic)
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_descendant(self, parent_type, parent_name, child_name):
        """Create story graph with parent and descendant."""
        graph_data = {'epics': []}
        
        if parent_type == 'Epic':
            epic = {'name': parent_name, 'sub_epics': []}
            epic['sub_epics'].append({'name': child_name, 'sequential_order': 0})
            graph_data['epics'].append(epic)
        elif parent_type == 'SubEpic':
            epic = {'name': 'Test Epic', 'sub_epics': []}
            subepic = {'name': parent_name, 'sequential_order': 0, 'sub_epics': []}
            subepic['sub_epics'].append({'name': child_name, 'sequential_order': 0})
            epic['sub_epics'].append(subepic)
            graph_data['epics'].append(epic)
        
        self.create_story_graph(graph_data)
        return graph_data
    
    def create_story_graph_with_node_and_actions(self, node_type, node_name, actions):
        """Create story graph with node and register bot actions."""
        graph_data = self.create_story_graph_with_node(node_type, 'parent', node_name)
        self.load_story_graph_into_bot()
        if node_type == 'Epic':
            node = self.bot.story_graph.epics[node_name]
        elif node_type == 'SubEpic':
            node = self.find_subepic_in_story_graph(node_name)
        else:
            node = self.find_story_in_story_graph(node_name)
        node._registered_actions = actions
        return graph_data
    
    def assert_story_graph_structure_valid(self):
        """Verify story graph structure is valid."""
        story_graph_path = self.parent.workspace / 'docs' / 'stories' / 'story-graph.json'
        assert story_graph_path.exists()
        story_graph_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
        assert 'epics' in story_graph_data
    
    def assert_child_created_at_position(self, parent, child_name, expected_position, total_children):
        """Assert child was created at expected position with correct total count."""
        children = list(parent.children)
        assert len(children) == total_children
        assert children[expected_position].name == child_name
    
    def assert_children_in_order(self, parent, expected_order_csv):
        """Assert children are in expected order."""
        expected_names = [name.strip() for name in expected_order_csv.split(',')]
        actual_names = [c.name for c in parent.children]
        assert actual_names == expected_names
    
    def assert_child_at_position(self, parent, child_name, expected_position):
        """Assert specific child is at expected position."""
        children = list(parent.children)
        assert children[expected_position].name == child_name
    
    def assert_node_removed_from_parent(self, parent, node_name):
        """Assert node no longer exists in parent's children."""
        child_names = [c.name for c in parent.children]
        assert node_name not in child_names
    
    def assert_node_added_to_parent(self, parent, node_name, expected_position=None):
        """Assert node exists in parent's children at optional position."""
        child_names = [c.name for c in parent.children]
        assert node_name in child_names
        if expected_position is not None:
            children = list(parent.children)
            assert children[expected_position].name == node_name
    
    def assert_children_promoted_to_grandparent(self, grandparent, promoted_children_csv, expected_total):
        """Assert children were promoted to grandparent."""
        grandparent_children = list(grandparent.children)
        assert len(grandparent_children) == expected_total
        grandparent_child_names = [c.name for c in grandparent_children]
        for child_name in [n.strip() for n in promoted_children_csv.split(',')]:
            assert child_name in grandparent_child_names
    
    def assert_parent_child_count(self, parent, expected_count):
        """Assert parent has expected number of children."""
        assert len(parent.children) == expected_count
    
    # =======================================================================================
    # Story Map / Epic Creation Helpers
    # =======================================================================================
    
    def create_story_map_empty(self) -> None:
        """Create an empty story map with no epics"""
        story_graph_data = {
            'epics': []
        }
        self.create_story_graph(story_graph_data)
    
    def create_story_map_with_epics(self, epic_names: list) -> None:
        """Create a story map with specified epic names"""
        epics = []
        for epic_name in epic_names:
            epics.append({
                'name': epic_name,
                'domain_concepts': [],
                'sub_epics': [],
                'story_groups': []
            })
        
        story_graph_data = {
            'epics': epics
        }
        self.create_story_graph(story_graph_data)
    
    def create_epic_with_children(self, epic_name: str, child_count: int, child_type: str = 'SubEpic') -> None:
        """Create an Epic with specified number of children."""
        epic = {
            'name': epic_name,
            'sequential_order': 0,
            'domain_concepts': [],
            'sub_epics': [],
            'story_groups': []
        }
        
        # Add children based on type
        for i in range(child_count):
            if child_type == 'SubEpic':
                epic['sub_epics'].append({
                    'name': f'{child_type}{i + 1}',
                    'sequential_order': i,
                    'sub_epics': [],
                    'story_groups': []
                })
        
        story_graph_data = {
            'epics': [epic]
        }
        self.create_story_graph(story_graph_data)
    
    def create_epic(self, epic_name: str) -> None:
        """Create a single epic with the given name. Appends to existing story graph if present."""
        story_graph_path = self.parent.workspace / 'docs' / 'stories' / 'story-graph.json'
        
        # Ensure directory exists
        story_graph_path.parent.mkdir(parents=True, exist_ok=True)
        
        if story_graph_path.exists():
            # Append to existing story graph
            existing_data = json.loads(story_graph_path.read_text(encoding='utf-8'))
            existing_data['epics'].append({
                'name': epic_name,
                'domain_concepts': [],
                'sub_epics': [],
                'story_groups': []
            })
            story_graph_path.write_text(json.dumps(existing_data, indent=2), encoding='utf-8')
            self.load_story_graph_into_bot()
        else:
            # Create new story graph
            story_graph_data = {
                'epics': [{
                    'name': epic_name,
                    'domain_concepts': [],
                    'sub_epics': [],
                    'story_groups': []
                }]
            }
            self.create_story_graph(story_graph_data)
    
    def create_story_graph_with_domain_concepts(self):
        """Create story graph with domain concepts at epic and sub-epic levels.
        
        Returns:
            Story graph dict with domain concepts including walkthroughs/realizations
        """
        story_graph = {
            "epics": [
                {
                    "name": "TestEpic",
                    "sequential_order": 0,
                    "domain_concepts": [
                        {
                            "name": "EpicDomainConcept",
                            "module": "test",
                            "responsibilities": [
                                {
                                    "name": "Manages epic operations",
                                    "collaborators": ["Operator1", "Operator2"]
                                }
                            ],
                            "realization": [
                                {
                                    "scope": "TestEpic.EpicDomainConcept",
                                    "scenario": "EpicDomainConcept manages operations",
                                    "walks": [
                                        {
                                            "covers": "Initialize concept",
                                            "object_flow": [
                                                "concept = EpicDomainConcept.create()"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "sub_epics": [
                        {
                            "name": "TestSubEpic",
                            "sequential_order": 0,
                            "domain_concepts": [
                                {
                                    "name": "SubEpicDomainConcept",
                                    "module": "test",
                                    "responsibilities": [
                                        {
                                            "name": "Handles sub-epic operations",
                                            "collaborators": ["Handler"]
                                        }
                                    ],
                                    "realization": [
                                        {
                                            "scope": "TestEpic.TestSubEpic.SubEpicDomainConcept",
                                            "scenario": "SubEpicDomainConcept handles operations",
                                            "walks": [
                                                {
                                                    "covers": "Process operations",
                                                    "object_flow": [
                                                        "result = concept.handle_operations()"
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "story_groups": [
                                {
                                    "name": "",
                                    "sequential_order": 0,
                                    "type": "and",
                                    "stories": [
                                        {
                                            "name": "TestStory",
                                            "sequential_order": 0,
                                            "scenarios": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        self.create_story_graph(story_graph)
        return story_graph
    
    def create_story_graph_with_sub_epics(self, epic_subepic_list):
        """Create story graph with epics and sub-epics.
        
        Args:
            epic_subepic_list: List of tuples [(epic_name, [subepic_names])]
        """
        epics = []
        for epic_name, subepic_names in epic_subepic_list:
            epic = {
                'name': epic_name,
                'sequential_order': len(epics),
                'domain_concepts': [],
                'sub_epics': [],
                'story_groups': []
            }
            for i, subepic_name in enumerate(subepic_names):
                epic['sub_epics'].append({
                    'name': subepic_name,
                    'sequential_order': i,
                    'sub_epics': [],
                    'story_groups': []
                })
            epics.append(epic)
        
        story_graph_data = {'epics': epics}
        self.create_story_graph(story_graph_data)
        return story_graph_data
    
    def assert_domain_concepts_match(self, actual_domain_concepts, expected_domain_concepts, context_path=""):
        """Comprehensively validate domain concepts match expected structure.
        
        Validates all fields including:
        - Basic fields: name, module, inherits_from, _source_path
        - Responsibilities: name, collaborators
        - Realizations: scope, scenario, walks with covers and object_flow
        
        Args:
            actual_domain_concepts: List of DomainConcept objects from loaded story map
            expected_domain_concepts: List of dicts with expected domain concept structure
            context_path: Path string for error messages (e.g., "TestEpic.TestSubEpic")
        
        Raises:
            AssertionError: If any field doesn't match expected structure
        """
        assert actual_domain_concepts is not None, f"Domain concepts should exist at {context_path}"
        assert len(actual_domain_concepts) == len(expected_domain_concepts), \
            f"Expected {len(expected_domain_concepts)} domain concepts at {context_path}, got {len(actual_domain_concepts)}"
        
        # Create lookup by name for easier matching
        actual_by_name = {dc.name: dc for dc in actual_domain_concepts}
        
        for expected_dc in expected_domain_concepts:
            expected_name = expected_dc['name']
            assert expected_name in actual_by_name, \
                f"Domain concept '{expected_name}' not found at {context_path}"
            
            actual_dc = actual_by_name[expected_name]
            dc_path = f"{context_path}.{expected_name}" if context_path else expected_name
            
            # Validate basic fields
            assert actual_dc.name == expected_name, \
                f"Domain concept name mismatch at {dc_path}: expected '{expected_name}', got '{actual_dc.name}'"
            
            if 'module' in expected_dc:
                assert actual_dc.module == expected_dc['module'], \
                    f"Domain concept module mismatch at {dc_path}: expected '{expected_dc['module']}', got '{actual_dc.module}'"
            
            if 'inherits_from' in expected_dc:
                assert actual_dc.inherits_from == expected_dc['inherits_from'], \
                    f"Domain concept inherits_from mismatch at {dc_path}: expected '{expected_dc['inherits_from']}', got '{actual_dc.inherits_from}'"
            
            if '_source_path' in expected_dc:
                assert actual_dc._source_path == expected_dc['_source_path'], \
                    f"Domain concept _source_path mismatch at {dc_path}: expected '{expected_dc['_source_path']}', got '{actual_dc._source_path}'"
            
            # Validate responsibilities
            expected_responsibilities = expected_dc.get('responsibilities', [])
            assert len(actual_dc.responsibilities) == len(expected_responsibilities), \
                f"Domain concept '{expected_name}' at {dc_path} should have {len(expected_responsibilities)} responsibilities, got {len(actual_dc.responsibilities)}"
            
            for idx, (actual_resp, expected_resp_dict) in enumerate(zip(actual_dc.responsibilities, expected_responsibilities)):
                expected_resp_name = expected_resp_dict['name']
                assert actual_resp.name == expected_resp_name, \
                    f"Responsibility {idx} name mismatch at {dc_path}: expected '{expected_resp_name}', got '{actual_resp.name}'"
                
                expected_collaborators = expected_resp_dict.get('collaborators', [])
                actual_collaborator_names = [c.name for c in actual_resp.collaborators]
                assert actual_collaborator_names == expected_collaborators, \
                    f"Responsibility '{actual_resp.name}' collaborators mismatch at {dc_path}: expected {expected_collaborators}, got {actual_collaborator_names}"
            
            # Validate realizations (walkthroughs)
            expected_realizations = expected_dc.get('realization', [])
            assert actual_dc.realization is not None, \
                f"Domain concept '{expected_name}' at {dc_path} should have realization field"
            assert len(actual_dc.realization) == len(expected_realizations), \
                f"Domain concept '{expected_name}' at {dc_path} should have {len(expected_realizations)} realizations, got {len(actual_dc.realization)}"
            
            for idx, (actual_real, expected_real) in enumerate(zip(actual_dc.realization, expected_realizations)):
                assert actual_real['scope'] == expected_real['scope'], \
                    f"Realization {idx} scope mismatch at {dc_path}: expected '{expected_real['scope']}', got '{actual_real['scope']}'"
                
                assert actual_real['scenario'] == expected_real['scenario'], \
                    f"Realization {idx} scenario mismatch at {dc_path}: expected '{expected_real['scenario']}', got '{actual_real['scenario']}'"
                
                expected_walks = expected_real.get('walks', [])
                assert 'walks' in actual_real, \
                    f"Realization {idx} at {dc_path} should have 'walks' field"
                assert len(actual_real['walks']) == len(expected_walks), \
                    f"Realization {idx} at {dc_path} should have {len(expected_walks)} walks, got {len(actual_real['walks'])}"
                
                for walk_idx, (actual_walk, expected_walk) in enumerate(zip(actual_real['walks'], expected_walks)):
                    assert actual_walk['covers'] == expected_walk['covers'], \
                        f"Walk {walk_idx} in realization {idx} at {dc_path}: covers mismatch - expected '{expected_walk['covers']}', got '{actual_walk['covers']}'"
                    
                    expected_object_flow = expected_walk.get('object_flow', [])
                    assert 'object_flow' in actual_walk, \
                        f"Walk {walk_idx} in realization {idx} at {dc_path} should have 'object_flow' field"
                    assert actual_walk['object_flow'] == expected_object_flow, \
                        f"Walk {walk_idx} in realization {idx} at {dc_path}: object_flow mismatch - expected {expected_object_flow}, got {actual_walk['object_flow']}"
    
    def get_expected_epic_domain_concepts(self):
        """Get expected domain concepts structure for TestEpic."""
        return [
            {
                "name": "EpicDomainConcept",
                "module": "test",
                "responsibilities": [
                    {
                        "name": "Manages epic operations",
                        "collaborators": ["Operator1", "Operator2"]
                    }
                ],
                "realization": [
                    {
                        "scope": "TestEpic.EpicDomainConcept",
                        "scenario": "EpicDomainConcept manages operations",
                        "walks": [
                            {
                                "covers": "Initialize concept",
                                "object_flow": [
                                    "concept = EpicDomainConcept.create()"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    
    def get_expected_subepic_domain_concepts(self):
        """Get expected domain concepts structure for TestSubEpic."""
        return [
            {
                "name": "SubEpicDomainConcept",
                "module": "test",
                "responsibilities": [
                    {
                        "name": "Handles sub-epic operations",
                        "collaborators": ["Handler"]
                    }
                ],
                "realization": [
                    {
                        "scope": "TestEpic.TestSubEpic.SubEpicDomainConcept",
                        "scenario": "SubEpicDomainConcept handles operations",
                        "walks": [
                            {
                                "covers": "Process operations",
                                "object_flow": [
                                    "result = concept.handle_operations()"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    
    def create_story_under_subepic(self, subepic, story_name, test_class=None):
        """Create a story under a SubEpic.
        
        Args:
            subepic: SubEpic node
            story_name: Name of the story to create
            test_class: Optional test class name
            
        Returns:
            Created Story node
        """
        # Create story using SubEpic's create_story method
        story = subepic.create_story(name=story_name)
        
        # Set test_class if provided
        if test_class:
            story.test_class = test_class
            story.save()
        
        return story
    
    def create_story_graph_with_nested_subepic_domain_concepts(self):
        """Create story graph with nested sub-epic containing domain concepts.
        
        Structure: Epic > ParentSubEpic > NestedSubEpic (with domain concepts)
        Note: ParentSubEpic must NOT have stories (constraint: cannot nest sub-epics under sub-epics with stories)
        
        Returns:
            Story graph dict with nested sub-epic structure
        """
        story_graph = {
            "epics": [
                {
                    "name": "TestEpic",
                    "sequential_order": 0,
                    "domain_concepts": [],
                    "sub_epics": [
                        {
                            "name": "ParentSubEpic",
                            "sequential_order": 0,
                            "domain_concepts": [],
                            "sub_epics": [
                                {
                                    "name": "NestedSubEpic",
                                    "sequential_order": 0,
                                    "domain_concepts": [
                                        {
                                            "name": "NestedSubEpicDomainConcept",
                                            "module": "test",
                                            "responsibilities": [
                                                {
                                                    "name": "Handles nested sub-epic operations",
                                                    "collaborators": ["NestedHandler"]
                                                }
                                            ],
                                            "realization": [
                                                {
                                                    "scope": "TestEpic.ParentSubEpic.NestedSubEpic.NestedSubEpicDomainConcept",
                                                    "scenario": "NestedSubEpicDomainConcept handles nested operations",
                                                    "walks": [
                                                        {
                                                            "covers": "Process nested operations",
                                                            "object_flow": [
                                                                "result = nested_concept.process_nested_operations()"
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "story_groups": [],
                                    "sub_epics": []
                                }
                            ],
                            "story_groups": []  # Must be empty - cannot nest under sub-epic with stories
                        }
                    ]
                }
            ]
        }
        
        self.create_story_graph(story_graph)
        return story_graph
    
    def get_expected_nested_subepic_domain_concepts(self):
        """Get expected domain concepts structure for NestedSubEpic."""
        return [
            {
                "name": "NestedSubEpicDomainConcept",
                "module": "test",
                "responsibilities": [
                    {
                        "name": "Handles nested sub-epic operations",
                        "collaborators": ["NestedHandler"]
                    }
                ],
                "realization": [
                    {
                        "scope": "TestEpic.ParentSubEpic.NestedSubEpic.NestedSubEpicDomainConcept",
                        "scenario": "NestedSubEpicDomainConcept handles nested operations",
                        "walks": [
                            {
                                "covers": "Process nested operations",
                                "object_flow": [
                                    "result = nested_concept.process_nested_operations()"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    
    def find_nested_subepic(self, parent_subepic, nested_subepic_name):
        """Find nested sub-epic under a parent sub-epic.
        
        Args:
            parent_subepic: Parent SubEpic node
            nested_subepic_name: Name of the nested sub-epic to find
            
        Returns:
            Nested SubEpic node or None if not found
        """
        # Find nested sub-epic by iterating through _children
        # Use type name check instead of isinstance to avoid import issues
        return next((child for child in parent_subepic._children if type(child).__name__ == 'SubEpic' and child.name == nested_subepic_name), None)
    
    # =======================================================================================
    # Behavior Determination Helpers
    # =======================================================================================
    
    def create_epic_with_sub_epics_for_behavior_test(self, epic_name, sub_epics_data):
        """Create an epic with sub-epics for behavior determination testing.
        
        Sub-epics can contain either:
        - Stories directly
        - Nested sub-epics with their own stories
        
        Args:
            epic_name: Name of the epic
            sub_epics_data: List of dicts with sub-epic configuration:
                {
                    'name': str,
                    'nested_sub_epics': [],  # Optional nested sub-epics
                    'stories': []  # Optional stories
                }
        
        Returns:
            Epic node from loaded story graph
        """
        # Create dummy test files for all stories with test_methods (including nested)
        self._create_test_files_for_sub_epics(sub_epics_data)
        
        # Build sub-epics
        sub_epics = []
        for idx, sub_epic_data in enumerate(sub_epics_data):
            sub_epic = self._build_sub_epic_for_behavior_test(sub_epic_data, idx)
            sub_epics.append(sub_epic)
        
        # Create story graph structure
        story_graph_data = {
            'epics': [
                {
                    'name': epic_name,
                    'behavior': 'exploration',
                    'domain_concepts': [],
                    'sub_epics': sub_epics
                }
            ]
        }
        
        # Save and load
        self.create_story_graph(story_graph_data)
        
        # Return the epic node
        return self.bot.story_graph.epics[epic_name]
    
    def _build_sub_epic_for_behavior_test(self, sub_epic_data, idx):
        """Build a sub-epic dict for behavior testing.
        
        Handles both stories and nested sub-epics recursively.
        """
        sub_epic = {
            'name': sub_epic_data['name'],
            'sequential_order': float(idx),
            'behavior': 'exploration',
            'test_file': None,
            'sub_epics': [],
            'story_groups': []
        }
        
        # Check if this sub-epic has nested sub-epics
        if sub_epic_data.get('nested_sub_epics'):
            # Build nested sub-epics recursively
            for nested_idx, nested_data in enumerate(sub_epic_data['nested_sub_epics']):
                nested_sub_epic = self._build_sub_epic_for_behavior_test(nested_data, nested_idx)
                sub_epic['sub_epics'].append(nested_sub_epic)
        
        # Build stories if present
        if sub_epic_data.get('stories'):
            stories = []
            # Collect all test classes for consolidation
            all_test_classes = {}  # test_class_name -> test_methods mapping
            test_file_for_sub_epic = None
            
            for story_data in sub_epic_data['stories']:
                if story_data.get('test_class') and story_data.get('test_methods'):
                    test_file = story_data.get('test_class')  # This is actually the test file name
                    # Use first story's test_file as SubEpic's test_file
                    if not test_file_for_sub_epic:
                        test_file_for_sub_epic = test_file
                    
                    # Extract class name from test file
                    test_class_name = test_file.replace('.py', '').replace('test_', '')
                    test_class_name = ''.join(word.capitalize() for word in test_class_name.split('_'))
                    test_class_name = 'Test' + test_class_name if not test_class_name.startswith('Test') else test_class_name
                    
                    # Store test class and methods for later consolidation
                    all_test_classes[test_class_name] = story_data.get('test_methods', [])
            
            # Create a single consolidated test file for the SubEpic
            if test_file_for_sub_epic and all_test_classes:
                self._create_consolidated_test_file(test_file_for_sub_epic, all_test_classes)
            
            # Set test_file on SubEpic
            sub_epic['test_file'] = test_file_for_sub_epic
            
            for story_idx, story_data in enumerate(sub_epic_data['stories']):
                story = self._build_story_for_behavior_test(story_data, story_idx)
                stories.append(story)
                
                # Get test file from first story with test_class
                if not test_file_for_sub_epic and story_data.get('test_class'):
                    test_file_for_sub_epic = story_data.get('test_class')  # This is the test file
            
            # Set test_file on sub-epic if found
            if test_file_for_sub_epic:
                sub_epic['test_file'] = test_file_for_sub_epic
            
            # Add stories to a story group
            sub_epic['story_groups'].append({
                'name': '',
                'sequential_order': 0.0,
                'type': 'and',
                'connector': None,
                'behavior': 'exploration',
                'stories': stories
            })
        
        return sub_epic
    
    def _build_story_for_behavior_test(self, story_data, idx):
        """Build a story dict for behavior testing."""
        # Extract test class name from test file
        test_file = story_data.get('test_class')  # This is actually the test file
        test_class_name = None
        if test_file:
            test_class_name = test_file.replace('.py', '').replace('test_', '')
            test_class_name = ''.join(word.capitalize() for word in test_class_name.split('_'))
            test_class_name = 'Test' + test_class_name if not test_class_name.startswith('Test') else test_class_name
        
        return {
            'name': story_data['story_name'],
            'sequential_order': float(idx + 1),
            'connector': None,
            'story_type': 'user',
            'users': [],
            # Stories don't have test_file - it comes from parent SubEpic
            'test_class': test_class_name,
            'scenarios': self._build_scenarios_for_behavior_test(
                story_data.get('scenarios', []),
                story_data.get('test_methods', [])
            ),
            'acceptance_criteria': self._build_acceptance_criteria_for_behavior_test(
                story_data.get('acceptance_criteria', '')
            ),
            'behavior': 'exploration'
        }
    
    def _build_scenarios_for_behavior_test(self, scenarios, test_methods):
        """Build scenarios list for behavior testing."""
        if not scenarios:
            return []
        
        scenario_list = []
        for idx, scenario_name in enumerate(scenarios):
            test_method = test_methods[idx] if idx < len(test_methods) else None
            scenario_list.append({
                'name': scenario_name,
                'sequential_order': float(idx + 1),
                'type': 'happy_path',
                'background': [],
                'test_method': test_method,
                'steps': ''
            })
        
        return scenario_list
    
    def _build_acceptance_criteria_for_behavior_test(self, acceptance_criteria):
        """Build acceptance criteria list for behavior testing."""
        if not acceptance_criteria:
            return []
        
        # Split by semicolon to get individual AC items
        ac_items = [ac.strip() for ac in acceptance_criteria.split(';') if ac.strip()]
        
        ac_list = []
        for idx, ac_text in enumerate(ac_items):
            ac_list.append({
                'name': ac_text,
                'text': ac_text,
                'sequential_order': float(idx + 1)
            })
        
        return ac_list
    
    def create_sub_epic_with_stories_for_behavior_test(self, sub_epic_name, stories_data):
        """Create a sub-epic with multiple stories for behavior determination testing.
        
        Args:
            sub_epic_name: Name of the sub-epic
            stories_data: List of dicts with story configuration
        
        Returns:
            SubEpic node from loaded story graph
        """
        # Create a single test file for the SubEpic containing all test classes
        # Determine SubEpic's test_file (use first story's test_file if available)
        sub_epic_test_file = None
        all_test_classes = {}  # test_class_name -> test_methods mapping
        
        for story_data in stories_data:
            if story_data.get('test_class') and story_data.get('test_methods'):
                test_file = story_data.get('test_class')  # This is actually the test file name
                # Use first story's test_file as SubEpic's test_file
                if not sub_epic_test_file:
                    sub_epic_test_file = test_file
                
                # Extract class name from test file
                test_class_name = test_file.replace('.py', '').replace('test_', '')
                test_class_name = ''.join(word.capitalize() for word in test_class_name.split('_'))
                test_class_name = 'Test' + test_class_name if not test_class_name.startswith('Test') else test_class_name
                
                # Store test class and methods for later consolidation
                all_test_classes[test_class_name] = story_data.get('test_methods', [])
        
        # Create a single consolidated test file for the SubEpic
        if sub_epic_test_file and all_test_classes:
            self._create_consolidated_test_file(sub_epic_test_file, all_test_classes)
        
        # Build stories for the story group
        stories = []
        for idx, story_data in enumerate(stories_data):
            story = self._build_story_for_behavior_test(story_data, idx)
            stories.append(story)
        
        # Create story graph structure with sub-epic containing multiple stories
        story_graph_data = {
            'epics': [
                {
                    'name': 'Test Epic',
                    'behavior': 'exploration',
                    'domain_concepts': [],
                    'sub_epics': [
                        {
                            'name': sub_epic_name,
                            'sequential_order': 0.0,
                            'behavior': 'exploration',
                            'test_file': sub_epic_test_file,
                            'sub_epics': [],
                            'story_groups': [
                                {
                                    'name': '',
                                    'sequential_order': 0.0,
                                    'type': 'and',
                                    'connector': None,
                                    'behavior': 'exploration',
                                    'stories': stories
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Save and load
        self.create_story_graph(story_graph_data)
        
        # Return the sub-epic node
        epic = self.bot.story_graph.epics['Test Epic']
        return epic.children[0]
    
    def create_story_with_state_for_behavior_test(self, epic_name, story_name, test_class, acceptance_criteria, scenarios, test_methods):
        """Create a story with specified completeness state for behavior determination testing.
        
        Returns a Story object with:
        - Acceptance criteria (if provided)
        - Scenarios (if provided)
        - Test methods mapped to scenarios (if provided)
        """
        # Create story graph structure
        story_graph_data = {
            'epics': [
                {
                    'name': epic_name,
                    'behavior': 'exploration',
                    'domain_concepts': [],
                    'sub_epics': [
                        {
                            'name': 'Test SubEpic',
                            'sequential_order': 0.0,
                            'behavior': 'exploration',
                            'test_file': test_class if test_class else None,
                            'sub_epics': [],
                            'story_groups': [
                                {
                                    'name': '',
                                    'sequential_order': 0.0,
                                    'type': 'and',
                                    'connector': None,
                                    'behavior': 'exploration',
                                    'stories': [
                                        {
                                            'name': story_name,
                                            'sequential_order': 1.0,
                                            'connector': None,
                                            'story_type': 'user',
                                            'users': [],
                                            'test_file': None,
                                            'test_class': test_class if test_class else None,
                                            'scenarios': self._build_scenarios_for_behavior_test(scenarios, test_methods),
                                            'acceptance_criteria': self._build_acceptance_criteria_for_behavior_test(acceptance_criteria),
                                            'behavior': 'exploration'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Create dummy test file if test_class and test_methods provided  
        # Extract test file and test class properly
        if test_class and test_methods:
            # test_class is actually the test file (e.g., "test_file_upload.py")
            test_file = test_class
            # Convert test file to class name (test_file_upload.py -> TestFileUpload)
            test_class_name = test_file.replace('.py', '').replace('test_', '')
            test_class_name = ''.join(word.capitalize() for word in test_class_name.split('_'))
            test_class_name = 'Test' + test_class_name if not test_class_name.startswith('Test') else test_class_name
            
            # Also set test_class on story for the domain to find
            story_graph_data['epics'][0]['sub_epics'][0]['story_groups'][0]['stories'][0]['test_class'] = test_class_name
            
            self._create_dummy_test_file(test_file, test_class_name, test_methods)
        
        # Save and load
        self.create_story_graph(story_graph_data)
        
        # Return the story node
        epic = self.bot.story_graph.epics[epic_name]
        sub_epic = epic.children[0]
        story = sub_epic.children[0]
        
        return story
    
    def _create_dummy_test_file(self, test_file, test_class, test_methods):
        """Create a dummy test file with test class and methods."""
        test_dir = self.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        
        test_path = test_dir / test_file
        
        # Generate test file content
        content = f"""import pytest

class {test_class}:
"""
        for test_method in test_methods:
            if test_method:
                content += f"""    def {test_method}(self):
        pass
    
"""
        
        test_path.write_text(content, encoding='utf-8')
    
    def _create_consolidated_test_file(self, test_file, test_classes_dict):
        """Create a single test file containing multiple test classes (one per story in SubEpic)."""
        test_dir = self.workspace / 'test'
        test_dir.mkdir(exist_ok=True)
        
        test_path = test_dir / test_file
        
        # Generate consolidated test file content with all test classes
        content = "import pytest\n\n"
        for test_class_name, test_methods in test_classes_dict.items():
            content += f"class {test_class_name}:\n"
            for test_method in test_methods:
                if test_method:
                    content += f"""    def {test_method}(self):
        pass
    
"""
            content += "\n"
        
        test_path.write_text(content, encoding='utf-8')
    
    def _create_test_files_for_sub_epics(self, sub_epics_data):
        """Recursively create test files for all stories in sub-epics."""
        for sub_epic_data in sub_epics_data:
            # Create test files for direct stories
            if sub_epic_data.get('stories'):
                for story_data in sub_epic_data['stories']:
                    if story_data.get('test_class') and story_data.get('test_methods'):
                        self._create_dummy_test_file_for_story(story_data)
            
            # Recursively handle nested sub-epics
            if sub_epic_data.get('nested_sub_epics'):
                self._create_test_files_for_sub_epics(sub_epic_data['nested_sub_epics'])
    
    def _create_dummy_test_file_for_story(self, story_data):
        """Create a dummy test file for a story with test_class and test_methods."""
        test_file = story_data.get('test_class')  # This is actually the test file
        test_methods = story_data.get('test_methods', [])
        
        if not test_file or not test_methods:
            return
        
        # Extract class name from test file (test_file_upload.py -> TestFileUpload)
        test_class_name = test_file.replace('.py', '').replace('test_', '')
        test_class_name = ''.join(word.capitalize() for word in test_class_name.split('_'))
        test_class_name = 'Test' + test_class_name if not test_class_name.startswith('Test') else test_class_name
        
        # Don't modify story_data - that will be used later to build the story
        # Just create the test file with the calculated class name
        self._create_dummy_test_file(test_file, test_class_name, test_methods)
    
    # =======================================================================================
    # File Testing Helpers
    # =======================================================================================
    
    def create_test_file(self, test_file_path: str, test_class: str, test_methods: list = None) -> Path:
        """Create a test file with test class and methods.
        
        Args:
            test_file_path: Relative path from workspace/test (e.g., 'invoke_bot/edit_story_map/test_open_story_related_files.py')
            test_class: Name of test class (e.g., 'TestOpenAllRelatedFiles')
            test_methods: List of test method names (e.g., ['test_graph_button_opens_story_graph'])
        
        Returns:
            Path to created test file
        """
        test_dir = self.parent.workspace / 'test'
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / test_file_path
        
        # Create parent directories if they don't exist
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"class {test_class}:\n"
        if test_methods:
            for method in test_methods:
                content += f"    def {method}(self):\n        pass\n"
        else:
            content += "    pass\n"
        
        test_file.write_text(content, encoding='utf-8')
        return test_file
    
    def assert_file_exists(self, file_path, description: str = "File") -> Path:
        """Assert that a file path exists and return Path object.
        
        Args:
            file_path: File path (string or Path)
            description: Description for error message
        
        Returns:
            Path object for the file
        """
        file_path_obj = Path(file_path)
        assert file_path_obj.exists(), f"{description} should exist at {file_path_obj}"
        return file_path_obj
    
    def assert_story_graph_line_contains_node(self, story_graph_path: Path, line_number: int, node_name: str):
        """Assert that a line in story graph JSON contains the node name.
        
        Args:
            story_graph_path: Path to story-graph.json
            line_number: Line number (1-based)
            node_name: Expected node name
        """
        assert story_graph_path.exists(), f"Story graph file should exist at {story_graph_path}"
        assert line_number is not None, "Line number should be found for node in JSON"
        with open(story_graph_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            line_at_position = lines[line_number - 1]
            assert f'"name": "{node_name}"' in line_at_position, f"Line {line_number} should contain node name: {line_at_position}"
    
    def create_story_files_for_node(self, node):
        """Create story markdown files for a node and all its children recursively.
        
        Args:
            node: StoryNode (Story, SubEpic, or Epic) to create files for
        """
        from story_graph.nodes import Story, Epic, SubEpic
        
        # Calculate file_link by calling save if it's a Story
        if isinstance(node, Story):
            node.save()  # This calculates file_link
            if node.file_link:
                story_file_path = Path(node.file_link)
                story_file_path.parent.mkdir(parents=True, exist_ok=True)
                story_file_path.write_text(f"# {node.name}\n\n", encoding='utf-8')
        elif isinstance(node, (Epic, SubEpic)):
            # Recursively create files for all child stories
            for child in node.children:
                self.create_story_files_for_node(child)

