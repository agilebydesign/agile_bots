# Process

## Action Flow

### 1. clarify


### 2. strategy


### 3. build

write test files (.py, .js, etc.) with executable test code based on the scenarios you have made within the story-graph.json file Each epic, sub_epic, story_group, and story has an optional notes field. Use notes in two situations: (1) Context below current level: When you find context that maps to something more detailed than what we're building (e.g., acceptance criteria when only shaping), put it in the notes field of the most locally specific node—do not discard it. (2) Explicit level cap: W...

### 4. validate

specification_tests: validate test code and domain language usage Validate that test code uses proper domain terminology (class names = domain entities, method names = domain responsibilities) Validate that all test files, classes, and methods are properly mapped to story-graph.json