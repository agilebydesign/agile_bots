# 📄 Execute Action Scoped To Story Node

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L317)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Scope Stories](..) / [⚙️ Manage Story Scope](.)  
**Sequential Order:** 7.0
**Story Type:** user

## Story Description

Execute Action Scoped To Story Node functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-execute-action-on-node-with-valid-parameters"></a>
### Scenario: [Execute action on node with valid parameters](#scenario-execute-action-on-node-with-valid-parameters) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L326)

**Steps:**
```gherkin
GIVEN: Node exists and bot has registered actions
AND: Node has scope <scope_type> <scope_name>
WHEN: Node executes action with valid parameters
THEN: Action completes successfully
AND: Instructions contain complete story_graph for selected scope with hierarchical relationships
```

**Examples:**

**Example 1: Story node executes action with complete story_graph**

**Parent Table:**
| scope_type | scope_name |
| --- | --- |
| story | Upload File |

**Story Graph Structure in Instructions:**
```
{
  "epics": [
    {
      "name": "File Management",
      "sequential_order": null,
      "domain_concepts": [],
      "sub_epics": [
        {
          "name": "File Operations",
          "sequential_order": 0.0,
          "behavior": "code",
          "sub_epics": [],
          "story_groups": [
            {
              "name": "",
              "sequential_order": 0.0,
              "type": "and",
              "connector": null,
              "behavior": "code",
              "stories": [
                {
                  "name": "Upload File",
                  "sequential_order": 0.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["User"],
                  "test_file": null,
                  "test_class": "test_file_upload.py",
                  "scenarios": [
                    {
                      "name": "User uploads valid file and sees success confirmation",
                      "sequential_order": 1.0,
                      "type": "happy_path",
                      "background": [],
                      "test_method": "test_user_uploads_valid_file_and_sees_success_confirmation",
                      "steps": "Given user is logged in\nWhen user uploads valid file\nThen user sees success confirmation"
                    }
                  ],
                  "acceptance_criteria": [
                    {
                      "name": "WHEN user selects file",
                      "text": "File size validated",
                      "sequential_order": 1.0
                    }
                  ],
                  "behavior": "code"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Example 2: Story node with scenarios and acceptance criteria**

**Parent Table:**
| scope_type | scope_name |
| --- | --- |
| story | Generate Bot Tools |

**Story Graph Structure in Instructions:**
```
{
  "epics": [
    {
      "name": "Build Agile Bots",
      "sequential_order": null,
      "domain_concepts": [
        {
          "name": "Story",
          "responsibilities": [
            {
              "name": "Get test class",
              "collaborators": ["String"]
            },
            {
              "name": "Get scenarios",
              "collaborators": ["List[Scenario]"]
            },
            {
              "name": "Get acceptance criteria",
              "collaborators": ["List[AcceptanceCriteria]"]
            }
          ]
        },
        {
          "name": "StoryNode",
          "responsibilities": [
            {
              "name": "Get/Update name",
              "collaborators": ["String"]
            },
            {
              "name": "Get node type",
              "collaborators": ["String"]
            },
            {
              "name": "Contains Children",
              "collaborators": ["StoryNodeChildren"]
            }
          ]
        }
      ],
      "sub_epics": [
        {
          "name": "Generate MCP Tools",
          "sequential_order": 0.0,
          "behavior": "code",
          "sub_epics": [],
          "story_groups": [
            {
              "name": "",
              "sequential_order": 0.0,
              "type": "and",
              "connector": "or",
              "behavior": "code",
              "stories": [
                {
                  "name": "Generate Bot Tools",
                  "sequential_order": 0.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["MCP Server Generator"],
                  "test_file": null,
                  "test_class": "TestGenerateBotTools",
                  "scenarios": [
                    {
                      "name": "Generator creates bot tool for test_bot",
                      "sequential_order": 1.0,
                      "type": "",
                      "background": [],
                      "test_method": "test_generator_creates_bot_tool_for_test_bot",
                      "steps": "Given A bot configuration file with a working directory and behaviors\nAnd A bot that has been initialized with that config file\nWhen Generator processes Bot Config\nThen Generator creates 1 bot tool instance"
                    }
                  ],
                  "acceptance_criteria": [
                    {
                      "name": "WHEN Generator processes Bot Config",
                      "text": "WHEN Generator processes Bot Config",
                      "sequential_order": 1.0
                    },
                    {
                      "name": "THEN Generator creates 1 bot tool instance",
                      "text": "THEN Generator creates 1 bot tool instance",
                      "sequential_order": 2.0
                    }
                  ],
                  "domain_concepts": [
                    {
                      "name": "Story",
                      "responsibilities": [
                        {
                          "name": "Get test class",
                          "collaborators": ["String"]
                        },
                        {
                          "name": "Get scenarios",
                          "collaborators": ["List[Scenario]"]
                        }
                      ]
                    }
                  ],
                  "behavior": "code"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Example 3: Sub-epic node executes action with full hierarchy**

**Parent Table:**
| scope_type | scope_name |
| --- | --- |
| sub_epic | User Authentication |

**Story Graph Structure in Instructions:**
```
{
  "epics": [
    {
      "name": "User Management",
      "sequential_order": null,
      "domain_concepts": [],
      "sub_epics": [
        {
          "name": "User Authentication",
          "sequential_order": 0.0,
          "behavior": "code",
          "sub_epics": [],
          "story_groups": [
            {
              "name": "",
              "sequential_order": 0.0,
              "type": "and",
              "connector": null,
              "behavior": "code",
              "stories": [
                {
                  "name": "Login User",
                  "sequential_order": 0.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["User"],
                  "test_file": null,
                  "test_class": "test_login_user.py",
                  "scenarios": [
                    {
                      "name": "User enters valid username and password",
                      "sequential_order": 1.0,
                      "type": "happy_path",
                      "background": [],
                      "test_method": "test_user_enters_valid_username_and_password",
                      "steps": "Given user is registered\nWhen user enters valid credentials\nThen user sees dashboard"
                    }
                  ],
                  "acceptance_criteria": [
                    {
                      "name": "WHEN user enters credentials",
                      "text": "Valid credentials accepted",
                      "sequential_order": 1.0
                    }
                  ],
                  "behavior": "code"
                },
                {
                  "name": "Logout User",
                  "sequential_order": 1.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["User"],
                  "test_file": null,
                  "test_class": "test_logout_user.py",
                  "scenarios": [],
                  "acceptance_criteria": [
                    {
                      "name": "WHEN user clicks logout",
                      "text": "Session terminated",
                      "sequential_order": 1.0
                    }
                  ],
                  "behavior": "code"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```


<a id="scenario-execute-action-with-invalid-parameters-returns-error"></a>
### Scenario: [Execute action with invalid parameters returns error](#scenario-execute-action-with-invalid-parameters-returns-error) (error)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L356)

**Steps:**
```gherkin
GIVEN: Node exists and bot has registered actions
WHEN: Node executes action with invalid parameters
THEN: Bot validates parameters and returns error
```


<a id="scenario-execute-non-existent-action-returns-error"></a>
### Scenario: [Execute non-existent action returns error](#scenario-execute-non-existent-action-returns-error) (error)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L384)

**Steps:**
```gherkin
GIVEN: Node exists and bot has registered actions
WHEN: Node attempts to execute non-existent action
THEN: Bot validates action exists and returns error
```

