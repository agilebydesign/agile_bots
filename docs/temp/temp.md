**Combined instructions:** The following combines multiple actions. Perform them one after another.

## Scope

**Story Scope:** Act With Selected Node

Please only work on the following scope.

Scope Filter: "Act With Selected Node"

Scope:

{
  "path": "C:\\dev\\agile_bots\\docs\\story\\story-graph.json",
  "has_epics": true,
  "has_increments": true,
  "has_domain_concepts": true,
  "epic_count": 1,
  "content": {
    "epics": [
      {
        "name": "Invoke Bot",
        "sub_epics": [
          {
            "name": "Work With Story Map",
            "sub_epics": [
              {
                "name": "Act With Selected Node",
                "sub_epics": [],
                "story_groups": [
                  {
                    "name": null,
                    "stories": [
                      {
                        "name": "Set scope to selected story node",
                        "acceptance_criteria": []
                      },
                      {
                        "name": "Submit action for selected story node",
                        "acceptance_criteria": [
                          {
                            "name": "Child1",
                            "text": "Child1",
                            "sequential_order": 1.0
                          }
                        ]
                      },
                      {
                        "name": "Submit Current Behavior Action For Selected Node",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN action executes\nTHEN action completes successfully",
                            "text": "WHEN action executes\nTHEN action completes successfully",
                            "sequential_order": 1.0
                          }
                        ]
                      },
                      {
                        "name": "Set scope to selected Increment",
                        "acceptance_criteria": []
                      },
                      {
                        "name": "Copy Story Node To Clipboard",
                        "acceptance_criteria": [
                          {
                            "name": "Right-click on a story node shows context menu with Copy node name and Copy full JSON",
                            "text": "Right-click on a story node shows context menu with Copy node name and Copy full JSON",
                            "sequential_order": 1.0
                          },
                          {
                            "name": "Copy node name writes node name to system clipboard via event -> CLI -> bot.copy_name",
                            "text": "Copy node name writes node name to system clipboard via event -> CLI -> bot.copy_name",
                            "sequential_order": 2.0
                          },
                          {
                            "name": "Copy full JSON writes node JSON (story-graph shape) to system clipboard via event -> CLI -> bot.copy_json",
                            "text": "Copy full JSON writes node JSON (story-graph shape) to system clipboard via event -> CLI -> bot.copy_json",
                            "sequential_order": 3.0
                          }
                        ]
                      },
                      {
                        "name": "Render Diagram Selected Node",
                        "acceptance_criteria": [
                          {
                            "name": "WHEN User selects story node in Panel story tree\nTHEN Panel action bar shows [Render diagram] [Save layout] [Clear layout] [Update graph] buttons",
                            "text": "WHEN User selects story node in Panel story tree\nTHEN Panel action bar shows [Render diagram] [Save layout] [Clear layout] [Update graph] buttons",
                            "sequential_order": 1.0
                          },
                          {
                            "name": "WHEN User clicks [Render diagram] in Panel\nTHEN Panel renders diagram for selected node scope",
                            "text": "WHEN User clicks [Render diagram] in Panel\nTHEN Panel renders diagram for selected node scope",
                            "sequential_order": 2.0
                          },
                          {
                            "name": "WHEN User clicks [Save layout] in Panel\nTHEN Panel persists layout to DrawIO file",
                            "text": "WHEN User clicks [Save layout] in Panel\nTHEN Panel persists layout to DrawIO file",
                            "sequential_order": 3.0
                          },
                          {
                            "name": "WHEN User clicks [Update graph] in Panel\nTHEN Panel generates update report AND Panel applies changes to story-graph.json",
                            "text": "WHEN User clicks [Update graph] in Panel\nTHEN Panel generates update report AND Panel applies changes to story-graph.json",
                            "sequential_order": 4.0
                          },
                          {
                            "name": "WHEN User runs cli.story_graph.\"Invoke Bot\".\"Act With Selected Node\".render_diagram\nTHEN CLI renders diagram for current scope AND CLI reports completion",
                            "text": "WHEN User runs cli.story_graph.\"Invoke Bot\".\"Act With Selected Node\".render_diagram\nTHEN CLI renders diagram for current scope AND CLI reports completion",
                            "sequential_order": 5.0
                          }
                        ]
                      },
                      {
                        "name": "Update Queie based on selectged Node",
                        "acceptance_criteria": []
                      },
                      {
                        "name": "Execute Scope \"Runs\"",
                        "acceptance_criteria": []
                      }
                    ]
                  }
                ],
                "domain_concepts": [
                  {
                    "name": "StoryMapView",
                    "responsibilities": [
                      {
                        "name": "Shows diagram action buttons",
                        "collaborators": [
                          "RenderDiagram",
                          "SaveLayout",
                          "ClearLayout",
                          "UpdateGraph"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "RenderDiagram",
                    "responsibilities": [
                      {
                        "name": "Renders diagram for scope",
                        "collaborators": [
                          "StoryNode",
                          "StoryMap"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "SaveLayout",
                    "responsibilities": [
                      {
                        "name": "Persists layout to DrawIO",
                        "collaborators": [
                          "DrawIO"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "ClearLayout",
                    "responsibilities": [
                      {
                        "name": "Clears diagram layout",
                        "collaborators": [
                          "DrawIO"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "UpdateGraph",
                    "responsibilities": [
                      {
                        "name": "Applies changes to story graph",
                        "collaborators": [
                          "UpdateReport",
                          "StoryMap"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "DrawIO",
                    "responsibilities": [
                      {
                        "name": "Persists layout",
                        "collaborators": [
                          "File"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "UpdateReport",
                    "responsibilities": [
                      {
                        "name": "Reports changes",
                        "collaborators": [
                          "StoryMap"
                        ]
                      }
                    ]
                  },
                  {
                    "name": "render_diagram",
                    "responsibilities": [
                      {
                        "name": "CLI command to render diagram for scope",
                        "collaborators": [
                          "RenderDiagram"
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
                "stories": []
              }
            ],
            "domain_concepts": [
              {
                "name": "StoryNode (Base)",
                "responsibilities": [
                  {
                    "name": "Serializes",
                    "collaborators": [
                      "StoryNodeSerializer"
                    ]
                  },
                  {
                    "name": "Get/Update name",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get node type",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get node ID",
                    "collaborators": [
                      "String",
                      "StoryNode",
                      "StoryNodeNavigator"
                    ]
                  },
                  {
                    "name": "Get parent",
                    "collaborators": [
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Get sequential order",
                    "collaborators": [
                      "StoryNodeNavigator",
                      "Float"
                    ]
                  },
                  {
                    "name": "Contains Children",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Delete self",
                    "collaborators": [
                      "StoryNodeSerializer"
                    ]
                  },
                  {
                    "name": "Delete with children",
                    "collaborators": [
                      "StoryNodeSerializer",
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Get/Update test",
                    "collaborators": [
                      "Test"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryNodeChildren",
                "responsibilities": [
                  {
                    "name": "Get children",
                    "collaborators": [
                      "List[StoryNode]"
                    ]
                  },
                  {
                    "name": "Find child by name",
                    "collaborators": [
                      "String",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Delete child",
                    "collaborators": [
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryNodeNavigator",
                "responsibilities": [
                  {
                    "name": "Build node ID from hierarchy path",
                    "collaborators": [
                      "String",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Get parent",
                    "collaborators": [
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Move to parent",
                    "collaborators": [
                      "New Parent",
                      "Position"
                    ]
                  },
                  {
                    "name": "Move after",
                    "collaborators": [
                      "StoryNode",
                      "sequential order"
                    ]
                  },
                  {
                    "name": "Move before",
                    "collaborators": [
                      "StoryNode",
                      "sequential order"
                    ]
                  },
                  {
                    "name": "DetermineOrder",
                    "collaborators": [
                      "FLoat",
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryNodeSerializer",
                "responsibilities": [
                  {
                    "name": "File",
                    "collaborators": [
                      "File"
                    ]
                  },
                  {
                    "name": "Create Node",
                    "collaborators": [
                      "File",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Load Node",
                    "collaborators": [
                      "File",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Update Node",
                    "collaborators": [
                      "File",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Delete Node",
                    "collaborators": [
                      "File",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "From JSON",
                    "collaborators": [
                      "JSON",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "To JSON",
                    "collaborators": [
                      "JSON",
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYStoryNode",
                "responsibilities": [
                  {
                    "name": "Serialize node to TTY",
                    "collaborators": [
                      "StoryNode",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format name",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format sequential order",
                    "collaborators": [
                      "Float",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format children",
                    "collaborators": [
                      "List[StoryNode]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Add child",
                    "collaborators": [
                      "StoryNode",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Add child at position",
                    "collaborators": [
                      "StoryNode",
                      "Position",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Delete child",
                    "collaborators": [
                      "StoryNode",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Delete this node",
                    "collaborators": [
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Delete with children",
                    "collaborators": [
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Update name",
                    "collaborators": [
                      "String",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Move to parent",
                    "collaborators": [
                      "New Parent",
                      "Position",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Move after target",
                    "collaborators": [
                      "Target StoryNode",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Move before target",
                    "collaborators": [
                      "Target StoryNode",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Reorder children",
                    "collaborators": [
                      "Start Pos",
                      "End Pos",
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Automatically refresh story graph",
                    "collaborators": [
                      "CLI Result"
                    ]
                  },
                  {
                    "name": "Wraps domain story node",
                    "collaborators": [
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "inherits_from": "TTYAdapter (Base)",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONStoryNode",
                "responsibilities": [
                  {
                    "name": "Serialize node to JSON",
                    "collaborators": [
                      "StoryNode",
                      "JSON String"
                    ]
                  },
                  {
                    "name": "Include name",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include sequential order",
                    "collaborators": [
                      "Float",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include children",
                    "collaborators": [
                      "List[StoryNode]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Add child",
                    "collaborators": [
                      "StoryNode",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Add child at position",
                    "collaborators": [
                      "StoryNode",
                      "Position",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Delete child",
                    "collaborators": [
                      "StoryNode",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Delete this node",
                    "collaborators": [
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Delete with children",
                    "collaborators": [
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Update name",
                    "collaborators": [
                      "String",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Move to parent",
                    "collaborators": [
                      "New Parent",
                      "Position",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Move after target",
                    "collaborators": [
                      "Target StoryNode",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Move before target",
                    "collaborators": [
                      "Target StoryNode",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Reorder children",
                    "collaborators": [
                      "Start Pos",
                      "End Pos",
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Automatically refresh story graph",
                    "collaborators": [
                      "JSON Result"
                    ]
                  },
                  {
                    "name": "Wraps domain story node",
                    "collaborators": [
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "inherits_from": "JSONAdapter (Base)",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownStoryNode",
                "responsibilities": [
                  {
                    "name": "Serialize node to Markdown",
                    "collaborators": [
                      "StoryNode",
                      "Markdown String"
                    ]
                  },
                  {
                    "name": "Format node header",
                    "collaborators": [
                      "String",
                      "Sequential Order",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format children list",
                    "collaborators": [
                      "List[StoryNode]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain story node",
                    "collaborators": [
                      "StoryNode"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "inherits_from": "MarkdownAdapter (Base)",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryNodeView",
                "responsibilities": [
                  {
                    "name": "Wraps story node JSON",
                    "collaborators": [
                      "StoryNode JSON"
                    ]
                  },
                  {
                    "name": "Toggles collapsed",
                    "collaborators": [
                      "State"
                    ]
                  },
                  {
                    "name": "Add child node",
                    "collaborators": [
                      "StoryNode",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Add child at position",
                    "collaborators": [
                      "StoryNode",
                      "Position",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Delete this node",
                    "collaborators": [
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Delete with children",
                    "collaborators": [
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Update node name",
                    "collaborators": [
                      "String",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Move to parent",
                    "collaborators": [
                      "New Parent",
                      "Position",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Move after target",
                    "collaborators": [
                      "Target StoryNode",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Move before target",
                    "collaborators": [
                      "Target StoryNode",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Drag and drop",
                    "collaborators": [
                      "Drop Target",
                      "Position",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Reorder children",
                    "collaborators": [
                      "Start Pos",
                      "End Pos",
                      "Panel Result"
                    ]
                  },
                  {
                    "name": "Automatically refresh story graph",
                    "collaborators": [
                      "Panel Result"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "inherits_from": "PanelView (Base)",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryMap",
                "responsibilities": [
                  {
                    "name": "Load from bot directory",
                    "collaborators": [
                      "Bot",
                      "StoryMap"
                    ]
                  },
                  {
                    "name": "Load from story graph",
                    "collaborators": [
                      "File Path",
                      "StoryMap"
                    ]
                  },
                  {
                    "name": "Walk nodes",
                    "collaborators": [
                      "StoryNode",
                      "Iterator[StoryNode]"
                    ]
                  },
                  {
                    "name": "Get all stories",
                    "collaborators": [
                      "List[Story]"
                    ]
                  },
                  {
                    "name": "Get all scenarios",
                    "collaborators": [
                      "List[Scenario]"
                    ]
                  },
                  {
                    "name": "Get all domain concepts",
                    "collaborators": [
                      "List[DomainConcept]"
                    ]
                  },
                  {
                    "name": "Find by name",
                    "collaborators": [
                      "Name",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Find node by path",
                    "collaborators": [
                      "Path String",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Get story graph dict",
                    "collaborators": [
                      "Dict"
                    ]
                  },
                  {
                    "name": "Get epics",
                    "collaborators": [
                      "List[Epic]"
                    ]
                  },
                  {
                    "name": "Save to story graph",
                    "collaborators": [
                      "File Path"
                    ]
                  },
                  {
                    "name": "Reload from story graph",
                    "collaborators": [
                      "File Path",
                      "StoryMap"
                    ]
                  },
                  {
                    "name": "Validate graph structure",
                    "collaborators": [
                      "Validation Result"
                    ]
                  }
                ],
                "module": "story_graph.story_map",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYStoryMap",
                "responsibilities": [
                  {
                    "name": "Serialize story map to TTY",
                    "collaborators": [
                      "StoryMap",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format epics list",
                    "collaborators": [
                      "List[Epic]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format story hierarchy",
                    "collaborators": [
                      "StoryMap",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Walk and format nodes",
                    "collaborators": [
                      "StoryNode",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain story map",
                    "collaborators": [
                      "StoryMap"
                    ]
                  }
                ],
                "module": "story_graph.story_map",
                "inherits_from": "TTYAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONStoryMap",
                "responsibilities": [
                  {
                    "name": "Serialize story map to JSON",
                    "collaborators": [
                      "StoryMap",
                      "JSON String"
                    ]
                  },
                  {
                    "name": "Include story graph",
                    "collaborators": [
                      "Dict",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include all epics",
                    "collaborators": [
                      "List[Epic]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Wraps domain story map",
                    "collaborators": [
                      "StoryMap"
                    ]
                  }
                ],
                "module": "story_graph.story_map",
                "inherits_from": "JSONAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownStoryMap",
                "responsibilities": [
                  {
                    "name": "Serialize story map to Markdown",
                    "collaborators": [
                      "StoryMap",
                      "Markdown String"
                    ]
                  },
                  {
                    "name": "Format epic hierarchy",
                    "collaborators": [
                      "List[Epic]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format story index",
                    "collaborators": [
                      "List[Story]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain story map",
                    "collaborators": [
                      "StoryMap"
                    ]
                  }
                ],
                "module": "story_graph.story_map",
                "inherits_from": "MarkdownAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryMapView",
                "responsibilities": [
                  {
                    "name": "Wraps story map JSON",
                    "collaborators": [
                      "StoryMap JSON"
                    ]
                  },
                  {
                    "name": "Renders story graph as tree hierarchy",
                    "collaborators": [
                      "StoryNode",
                      "HTML"
                    ]
                  },
                  {
                    "name": "Displays epic hierarchy",
                    "collaborators": [
                      "EpicView",
                      "Epic JSON"
                    ]
                  },
                  {
                    "name": "Shows context-appropriate action buttons",
                    "collaborators": [
                      "StoryNode",
                      "ButtonSet"
                    ]
                  },
                  {
                    "name": "Refreshes tree display",
                    "collaborators": [
                      "StoryGraph",
                      "DOM"
                    ]
                  },
                  {
                    "name": "Searches stories",
                    "collaborators": [
                      "Filter",
                      "StoryGraph JSON"
                    ]
                  },
                  {
                    "name": "Opens story graph file",
                    "collaborators": [
                      "CLI",
                      "File JSON"
                    ]
                  },
                  {
                    "name": "Opens story map file",
                    "collaborators": [
                      "CLI",
                      "File JSON"
                    ]
                  },
                  {
                    "name": "Delegates to InlineNameEditor",
                    "collaborators": [
                      "InlineNameEditor",
                      "StoryNode"
                    ]
                  },
                  {
                    "name": "Delegates to StoryNodeDragDropManager",
                    "collaborators": [
                      "StoryNodeDragDropManager",
                      "StoryNode"
                    ]
                  }
                ],
                "realization": [
                  {
                    "scope": "Invoke Bot Through Panel.Filter And Navigate Scope.Display Story Scope Hierarchy",
                    "scenario": "Panel displays nested epic/sub-epic/story/scenario hierarchy from story graph JSON, user can expand/collapse and navigate",
                    "walks": [
                      {
                        "covers": "Rendering 4-level nested hierarchy from JSON",
                        "object_flow": [
                          "this.storyMapJSON = storyMapJSON",
                          "this.cliClient = cliClient",
                          "html: String = this.render()",
                          "  -> epicsHTML: String = this.render_all_epics()",
                          "     epicView: EpicView = new EpicView(epic, this.cliClient)",
                          "     epicHTML: String = epicView.render()",
                          "       -> name: String = this.epicJSON.name",
                          "       -> icon: String = this.epicJSON.icon",
                          "       -> subEpicsHTML: String = this.render_sub_epics()",
                          "          subEpicView: SubEpicView = new SubEpicView(subEpic, this.cliClient)",
                          "          subEpicHTML: String = subEpicView.render()",
                          "            -> storiesHTML: String = this.render_stories()",
                          "               storyView: StoryView = new StoryView(story, this.cliClient)",
                          "               storyHTML: String = storyView.render()",
                          "                 -> scenariosHTML: String = this.render_scenarios()",
                          "                    return scenariosHTML: \"<div>Scenario 1</div>...\"",
                          "                 return `<div>${this.storyJSON.name}${scenariosHTML}</div>`",
                          "               return storiesHTML: \"<div>Story 1...</div>\"",
                          "            return `<div>${this.subEpicJSON.name}${storiesHTML}</div>`",
                          "          return subEpicsHTML: \"<div>Sub-Epic 1...</div>\"",
                          "       return `<div>${name}${subEpicsHTML}</div>`",
                          "     return epicsHTML: \"<div>Epic 1...</div>\"",
                          "return epicsHTML"
                        ]
                      },
                      {
                        "covers": "User opens epic folder via CLI",
                        "object_flow": [
                          "EpicView.onFolderClick()",
                          "  -> folderPath: String = this.epicJSON.folder_path",
                          "  -> this.cliClient.sendMessage({command: 'openScope', filePath: folderPath})",
                          "     -> vscode.commands.executeCommand('vscode.open', fileUri)",
                          "return"
                        ]
                      }
                    ],
                    "model_updates": []
                  }
                ],
                "module": "story_graph.story_map",
                "inherits_from": "PanelView",
                "_source_path": "Invoke Bot.Invoke Bot Directly",
                "instantiated_with": [
                  "StoryGraph",
                  "PanelView"
                ],
                "ownership": {
                  "has": [
                    "InlineNameEditor",
                    "StoryNodeDragDropManager",
                    "ValidationMessageDisplay"
                  ],
                  "references": [
                    "StoryGraph",
                    "StoryNode"
                  ]
                }
              },
              {
                "name": "Epic",
                "responsibilities": [
                  {
                    "name": "Test file property",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get all stories",
                    "collaborators": [
                      "List[Story]"
                    ]
                  },
                  {
                    "name": "Get domain concepts",
                    "collaborators": [
                      "List[DomainConcept]"
                    ]
                  }
                ],
                "module": "story_graph.epic",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYEpic",
                "responsibilities": [
                  {
                    "name": "Format domain concepts",
                    "collaborators": [
                      "List[DomainConcept]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain epic",
                    "collaborators": [
                      "Epic"
                    ]
                  }
                ],
                "module": "story_graph.epic",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONEpic",
                "responsibilities": [
                  {
                    "name": "Include domain concepts",
                    "collaborators": [
                      "List[DomainConcept]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Wraps domain epic",
                    "collaborators": [
                      "Epic"
                    ]
                  }
                ],
                "module": "story_graph.epic",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownEpic",
                "responsibilities": [
                  {
                    "name": "Format domain concepts table",
                    "collaborators": [
                      "List[DomainConcept]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain epic",
                    "collaborators": [
                      "Epic"
                    ]
                  }
                ],
                "module": "story_graph.epic",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "EpicView",
                "responsibilities": [
                  {
                    "name": "Wraps epic JSON",
                    "collaborators": [
                      "Epic JSON"
                    ]
                  },
                  {
                    "name": "Displays epic name",
                    "collaborators": [
                      "String",
                      "Epic JSON"
                    ]
                  },
                  {
                    "name": "Displays epic icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Displays sub epics",
                    "collaborators": [
                      "SubEpicView",
                      "SubEpic JSON"
                    ]
                  },
                  {
                    "name": "Opens epic folder",
                    "collaborators": [
                      "CLI",
                      "Epic JSON"
                    ]
                  },
                  {
                    "name": "Opens epic test file",
                    "collaborators": [
                      "CLI",
                      "Epic JSON"
                    ]
                  }
                ],
                "realization": [
                  {
                    "scope": "Invoke Bot Through Panel.Filter And Navigate Scope.Display Story Scope Hierarchy",
                    "scenario": "Panel displays nested epic/sub-epic/story/scenario hierarchy from story graph JSON, user can expand/collapse and navigate",
                    "walks": [
                      {
                        "covers": "Rendering 4-level nested hierarchy from JSON",
                        "object_flow": [
                          "this.storyMapJSON = storyMapJSON",
                          "this.cliClient = cliClient",
                          "html: String = this.render()",
                          "  -> epicsHTML: String = this.render_all_epics()",
                          "     epicView: EpicView = new EpicView(epic, this.cliClient)",
                          "     epicHTML: String = epicView.render()",
                          "       -> name: String = this.epicJSON.name",
                          "       -> icon: String = this.epicJSON.icon",
                          "       -> subEpicsHTML: String = this.render_sub_epics()",
                          "          subEpicView: SubEpicView = new SubEpicView(subEpic, this.cliClient)",
                          "          subEpicHTML: String = subEpicView.render()",
                          "            -> storiesHTML: String = this.render_stories()",
                          "               storyView: StoryView = new StoryView(story, this.cliClient)",
                          "               storyHTML: String = storyView.render()",
                          "                 -> scenariosHTML: String = this.render_scenarios()",
                          "                    return scenariosHTML: \"<div>Scenario 1</div>...\"",
                          "                 return `<div>${this.storyJSON.name}${scenariosHTML}</div>`",
                          "               return storiesHTML: \"<div>Story 1...</div>\"",
                          "            return `<div>${this.subEpicJSON.name}${storiesHTML}</div>`",
                          "          return subEpicsHTML: \"<div>Sub-Epic 1...</div>\"",
                          "       return `<div>${name}${subEpicsHTML}</div>`",
                          "     return epicsHTML: \"<div>Epic 1...</div>\"",
                          "return epicsHTML"
                        ]
                      },
                      {
                        "covers": "User opens epic folder via CLI",
                        "object_flow": [
                          "EpicView.onFolderClick()",
                          "  -> folderPath: String = this.epicJSON.folder_path",
                          "  -> this.cliClient.sendMessage({command: 'openScope', filePath: folderPath})",
                          "     -> vscode.commands.executeCommand('vscode.open', fileUri)",
                          "return"
                        ]
                      }
                    ],
                    "model_updates": []
                  }
                ],
                "module": "story_graph.epic",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "SubEpic",
                "responsibilities": [
                  {
                    "name": "Test file property",
                    "collaborators": [
                      "String"
                    ]
                  }
                ],
                "module": "story_graph.sub_epic",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "SubEpicView",
                "responsibilities": [
                  {
                    "name": "Wraps sub epic JSON",
                    "collaborators": [
                      "SubEpic JSON"
                    ]
                  },
                  {
                    "name": "Displays sub epic name",
                    "collaborators": [
                      "String",
                      "SubEpic JSON"
                    ]
                  },
                  {
                    "name": "Displays sub epic icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Displays nested sub epics",
                    "collaborators": [
                      "SubEpicView",
                      "SubEpic JSON"
                    ]
                  },
                  {
                    "name": "Displays stories",
                    "collaborators": [
                      "StoryView",
                      "Story JSON"
                    ]
                  },
                  {
                    "name": "Opens sub epic folder",
                    "collaborators": [
                      "CLI",
                      "SubEpic JSON"
                    ]
                  },
                  {
                    "name": "Opens sub epic test file",
                    "collaborators": [
                      "CLI",
                      "SubEpic JSON"
                    ]
                  }
                ],
                "module": "story_graph.sub_epic",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryGroup",
                "responsibilities": [],
                "module": "story_graph.story_group",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "Story",
                "responsibilities": [
                  {
                    "name": "Test class property",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get test class",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get default test class",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get story type",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get users",
                    "collaborators": [
                      "List[StoryUser]"
                    ]
                  },
                  {
                    "name": "Get scenarios",
                    "collaborators": [
                      "List[Scenario]"
                    ]
                  },
                  {
                    "name": "Get scenario outlines",
                    "collaborators": [
                      "List[ScenarioOutline]"
                    ]
                  },
                  {
                    "name": "Get acceptance criteria",
                    "collaborators": [
                      "List[AcceptanceCriteria]"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYStory",
                "responsibilities": [
                  {
                    "name": "Format users",
                    "collaborators": [
                      "List[StoryUser]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test metadata",
                    "collaborators": [
                      "Test File",
                      "Test Class",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain story",
                    "collaborators": [
                      "Story"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONStory",
                "responsibilities": [
                  {
                    "name": "Include users",
                    "collaborators": [
                      "List[StoryUser]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Include test metadata",
                    "collaborators": [
                      "Test File",
                      "Test Class",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Wraps domain story",
                    "collaborators": [
                      "Story"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownStory",
                "responsibilities": [
                  {
                    "name": "Format story card",
                    "collaborators": [
                      "Story",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format users section",
                    "collaborators": [
                      "List[StoryUser]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain story",
                    "collaborators": [
                      "Story"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryView",
                "responsibilities": [
                  {
                    "name": "Wraps story JSON",
                    "collaborators": [
                      "Story JSON"
                    ]
                  },
                  {
                    "name": "Displays story name",
                    "collaborators": [
                      "String",
                      "Story JSON"
                    ]
                  },
                  {
                    "name": "Displays story icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Displays scenarios",
                    "collaborators": [
                      "ScenarioView",
                      "Scenario JSON"
                    ]
                  },
                  {
                    "name": "Opens test at class",
                    "collaborators": [
                      "CLI",
                      "Story JSON"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "Scenario",
                "responsibilities": [
                  {
                    "name": "Test method property",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get default test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get steps",
                    "collaborators": [
                      "List[Step]"
                    ]
                  }
                ],
                "module": "story_graph.scenario",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYScenario",
                "responsibilities": [
                  {
                    "name": "Format steps",
                    "collaborators": [
                      "List[Step]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test method",
                    "collaborators": [
                      "Test Method",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario",
                    "collaborators": [
                      "Scenario"
                    ]
                  }
                ],
                "module": "story_graph.scenario",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONScenario",
                "responsibilities": [
                  {
                    "name": "Include steps",
                    "collaborators": [
                      "List[Step]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Include test method",
                    "collaborators": [
                      "Test Method",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario",
                    "collaborators": [
                      "Scenario"
                    ]
                  }
                ],
                "module": "story_graph.scenario",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownScenario",
                "responsibilities": [
                  {
                    "name": "Format Gherkin scenario",
                    "collaborators": [
                      "Scenario",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format steps as Given/When/Then",
                    "collaborators": [
                      "List[Step]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario",
                    "collaborators": [
                      "Scenario"
                    ]
                  }
                ],
                "module": "story_graph.scenario",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "ScenarioView",
                "responsibilities": [
                  {
                    "name": "Wraps scenario JSON",
                    "collaborators": [
                      "Scenario JSON"
                    ]
                  },
                  {
                    "name": "Displays scenario name",
                    "collaborators": [
                      "String",
                      "Scenario JSON"
                    ]
                  },
                  {
                    "name": "Displays scenario icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Opens test at scenario",
                    "collaborators": [
                      "CLI",
                      "Scenario JSON"
                    ]
                  }
                ],
                "module": "story_graph.scenario",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "ScenarioOutline",
                "responsibilities": [
                  {
                    "name": "Test method property",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get default test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get examples",
                    "collaborators": [
                      "List[Dict]"
                    ]
                  },
                  {
                    "name": "Get steps",
                    "collaborators": [
                      "List[Step]"
                    ]
                  }
                ],
                "module": "story_graph.scenario_outline",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYScenarioOutline",
                "responsibilities": [
                  {
                    "name": "Format steps",
                    "collaborators": [
                      "List[Step]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format examples",
                    "collaborators": [
                      "List[Dict]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test method",
                    "collaborators": [
                      "Test Method",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario outline",
                    "collaborators": [
                      "ScenarioOutline"
                    ]
                  }
                ],
                "module": "story_graph.scenario_outline",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONScenarioOutline",
                "responsibilities": [
                  {
                    "name": "Include steps",
                    "collaborators": [
                      "List[Step]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Include examples",
                    "collaborators": [
                      "List[Dict]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Include test method",
                    "collaborators": [
                      "Test Method",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario outline",
                    "collaborators": [
                      "ScenarioOutline"
                    ]
                  }
                ],
                "module": "story_graph.scenario_outline",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownScenarioOutline",
                "responsibilities": [
                  {
                    "name": "Format Gherkin scenario outline",
                    "collaborators": [
                      "ScenarioOutline",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format steps as Given/When/Then",
                    "collaborators": [
                      "List[Step]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format examples table",
                    "collaborators": [
                      "List[Dict]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain scenario outline",
                    "collaborators": [
                      "ScenarioOutline"
                    ]
                  }
                ],
                "module": "story_graph.scenario_outline",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "ScenarioOutlineView",
                "responsibilities": [
                  {
                    "name": "Wraps scenario outline JSON",
                    "collaborators": [
                      "ScenarioOutline JSON"
                    ]
                  },
                  {
                    "name": "Displays scenario outline name",
                    "collaborators": [
                      "String",
                      "ScenarioOutline JSON"
                    ]
                  },
                  {
                    "name": "Displays scenario outline icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Displays examples table",
                    "collaborators": [
                      "List[Dict]",
                      "Table HTML"
                    ]
                  },
                  {
                    "name": "Opens test at scenario outline",
                    "collaborators": [
                      "CLI",
                      "ScenarioOutline JSON"
                    ]
                  }
                ],
                "module": "story_graph.scenario_outline",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "AcceptanceCriteria",
                "responsibilities": [
                  {
                    "name": "Get steps",
                    "collaborators": [
                      "List[Step]"
                    ]
                  }
                ],
                "module": "story_graph.acceptance_criteria",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYAcceptanceCriteria",
                "responsibilities": [
                  {
                    "name": "Format steps",
                    "collaborators": [
                      "List[Step]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format criteria list",
                    "collaborators": [
                      "List[Step]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain acceptance criteria",
                    "collaborators": [
                      "AcceptanceCriteria"
                    ]
                  }
                ],
                "module": "story_graph.acceptance_criteria",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONAcceptanceCriteria",
                "responsibilities": [
                  {
                    "name": "Include steps",
                    "collaborators": [
                      "List[Step]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Wraps domain acceptance criteria",
                    "collaborators": [
                      "AcceptanceCriteria"
                    ]
                  }
                ],
                "module": "story_graph.acceptance_criteria",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownAcceptanceCriteria",
                "responsibilities": [
                  {
                    "name": "Format criteria as checklist",
                    "collaborators": [
                      "List[Step]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format steps list",
                    "collaborators": [
                      "List[Step]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain acceptance criteria",
                    "collaborators": [
                      "AcceptanceCriteria"
                    ]
                  }
                ],
                "module": "story_graph.acceptance_criteria",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "AcceptanceCriteriaView",
                "responsibilities": [
                  {
                    "name": "Wraps acceptance criteria JSON",
                    "collaborators": [
                      "AcceptanceCriteria JSON"
                    ]
                  },
                  {
                    "name": "Displays criteria name",
                    "collaborators": [
                      "String",
                      "AcceptanceCriteria JSON"
                    ]
                  },
                  {
                    "name": "Displays criteria icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Displays steps as checklist",
                    "collaborators": [
                      "List[Step]",
                      "HTML"
                    ]
                  }
                ],
                "module": "story_graph.acceptance_criteria",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "Step",
                "responsibilities": [
                  {
                    "name": "Get text",
                    "collaborators": [
                      "String"
                    ]
                  }
                ],
                "module": "story_graph.step",
                "inherits_from": "StoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYStep",
                "responsibilities": [
                  {
                    "name": "Format step text",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format step keyword",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain step",
                    "collaborators": [
                      "Step"
                    ]
                  }
                ],
                "module": "story_graph.step",
                "inherits_from": "TTYStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONStep",
                "responsibilities": [
                  {
                    "name": "Include step text",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Wraps domain step",
                    "collaborators": [
                      "Step"
                    ]
                  }
                ],
                "module": "story_graph.step",
                "inherits_from": "JSONStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownStep",
                "responsibilities": [
                  {
                    "name": "Format step as Gherkin",
                    "collaborators": [
                      "Step",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain step",
                    "collaborators": [
                      "Step"
                    ]
                  }
                ],
                "module": "story_graph.step",
                "inherits_from": "MarkdownStoryNode",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StepView",
                "responsibilities": [
                  {
                    "name": "Wraps step JSON",
                    "collaborators": [
                      "Step JSON"
                    ]
                  },
                  {
                    "name": "Displays step text",
                    "collaborators": [
                      "String",
                      "Step JSON"
                    ]
                  },
                  {
                    "name": "Displays step icon",
                    "collaborators": [
                      "Image"
                    ]
                  }
                ],
                "module": "story_graph.step",
                "inherits_from": "StoryNodeView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "Test",
                "responsibilities": [
                  {
                    "name": "Get test file",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get test class",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get default test class",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Get default test method",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "Build from story node",
                    "collaborators": [
                      "StoryNode",
                      "TestMetadata"
                    ]
                  }
                ],
                "module": "story_graph.test",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYTest",
                "responsibilities": [
                  {
                    "name": "Serialize test to TTY",
                    "collaborators": [
                      "Test",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test file",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test class",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format test method",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain test",
                    "collaborators": [
                      "Test"
                    ]
                  }
                ],
                "module": "story_graph.test",
                "inherits_from": "TTYAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONTest",
                "responsibilities": [
                  {
                    "name": "Serialize test to JSON",
                    "collaborators": [
                      "Test",
                      "JSON String"
                    ]
                  },
                  {
                    "name": "Include test file",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include test class",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include test method",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Wraps domain test",
                    "collaborators": [
                      "Test"
                    ]
                  }
                ],
                "module": "story_graph.test",
                "inherits_from": "JSONAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownTest",
                "responsibilities": [
                  {
                    "name": "Serialize test to Markdown",
                    "collaborators": [
                      "Test",
                      "Markdown String"
                    ]
                  },
                  {
                    "name": "Format test link",
                    "collaborators": [
                      "Test File",
                      "Test Class",
                      "Test Method",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain test",
                    "collaborators": [
                      "Test"
                    ]
                  }
                ],
                "module": "story_graph.test",
                "inherits_from": "MarkdownAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TestView",
                "responsibilities": [
                  {
                    "name": "Wraps test JSON",
                    "collaborators": [
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Displays test file",
                    "collaborators": [
                      "String",
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Displays test class",
                    "collaborators": [
                      "String",
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Displays test method",
                    "collaborators": [
                      "String",
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Opens test file",
                    "collaborators": [
                      "CLI",
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Opens test at class",
                    "collaborators": [
                      "CLI",
                      "Test JSON"
                    ]
                  },
                  {
                    "name": "Opens test at method",
                    "collaborators": [
                      "CLI",
                      "Test JSON"
                    ]
                  }
                ],
                "module": "story_graph.test",
                "inherits_from": "PanelView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryUser",
                "responsibilities": [
                  {
                    "name": "Get name",
                    "collaborators": [
                      "String"
                    ]
                  },
                  {
                    "name": "From string",
                    "collaborators": [
                      "String",
                      "StoryUser"
                    ]
                  },
                  {
                    "name": "From list",
                    "collaborators": [
                      "List[String]",
                      "List[StoryUser]"
                    ]
                  },
                  {
                    "name": "To string",
                    "collaborators": [
                      "String"
                    ]
                  }
                ],
                "module": "story_graph.story_user",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "TTYStoryUser",
                "responsibilities": [
                  {
                    "name": "Serialize user to TTY",
                    "collaborators": [
                      "StoryUser",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format user name",
                    "collaborators": [
                      "String",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Format user list",
                    "collaborators": [
                      "List[StoryUser]",
                      "TTY String"
                    ]
                  },
                  {
                    "name": "Wraps domain story user",
                    "collaborators": [
                      "StoryUser"
                    ]
                  }
                ],
                "module": "story_graph.story_user",
                "inherits_from": "TTYAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "JSONStoryUser",
                "responsibilities": [
                  {
                    "name": "Serialize user to JSON",
                    "collaborators": [
                      "StoryUser",
                      "JSON String"
                    ]
                  },
                  {
                    "name": "Include user name",
                    "collaborators": [
                      "String",
                      "JSON"
                    ]
                  },
                  {
                    "name": "Include user list",
                    "collaborators": [
                      "List[StoryUser]",
                      "JSON Array"
                    ]
                  },
                  {
                    "name": "Wraps domain story user",
                    "collaborators": [
                      "StoryUser"
                    ]
                  }
                ],
                "module": "story_graph.story_user",
                "inherits_from": "JSONAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "MarkdownStoryUser",
                "responsibilities": [
                  {
                    "name": "Serialize user to Markdown",
                    "collaborators": [
                      "StoryUser",
                      "Markdown String"
                    ]
                  },
                  {
                    "name": "Format user badge",
                    "collaborators": [
                      "StoryUser",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Format user list",
                    "collaborators": [
                      "List[StoryUser]",
                      "Markdown"
                    ]
                  },
                  {
                    "name": "Wraps domain story user",
                    "collaborators": [
                      "StoryUser"
                    ]
                  }
                ],
                "module": "story_graph.story_user",
                "inherits_from": "MarkdownAdapter",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryUserView",
                "responsibilities": [
                  {
                    "name": "Wraps story user JSON",
                    "collaborators": [
                      "StoryUser JSON"
                    ]
                  },
                  {
                    "name": "Displays user name",
                    "collaborators": [
                      "String",
                      "StoryUser JSON"
                    ]
                  },
                  {
                    "name": "Displays user icon",
                    "collaborators": [
                      "Image"
                    ]
                  },
                  {
                    "name": "Filters stories by user",
                    "collaborators": [
                      "StoryUser",
                      "Panel Result"
                    ]
                  }
                ],
                "module": "story_graph.story_user",
                "inherits_from": "PanelView",
                "_source_path": "Invoke Bot.Invoke Bot Directly"
              },
              {
                "name": "StoryNode (Base)",
                "responsibilities": [
                  {
                    "name": "Execute action scoped to node: Action, Parameters",
                    "collaborators": [
                      "Bot"
                    ]
                  },
                  {
                    "name": "Create child node with name and position",
                    "collaborators": [
                      "StoryNodeChildren",
                      "NodeValidator"
                    ]
                  },
                  {
                    "name": "Delete self and handle children",
                    "collaborators": [
                      "Parent",
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Validate child name unique among siblings",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Adjust position to valid range",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Resequence children after insert or delete",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  }
                ],
                "realization": [
                  {
                    "scope": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Create child node with specified position",
                    "scenario": "Parent node creates new child at specific position, shifting existing children and maintaining sequential order",
                    "walks": [
                      {
                        "covers": "Steps 1-2 (Initialize parent, validate position)",
                        "object_flow": [
                          "parent_node: Epic = StoryGraph.get_epic(name: 'User Management')",
                          "existing_children: ['SubEpic A', 'SubEpic B'] = parent_node.get_children()",
                          "target_position: 1 = request.position",
                          "is_valid: True = parent_node.validate_position(position: 1, child_count: 2)",
                          "  -> max_position: 2 = StoryNodeChildren.get_max_position(children: ['SubEpic A', 'SubEpic B'])",
                          "  -> is_in_range: True = (position: 1 <= max_position: 2)",
                          "     return is_in_range: True",
                          "return is_valid: True"
                        ]
                      },
                      {
                        "covers": "Step 3 (Create child and insert at position)",
                        "object_flow": [
                          "new_child: SubEpic = parent_node.create_child(name: 'SubEpic C', position: 1)",
                          "  -> is_duplicate: False = parent_node.validate_child_name_unique(name: 'SubEpic C')",
                          "     -> existing_names: ['SubEpic A', 'SubEpic B'] = StoryNodeChildren.get_child_names()",
                          "     -> is_unique: True = ('SubEpic C' not in existing_names)",
                          "        return is_unique: True",
                          "     return is_duplicate: False",
                          "  -> child: SubEpic = SubEpic.create(name: 'SubEpic C', parent: Epic)",
                          "  -> parent_node.resequence_children(insert_at: 1, new_child: child)",
                          "     -> children_to_shift: ['SubEpic B'] = StoryNodeChildren.get_children_from_position(position: 1)",
                          "     -> StoryNodeChildren.shift_positions(children: ['SubEpic B'], offset: 1)",
                          "        SubEpic B.position = 1 + 1 = 2",
                          "     -> StoryNodeChildren.insert(child: SubEpic C, position: 1)",
                          "        SubEpic C.position = 1",
                          "  -> final_order: ['SubEpic A', 'SubEpic C', 'SubEpic B'] = parent_node.get_children()",
                          "     return final_order",
                          "return new_child: SubEpic"
                        ]
                      }
                    ],
                    "model_updates": [
                      "Added 'Create child node with name and position' responsibility to StoryNode",
                      "Added 'Validate child name unique among siblings' responsibility to StoryNode",
                      "Added 'Adjust position to valid range' responsibility to StoryNode",
                      "Added 'Resequence children after insert or delete' responsibility to StoryNode",
                      "Added NodeValidator as collaborator for validation operations",
                      "Added Parent as collaborator for delete operations"
                    ]
                  },
                  {
                    "scope": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Delete Story Node.Delete node including children (cascade delete)",
                    "scenario": "Node with descendants is deleted using cascade option, removing entire subtree and resequencing siblings",
                    "walks": [
                      {
                        "covers": "Steps 1-3 (Locate node, count descendants, initiate cascade delete)",
                        "object_flow": [
                          "parent_node: Epic = StoryGraph.get_epic(name: 'User Management')",
                          "target_node: SubEpic = parent_node.get_child(name: 'SubEpic B')",
                          "child_count: 2 = target_node.count_children()",
                          "  -> direct_children: ['Story A', 'Story B'] = StoryNodeChildren.get_children()",
                          "     return len(direct_children): 2",
                          "total_descendants: 5 = target_node.count_all_descendants()",
                          "  -> count: 2 = child_count",
                          "  -> for each child in direct_children:",
                          "     -> child_descendants: 3 = child.count_all_descendants()",
                          "        count = count + 1 + child_descendants = 2 + 1 + 2 = 5",
                          "     return count: 5",
                          "cascade_flag: True = request.cascade",
                          "return {node: target_node, descendants: 5, cascade: True}"
                        ]
                      },
                      {
                        "covers": "Steps 4-5 (Recursively delete descendants, remove from parent)",
                        "object_flow": [
                          "target_node.delete(cascade: True)",
                          "  -> target_node.delete_all_descendants()",
                          "     -> children: ['Story A', 'Story B'] = target_node.get_children()",
                          "     -> for each child in children:",
                          "        -> child.delete(cascade: True)",
                          "           -> nested_children = child.get_children()",
                          "           -> for each nested in nested_children:",
                          "              -> nested.delete(cascade: True)",
                          "                 # Recursively deletes scenarios under stories",
                          "           -> child.remove_from_parent()",
                          "        # Stories A and B and their scenarios deleted",
                          "  -> target_node.remove_from_parent()",
                          "     -> parent: Epic = target_node.parent",
                          "     -> position: 1 = target_node.position",
                          "     -> parent.remove_child(child: target_node)",
                          "        -> StoryNodeChildren.remove(child: target_node)",
                          "        -> parent.resequence_children(deleted_position: 1)",
                          "           -> siblings_after: ['SubEpic C', 'SubEpic D'] = StoryNodeChildren.get_children_from_position(position: 2)",
                          "           -> StoryNodeChildren.shift_positions(children: siblings_after, offset: -1)",
                          "              SubEpic C.position = 2 - 1 = 1",
                          "              SubEpic D.position = 3 - 1 = 2",
                          "           -> final_children: ['SubEpic A', 'SubEpic C', 'SubEpic D'] = parent.get_children()",
                          "              return final_children",
                          "return deleted: True"
                        ]
                      }
                    ],
                    "model_updates": [
                      "Added 'Delete self and handle children' responsibility to StoryNode",
                      "Confirmed 'Resequence children after insert or delete' handles both insert and delete cases",
                      "Added recursive deletion pattern for cascade deletes"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph"
              },
              {
                "name": "SubEpic",
                "responsibilities": [
                  {
                    "name": "Validate cannot mix Sub-Epics and Stories",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Create StoryGroup when first Story added",
                    "collaborators": [
                      "StoryGroup"
                    ]
                  },
                  {
                    "name": "Check child type compatibility before add",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  }
                ],
                "realization": [
                  {
                    "scope": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.SubEpic with SubEpics cannot create Story child",
                    "scenario": "SubEpic that already contains SubEpic children rejects attempt to add Story child, maintaining hierarchy rules",
                    "walks": [
                      {
                        "covers": "Steps 1-4 (Attempt Story creation, validate hierarchy, reject with error)",
                        "object_flow": [
                          "subepic_node: SubEpic = StoryGraph.get_subepic(name: 'User Management')",
                          "existing_subepic: SubEpic = subepic_node.get_child(name: 'Authentication')",
                          "requested_child_type: 'Story' = request.child_type",
                          "can_add: False = subepic_node.check_child_type_compatibility(child_type: 'Story')",
                          "  -> has_subepics: True = subepic_node.has_children_of_type(type: 'SubEpic')",
                          "     -> children: [Authentication] = StoryNodeChildren.get_children()",
                          "     -> subepic_count: 1 = len([c for c in children if c.type == 'SubEpic'])",
                          "     -> has_subepics: True = (subepic_count: 1 > 0)",
                          "        return has_subepics: True",
                          "  -> is_compatible: False = SubEpic.validate_cannot_mix_subepics_and_stories(has_subepics: True, adding_type: 'Story')",
                          "     -> if has_subepics: True and adding_type: 'Story':",
                          "        return is_compatible: False",
                          "  return can_add: False",
                          "error: ValidationError = SubEpic.create_hierarchy_error(message: 'Cannot create Story under SubEpic with SubEpics')",
                          "return error: ValidationError"
                        ]
                      }
                    ],
                    "model_updates": [
                      "Added 'Create StoryGroup when first Story added' responsibility to SubEpic",
                      "Added 'Check child type compatibility before add' responsibility to SubEpic",
                      "Clarified that 'Validate cannot mix Sub-Epics and Stories' is used during create_child operations"
                    ]
                  }
                ],
                "module": "story_graph.sub_epic",
                "_source_path": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph"
              },
              {
                "name": "Story",
                "responsibilities": [
                  {
                    "name": "Maintain separate sequential ordering for scenarios and acceptance criteria",
                    "collaborators": [
                      "StoryNodeChildren"
                    ]
                  },
                  {
                    "name": "Route child to correct collection by type",
                    "collaborators": [
                      "ScenarioCollection",
                      "AcceptanceCriteriaCollection"
                    ]
                  }
                ],
                "realization": [
                  {
                    "scope": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph.Create Child Story Node.Story creates child and adds to correct collection",
                    "scenario": "Story creates Scenario and AcceptanceCriteria children, routing each to separate collections with independent ordering",
                    "walks": [
                      {
                        "covers": "Steps 1-3 (Create Scenario child, route to scenarios collection)",
                        "object_flow": [
                          "story_node: Story = StoryGraph.get_story(name: 'Validate Password')",
                          "child_type: 'Scenario' = request.child_type",
                          "child_name: 'Valid Password Entered' = request.child_name",
                          "new_scenario: Scenario = story_node.create_child(name: child_name, type: child_type)",
                          "  -> target_collection: 'scenarios' = story_node.route_child_to_correct_collection(child_type: 'Scenario')",
                          "     -> if child_type in ['Scenario', 'ScenarioOutline']:",
                          "        return collection: 'scenarios'",
                          "     -> elif child_type == 'AcceptanceCriteria':",
                          "        return collection: 'acceptance_criteria'",
                          "  -> scenario: Scenario = Scenario.create(name: 'Valid Password Entered', parent: story_node)",
                          "  -> position: 0 = ScenarioCollection.get_next_position()",
                          "  -> ScenarioCollection.add(child: scenario, position: 0)",
                          "     scenario.position = 0",
                          "  -> scenarios: ['Valid Password Entered'] = ScenarioCollection.get_all()",
                          "  -> acceptance_criteria: [] = AcceptanceCriteriaCollection.get_all()",
                          "     # Verify scenario NOT added to acceptance_criteria collection",
                          "     return {scenarios: scenarios, acceptance_criteria: acceptance_criteria}",
                          "return new_scenario: Scenario"
                        ]
                      },
                      {
                        "covers": "Steps 4-6 (Create AcceptanceCriteria child, route to separate collection with independent ordering)",
                        "object_flow": [
                          "ac_child_type: 'AcceptanceCriteria' = request.child_type",
                          "ac_name: 'Password Must Not Be Empty' = request.child_name",
                          "new_ac: AcceptanceCriteria = story_node.create_child(name: ac_name, type: ac_child_type)",
                          "  -> target_collection: 'acceptance_criteria' = story_node.route_child_to_correct_collection(child_type: 'AcceptanceCriteria')",
                          "     return collection: 'acceptance_criteria'",
                          "  -> ac: AcceptanceCriteria = AcceptanceCriteria.create(name: 'Password Must Not Be Empty', parent: story_node)",
                          "  -> ac_position: 0 = AcceptanceCriteriaCollection.get_next_position()",
                          "     # Independent ordering from scenarios - both start at 0",
                          "  -> AcceptanceCriteriaCollection.add(child: ac, position: 0)",
                          "     ac.position = 0",
                          "  -> scenarios: ['Valid Password Entered'] = ScenarioCollection.get_all()",
                          "     # Verify AC NOT added to scenarios collection",
                          "  -> acceptance_criteria: ['Password Must Not Be Empty'] = AcceptanceCriteriaCollection.get_all()",
                          "     return {scenarios: scenarios, acceptance_criteria: acceptance_criteria}",
                          "return new_ac: AcceptanceCriteria"
                        ]
                      }
                    ],
                    "model_updates": [
                      "Added 'Route child to correct collection by type' responsibility to Story",
                      "Added ScenarioCollection and AcceptanceCriteriaCollection as collaborators",
                      "Clarified that 'Maintain separate sequential ordering' means independent position counters per collection"
                    ]
                  }
                ],
                "module": "story_graph.story",
                "_source_path": "Invoke Bot.Invoke Bot Directly.Manage Story Graph.Edit Story Graph"
              },
              {
                "name": "InlineNameEditor",
                "responsibilities": [
                  {
                    "name": "Enables inline editing mode",
                    "collaborators": [
                      "DOM Element",
                      "Input Field"
                    ]
                  },
                  {
                    "name": "Validates name in real-time",
                    "collaborators": [
                      "StoryNode",
                      "Siblings Collection"
                    ]
                  },
                  {
                    "name": "Saves name on blur or Enter",
                    "collaborators": [
                      "StoryNode",
                      "Event"
                    ]
                  },
                  {
                    "name": "Cancels on Escape",
                    "collaborators": [
                      "Event",
                      "Original Value"
                    ]
                  },
                  {
                    "name": "Shows validation messages",
                    "collaborators": [
                      "ValidationMessageDisplay",
                      "Message"
                    ]
                  }
                ],
                "module": "story_graph.nodes",
                "_source_path": "Invoke Bot.Invoke Bot Through Panel",
                "instantiated_with": [
                  "StoryNode"
                ],
                "ownership": {
                  "has": [
                    "ValidationMessageDisplay"
                  ],
                  "references": [
                    "StoryNode"
                  ]
                }
              },
              {
                "name": "StoryNodeDragDropManager",
                "responsibilities": [
                  {
                    "name": "Shows drag cursor with icon",
                    "collaborators": [
                      "Cursor Style",
                      "Node Icon"
                    ]
                  },
                  {
                    "name": "Validates drop target compatibility at UI level",
                    "collaborators": [
                      "Source Node Type",
                      "Target Parent Type"
                    ]
                  },
                  {
                    "name": "Shows no-drop cursor for incompatible targets",
                    "collaborators": [
                      "Cursor Style"
                    ]
                  },
                  {
                    "name": "Highlights valid drop target",
                    "collaborators": [
                      "Target Element",
                      "CSS Class"
                    ]
                  },
                  {
                    "name": "Delegates move to StoryNode domain operation",
                    "collaborators": [
                      "StoryNode",
                      "Target Parent",
                      "Position"
                    ]
                  },
                  {
                    "name": "Returns node to original on invalid drop",
                    "collaborators": [
                      "Original Position",
                      "Animation"
                    ]
                  }
                ],
                "module": "story_graph.story_map",
                "_source_path": "Invoke Bot.Invoke Bot Through REPL",
                "instantiated_with": [
                  "StoryGraph"
                ],
                "ownership": {
                  "references": [
                    "StoryGraph",
                    "StoryNode"
                  ]
                }
              }
            ]
          }
        ],
        "domain_concepts": []
      }
    ],
    "increments": []
  }
}

---

# Behavior: scenarios

## Behavior Instructions - scenarios

The purpose of this behavior is to write detailed plain-english scenarios (given/when/then) that specify exact behavior for each story

Organize stories into delivery increments based on business value, dependencies, and risk

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

---

**Look for context in the following locations:**
- in this message and chat history
- `C:/dev/agile_bots/docs/story/story-graph.json` - the story graph and related  knowledge built so far
- `C:/dev/agile_bots/docs/story/strategy.json` - strategy decisions made
- `C:/dev/agile_bots/docs/story/clarification.json` - clarification answers
- `C:/dev/agile_bots/test/` and `C:/dev/agile_bots/src/` - existing code and tests
- any folder named `context/` anywhere in `C:/dev/agile_bots/` - additional context files

IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/scenarios/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
Follow agile_bot/bots/story_bot/behaviors/scenarios/content/story_graph/instructions.json
specification_scenarios: build scenarios using domain language
Use proper domain terminology in scenario steps - refer to domain concepts and entities
Add/update scenarios and scenario_outlines ONLY in main epics section (single source of truth), NOT in increments section

**STORY GRAPH UPDATE STRATEGY (use when story-graph.json already exists):**

When updating an existing story graph, do NOT read and rewrite the entire story-graph.json manually.
Choose one of these approaches in order of preference:

1. **API approach (preferred for targeted changes):**
   Use the StoryMap node API via CLI dot-notation to make surgical changes.
   - Navigate: story_map.filter_by_name name:"Story Name" to read only the relevant subtree
   - Create:  story_map."Epic"."SubEpic"."Story".create_scenario name:"Scenario Name"
   - Create:  story_map."Epic"."SubEpic"."Story".create_acceptance_criteria name:"WHEN condition THEN outcome"
   - Rename:  story_map."Epic"."SubEpic"."Story".rename name:"New Name"
   - Move:    story_map."Epic"."SubEpic"."Story".move_to target:"Other SubEpic"
   - Reorder: story_map."Epic"."SubEpic"."Story".move_to at_position:2
   - Delete:  story_map."Epic"."SubEpic"."Story"."Old Scenario".delete
   Each call auto-saves the full graph safely through in-memory tree serialization.

2. **Bulk approach (for sweeping changes across many stories):**
   Build a temporary StoryMap with just your changes using the same create API (without bot context),
   then use generate_merge_report() to compare against the original, and merge_story_graphs() to apply.
   The merge preserves all original data (acceptance_criteria, scenarios, steps, metadata) you did not change.

3. **Manual JSON edit (last resort only):**
   Only if the API and bulk approaches cannot handle the situation.
   Use filter_by_name to read a scoped subtree rather than the full file.
   Write changes back through the StoryMap.save() method, as opposed to by editing story-graph.json directly.

When building or adding to the story graph follow these rules,
Rules to follow:

- **scenario_language_matches_domain**: Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
  DO: Use domain language in scenario steps - reference domain concepts by name.
  DON'T: Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

- **example_tables_use_domain_language**: Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
  DO: Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
  DON'T: Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

- **given_describes_state_not_actions**: Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
  DO: Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
  DON'T: Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

- **background_vs_scenario_setup**: Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
  DO: Use Background for shared context with {Concept} references to example tables.
  DON'T: Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

- **keep_scenarios_consistent_across_connected_domains**: Scaling concern: at small scale, scenarios for different domain objects can share a single story. As domain objects develop distinct behavior, write parallel scenario structures per domain. Keep the structure consistent: same Given/When/Then pattern, same step count for the same operation. Unique scenarios only where one domain object's behavior diverges.
  DO: At small scale keep scenarios together. As you scale, write parallel structures across connected domains with consistent depth.
  DON'T: When scaling, do not write inconsistent scenario structures or duplicate logic with hardcoded values.

- **scenarios_cover_all_cases**: Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
  DO: Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
  DON'T: Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

- **use_scenario_outline_when_needed**: Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
  DO: Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
  DON'T: Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

- **write_concrete_scenarios**: Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
  DO: Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
  DON'T: Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

- **scenarios_on_story_docs**: Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
  DO: Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
  DON'T: Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

- **map_table_columns_to_scenario_parameters**: Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
  DO: Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
  DON'T: Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.

### Key Questions

- What system and user actions initiate this story's flow?
- What is the intended system response after each user action?
- What preconditions or data states are required before this story can begin?
- What are the success criteria for the story (from a domain and user perspective)?
- What are the expected alternate flows, error paths, and edge cases?
- Are there any mandatory sequencing constraints within or across stories?
- What domain rules, calculations, or business policies does this story validate?
- Is the story testable independently (including setup and teardown conditions)?
- What external systems or services does this story need to interact with?
- What requests, responses, or contracts are involved in those system interactions?
- Are there system integration points that require validation or simulation?
- How do we handle failures, timeouts, or retries for those system calls?
- What data variations (e.g., boundary conditions, common examples) are required for test coverage?
- What are the input values needed to test each scenario?
- What are the expected output values for each input?
- Are there formulas or calculations that need multiple data points to validate?
- Are there domain entities with named values that should be tested?
- What are the boundary conditions (min, max, edge cases) for each data point?

### Evidence

Acceptance criteria from Exploration stage (Domain AC at feature level, Behavioral AC at story level), High fidelity UX flows, Cross-functional walkthrough outputs, Integration contracts or API mocks, Behavior diagrams (state, sequence)

### Decisions

**Your Decisions:**

**examples_representation:**
  Verification Data Table

**scenario_outline:**
  Scenario Outline with Examples

**scenario_coverage:**
  - Happy Path
  - Edge Cases


### Assumptions

**Your Assumptions:**

- One story is specified at a time
- Acceptance criteria must be testable, unambiguous, and executable
- Gherkin syntax or structured language (Given/When/Then) is preferred
- Scenarios are written in plain English. When using Scenario Outline, variables are clearly marked and defined in Examples tables with actual test data.
- Examples tables when used must include ALL variables used in scenario steps
- Examples tables when used must have exact values for both input AND output variables
- Every variable when used in scenario steps must have a corresponding column in Examples table
- Examples tables when used must have actual test data, not placeholders
- Output/expected result variables must be included in Examples tables when used
- scnarios follow this pattern
- bulk of business logic tests done against the domain layer objects directly
- minimal happy path testing done with separate tgests that go theoiugh CLI
- JS nodetest for panel test focus on rendering and button layout

---
## Next action: validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Scenario Language Matches Domain | `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json` | `scanners.scenarios.scenario_language_scanner.ScenarioLanguageScanner` |
| Example Tables Use Domain Language | `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json` | `scanners.scenarios.example_table_scanner.ExampleTableScanner` |
| Given Describes State Not Actions | `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json` | `scanners.scenarios.given_state_not_actions_scanner.GivenStateNotActionsScanner` |
| Background Vs Scenario Setup | `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json` | `scanners.scenarios.background_common_setup_scanner.BackgroundCommonSetupScanner` |
| Keep Scenarios Consistent Across Connected Domains | `story_bot/behaviors/scenarios/rules/keep_scenarios_consistent_across_connected_domains.json` | `scanners.parallel_scenario_structure_scanner.ParallelScenarioStructureScanner` |
| Scenarios Cover All Cases | `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json` | `scanners.scenarios.scenarios_cover_all_cases_scanner.ScenariosCoverAllCasesScanner` |
| Use Scenario Outline When Needed | `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json` | `scanners.scenarios.scenario_outline_scanner.ScenarioOutlineScanner` |
| Write Concrete Scenarios | `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json` | `scanners.scenarios.parameterized_scenarios_scanner.ParameterizedScenariosScanner` |
| Scenarios On Story Docs | `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json` | `scanners.scenarios.scenarios_on_story_docs_scanner.ScenariosOnStoryDocsScanner` |
| Map Table Columns To Scenario Parameters | `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json` | `scanners.table_column_parameter_scanner.TableColumnParameterScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Scenario Language Matches Domain (Priority 1) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenario_language_matches_domain.json`
**Description:** Scenario language MUST use domain concept terminology. Given/When/Then steps should reference domain entities and concepts, not UI elements or technical implementation details.
**DO:** Use domain language in scenario steps - reference domain concepts by name.
**DON'T:** Don't use UI element names, technical implementation terms, or generic words instead of domain concepts.

### Rule: Example Tables Use Domain Language (Priority 2) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/example_tables_use_domain_language.json`
**Description:** Example tables MUST be grounded in scenario steps AND use domain-rich language. Table columns = nouns from Given/When/Then steps. Use domain terminology, not UI elements. Omit ID columns used purely for linking tables - relationships are expressed via collaboration field and table ordering. Concrete values with domain context, not generic JSON or placeholders. Use source entity data, not aggregated/calculated values - this is the stage where you figure out the real examples.
**DO:** Ground tables in scenario nouns, use domain terminology, connect tables using domain responsibility sentences. Omit implementation IDs. Show source entities, not derived counts.
**DON'T:** Don't use UI elements, flat lookup tables, generic JSON, abstract descriptions, invented terminology, or aggregated/calculated values.

### Rule: Given Describes State Not Actions (Priority 3) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/given_describes_state_not_actions.json`
**Description:** Given statements describe STATE/PRECONDITIONS, not actions or functionality. Given = what exists before test. When = first action. Then = expected behavior. Example: Given user is logged in (state), not Given user logs in (action).
**DO:** Given describes state/preconditions only. Example: 'Given user is logged in' (state), 'Given character sheet exists' (precondition)
**DON'T:** Don't describe actions, UI navigation, or functionality in Given. Example: 'Given user logs in' (action - wrong), 'Given User is on PaymentDetails step' (navigation - wrong)

### Rule: Background Vs Scenario Setup (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/background_vs_scenario_setup.json`
**Description:** Background = shared setup for 3+ scenarios (Given/And only, no When/Then). Background steps MUST use {Concept} notation to reference domain objects. Use {Concept.property} when a specific attribute is important. Don't repeat Background in Steps.
**DO:** Use Background for shared context with {Concept} references to example tables.
**DON'T:** Don't use hardcoded values or column names in Background - use {Concept} notation. Don't include When/Then.

### Rule: Keep Scenarios Consistent Across Connected Domains (Priority 4) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/keep_scenarios_consistent_across_connected_domains.json`
**Description:** Scaling concern: at small scale, scenarios for different domain objects can share a single story. As domain objects develop distinct behavior, write parallel scenario structures per domain. Keep the structure consistent: same Given/When/Then pattern, same step count for the same operation. Unique scenarios only where one domain object's behavior diverges.
**DO:** At small scale keep scenarios together. As you scale, write parallel structures across connected domains with consistent depth.
**DON'T:** When scaling, do not write inconsistent scenario structures or duplicate logic with hardcoded values.

### Rule: Scenarios Cover All Cases (Priority 5) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_cover_all_cases.json`
**Description:** Scenarios must cover happy path, edge cases, and error cases based on acceptance criteria. Example: Valid input → success; Boundary value → validates; Invalid input → error message.
**DO:** Cover all case types: happy path, edge cases, error cases. Example: User enters valid data → success; User enters boundary → validates; User enters invalid → error
**DON'T:** Don't skip case types. Example: Only happy path scenarios (missing edge and error cases)

### Rule: Use Scenario Outline When Needed (Priority 6) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/use_scenario_outline_when_needed.json`
**Description:** Use Scenario Outline with Examples when story warrants concrete data: formulas need validation, domain has named entities, parameter variations exist. Example: Calculate ability modifier with Examples table Rank 10→0, Rank 12→+1, Rank 14→+2.
**DO:** Scenario Outline for formulas, domain entities, or data variations. Example: Scenario Outline: Calculate modifier with Examples table showing input→output pairs
**DON'T:** Don't use Scenario Outline for simple behaviors. Example: Scenario Outline: User clicks button (too simple - use regular scenario)

### Rule: Write Concrete Scenarios (Priority 7) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/write_concrete_scenarios.json`
**Description:** Parameterize domain concepts in scenarios using {Concept} notation for objects and {Concept.property} for specific attributes. Every {parameter} in Background/Steps MUST have corresponding example table. Use object references, not column names directly.
**DO:** Use {Concept} for object references, {Concept.property} for specific attributes. Connect to example tables.
**DON'T:** Don't hardcode values without examples, don't use non-domain placeholders, don't skip base data dependencies.

### Rule: Scenarios On Story Docs (Priority 8) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/scenarios_on_story_docs.json`
**Description:** Scenarios must be in story-graph.json (in scenarios or scenario_outlines fields), NOT in separate markdown files. NEVER create feature specification documents. Example: story-graph.json epics[].stories[].scenarios[], not docs/story/scenarios.md.
**DO:** Add scenarios to story-graph.json. Example: story-graph.json epics[].stories[].scenarios[] array
**DON'T:** Dont create separate scenario files or feature specifications. Example: docs/story/Epic/Feature/Feature Specification.md (wrong)

### Rule: Map Table Columns To Scenario Parameters (Priority 9) [Scanner]
**File:** `story_bot/behaviors/scenarios/rules/map_table_columns_to_scenario_parameters.json`
**Description:** Map example tables to {Concept} references bidirectionally. Every example table maps to a {Concept} in Background/Steps. Use {Concept} for object references and {Concept.property} for specific attributes. Keep tables minimal and domain-focused.
**DO:** Bidirectional mapping: Example table name ↔ {Concept} reference in steps.
**DON'T:** Don't use <column_name> notation - use {Concept} or {Concept.property}. Don't have orphaned tables or references.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_scenarios: validate scenario structure and domain language usage
Validate that scenarios use proper domain terminology and reference domain concepts correctly

---
## Next action: render
**Next:** Perform the following action.

## Action Instructions - render

The purpose of this action is to render output documents and artifacts from story graph using templates and synchronizers

specification_scenarios: render story documents with scenarios

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

Please follow the instructions below in order to manually render output documents using templates

All render configurations are automatically loaded and injected below. Process ALL configs - do not skip any.



**Final Steps:**
- Process ALL configs above - do not skip any
- Priority order: synchronizer > template
- Verify each output file exists after execution
- If execution fails, report the error and continue with other outputs
- After completing all renders, pause and wait for human confirmation before proceeding to next behavior

**Creating New Render Outputs:**
If you need to create code to render a new output format:
1. Create a new synchronizer file in {workspace}/synchronizers/ (create folder if it doesn't exist)
2. Follow this signature pattern: output_file = synchronizer.render(story_graph_file)
3. The synchronizer should read the story-graph.json and produce the desired output file
4. Add the new synchronizer to the behavior's render config to include it in future renders
specification_scenarios: render story documents with scenarios
IMPORTANT: After completing all template-based rendering, you MUST execute the synchronizer-based render specs by running: scenarios.render.renderAll
This will render the following outputs: render_story_scenarios

---
## Next action: tests.build
**Next:** Perform the following action.

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/tests/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file
After writing test files, update story-graph.json with further test_file, test_class, and test_method mapping changes you have made
| Field | Level | Format | Example |
|-------|-------|--------|---------|
| test_file | sub_epic | "test/<domain|CLI|panel>/test_<sub_epic>.py" | "test/domain/test_edit_story_graph.py" |
| test_class | story | "Test<StoryName>" | "TestCreatesChildStoryNode" |
| test_method | scenario | "test_<scenario_name>" | "test_user_creates_child_under_epic" |

Hierarchy: epic → sub_epic(test_file) → story_group → story(test_class) → scenario(test_method)

Rules:
- One test_file per sub_epic (all stories share it)
- One test_class per story (only if story has scenarios)
- One test_method per scenario
- Read story-graph.json first, preserve existing fields

When building or adding to the story graph follow these rules,
Rules to follow:

- **use_class_based_organization**: CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
  DO: Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
  DON'T: Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

- **use_domain_language**: Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
  DO: Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
  DON'T: Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

- **consistent_vocabulary**: Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
  DO: Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
  DON'T: Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

- **domain_oriented_test_inheritance**: Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
  DO: At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
  DON'T: When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

- **no_defensive_code_in_tests**: Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
  DO: Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
  DON'T: Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

- **production_code_clean_functions**: Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
  DO: Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
  DON'T: Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

- **bug_fix_test_first**: When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
  DO: Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
  DON'T: Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

- **call_production_code_directly**: Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
  DO: Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
  DON'T: Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

- **cover_all_behavior_paths**: Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
  DO: Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
  DON'T: Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

- **mock_only_boundaries**: Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
  DO: Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
  DON'T: Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

- **create_parameterized_tests_for_scenarios**: If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
  DO: Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
  DON'T: Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

- **define_fixtures_in_test_file**: Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
  DO: Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
  DON'T: Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

- **design_api_through_failing_tests**: Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
  DO: Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
  DON'T: Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

- **test_observable_behavior**: Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
  DO: Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
  DON'T: Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

- **helper_extraction_and_reuse**: Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
  DO: Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
  DON'T: Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

- **match_specification_scenarios**: Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
  DO: Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
  DON'T: Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

- **place_imports_at_top**: Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
  DO: All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
  DON'T: Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

- **object_oriented_test_helpers**: Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
  DO: Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
  DON'T: Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

- **production_code_explicit_dependencies**: Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
  DO: Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
  DON'T: Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

- **self_documenting_tests**: Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
  DO: Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
  DON'T: Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

- **standard_test_data_sets**: Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
  DO: Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
  DON'T: Do not create new ad-hoc values per test or assert only one field from a complex object.

- **assert_full_results**: Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
  DO: Compare entire objects/dicts/dataclasses against standard data fixtures.
  DON'T: Do not assert single fields or lengths when validating complex results.

- **use_ascii_only**: All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
  DO: Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
  DON'T: Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

- **pytest_bdd_orchestrator_pattern**: Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
  DO: Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
  DON'T: Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

- **use_exact_variable_names**: Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
  DO: Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
  DON'T: Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

- **use_given_when_then_helpers**: Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
  DO: Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
  DON'T: Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)

---
## Next action: tests.validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Use Class Based Organization | `story_bot/behaviors/tests/rules/use_class_based_organization.json` | `scanners.code.python.class_based_organization_scanner.ClassBasedOrganizationScanner` |
| Use Domain Language | `story_bot/behaviors/tests/rules/use_domain_language.json` | `scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner` |
| Consistent Vocabulary | `story_bot/behaviors/tests/rules/consistent_vocabulary.json` | `scanners.code.python.consistent_vocabulary_scanner.ConsistentVocabularyScanner` |
| Domain Oriented Test Inheritance | `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json` | `scanners.code.python.duplicate_assertion_scanner.DuplicateAssertionScanner` |
| No Defensive Code In Tests | `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json` | `scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner` |
| Production Code Clean Functions | `story_bot/behaviors/tests/rules/production_code_clean_functions.json` | `scanners.code.python.function_size_scanner.FunctionSizeScanner` |
| Bug Fix Test First | `story_bot/behaviors/tests/rules/bug_fix_test_first.json` | `scanners.bug_fix_test_first_scanner.BugFixTestFirstScanner` |
| Call Production Code Directly | `story_bot/behaviors/tests/rules/call_production_code_directly.json` | `scanners.code.python.real_implementations_scanner.RealImplementationsScanner` |
| Cover All Behavior Paths | `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json` | `scanners.code.python.cover_all_paths_scanner.CoverAllPathsScanner` |
| Mock Only Boundaries | `story_bot/behaviors/tests/rules/mock_only_boundaries.json` | `scanners.code.python.mock_boundaries_scanner.MockBoundariesScanner` |
| Create Parameterized Tests For Scenarios | `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json` | `scanners.parameterized_tests_scanner.ParameterizedTestsScanner` |
| Define Fixtures In Test File | `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json` | `scanners.code.python.fixture_placement_scanner.FixturePlacementScanner` |
| Design Api Through Failing Tests | `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json` | `scanners.failing_test_api_scanner.FailingTestApiScanner` |
| Test Observable Behavior | `story_bot/behaviors/tests/rules/test_observable_behavior.json` | `scanners.code.python.observable_behavior_scanner.ObservableBehaviorScanner` |
| Helper Extraction And Reuse | `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json` | `scanners.helper_extraction_scanner.HelperExtractionScanner` |
| Match Specification Scenarios | `story_bot/behaviors/tests/rules/match_specification_scenarios.json` | `scanners.specification_match_scanner.SpecificationMatchScanner` |
| Place Imports At Top | `story_bot/behaviors/tests/rules/place_imports_at_top.json` | `scanners.code.python.import_placement_scanner.ImportPlacementScanner` |
| Object Oriented Test Helpers | `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json` | `scanners.code.python.object_oriented_helpers_scanner.ObjectOrientedHelpersScanner` |
| Production Code Explicit Dependencies | `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json` | `scanners.code.python.explicit_dependencies_scanner.ExplicitDependenciesScanner` |
| Self Documenting Tests | `story_bot/behaviors/tests/rules/self_documenting_tests.json` | `scanners.code.python.intention_revealing_names_scanner.IntentionRevealingNamesScanner` |
| Standard Test Data Sets | `story_bot/behaviors/tests/rules/standard_test_data_sets.json` | `scanners.code.python.standard_data_reuse_scanner.StandardDataReuseScanner` |
| Assert Full Results | `story_bot/behaviors/tests/rules/assert_full_results.json` | `scanners.code.python.full_result_assertions_scanner.FullResultAssertionsScanner` |
| Use Ascii Only | `story_bot/behaviors/tests/rules/use_ascii_only.json` | `scanners.code.python.ascii_only_scanner.AsciiOnlyScanner` |
| Pytest Bdd Orchestrator Pattern | `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json` | `scanners.orchestrator_pattern_scanner.OrchestratorPatternScanner` |
| Use Exact Variable Names | `story_bot/behaviors/tests/rules/use_exact_variable_names.json` | `scanners.code.python.exact_variable_names_scanner.ExactVariableNamesScanner` |
| Use Given When Then Helpers | `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json` | `scanners.code.python.given_when_then_helpers_scanner.GivenWhenThenHelpersScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Use Class Based Organization (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_class_based_organization.json`
**Description:** CRITICAL STRUCTURAL RULE: Test structure matches story graph hierarchy. File = sub-epic (test_<sub_epic>.py), Class = story (Test<ExactStoryName>), Method = scenario (test_<scenario_snake_case>). Getting this wrong creates files in wrong locations requiring deletion/recreation. BEFORE writing any test code, identify the parent sub-epic that contains the story.
**DO:** Map story hierarchy to test structure exactly. CRITICAL: File name comes from SUB-EPIC, not story.
**DON'T:** Don't use generic/abbreviated names or wrong hierarchy level for file naming. Don't create files in wrong locations.

### Rule: Use Domain Language (Priority 1) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_domain_language.json`
**Description:** Use Ubiquitous Language (DDD): Same vocabulary in domain model, stories, scenarios, AND code. Class names = domain entities/nouns. Method names = domain responsibilities/verbs. Test names read like plain English stories. Example: test_agent_loads_configuration_when_file_exists (not test_agt_init_sets_vars)
**DO:** Use domain language for classes, methods, and test names. Example: class GatherContextAction, def inject_guardrails(), test_agent_loads_config_when_file_exists
**DON'T:** Don't use generic technical terms or implementation-specific names. Example: class StdioHandler (wrong), def execute_with_guardrails (wrong), test_agt_init_sets_vars (wrong)

### Rule: Consistent Vocabulary (Priority 2) [Scanner]
**File:** `story_bot/behaviors/tests/rules/consistent_vocabulary.json`
**Description:** Use ONE word per concept across entire codebase. Pick consistent vocabulary: create (not build/make/construct), verify (not check/assert/validate), load (not fetch/get/retrieve). Use intention-revealing names that describe behavior. Example: create_agent(), verify_initialized(), load_config() - same verbs everywhere
**DO:** Use same word for same concept everywhere. Example: create_agent(), create_config(), create_workspace() - all use 'create'
**DON'T:** Don't mix synonyms for same concept. Example: create_agent() + build_config() + make_workspace() (wrong - pick one verb)

### Rule: Domain Oriented Test Inheritance (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/domain_oriented_test_inheritance.json`
**Description:** Scaling extension of helper_extraction_and_reuse, object_oriented_test_helpers, and standard_test_data_sets. At small scale, a single test class covering multiple domain objects is fine. As domain objects develop distinct behavior, break out into domain-specific test classes. Use abstract base classes for common operations. Share parameter data and fixtures only when there is obvious shared logic across sub-epics. Place shared base files at the appropriate hierarchy level.
**DO:** At small scale keep together. As you scale, use abstract bases, share fixtures only with explicit need, and place shared files at the right hierarchy level.
**DON'T:** When scaling, do not copy assertion logic, do not create shared files preemptively, and do not group tests by operation or technology.

### Rule: No Defensive Code In Tests (Priority 3) [Scanner]
**File:** `story_bot/behaviors/tests/rules/no_defensive_code_in_tests.json`
**Description:** Tests must NEVER contain guard clauses, defensive conditionals, or fallback paths. We control test setup - if it's wrong, the test MUST fail immediately. Guard clauses hide problems. Tests should assume positive outcomes. Example: Just call the code directly, don't wrap in if-checks
**DO:** Assume correct setup - let test fail if wrong. Example: behavior = Behavior(name='shape') then assert behavior.name == 'shape'
**DON'T:** Don't add if-checks, type guards, or fallback handling in tests. Example: if behavior_file.exists(): (wrong - test should fail if it doesn't)

### Rule: Production Code Clean Functions (Priority 4) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_clean_functions.json`
**Description:** Production code functions should do ONE thing, be under 20 lines, and have one level of abstraction. No hidden side effects. Name reveals complete behavior. Extract multiple concerns into separate functions. Example: load_config(), validate_config(), apply_config() - each does one thing
**DO:** Single responsibility, small focused functions. Example: initialize_from_config() calls validate_exists(), load_config(), validate_structure(), apply_config()
**DON'T:** Don't make functions that do multiple unrelated things or are too long. Example: 50-line function that loads, validates, and applies config

### Rule: Bug Fix Test First (Priority 5) [Scanner]
**File:** `story_bot/behaviors/tests/rules/bug_fix_test_first.json`
**Description:** When production code breaks, follow test-first workflow: write failing test, verify failure, fix code, verify success. Never fix bugs without a failing test first. Example: test_mcp_tool_initializes_bot() fails -> fix initialization -> test passes
**DO:** Follow RED-GREEN-PRODUCTION workflow. Example: Write test reproducing bug -> Run test (RED) -> Fix minimal code -> Run test (GREEN) -> Run full suite
**DON'T:** Don't fix bugs directly without failing test first. Example: Editing production code without test -> deploying -> hoping it works (wrong)

### Rule: Call Production Code Directly (Priority 6) [Scanner]
**File:** `story_bot/behaviors/tests/rules/call_production_code_directly.json`
**Description:** Call production code directly in tests. Let tests fail naturally if code doesn't exist. Don't comment out calls, mock business logic, or fake state. Only mock external boundaries. Example: agent = Agent(); agent.initialize() (not agent = Mock())
**DO:** Call production code directly, let it fail naturally. Example: agent = Agent(workspace); agent.initialize(config); assert agent.is_initialized
**DON'T:** Don't mock class under test, comment out calls, or fake state. Example: agent = Mock(spec=Agent) (wrong); agent._initialized = True (wrong)

### Rule: Cover All Behavior Paths (Priority 7) [Scanner]
**File:** `story_bot/behaviors/tests/rules/cover_all_behavior_paths.json`
**Description:** Cover all behavior paths: normal (happy path), edge cases, and failure scenarios. Each distinct behavior needs its own focused test. Tests must be independent. Example: test_loads_valid_config(), test_loads_empty_config(), test_raises_error_when_file_missing()
**DO:** Test normal, edge, and failure paths separately. Example: test_loads_valid_config() (happy), test_loads_empty_config() (edge), test_raises_when_missing() (failure)
**DON'T:** Don't test only happy path or combine multiple behaviors in one test. Example: Single test for both success and failure (wrong)

### Rule: Mock Only Boundaries (Priority 8) [Scanner]
**File:** `story_bot/behaviors/tests/rules/mock_only_boundaries.json`
**Description:** Mock ONLY at architectural boundaries: external APIs, network, uncontrollable services. Don't mock internal business logic, classes under test, or file operations (use temp files). Example: patch('requests.get') (OK); patch('agent.validate') (wrong)
**DO:** Mock only external dependencies you can't control. Example: with patch('requests.get') as mock: (external API - OK to mock)
**DON'T:** Don't mock internal logic, class under test, or file I/O. Example: with patch('agent.validate_config') (wrong - test the logic!)

### Rule: Create Parameterized Tests For Scenarios (Priority 9) [Scanner]
**File:** `story_bot/behaviors/tests/rules/create_parameterized_tests_for_scenarios.json`
**Description:** If scenarios have Examples tables, create parameterized tests using @pytest.mark.parametrize. Each row becomes a test case. Don't write single tests that only test one example. Example: @pytest.mark.parametrize('input,expected', [(1, 2), (3, 4)])
**DO:** Create parameterized tests from Examples tables. Example: @pytest.mark.parametrize('paths,count', [(['p1','p2'], 2), (['p3'], 1)])
**DON'T:** Don't hardcode single example or duplicate test methods. Example: def test_with_value_1(): (wrong); def test_with_value_2(): (wrong - use parametrize)

### Rule: Define Fixtures In Test File (Priority 10) [Scanner]
**File:** `story_bot/behaviors/tests/rules/define_fixtures_in_test_file.json`
**Description:** Define fixtures in the test file, not separate conftest.py. Truly reusable fixtures (file ops, location helpers) go in base conftest.py. Example: @pytest.fixture def workspace_root(tmp_path): return tmp_path / 'workspace'
**DO:** Define fixtures in same test file. Example: @pytest.fixture def config_file(tmp_path): ... (in test_agent.py)
**DON'T:** Don't create separate conftest.py for agent-specific fixtures. Don't create shared files without explicit need.

### Rule: Design Api Through Failing Tests (Priority 11) [Scanner]
**File:** `story_bot/behaviors/tests/rules/design_api_through_failing_tests.json`
**Description:** Write tests against the REAL expected API BEFORE implementing code. Tests MUST fail initially. Set up real test data and call real API. Failure reveals complete API design. Example: project = Project(path=path); project.initialize() (doesn't exist yet -> fails -> drives implementation)
**DO:** Write test against real expected API that fails initially. Example: project = Project(path); project.initialize(); assert project.is_ready (fails until implemented)
**DON'T:** Don't use placeholders, dummy values, or skip the failing step. Example: project = 'TODO' (wrong); assuming test passes first (wrong)

### Rule: Test Observable Behavior (Priority 12) [Scanner]
**File:** `story_bot/behaviors/tests/rules/test_observable_behavior.json`
**Description:** Test observable behavior, not implementation details. Verify public API and visible state changes. Don't assert on private methods or internal flags. Example: assert agent.config_path.exists() (observable); not assert agent._internal_flag (private)
**DO:** Test observable outcomes through public API. Example: assert agent.config_path == expected; assert agent.is_initialized (public properties)
**DON'T:** Don't test private state or implementation details. Example: assert agent._initialized (wrong); assert agent._config_cache (wrong)

### Rule: Helper Extraction And Reuse (Priority 13) [Scanner]
**File:** `story_bot/behaviors/tests/rules/helper_extraction_and_reuse.json`
**Description:** Extract duplicate test setup to reusable helper functions. Keep test bodies focused on specific behavior. Example: create_agent_with_config(), create_config_file(), verify_agent_initialized() - reusable across tests
**DO:** Extract duplicate setup to reusable helpers. Example: create_agent_with_config(name, workspace, config) returns initialized Agent
**DON'T:** Don't duplicate setup code across tests. Example: Same 10 lines of setup in every test method (wrong - extract to helper)

### Rule: Match Specification Scenarios (Priority 14) [Scanner]
**File:** `story_bot/behaviors/tests/rules/match_specification_scenarios.json`
**Description:** Tests must match specification scenarios exactly. Test names, steps, and assertions verify exactly what the scenario states. Use exact variable names and terminology from specification. Example: agent_name='story_bot' (from spec), not name='bot'
**DO:** Test matches specification exactly. Example: GIVEN config exists, WHEN Agent(agent_name='story_bot'), THEN config_path == agents/base/agent.json
**DON'T:** Don't use different terminology or assert things not in specification. Example: assert agent._internal_flag (not in spec - wrong)

### Rule: Place Imports At Top (Priority 15) [Scanner]
**File:** `story_bot/behaviors/tests/rules/place_imports_at_top.json`
**Description:** Place all imports at top of test file, after docstrings, before code. Group: stdlib, third-party, then local. Example: import json; import pytest; from mymodule import MyClass
**DO:** All imports at top, grouped by type. Example: import json; import pytest; from agile_bot.bots... import X
**DON'T:** Don't place imports inside functions or after code. Example: def test(): from pathlib import Path (wrong - import inside function)

### Rule: Object Oriented Test Helpers (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/object_oriented_test_helpers.json`
**Description:** Consolidate tests around object-oriented helpers/factories (e.g., BotTestHelper test hopper) that build complete domain objects with standard data. Example: helper = BotTestHelper(tmp_path); helper.set_state('shape','clarify'); helper.assert_at_behavior_action('shape','clarify'). Avoid scattering many primitive parameters across parametrize blocks or inline setups.
**DO:** Use shared helper objects to create full test fixtures and assert against complete domain objects, not fragments.
**DON'T:** Do not spread test setup across many primitive parameters or cherry-pick single values from partial objects.

### Rule: Production Code Explicit Dependencies (Priority 16) [Scanner]
**File:** `story_bot/behaviors/tests/rules/production_code_explicit_dependencies.json`
**Description:** Production code: make dependencies explicit through constructor injection. Pass all external dependencies as constructor parameters. No hidden global state. Tests easily inject test doubles. Example: Agent(config_loader=loader, domain_graph=graph)
**DO:** Inject all dependencies through constructor. Example: def __init__(self, config_loader, domain_graph): self._loader = config_loader
**DON'T:** Don't access globals, singletons, or create dependencies internally. Example: self._loader = ConfigLoader() (wrong - creates internally)

### Rule: Self Documenting Tests (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/self_documenting_tests.json`
**Description:** Tests are self-documenting through code structure. Don't add verbose comments explaining failures. Imports, calls, and assertions show the API design. Let code speak for itself. Example: generator = MCPServerGenerator(bot_name, config_path); server = generator.generate_server()
**DO:** Let code structure document the test. Example: generator = MCPServerGenerator(name, config); file = generator.generate() - API is clear
**DON'T:** Don't add verbose comments explaining obvious things. Example: # This will fail because API doesn't exist yet (unnecessary)

### Rule: Standard Test Data Sets (Priority 17) [Scanner]
**File:** `story_bot/behaviors/tests/rules/standard_test_data_sets.json`
**Description:** Use standard, named test data sets across tests instead of recreating ad-hoc values. Example: STANDARD_STATE = {...}; helper.set_state(...); assert helper.get_state() == STANDARD_STATE.
**DO:** Define canonical data once (helper constants/factories) and reuse it so every test exercises the full domain object.
**DON'T:** Do not create new ad-hoc values per test or assert only one field from a complex object.

### Rule: Assert Full Results (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/assert_full_results.json`
**Description:** Assert full domain results (state/log/graph objects), not single cherry-picked fields. Example: assert helper.get_state() == STANDARD_STATE, not assert helper.get_state()['current'] == 'shape.clarify'.
**DO:** Compare entire objects/dicts/dataclasses against standard data fixtures.
**DON'T:** Do not assert single fields or lengths when validating complex results.

### Rule: Use Ascii Only (Priority 18) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_ascii_only.json`
**Description:** All test code must use ASCII-only characters. No Unicode symbols, emojis, or special characters. Use plain ASCII alternatives. Example: print('[PASS] Success') not print('[checkmark] Success')
**DO:** Use ASCII-only characters. Example: print('[PASS] Agent initialized'); print('[ERROR] Config not found')
**DON'T:** Don't use Unicode or emojis. Example: print('[checkmark] Done') (wrong); print('[green_check] OK') (wrong)

### Rule: Pytest Bdd Orchestrator Pattern (Priority 19) [Scanner]
**File:** `story_bot/behaviors/tests/rules/pytest_bdd_orchestrator_pattern.json`
**Description:** Use pytest with orchestrator pattern for story-based tests. NO FEATURE FILES. Test classes contain orchestrator methods (under 20 lines) showing Given-When-Then flow by calling helper functions. Example: def test_agent_loads_config(): given_config_exists(); agent = when_agent_initialized(); then_agent_is_configured(agent)
**DO:** Orchestrator pattern: test shows flow, delegates to helpers. Example: # Given; create_config_file(); # When; agent.initialize(); # Then; assert agent.is_initialized
**DON'T:** Don't use feature files or inline complex setup. Example: @given('config exists') def step(): ... (wrong - use pytest directly)

### Rule: Use Exact Variable Names (Priority 21) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_exact_variable_names.json`
**Description:** Use exact variable names from specification scenarios. When spec mentions agent_name, workspace_root, config_path - use those exact names in tests and production code. Example: agent_name = 'story_bot' (from spec), not name = 'story_bot'
**DO:** Use exact names from specification in tests and production. Example: agent_name, workspace_root, config_path - all from spec
**DON'T:** Don't use different names than specification. Example: name = 'bot' when spec says agent_name (wrong)

### Rule: Use Given When Then Helpers (Priority 22) [Scanner]
**File:** `story_bot/behaviors/tests/rules/use_given_when_then_helpers.json`
**Description:** Use reusable helper functions instead of inline code blocks of 4+ lines. Optimize for reusability, not exact step names. Place helpers at correct scope: story-level in class, sub-epic in module, epic in separate file. Example: given_config_exists(), when_agent_initialized(), then_agent_is_configured()
**DO:** Use Given/When/Then helper functions for setup, action, assertion. Example: given_bot_config_exists(); bot = when_bot_instantiated(); then_bot_uses_correct_directories(bot)
**DON'T:** Don't use inline operations of 4+ lines. Example: config_dir = ...; config_dir.mkdir(); config_file = ...; config_file.write_text() (wrong - extract to helper)


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
specification_tests: validate test code and domain language usage
Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities)
Validate that all test files, classes, and methods are properly mapped to story-graph.json

---
## Next action: code.build
**Next:** Perform the following action.

## Action Instructions - build

The purpose of this action is to build story graph from content area and render using story graph renderer

code: render code required to implement all tests that have been recently built or updated

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

@build-instructions.txt

**BUILD PROCESS:**

**1. Load Context**
Load clarification.json, planning.json, and source material from context sources (listed above).

**2. Load Build Configs**
From `c:\dev\agile_bots\bots\story_bot/behaviors/code/content/`, each folder contains:
- `build_*.json` - Config (name, path, template, output)
- `instructions.json` - Build instructions
- `template-file.json` - Output schema/structure

**3. Execute Build**
1. Load config, instructions, and template (injected as 'story_graph_template')
2. Check if output file exists - read it FIRST
3. Follow instructions.json - match template structure exactly (check '_explanation' section)
4. Apply context from Step 1
5. If file exists: ADD/EXTEND only, never overwrite/delete
6. Validate against template schema
7. Write to `C:\dev\agile_bots/{config.path}/{config.output}`
- Read existing files before changes - preserve all content
- Match template structure exactly - don't invent schemas
- Trace all knowledge to clarification/planning data
- Process builds sequentially - validate each

**4. SOURCE TRACEABILITY**
Knowledge artifacts should include source references when available:
- `context_source` field on epics, sub_epics, story_groups, stories, and domain concepts
- Format: `{"file": "filename.pdf", "page": "12", "section": "3.2.1 Payment Flow"}`
- For multiple sources: use array of source objects
- If source is chat/conversation: `{"type": "chat", "description": "User clarification on approval workflow"}`
- If source is code: `{"file": "path/to/file.py", "lines": "45-67", "function": "process_payment"}`
- Prefer tracing knowledge to a source when possible
- When source is unclear, mark as `{"type": "inferred", "basis": "description of inference basis"}`
code: render code required to implement all tests that have been recently built or updated

When building or adding to the story graph follow these rules,
Rules to follow:

- **avoid_excessive_guards**: Excessive guard clauses add to cyclomatic complexity and make code harder to read. Centralize error handling in one place rather than scattering defensive checks throughout the code. Let code fail fast with clear errors rather than silently handling missing components.

- **avoid_unnecessary_parameter_passing**: Don't pass parameters to internal methods when the value is already accessible through instance variables. Access instance properties directly instead of passing them around unnecessarily.

- **chain_dependencies_properly**: CRITICAL: Code must chain dependencies properly with constructor injection. Map dependencies in a chain: highest-level object → collaborator → sub-collaborator. Inject collaborators at construction time so methods can use them without passing them as parameters. Access sub-collaborators through their owning objects.

- **classify_exceptions_by_caller_needs**: Design exceptions based on how callers will handle them. Create exception types based on caller's needs, use special case objects for predictable failures, and wrap third-party exceptions at boundaries.

- **delegate_to_lowest_level**: CRITICAL: Code must delegate responsibilities to the lowest-level object that can handle them. If a collection class can do something, delegate to it rather than implementing it in the parent.

- **detect_legacy_unused_code**: CRITICAL: Legacy code that is not used by any other code or front-end interfaces (CLI, MCP, web) should be removed. Unused code increases maintenance burden, creates confusion, and violates YAGNI (You Aren't Gonna Need It) principle.

- **eliminate_duplication**: CRITICAL: Every piece of knowledge should have a single, authoritative representation (DRY principle). Extract repeated logic into reusable functions and use abstraction to capture common patterns.

- **enforce_encapsulation**: CRITICAL: Hide implementation details and expose minimal interface. Make fields private by default, expose behavior not data. NEVER pass raw dicts/lists that expose internal structure - use typed objects that encapsulate the data. Follow Law of Demeter (principle of least knowledge).

- **favor_code_representation**: CRITICAL: Code should represent domain concepts directly. Domain models should match code. If code doesn't match domain concepts, refactor the code rather than creating abstract domain models.

- **group_by_domain**: CRITICAL: Code must be organized by domain area and relationships, not by technical layers, object types, or architectural concerns.

- **hide_business_logic_behind_properties**: CRITICAL: Hide business logic behind properties. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.

- **hide_calculation_timing**: CRITICAL: Code must hide calculations. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.

- **keep_classes_small_with_single_responsibility**: CRITICAL: Classes should be small (under 200-300 lines) with a single responsibility. Keep classes cohesive (methods/data interdependent), eliminate dead code, and favor many small focused classes over few large ones.

- **keep_functions_single_responsibility**: CRITICAL: Functions should do one thing and do it well, with no hidden side effects. Each function must have a single, well-defined responsibility.

- **keep_functions_small_focused**: Functions should be small enough to understand at a glance. Keep functions under 20 lines when possible and extract complex logic into named helper functions.

- **maintain_vertical_density**: Related code should be visually close. Group related concepts together, declare variables close to usage, and keep files under 500 lines when possible.

- **never_swallow_exceptions**: CRITICAL: Never swallow exceptions silently. Empty catch blocks hide failures and make debugging impossible. Always log, handle, or rethrow exceptions with context.

- **place_imports_at_top**: Place all import statements at the top of the file, after module docstrings and comments, but before any executable code. This improves readability and makes dependencies clear.

- **prefer_object_model_over_config**: Use existing object model to access information instead of directly accessing configuration files

- **provide_meaningful_context**: Names should provide appropriate context without redundancy. Use longer names for longer scopes and replace magic numbers with named constants.

- **refactor_completely_not_partially**: CRITICAL: When refactoring, replace old code completely - don't try to support both legacy and new patterns. Write new code, delete old code, fix tests. Clean breaks are better than compatibility bridges that create technical debt.

- **refactor_tests_with_production_code**: CRITICAL: When refactoring production code, update tests immediately to maintain green builds. Tests should verify behavior, not implementation details, so they remain valid through refactoring.

- **simplify_control_flow**: Keep nesting minimal and control flow straightforward. Use guard clauses to reduce nesting and extract nested blocks into separate functions.

- **stop_writing_useless_comments**: CRITICAL: DO NOT WRITE COMMENTS. Delete all comments written by the AI chat. Code must be self-explanatory through clear naming and structure. ONLY exception: legal/license requirements. If you think a comment is needed, the code is wrong - fix the code instead.

- **use_clear_function_parameters**: CRITICAL: Function signatures must be simple and intention-revealing. Prefer 0-2 parameters. NEVER pass Dict[str, Any] or List[str] for complex data - create typed objects instead. Examples: parameters dict → ParametersObject, files dict → FilesCollection, exclude list → ExcludePatterns.

- **use_consistent_indentation**: Use consistent, meaningful indentation. Use 2-4 spaces consistently (or tabs if team prefers), indent to show code structure, and keep lines under 80-120 characters.

- **use_consistent_naming**: Use one word per concept across the entire codebase. Pick consistent terms (get/fetch/retrieve → choose one) and follow domain language for business concepts.

- **use_domain_language**: CRITICAL: Code must use domain-specific language, not generic terms. NEVER use Dict[str, Any], List[str], or generic 'data'/'config'/'parameters' - use typed domain objects. Objects should expose properties representing what they contain (e.g., recommended_trades), not methods that 'generate' or 'calculate' things.

- **use_exceptions_properly**: Prefer exceptions over error codes for exceptional conditions. Use exceptions for truly exceptional situations, provide informative error messages, and create domain-specific exception types.

- **use_explicit_dependencies**: CRITICAL: Make dependencies visible through constructor injection. Pass dependencies through constructors, make all dependencies explicit and visible, and use dependency injection for flexibility.

- **use_natural_english**: CRITICAL: Code must use natural English for method names, variable names, and relationships. Use 'many' for collections, 'may' for optional, 'will' for required. Don't use technical notation or abbreviations.

- **use_resource_oriented_design**: CRITICAL: Code must use resource-oriented, object-oriented design. Use object-oriented classes (singular or collection) with responsibilities that encapsulate logic over manager/doer/loader patterns. Maximize encapsulation through collaborator relationships.

---
## Next action: code.validate
**Next:** Perform the following action. Fix any errors found in the Violation.

## Action Instructions - validate

The purpose of this action is to validate story graph and/or artifacts against behavior-specific rules, checking for violations and compliance

code: validate source code quality and domain language usage
Validate that code uses proper domain terminology and follows domain patterns
Validate that all source files, classes, and functions are properly mapped to story-graph.json
MANDATORY: Discover and pass code_files parameter - CodeScanner requires explicit file paths to scan for violations

---


IMPORTANT: Follow these action instructions specifically. Frame the behavior instructions above within the context of this action.

## Step 1: Run Scanners Then Review Violations

**Scanners you must run (with params below). Do not assume pre-run results.**

| Rule | Rule file | Scanner module |
|------|-----------|----------------|
| Avoid Excessive Guards | `story_bot/behaviors/code/rules/avoid_excessive_guards.json` | `scanners.code.python.excessive_guards_scanner.ExcessiveGuardsScanner` |
| Avoid Unnecessary Parameter Passing | `story_bot/behaviors/code/rules/avoid_unnecessary_parameter_passing.json` | `scanners.code.python.unnecessary_parameter_passing_scanner.UnnecessaryParameterPassingScanner` |
| Chain Dependencies Properly | `story_bot/behaviors/code/rules/chain_dependencies_properly.json` | `scanners.dependency_chaining_scanner.DependencyChainingScanner` |
| Classify Exceptions By Caller Needs | `story_bot/behaviors/code/rules/classify_exceptions_by_caller_needs.json` | `scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner` |
| Delegate To Lowest Level | `story_bot/behaviors/code/rules/delegate_to_lowest_level.json` | `scanners.delegation_scanner.DelegationScanner` |
| Detect Legacy Unused Code | `story_bot/behaviors/code/rules/detect_legacy_unused_code.json` | `scanners.code.python.dead_code_scanner.DeadCodeScanner` |
| Eliminate Duplication | `story_bot/behaviors/code/rules/eliminate_duplication.json` | `scanners.code.python.duplication_scanner.DuplicationScanner` |
| Enforce Encapsulation | `story_bot/behaviors/code/rules/enforce_encapsulation.json` | `scanners.property_encapsulation_scanner.PropertyEncapsulationScanner` |
| Favor Code Representation | `story_bot/behaviors/code/rules/favor_code_representation.json` | `scanners.code_representation_scanner.CodeRepresentationScanner` |
| Group By Domain | `story_bot/behaviors/code/rules/group_by_domain.json` | `scanners.code.python.domain_grouping_code_scanner.DomainGroupingCodeScanner` |
| Hide Business Logic Behind Properties | `story_bot/behaviors/code/rules/hide_business_logic_behind_properties.json` | `scanners.code.python.calculation_timing_code_scanner.CalculationTimingCodeScanner` |
| Hide Calculation Timing | `story_bot/behaviors/code/rules/hide_calculation_timing.json` | `scanners.code.python.calculation_timing_code_scanner.CalculationTimingCodeScanner` |
| Keep Classes Small With Single Responsibility | `story_bot/behaviors/code/rules/keep_classes_small_with_single_responsibility.json` | `scanners.code.python.class_size_scanner.ClassSizeScanner` |
| Keep Functions Single Responsibility | `story_bot/behaviors/code/rules/keep_functions_single_responsibility.json` | `scanners.code.python.single_responsibility_scanner.SingleResponsibilityScanner` |
| Keep Functions Small Focused | `story_bot/behaviors/code/rules/keep_functions_small_focused.json` | `scanners.code.python.function_size_scanner.FunctionSizeScanner` |
| Maintain Vertical Density | `story_bot/behaviors/code/rules/maintain_vertical_density.json` | `scanners.code.python.vertical_density_scanner.VerticalDensityScanner` |
| Never Swallow Exceptions | `story_bot/behaviors/code/rules/never_swallow_exceptions.json` | `scanners.code.python.swallowed_exceptions_scanner.SwallowedExceptionsScanner` |
| Place Imports At Top | `story_bot/behaviors/code/rules/place_imports_at_top.json` | `scanners.code.python.import_placement_scanner.ImportPlacementScanner` |
| Prefer Object Model Over Config | `story_bot/behaviors/code/rules/prefer_object_model_over_config.json` | `scanners.code.python.prefer_object_model_over_config_scanner.PreferObjectModelOverConfigScanner` |
| Provide Meaningful Context | `story_bot/behaviors/code/rules/provide_meaningful_context.json` | `scanners.code.python.meaningful_context_scanner.MeaningfulContextScanner` |
| Refactor Completely Not Partially | `story_bot/behaviors/code/rules/refactor_completely_not_partially.json` | `scanners.code.python.complete_refactoring_scanner.CompleteRefactoringScanner` |
| Refactor Tests With Production Code | `story_bot/behaviors/code/rules/refactor_tests_with_production_code.json` | `[Manual check - no scanner]` |
| Simplify Control Flow | `story_bot/behaviors/code/rules/simplify_control_flow.json` | `scanners.code.python.simplify_control_flow_scanner.SimplifyControlFlowScanner` |
| Stop Writing Useless Comments | `story_bot/behaviors/code/rules/stop_writing_useless_comments.json` | `scanners.code.python.useless_comments_scanner.UselessCommentsScanner` |
| Use Clear Function Parameters | `story_bot/behaviors/code/rules/use_clear_function_parameters.json` | `scanners.code.python.clear_parameters_scanner.ClearParametersScanner` |
| Use Consistent Indentation | `story_bot/behaviors/code/rules/use_consistent_indentation.json` | `scanners.code.python.consistent_indentation_scanner.ConsistentIndentationScanner` |
| Use Consistent Naming | `story_bot/behaviors/code/rules/use_consistent_naming.json` | `scanners.code.python.consistent_naming_scanner.ConsistentNamingScanner` |
| Use Domain Language | `story_bot/behaviors/code/rules/use_domain_language.json` | `scanners.code.python.domain_language_code_scanner.DomainLanguageCodeScanner` |
| Use Exceptions Properly | `story_bot/behaviors/code/rules/use_exceptions_properly.json` | `scanners.code.python.exception_handling_scanner.ExceptionHandlingScanner` |
| Use Explicit Dependencies | `story_bot/behaviors/code/rules/use_explicit_dependencies.json` | `scanners.code.python.explicit_dependencies_scanner.ExplicitDependenciesScanner` |
| Use Natural English | `story_bot/behaviors/code/rules/use_natural_english.json` | `scanners.code.python.natural_english_code_scanner.NaturalEnglishCodeScanner` |
| Use Resource Oriented Design | `story_bot/behaviors/code/rules/use_resource_oriented_design.json` | `scanners.code.python.resource_oriented_code_scanner.ResourceOrientedCodeScanner` |

**Params to pass when running scanners:**
- **Scope:** all epics, sub-epics, stories, and domain concepts in the story graph
- **Workspace:** `C:\dev\agile_bots`
- **Story graph path:** `docs/story/story-graph.json` (or behavior-specific path)

Run each scanner with the above scope and workspace; then report violations and fix the story graph as needed.

Run each scanner with the params above, then review the violations they report as follows:
1. For each violation message, locate the corresponding element in the story graph.
2. Open the relevant rule file and read all DO and DON'T examples thoroughly.
3. Decide if the violation is **Valid** (truly a rule breach per examples) or a **False Positive** (explain why if so).
4. Determine the **Root Cause** (e.g., 'incorrect concept naming', 'missing actor', etc.).
5. Assign a **Theme** grouping based on the type of issue (e.g., 'noun-only naming', 'incomplete acceptance criteria').
6. Extract an **Example** from the actual code/content showing the problem.
7. Suggest a clear, concrete **Fix** with a code example informed by DO examples in the rule.

## Step 2: Manual Rule Review

**Rules to validate against (read each file for full DO/DON'T examples):**

### Rule: Avoid Excessive Guards (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/avoid_excessive_guards.json`
**Description:** Excessive guard clauses add to cyclomatic complexity and make code harder to read. Centralize error handling in one place rather than scattering defensive checks throughout the code. Let code fail fast with clear errors rather than silently handling missing components.

### Rule: Avoid Unnecessary Parameter Passing (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/avoid_unnecessary_parameter_passing.json`
**Description:** Don't pass parameters to internal methods when the value is already accessible through instance variables. Access instance properties directly instead of passing them around unnecessarily.

### Rule: Chain Dependencies Properly (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/chain_dependencies_properly.json`
**Description:** CRITICAL: Code must chain dependencies properly with constructor injection. Map dependencies in a chain: highest-level object → collaborator → sub-collaborator. Inject collaborators at construction time so methods can use them without passing them as parameters. Access sub-collaborators through their owning objects.

### Rule: Classify Exceptions By Caller Needs (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/classify_exceptions_by_caller_needs.json`
**Description:** Design exceptions based on how callers will handle them. Create exception types based on caller's needs, use special case objects for predictable failures, and wrap third-party exceptions at boundaries.

### Rule: Delegate To Lowest Level (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/delegate_to_lowest_level.json`
**Description:** CRITICAL: Code must delegate responsibilities to the lowest-level object that can handle them. If a collection class can do something, delegate to it rather than implementing it in the parent.

### Rule: Detect Legacy Unused Code (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/detect_legacy_unused_code.json`
**Description:** CRITICAL: Legacy code that is not used by any other code or front-end interfaces (CLI, MCP, web) should be removed. Unused code increases maintenance burden, creates confusion, and violates YAGNI (You Aren't Gonna Need It) principle.

### Rule: Eliminate Duplication (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/eliminate_duplication.json`
**Description:** CRITICAL: Every piece of knowledge should have a single, authoritative representation (DRY principle). Extract repeated logic into reusable functions and use abstraction to capture common patterns.

### Rule: Enforce Encapsulation (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/enforce_encapsulation.json`
**Description:** CRITICAL: Hide implementation details and expose minimal interface. Make fields private by default, expose behavior not data. NEVER pass raw dicts/lists that expose internal structure - use typed objects that encapsulate the data. Follow Law of Demeter (principle of least knowledge).

### Rule: Favor Code Representation (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/favor_code_representation.json`
**Description:** CRITICAL: Code should represent domain concepts directly. Domain models should match code. If code doesn't match domain concepts, refactor the code rather than creating abstract domain models.

### Rule: Group By Domain (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/group_by_domain.json`
**Description:** CRITICAL: Code must be organized by domain area and relationships, not by technical layers, object types, or architectural concerns.

### Rule: Hide Business Logic Behind Properties (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/hide_business_logic_behind_properties.json`
**Description:** CRITICAL: Hide business logic behind properties. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.

### Rule: Hide Calculation Timing (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/hide_calculation_timing.json`
**Description:** CRITICAL: Code must hide calculations. Properties hide logic that occurs—it may be computed on-demand, cached, pre-computed, or loaded from storage. The caller shouldn't know or care when the values are calculated / determined.

### Rule: Keep Classes Small With Single Responsibility (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/keep_classes_small_with_single_responsibility.json`
**Description:** CRITICAL: Classes should be small (under 200-300 lines) with a single responsibility. Keep classes cohesive (methods/data interdependent), eliminate dead code, and favor many small focused classes over few large ones.

### Rule: Keep Functions Single Responsibility (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/keep_functions_single_responsibility.json`
**Description:** CRITICAL: Functions should do one thing and do it well, with no hidden side effects. Each function must have a single, well-defined responsibility.

### Rule: Keep Functions Small Focused (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/keep_functions_small_focused.json`
**Description:** Functions should be small enough to understand at a glance. Keep functions under 20 lines when possible and extract complex logic into named helper functions.

### Rule: Maintain Vertical Density (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/maintain_vertical_density.json`
**Description:** Related code should be visually close. Group related concepts together, declare variables close to usage, and keep files under 500 lines when possible.

### Rule: Never Swallow Exceptions (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/never_swallow_exceptions.json`
**Description:** CRITICAL: Never swallow exceptions silently. Empty catch blocks hide failures and make debugging impossible. Always log, handle, or rethrow exceptions with context.

### Rule: Place Imports At Top (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/place_imports_at_top.json`
**Description:** Place all import statements at the top of the file, after module docstrings and comments, but before any executable code. This improves readability and makes dependencies clear.

### Rule: Prefer Object Model Over Config (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/prefer_object_model_over_config.json`
**Description:** Use existing object model to access information instead of directly accessing configuration files

### Rule: Provide Meaningful Context (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/provide_meaningful_context.json`
**Description:** Names should provide appropriate context without redundancy. Use longer names for longer scopes and replace magic numbers with named constants.

### Rule: Refactor Completely Not Partially (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/refactor_completely_not_partially.json`
**Description:** CRITICAL: When refactoring, replace old code completely - don't try to support both legacy and new patterns. Write new code, delete old code, fix tests. Clean breaks are better than compatibility bridges that create technical debt.

### Rule: Refactor Tests With Production Code (Priority 99) [Manual Check]
**File:** `story_bot/behaviors/code/rules/refactor_tests_with_production_code.json`
**Description:** CRITICAL: When refactoring production code, update tests immediately to maintain green builds. Tests should verify behavior, not implementation details, so they remain valid through refactoring.

### Rule: Simplify Control Flow (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/simplify_control_flow.json`
**Description:** Keep nesting minimal and control flow straightforward. Use guard clauses to reduce nesting and extract nested blocks into separate functions.

### Rule: Stop Writing Useless Comments (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/stop_writing_useless_comments.json`
**Description:** CRITICAL: DO NOT WRITE COMMENTS. Delete all comments written by the AI chat. Code must be self-explanatory through clear naming and structure. ONLY exception: legal/license requirements. If you think a comment is needed, the code is wrong - fix the code instead.

### Rule: Use Clear Function Parameters (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_clear_function_parameters.json`
**Description:** CRITICAL: Function signatures must be simple and intention-revealing. Prefer 0-2 parameters. NEVER pass Dict[str, Any] or List[str] for complex data - create typed objects instead. Examples: parameters dict → ParametersObject, files dict → FilesCollection, exclude list → ExcludePatterns.

### Rule: Use Consistent Indentation (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_consistent_indentation.json`
**Description:** Use consistent, meaningful indentation. Use 2-4 spaces consistently (or tabs if team prefers), indent to show code structure, and keep lines under 80-120 characters.

### Rule: Use Consistent Naming (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_consistent_naming.json`
**Description:** Use one word per concept across the entire codebase. Pick consistent terms (get/fetch/retrieve → choose one) and follow domain language for business concepts.

### Rule: Use Domain Language (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_domain_language.json`
**Description:** CRITICAL: Code must use domain-specific language, not generic terms. NEVER use Dict[str, Any], List[str], or generic 'data'/'config'/'parameters' - use typed domain objects. Objects should expose properties representing what they contain (e.g., recommended_trades), not methods that 'generate' or 'calculate' things.

### Rule: Use Exceptions Properly (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_exceptions_properly.json`
**Description:** Prefer exceptions over error codes for exceptional conditions. Use exceptions for truly exceptional situations, provide informative error messages, and create domain-specific exception types.

### Rule: Use Explicit Dependencies (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_explicit_dependencies.json`
**Description:** CRITICAL: Make dependencies visible through constructor injection. Pass dependencies through constructors, make all dependencies explicit and visible, and use dependency injection for flexibility.

### Rule: Use Natural English (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_natural_english.json`
**Description:** CRITICAL: Code must use natural English for method names, variable names, and relationships. Use 'many' for collections, 'may' for optional, 'will' for required. Don't use technical notation or abbreviations.

### Rule: Use Resource Oriented Design (Priority 99) [Scanner]
**File:** `story_bot/behaviors/code/rules/use_resource_oriented_design.json`
**Description:** CRITICAL: Code must use resource-oriented, object-oriented design. Use object-oriented classes (singular or collection) with responsibilities that encapsulate logic over manager/doer/loader patterns. Maximize encapsulation through collaborator relationships.


Scanner tools don't cover or catch every rule violation. Do a second pass:
1. Carefully read each rule file, fully reviewing DO and DON'T sections, and every provided example.
2. Inspect all epics, sub-epics, stories, and domain concepts in the story graph for compliance.
3. Compare the properties and content of each element against the rule's requirements.
4. Document any violations the scanner could not find.
5. For each violation, extract an **Example** showing the problem and provide a **Fix** with code example.

## Violations Found

Record ALL findings (scanner + manual) using this readable format. Group by theme for narrow IDE chat panels:

### [Theme Name] (X violations)

**1. [Rule Name]**
- Location: `path.to.element`
- Status: Valid / False Positive
- Source: Scanner / Manual / Both
- Problem: `"actual problematic text"`
- Fix: `"corrected text"`
- Root Cause: Brief explanation

**2. [Rule Name]**
- Location: `path.to.element`
- ...

---

### [Next Theme] (Y violations)
...

Use this list format instead of tables - tables are unreadable in narrow IDE side chat panels.

## Step 3: Summarize Findings & Recommendations

Provide a concise summary:
- Report how many **scanner violations** were valid vs false positives.
- Enumerate any **additional manual findings** not caught by scanners.
- Group all violations by recurring theme or pattern.
- Split violations into **Priority Fixes** (must resolve before continuing) and **Optional Improvements**.

Present your summary and await user confirmation before automatically applying or proposing corrections.
code: validate source code quality and domain language usage
Validate that code uses proper domain terminology and follows domain patterns
Validate that all source files, classes, and functions are properly mapped to story-graph.json
MANDATORY: Discover and pass code_files parameter - CodeScanner requires explicit file paths to scan for violations