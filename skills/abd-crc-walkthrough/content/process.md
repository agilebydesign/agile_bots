# Process

## Action Flow

### 1. clarify

Gather context for CRC walkthrough - identify key scenarios, architectural risks, and integration points to trace

### 2. strategy

Determine walkthrough purpose: business complexity, architecture complexity, integration complexity, or new frameworks Make strategic decisions about walkthrough scope and depth

### 3. build

Select node from story graph (epic, sub-epic, story, or scenario) Document Scope in dot notation: Epic.Sub-Epic.Story.Scenario (parent context) Break scenario into multiple walks, each covering a logical subset For each walk, document Covers: what specific part it traces (steps, stories, sub-epics) Identify first domain concept and responsibility for each walk Trace responsibilities and collaborations using Object.method(param: value) format Show nested calls with -> indentation and return value...

### 4. validate

Validate walkthrough scenarios against domain model Verify object flows align to domain language in stories/epics Confirm all discovered responsibilities, collaborators, and concepts have been added to story-graph.json Verify walkthrough document includes 'Model Updates Discovered' section documenting changes

### 5. render

Render walkthrough realization documents from story-graph.json Include 'Model Updates Discovered' section showing all added/modified responsibilities, collaborators, and concepts

### 6. rules

Display walkthrough rules for this behavior as AI context