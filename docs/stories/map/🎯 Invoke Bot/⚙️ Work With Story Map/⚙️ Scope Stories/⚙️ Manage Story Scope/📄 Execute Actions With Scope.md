# 📄 Execute Actions With Scope

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L203)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Scope Stories](..) / [⚙️ Manage Story Scope](.)  
**Sequential Order:** 8.0
**Story Type:** user

## Story Description

Execute Actions With Scope functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-build-action-includes-scope-in-instructions"></a>
### Scenario: [Build action includes scope in instructions](#scenario-build-action-includes-scope-in-instructions) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L205)

**Steps:**
```gherkin
Given Build action with story scope <scope_type> <scope_name>
When Instructions are retrieved
Then Instructions contain complete story_graph for selected scope with hierarchical relationships
And Story graph includes <included_elements>
```

**Examples:**

**Example 1: Single story scope - story_graph includes story with scenarios and acceptance criteria**

**Parent Table:**
| scope_type | scope_name | included_elements |
| --- | --- | --- |
| story | Upload File | epic, story, scenarios, acceptance_criteria |

**Story Graph Structure:**
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

**Example 2: Story with domain models**

**Parent Table:**
| scope_type | scope_name | included_elements |
| --- | --- | --- |
| story | Generate Bot Tools | epic, story, acceptance_criteria, domain_concepts |

**Story Graph Structure:**
```
{
  "epics": [
    {
      "name": "Build Agile Bots",
      "sequential_order": null,
      "domain_concepts": ["Bot Config", "MCP Server", "Behavior", "Tool"],
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
                  "domain_concepts": ["Bot Config", "Bot", "Tool", "Behavior"],
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

**Example 3: Multiple stories scope**

**Parent Table:**
| scope_type | scope_name | included_elements |
| --- | --- | --- |
| story_group | File Operations | epic, story_group, multiple stories, scenarios |

**Story Graph Structure:**
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
              "name": "File Operations",
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
                      "name": "User uploads valid file",
                      "sequential_order": 1.0,
                      "type": "happy_path",
                      "background": [],
                      "test_method": "test_user_uploads_valid_file",
                      "steps": "Given user is logged in\nWhen user uploads valid file\nThen user sees success"
                    }
                  ],
                  "acceptance_criteria": [],
                  "behavior": "code"
                },
                {
                  "name": "Download File",
                  "sequential_order": 1.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["User"],
                  "test_file": null,
                  "test_class": "test_file_download.py",
                  "scenarios": [
                    {
                      "name": "User downloads file successfully",
                      "sequential_order": 1.0,
                      "type": "happy_path",
                      "background": [],
                      "test_method": "test_user_downloads_file_successfully",
                      "steps": "Given file exists\nWhen user downloads file\nThen file downloads"
                    }
                  ],
                  "acceptance_criteria": [],
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

**Example 4: Sub-epic scope with full hierarchy**

**Parent Table:**
| scope_type | scope_name | included_elements |
| --- | --- | --- |
| sub_epic | User Authentication | epic, sub_epic, story_groups, stories, scenarios, acceptance_criteria |

**Story Graph Structure:**
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

**Example 5: Epic scope with multiple sub-epics**

**Parent Table:**
| scope_type | scope_name | included_elements |
| --- | --- | --- |
| epic | File Management | epic, multiple sub_epics, story_groups, stories |

**Story Graph Structure:**
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
                  "scenarios": [],
                  "acceptance_criteria": [],
                  "behavior": "code"
                }
              ]
            }
          ]
        },
        {
          "name": "File Search",
          "sequential_order": 1.0,
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
                  "name": "Search Files",
                  "sequential_order": 0.0,
                  "connector": "and",
                  "story_type": "user",
                  "users": ["User"],
                  "test_file": null,
                  "test_class": "test_search_files.py",
                  "scenarios": [],
                  "acceptance_criteria": [],
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


<a id="scenario-validate-action-accepts-scope-context"></a>
### Scenario: [Validate action accepts scope context](#scenario-validate-action-accepts-scope-context) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L230)

**Steps:**
```gherkin
Given Validate action with story scope <scope_type> <scope_name> and story graph file
When Instructions are retrieved
Then No errors occur and scope is processed
And Instructions contain complete story_graph for selected scope with hierarchical relationships
```

**Examples:**

**Example 1: Validate action with story scope includes complete story_graph**

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

**Example 2: Validate action with sub-epic scope includes full hierarchy**

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
                  "scenarios": [],
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


<a id="scenario-render-action-accepts-scope-context"></a>
### Scenario: [Render action accepts scope context](#scenario-render-action-accepts-scope-context) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L261)

**Steps:**
```gherkin
Given Render action with story scope <scope_type> <scope_name>
When Instructions are retrieved
Then No errors occur (render supports ScopeActionContext)
And Instructions contain complete story_graph for selected scope with hierarchical relationships
```

**Examples:**

**Example 1: Render action with story scope includes complete story_graph**

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


<a id="scenario-clarify-action-does-not-support-scope"></a>
### Scenario: [Clarify action does not support scope](#scenario-clarify-action-does-not-support-scope) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L283)

**Steps:**
```gherkin
Given Clarify action
When Context is checked
Then Uses ClarifyActionContext (not ScopeActionContext)
```


<a id="scenario-strategy-action-does-not-support-scope"></a>
### Scenario: [Strategy action does not support scope](#scenario-strategy-action-does-not-support-scope) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L300)

**Steps:**
```gherkin
Given Strategy action
When Context is checked
Then Uses StrategyActionContext (not ScopeActionContext)
```

