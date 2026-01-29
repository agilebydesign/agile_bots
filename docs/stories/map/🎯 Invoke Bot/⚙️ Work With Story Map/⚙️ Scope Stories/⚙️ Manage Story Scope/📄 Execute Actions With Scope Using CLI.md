# 📄 Execute Actions With Scope Using CLI

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L415)

**User:** User
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Scope Stories](..) / [⚙️ Manage Story Scope](.)  
**Sequential Order:** 5.0
**Story Type:** user

## Story Description

Execute Actions With Scope Using CLI functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-action-execution-uses-active-scope-via-cli"></a>
### Scenario: [Action execution uses active scope via CLI](#scenario-action-execution-uses-active-scope-via-cli) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L428)

**Steps:**
```gherkin
GIVEN: CLI session with scope set to <scope_type> <scope_name>
WHEN: action executed
THEN: Action operates within scope
AND: Instructions contain complete story_graph for selected scope with hierarchical relationships
```

**Examples:**

**Example 1: CLI executes action with story scope - includes complete story_graph**

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

**Example 2: CLI executes action with sub-epic scope - includes full hierarchy**

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

**Example 3: CLI executes action with epic scope - includes multiple sub-epics**

**Parent Table:**
| scope_type | scope_name |
| --- | --- |
| epic | File Management |

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
                  "scenarios": [],
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

