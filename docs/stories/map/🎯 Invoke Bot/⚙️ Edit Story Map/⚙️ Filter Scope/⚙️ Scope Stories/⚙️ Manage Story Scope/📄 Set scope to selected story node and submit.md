# 📄 Set scope to selected story node and submit

**Navigation:** [📄‹ Story Map](../../../../story-map.drawio) | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L203)

**User:** System
**Path:** [🎯 Invoke Bot](../..) / [⚙️ Edit Story Map](..) / [⚙️ Filter Scope](../..) / [⚙️ Scope Stories](..) / [⚙️ Manage Story Scope](.)  
**Sequential Order:** 8.0
**Story Type:** user

## Story Description

Set scope to selected story node and submit functionality for the mob minion system.

## Acceptance Criteria

### Behavioral Acceptance Criteria

- **When** action executes, **then** action completes successfully

## Scenarios

<a id="scenario-determine-behavior-for-story"></a>
### Scenario: [Determine Behavior For Story](#scenario-determine-behavior-for-story) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L338)

**Steps:**
```gherkin
Given Bot has story map loaded with epic <epic_name>
And Epic contains story <story_name>
And Story has acceptance criteria <acceptance_criteria>
And Story has scenarios <scenarios>
And Story has test class <test_class>
And Story has test methods <test_methods>
When Bot determines behavior for the story
Then Bot returns behavior <expected_behavior>
```


<a id="scenario-determine-behavior-for-sub-epic"></a>
### Scenario: [Determine Behavior For Sub Epic](#scenario-determine-behavior-for-sub-epic) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L566)

**Steps:**
```gherkin
Given Bot has story map loaded with sub-epic <sub_epic_name>
And Sub-epic contains stories shown in table
When Bot determines behavior for the sub-epic
Then Bot returns behavior <expected_behavior>
```


<a id="scenario-determine-behavior-for-epic"></a>
### Scenario: [Determine Behavior For Epic](#scenario-determine-behavior-for-epic) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L998)

**Steps:**
```gherkin
Given Bot has story map loaded with epic <epic_name>
And Epic contains sub-epics shown in table
When Bot determines behavior for the epic
Then Bot returns behavior <expected_behavior>
```


<a id="scenario-determine-behavior-for-story"></a>
### Scenario: [Determine Behavior For Story](#scenario-determine-behavior-for-story) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L338)

**Steps:**
```gherkin
Given Bot has story map loaded with epic <epic_name>
And Epic contains story <story_name>
And Story has acceptance criteria <acceptance_criteria>
And Story has scenarios <scenarios>
And Story has test class <test_class>
And Story has test methods <test_methods>
When Bot determines behavior for the story
Then Bot returns behavior <expected_behavior>
```

**Examples:**
| epic_name | story_name | test_class | acceptance_criteria | scenarios | test_methods | expected_behavior | description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| File Management | Upload File | test_file_upload.py | File size validated; File type checked; Upload progress tracked | (1) User uploads valid file and sees success confirmation (2) User uploads oversized file and sees size limit error (3) User uploads invalid file type and sees type error (4) User cancels upload mid-transfer and sees cancellation confirmation (5) Upload fails with network error and user sees retry option | test_user_uploads_valid_file_and_sees_success_confirmation; test_user_uploads_oversized_file_and_sees_size_limit_error; test_user_uploads_invalid_file_type_and_sees_type_error; test_user_cancels_upload_mid_transfer_and_sees_cancellation_confirmation; test_upload_fails_with_network_error_and_user_sees_retry_option | code | All scenarios have tests, ready for implementation |
| File Management | Download File | test_file_download.py | Download initiated; Progress displayed | (1) User downloads file successfully and sees progress (2) User cancels download mid-transfer (3) Download fails due to network error and user sees error message | test_user_downloads_file_successfully_and_sees_progress; test_user_cancels_download_mid_transfer | test | Some scenarios tested, missing test_download_fails |
| File Management | Delete File | test_file_delete.py | Confirmation required; File removed from storage | (1) User confirms delete and file is removed from system (2) User cancels delete and file remains (3) Delete operation fails due to permissions and user sees error |  | test | Scenarios exist but no tests written |
| User Management | Create User |  | Email validated; Password meets requirements |  |  | scenario | Has AC but no scenarios, need to write scenarios |
| Reporting | View Report |  |  |  |  | explore | No AC and no scenarios, need exploration first |
| Authentication | Reset Password | test_reset_password.py |  | (1) User requests password reset and receives reset email (2) User submits new password meeting requirements and password is updated (3) User submits invalid password not meeting requirements and sees validation error | test_user_requests_password_reset_and_receives_reset_email; test_user_submits_new_password_meeting_requirements_and_password_is_updated; test_user_submits_invalid_password_not_meeting_requirements_and_sees_validation_error | code | No AC but has scenarios with tests, lower level determines behavior |
| Data Export | Export CSV | test_export_csv.py |  | (1) User exports data to CSV and file downloads successfully (2) Export handles empty data set and generates valid empty CSV (3) Export handles large dataset and shows progress indicator (4) Export with special characters in data and properly escapes them in CSV | test_user_exports_data_to_csv_and_file_downloads_successfully; test_export_handles_empty_data_set_and_generates_valid_empty_csv | test | No AC but has scenarios, only some tested |
| Payment | Process Payment | test_process_payment.py |  | (1) Payment processed with valid card and transaction completes successfully (2) Payment attempted with expired card and user sees card expired error |  | test | No AC but has scenarios without tests, need to write tests |


<a id="scenario-determine-behavior-for-sub-epic"></a>
### Scenario: [Determine Behavior For Sub Epic](#scenario-determine-behavior-for-sub-epic) (happy_path)  | [Test](/test/invoke_bot/edit_story_map/test_manage_story_scope.py#L566)

**Steps:**
```gherkin
Given Bot has story map loaded with sub-epic <sub_epic_name>
And Sub-epic contains stories shown in table
When Bot determines behavior for the sub-epic
Then Bot returns behavior <expected_behavior>
```

**Examples:**
| sub_epic_name | expected_behavior | description |
| --- | --- | --- |
| User Authentication | code | All 3 stories (Login, Logout, Refresh Token) have all scenarios tested |
| Payment Processing | scenario | Process Payment needs tests, Refund Payment needs scenarios - lowest is scenario |
| Data Management | explore | Archive Data has no AC making entire sub-epic explore level |
| File Operations | test | Upload File has tests, Download/Delete need tests - lowest is test |
| Search | scenario | Single story Basic Search at scenario level |


<a id="scenario-submit-button-displays-behavior-specific-icon"></a>
### Scenario: [Submit button displays behavior-specific icon](#scenario-submit-button-displays-behavior-specific-icon) (happy_path)

**Steps:**
```gherkin
Given User has selected a <node_type> in the panel
And Node state indicates <behavior> behavior is needed
When Panel renders the submit button
Then Submit button displays <icon_file> icon indicating <behavior> behavior
```

**Examples:**
| node_type | behavior | icon_file | description |
| --- | --- | --- | --- |
| empty epic | shape | submit_subepic.png | Epic needs structure |
| empty sub-epic | shape | submit_subepic.png | Sub-epic needs structure |
| story without AC | explore | submit_story.png | Story needs exploration |
| story without scenarios | scenarios | submit_ac.png | Story needs scenarios |
| story without tests | tests | submit_tests.png | Story needs tests |
| story with failing tests | code | submit_code.png | Story needs code implementation |

