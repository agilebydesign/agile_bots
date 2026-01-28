# 📄 Execute Actions With Scope

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L203)

**User:** Bot Behavior
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Work With Story Map](..) / [⚙️ Scope Stories](..) / [⚙️ Manage Story Scope](.)  
**Sequential Order:** 8.0
**Story Type:** user

## Story Description

Execute Actions With Scope functionality that includes complete JSON data (epics, features, stories) from the scope into action instructions, rather than just story names.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes with scope, **then** complete JSON for scoped epics, features, and stories is included in instructions
- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-build-action-includes-scope-in-instructions"></a>
### Scenario: [Build action includes scope in instructions](#scenario-build-action-includes-scope-in-instructions) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L205)

**Steps:**
```gherkin
Given Build action with scope type <scope_type> and scope value <scope_value>
When Instructions are retrieved
Then Instructions contain scope configuration with type <scope_type>
And Instructions contain scope_content with complete JSON structure shown in tables
And Complete JSON includes <json_elements> from the scoped nodes
```

**Examples:**

**Example 1: Scope set to single story - complete story JSON included**

**Parent Table:**
| scope_type | scope_value | action | json_elements |
| --- | --- | --- | --- |
| story | Upload File | build | story name, sequential_order, story_type, users, test_class, acceptance_criteria, scenarios with test_methods |

**Children Table (Acceptance Criteria in scope_content):**
| story_name | acceptance_criteria |
| --- | --- |
| Upload File | File size validated; File type checked; Upload progress tracked |

**Grandchildren Table (Scenarios in scope_content):**
| story_name | scenario | test_method | steps |
| --- | --- | --- | --- |
| Upload File | User uploads valid file and sees success confirmation | test_user_uploads_valid_file | Given file is valid\nWhen user uploads file\nThen success message shown |
| Upload File | User uploads oversized file and sees error | test_user_uploads_oversized_file | Given file exceeds limit\nWhen user uploads file\nThen size error shown |
| Upload File | User uploads invalid type and sees error | test_user_uploads_invalid_type | Given file type not allowed\nWhen user uploads file\nThen type error shown |

**Example 2: Scope set to epic - complete epic with sub-epics and stories JSON included**

**Parent Table:**
| scope_type | scope_value | action | json_elements |
| --- | --- | --- | --- |
| epic | File Management | build | epic name, sub_epics array with nested stories, story_groups, all scenarios and acceptance_criteria |

**Children Table (Sub-Epics in scope_content):**
| epic_name | sub_epic_name | sub_epic_behavior | test_file |
| --- | --- | --- | --- |
| File Management | File Operations | code | test/file_operations.py |
| File Management | File Search | test | test/file_search.py |

**Grandchildren Table (Stories in scope_content):**
| sub_epic_name | story_name | story_type | test_class | acceptance_criteria |
| --- | --- | --- | --- | --- |
| File Operations | Upload File | user | TestUploadFile | File size validated; File type checked |
| File Operations | Download File | user | TestDownloadFile | Download initiated; Progress displayed |
| File Operations | Delete File | user | TestDeleteFile | Confirmation required; File removed |
| File Search | Search Files | user | TestSearchFiles | Search term entered; Results displayed |

**Great-Grandchildren Table (Scenarios in scope_content):**
| story_name | scenario | sequential_order | type | test_method |
| --- | --- | --- | --- | --- |
| Upload File | User uploads valid file and sees success | 1.0 | happy_path | test_valid_upload |
| Upload File | User uploads oversized file and sees error | 2.0 | error_case | test_oversized_file |
| Download File | User downloads file and sees progress | 1.0 | happy_path | test_download_progress |
| Delete File | User confirms delete and file removed | 1.0 | happy_path | test_confirm_delete |
| Search Files | User enters term and sees matching results | 1.0 | happy_path | test_search_results |

**Example 3: Scope set to multiple stories - complete JSON for each story included**

**Parent Table:**
| scope_type | scope_value | action | json_elements |
| --- | --- | --- | --- |
| story | Upload File, Download File | validate | multiple story objects each with full name, test_class, scenarios, acceptance_criteria |

**Children Table (Stories in scope_content):**
| story_name | test_class | acceptance_criteria | scenario_count |
| --- | --- | --- | --- |
| Upload File | TestUploadFile | File size validated; File type checked; Upload progress tracked | 3 |
| Download File | TestDownloadFile | Download initiated; Progress displayed; Download completes successfully | 2 |

**Grandchildren Table (All Scenarios in scope_content):**
| story_name | scenario | test_method | background |
| --- | --- | --- | --- |
| Upload File | User uploads valid file and sees success | test_valid_upload | Given user is authenticated\nAnd user has upload permissions |
| Upload File | User uploads oversized file and sees error | test_oversized_file | Given user is authenticated\nAnd user has upload permissions |
| Upload File | User uploads invalid type and sees error | test_invalid_type | Given user is authenticated\nAnd user has upload permissions |
| Download File | User downloads file and sees progress | test_download_progress | Given file exists in system |
| Download File | Download completes and file appears locally | test_download_complete | Given file exists in system |

**Example 4: Scope set to increment - complete JSON for all stories in increment**

**Parent Table:**
| scope_type | scope_value | action | json_elements |
| --- | --- | --- | --- |
| increment | 1 | build | all stories from increment with complete epic/sub-epic hierarchy, scenarios, acceptance_criteria |

**Children Table (Stories in Increment 1 scope_content):**
| increment_priority | story_name | parent_sub_epic | parent_epic | test_class |
| --- | --- | --- | --- | --- |
| 1 | Upload File | File Operations | File Management | TestUploadFile |
| 1 | Login User | Authentication | User Management | TestLoginUser |
| 1 | View Dashboard | Dashboard | Reporting | TestViewDashboard |

**Grandchildren Table (Scenarios for Increment Stories in scope_content):**
| story_name | scenario | type | test_method | steps |
| --- | --- | --- | --- | --- |
| Upload File | Valid upload succeeds | happy_path | test_valid_upload | Given valid file\nWhen upload\nThen success |
| Login User | Valid credentials accepted | happy_path | test_valid_login | Given valid user\nWhen login\nThen dashboard shown |
| View Dashboard | Dashboard displays widgets | happy_path | test_dashboard_widgets | Given logged in\nWhen view dashboard\nThen widgets shown |

**Example 5: Scope with sub-epic - complete JSON with nested structure**

**Parent Table:**
| scope_type | scope_value | action | json_elements |
| --- | --- | --- | --- |
| epic | User Management | render | epic with sub_epics containing stories, each story with scenarios, acceptance_criteria, test linkage |

**Children Table (Sub-Epic Hierarchy in scope_content):**
| epic_name | sub_epic_name | sub_epic_sequential_order | behavior | nested_sub_epics |
| --- | --- | --- | --- | --- |
| User Management | Authentication | 1.0 | code | false |
| User Management | User Profile | 2.0 | scenario | true (Profile Settings) |
| User Management | User Roles | 3.0 | test | false |

**Grandchildren Table (Stories with Full Details in scope_content):**
| sub_epic_name | story_name | story_type | users | test_class | acceptance_criteria | scenarios |
| --- | --- | --- | --- | --- | --- | --- |
| Authentication | Login User | user | User, Admin | TestLoginUser | Valid credentials accepted; Invalid rejected; Locked after 3 failures | 3 scenarios |
| Authentication | Logout User | user | User, Admin | TestLogoutUser | Session terminated; Redirected to login; Token invalidated | 3 scenarios |
| User Profile | Edit Profile | user | User | TestEditProfile | Name updated; Email validated; Avatar uploaded | 4 scenarios |
| User Roles | Assign Role | user | Admin | TestAssignRole | Role assigned to user; Permissions updated | 2 scenarios |

**Great-Grandchildren Table (Complete Scenario Details in scope_content):**
| story_name | scenario | sequential_order | type | background | steps | test_method |
| --- | --- | --- | --- | --- | --- | --- |
| Login User | Valid login shows dashboard | 1.0 | happy_path | Given user exists\nAnd credentials valid | When user logs in\nThen dashboard displayed | test_valid_login |
| Login User | Invalid password shows error | 2.0 | error_case | Given user exists\nAnd password wrong | When user logs in\nThen error shown | test_invalid_password |
| Edit Profile | User updates name successfully | 1.0 | happy_path | Given user logged in | When update name\nThen name changed | test_update_name |
| Assign Role | Admin assigns role to user | 1.0 | happy_path | Given admin logged in\nAnd target user exists | When assign role\nThen role applied | test_assign_role |
```


<a id="scenario-validate-action-accepts-scope-context"></a>
### Scenario: [Validate action accepts scope context](#scenario-validate-action-accepts-scope-context) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L230)

**Steps:**
```gherkin
Given Validate action with scope type <scope_type> and scope value <scope_value>
And Story graph file exists
When Instructions are retrieved
Then No errors occur and scope is processed
And Instructions contain scope_content with complete JSON for <scope_value>
And JSON includes all nested elements shown in tables
```

**Examples:**

**Example 1: Validate scoped to single story with scenarios**

**Parent Table:**
| scope_type | scope_value | story_graph_exists | expected_scope_content_includes |
| --- | --- | --- | --- |
| story | Delete File | true | story object with name, test_class, acceptance_criteria array, scenarios array |

**Children Table (Story Content in scope_content):**
| story_name | test_class | acceptance_criteria | scenario_count |
| --- | --- | --- | --- |
| Delete File | TestDeleteFile | Confirmation required; File removed from storage; Audit log updated | 3 |

**Grandchildren Table (Scenarios in scope_content):**
| story_name | scenario | type | steps | test_method |
| --- | --- | --- | --- | --- |
| Delete File | User confirms delete and file removed | happy_path | Given file exists\nWhen user confirms\nThen file deleted | test_confirm_delete |
| Delete File | User cancels and file remains | happy_path | Given file exists\nWhen user cancels\nThen file unchanged | test_cancel_delete |
| Delete File | Delete fails with permissions error | error_case | Given no permissions\nWhen user tries delete\nThen error shown | test_permission_error |

**Example 2: Validate scoped to epic with full hierarchy**

**Parent Table:**
| scope_type | scope_value | story_graph_exists | expected_scope_content_includes |
| --- | --- | --- | --- |
| epic | Payment Processing | true | epic with name, sub_epics array, stories with scenarios, acceptance_criteria for all stories |

**Children Table (Epic Structure in scope_content):**
| epic_name | sub_epic_count | total_stories | total_scenarios |
| --- | --- | --- | --- |
| Payment Processing | 2 | 4 | 12 |

**Grandchildren Table (Sub-Epics and Stories in scope_content):**
| epic_name | sub_epic_name | story_name | test_class |
| --- | --- | --- | --- |
| Payment Processing | Process Payment | Accept Payment | TestAcceptPayment |
| Payment Processing | Process Payment | Validate Card | TestValidateCard |
| Payment Processing | Refund Payment | Issue Refund | TestIssueRefund |
| Payment Processing | Refund Payment | Calculate Refund | TestCalculateRefund |

**Great-Grandchildren Table (Acceptance Criteria in scope_content):**
| story_name | acceptance_criteria |
| --- | --- |
| Accept Payment | Card validated; Amount verified; Receipt generated |
| Validate Card | Card number checked; Expiry validated; CVV verified |
| Issue Refund | Original payment found; Refund amount calculated; Customer notified |
| Calculate Refund | Partial refund allowed; Full refund calculated; Processing fee deducted |
```


<a id="scenario-render-action-accepts-scope-context"></a>
### Scenario: [Render action accepts scope context](#scenario-render-action-accepts-scope-context) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L261)

**Steps:**
```gherkin
Given Render action with story scope
When Instructions are retrieved
Then No errors occur (render supports ScopeActionContext)
And Instructions contain complete JSON for scoped nodes
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

