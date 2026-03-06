# Core Definitions

## Behavior

**shape** — Create a story map that captures the user's journey through epics, features, and stories

## Goal

Shape story map from user context - capture user needs, business requirements, and story structure

## Inputs

User context, interviews, vision documents, existing requirements, business domain experts interviews

## Outputs

story-map.md, story-map-outline.drawio, story-map.txt

---

# Process

## Action Flow

### 1. clarify

Gather context for story mapping

### 2. strategy


### 3. build

shape: build story map structure Apply story shaping rules (context: 'when shaping stories') for story structure Each epic, sub_epic, story_group, and story has an optional notes field. Use notes in two situations: (1) Context below current level: When you find context that maps to something more detailed than what we're building (e.g., acceptance criteria when only shaping), put it in the notes field of the most locally specific node—do not discard it. (2) Explicit level cap: When the lowest le...

### 4. validate

shape: validate hierarchy and story structure Apply story shaping rules (context: 'when shaping stories') for story structure

### 5. render

shape: render story map documents

---

# Outputs

## Artifacts

- story-graph.json
- story-map.md
- story-map-outline.drawio
- story-map.txt

---

---
title: active-business-and-behavioral-language
priority: 2
---

## active-business-and-behavioral-language

Use active business language focused on user/system behavior. Describe what actors do with clear action verbs
not technical implementation or passive constructions.

**DO**

Use active voice with business language. Example: 'User --> submit order' (active voice
base verb form
business language describing what actor does)

Use base verb forms (infinitive/imperative) to describe what happens in active voice with business language focused on user/system behavior

```
User --> submit order
```

```
System --> validate payment
```

```
Customer --> place order
```

```
Admin --> approve request
```

Action verbs that describe user/system behavior clearly - use base verb forms like submit
view
validate
send
display
place
edit
create
load
save
invoke
process
generate
update

```
User --> submit form
```

```
Customer --> view product catalog
```

```
System --> validate input data
```

```
Admin --> send notification
```

```
System --> display results
```

```
User --> place order
```

```
Developer --> edit configuration
```

```
System --> create report
```

```
User --> load dashboard
```

```
System --> save changes
```

```
User --> invoke command
```

```
System --> process payment
```

```
System --> generate invoice
```

```
Admin --> update settings
```

Prefer user/system stories over technical stories - transform technical language into business behavior. Wrong: 'Set up database schema' (technical). Correct: 'System --> store user data' (business
user story).

```
System --> store user data (not 'Set up database schema')
```

```
System --> expose user data via API (not 'Create API endpoint')
```

```
Developer --> verify story behavior (not 'Write unit tests')
```

When technical stories are necessary
mark with story_type: 'technical' and keep minimal and focused

```
System --> migrate legacy data format (story_type: 'technical')
```

```
Developer --> refactor authentication module (story_type: 'technical')
```

**DO NOT**

Don't use passive voice or technical implementation language. Example: 'Order is submitted' (passive voice
unclear actor) â†' 'User --> submit order' (active voice
base verb form
clear actor)

Don't describe behaviors passively or vaguely - always use active voice with base verb forms that clearly identifies who performs the action. Wrong: 'Order is submitted' (passive - by whom?). Correct: 'User --> submit order' (active
base verb
clear actor).

```
User --> submit order (not 'Order is submitted')
```

```
System --> validate payment (not 'Payment gets validated')
```

```
User --> place order (not 'Order is placed by user')
```

Don't use technical implementation details or development task language - focus on business behavior. Wrong: 'Developer --> write code'
'Developer --> create class'. Correct: 'Developer --> implement feature'
'System --> store data'.

```
Developer --> write code
```

```
Developer --> create class
```

```
Developer --> add method
```

```
Developer --> set up CI/CD
```

```
Developer --> configure database
```

```
Developer --> install package
```

```
Developer --> implement order system
```

```
Developer --> create database schema
```

```
System --> query database
```

```
System --> call API
```

```
System --> update table
```

Development task verbs to avoid - these describe implementation
not business behavior. Use business language instead.

```
Developer --> implement feature (avoid)
```

```
Developer --> create module (avoid)
```

```
Developer --> refactor code (avoid)
```

```
Developer --> optimize performance (avoid)
```

```
Developer --> fix bug (avoid)
```

```
Developer --> build system (avoid)
```

```
Developer --> set up infrastructure (avoid)
```

---

---
title: consolidate-superficial-stories
priority: 13
---

## consolidate-superficial-stories

Consolidate similar stories that differ superficially. When multiple stories use the same logic and only differ in data values or enumeration
combine them into a single parameterized story. NOTE: This rule operates on a different axis than P14 (Expand System Stories). P13 eliminates data-value duplication (same behavior
different input values). P14 decomposes by system component interactions (different behaviors within one story). Apply P13 first to consolidate data variations
then apply P14 to expand the consolidated story by component behavior if needed.

**DO**

Identify and consolidate stories that differ only superficially (data values
enumeration)

Consolidate stories that use the same validation logic but differ only in the specific value being validated

```
Before consolidation:
```

```
  - User assigns strength ability
```

```
  - User assigns dexterity ability
```

```
  - User assigns constitution ability
```

```
  - User assigns intelligence ability
```

```
  - User assigns wisdom ability
```

```
  - User assigns charisma ability
```

```
After consolidation:
```

```
  - User assigns ability (STR, DEX, CON, INT, WIS, CHA)
```

```
(Same validation logic, different data values)
```

Consolidate stories that use the same calculation formula but differ only in which attribute is being calculated

```
Before consolidation:
```

```
  - System calculates strength modifier
```

```
  - System calculates dexterity modifier
```

```
  - System calculates constitution modifier
```

```
After consolidation:
```

```
  - System calculates ability modifiers
```

```
(Same calculation formula applied to different attributes)
```

Consolidate stories that perform the same operation on different entity types

```
Before consolidation:
```

```
  - User creates character
```

```
  - User creates weapon
```

```
  - User creates armor
```

```
  - User creates spell
```

```
After consolidation:
```

```
  - User creates game entity (character, weapon, armor, spell)
```

```
(Same creation operation, different entity types)
```

**DO NOT**

Don't keep stories separate when they differ only superficially

Don't enumerate every permutation when the logic is identical and only the data value changes

```
WRONG: Keep separate stories for each attribute:
```

```
  - User validates email format
```

```
  - User validates phone format
```

```
  - User validates postal code format
```

```
RIGHT: Consolidate to single story:
```

```
  - User validates input format (email, phone, postal code)
```

Don't split stories by data value when the business logic and validation rules are the same

```
WRONG: Separate story for each product type:
```

```
  - User adds book to cart
```

```
  - User adds electronics to cart
```

```
  - User adds clothing to cart
```

```
RIGHT: Single parameterized story:
```

```
  - User adds product to cart (book, electronics, clothing)
```

Don't create separate stories for each status transition when they follow the same workflow pattern

```
WRONG: One story per status:
```

```
  - User changes order to pending
```

```
  - User changes order to processing
```

```
  - User changes order to shipped
```

```
  - User changes order to delivered
```

```
RIGHT: Single workflow story:
```

```
  - User updates order status (pending, processing, shipped, delivered)
```

---

---
title: ensure-vertical-slices
priority: 9
---

## ensure-vertical-slices

Ensure increments remain vertical slices (end-to-end flows across multiple epics/features
NOT horizontal layers). Each increment must deliver a complete working flow.

**DO**

Design increments as vertical slices with end-to-end flows

Include partial features from multiple epics in each increment to create complete end-to-end working flow

```
Increment 1: Basic Order Flow
```

```
  Epic: Order Entry (2/5) - create order with name and item, validate basic info
```

```
  Epic: Payment Processing (1/3) - process payment manually via admin tool
```

```
  Epic: Order Storage (1/3) - save order to file
```

```
  Epic: Order Display (1/4) - view order confirmation
```

```
  Result: Complete flow from order entry through payment to confirmation
```

Each increment demonstrates working software from start to finish
not just one layer

```
Increment 1: Manual Character Creation
```

```
  Epic: Character Creation (2/8) - enter character name, assign basic abilities manually
```

```
  Epic: Character Storage (1/3) - save character to file
```

```
  Epic: Character Display (1/5) - view basic character sheet
```

```
  Result: Can create, save, and view a character (complete vertical slice)
```

**DO NOT**

Don't create horizontal layer increments that complete one epic at a time

Don't complete all features in one epic before moving to the next epic

```
Increment 1: Complete Epic A (all features done)
```

```
Increment 2: Complete Epic B (all features done)
```

```
WRONG: This creates horizontal layers that can't be tested end-to-end until final increment
```

Don't create increments that only touch one part of the system without complete flow

```
Increment 1: Order Entry Complete
```

```
  Epic: Order Entry (8/8) - all order entry features complete
```

```
  NO payment, NO storage, NO confirmation
```

```
WRONG: Can't deliver working software, can't test end-to-end flow
```

---

---
title: enumerate-all-stories-explicitly
priority: 10
---

## enumerate-all-stories-explicitly

Enumerate ALL stories for increment(s) in focus explicitly (no ~X stories notation). Use story counts (~X stories) only for other increments. When applying new approach (System stories
component interactions)
MUST expand existing stories into component-level stories.

**DO**

List all stories explicitly for focus increment
including newly expanded stories

Explicitly enumerate every story in the focus increment with full story names

```
Increment 1 (FOCUS):
```

```
  - User enters character name
```

```
  - User assigns strength ability
```

```
  - User assigns dexterity ability
```

```
  - System validates ability scores
```

```
  - System calculates ability modifiers
```

```
  - User saves character
```

```
  - System stores character to file
```

```
  - User views character sheet
```

```
Increment 2: ~15 stories (not in focus, use count)
```

When new approach requires component interactions
expand stories from user actions into system/component stories

```
Original: 'Group tokens from canvas into mob' (1 story)
```

```
Expanded with System approach:
```

```
  - User groups tokens from canvas into mob (user action)
```

```
  - Mob manager creates mob with selected tokens (system)
```

```
  - System assigns leader randomly (system)
```

```
(1 story expanded to 3 stories showing component interactions)
```

Story count WILL increase when expanding for component-level granularity

```
Original approach: 8 user stories
```

```
After System/component approach: 23 stories
```

```
  - Original user action stories: 8
```

```
  - New system component stories: 15
```

```
(Expected increase when showing component interactions explicitly)
```

**DO NOT**

Don't use ~X notation for focus increment or keep original stories without expansion

Don't use story count notation (~X stories) for the focus increment

```
Increment 1 (FOCUS): ~8 stories (WRONG: should list all stories explicitly)
```

```
Should be: Increment 1 (FOCUS): User enters name, User assigns strength, User assigns dexterity, ... (all listed)
```

Don't keep original stories without expansion when new approach requires component-level detail

```
Keeping: 'Group tokens from canvas into mob' as single story
```

```
WRONG when System approach requires component interactions
```

```
Should expand to: User groups tokens (user), Mob manager creates mob (system), System assigns leader (system)
```

---

---
title: instructions-quality
priority: 2
---

## instructions-quality

Evaluate instruction quality across the bot/behavior/action chain. Checks for duplicated text
wordiness
vague language
and inconsistencies between instruction levels.

**DO**

Keep instructions concise
specific
and consistent across levels

Each instruction level (behavior
action
base action) should have a distinct purpose. Behavior sets context
action gives specific steps
base action provides the template.

```
Behavior: 'Create a story map capturing user journeys through epics and stories'
```

```
Action: 'Gather context for story mapping' (specific to clarify)
```

```
Base action: 'Review context, answer each question, save to clarification.json' (reusable template)
```

**DO NOT**

Do not duplicate instructions across levels or use vague language

Same instruction text repeated at behavior and action level adds noise. Vague words like 'consider'
'might'
'should probably' weaken guidance.

```
Duplicate: behavior says 'validate story structure' AND action says 'validate story structure'
```

```
Vague: 'You might want to consider checking the story names' -> 'Check each story name follows verb-noun format'
```

---

---
title: lightweight-and-precise
priority: 4
---

## lightweight-and-precise

Create lightweight but precise documentation during shaping. Focus on structure and scope
not detailed specifications.

**DO**

Keep documentation lightweight and easy to walk through. Example: '(E) Manage Orders → (SE) Place Order → (S) Validate Order Items' (shows hierarchy
not specs)

Focus on structure and scope without over-elaboration - make the map easy to walk through as it tells a story
showing hierarchy and flow without detailed specifications

```
(E) Manage Orders
  (SE) Place Order
    (S) Validate Order Items
(Shows hierarchy and flow, not detailed specs)
```

**DO NOT**

Don't over-elaborate or add detailed specifications during shaping. Example: '(E) Manage Orders → Detailed API specs
database schema
UI mockups' (TOO MUCH)

Don't add detailed technical specifications or over-elaborate story mapping during the shaping phase - keep it lightweight

```
(E) Manage Orders
  → Detailed API specs, database schema, UI mockups, validation rules
(Too much detail for shaping phase)
```

---

---
title: outcome-oriented-language
priority: 3
---

## outcome-oriented-language

Use outcome-oriented language over mechanism-oriented language. Focus on what is created or achieved
not how it's shown or communicated.

**DO**

Focus on outcomes and artifacts
not mechanisms. Example: 'Power Activation Animation' not 'Visualizing Power Activation'

Use verbs that describe artifacts and outcomes - name concepts by what they ARE or CREATE
focusing on tangible results. Ask: What is being created? What does the user get?

```
System --> shows animation (not 'Visualizing')
```

```
System --> provides feedback (not 'Displaying')
```

```
System --> displays indicators (not 'Showing')
```

```
System --> loads configuration (not 'Providing Settings')
```

```
System --> displays power activation animation (not 'Visualizing Power Activation')
```

```
System --> provides combat outcome feedback (not 'Showing Combat Results')
```

```
System --> displays hit indicators (not 'Displaying Hit Information')
```

**DO NOT**

Don't focus on communication mechanisms. Example: 'Showing Combat Results' (mechanism) â†’ 'Combat Outcome Feedback' (outcome)

Don't use generic communication or mechanism verbs - don't name concepts by their mechanism of delivery

```
Visualizing Power Activation (wrong) â†’ System --> displays power activation animation (correct)
```

```
Showing Combat Results (wrong) â†’ System --> provides combat outcome feedback (correct)
```

```
Displaying Hit Information (wrong) â†’ System --> displays hit indicators (correct)
```

```
Presenting Configuration Options (wrong) â†’ System --> loads configuration panel (correct)
```

Mechanism verbs to avoid - these describe how something is shown rather than what is created

```
Showing results
```

```
Displaying information
```

```
Visualizing data
```

```
Presenting options
```

```
Providing settings
```

```
Enabling features
```

```
Allowing access
```

---

---
title: review-and-expand-stories
priority: 14
---

## review-and-expand-stories

Review and expand stories based on new approach granularity. When planning decisions specify 'System stories' or detailed component interactions
MUST break down existing stories into component-interaction stories. The story count WILL increase. NOTE: This rule operates on a different axis than P13 (Consolidate Superficial Stories). P14 decomposes by system component behavior (different behaviors within one story). P13 eliminates data-value duplication (same behavior
different input values). Apply P13 first to consolidate data variations
then apply P14 to expand by component behavior.

**DO**

Break down stories into component interactions when System or Technology or Infrastructure approach is selected

When System/Technology/Infrastructure approach is chosen
expand user action stories into user + system component stories

```
Original: 'Group tokens from canvas into mob' (1 user story)
```

```
Expanded with System/ Technology/Infrastructure approach (3 stories):
```

```
  1. User groups tokens from canvas into mob (user action)
```

```
  2. Mob manager creates mob with all selected tokens (system/component)
```

```
  3. System assigns leader randomly (system/component)
```

```
Story count increased from 1 to 3
```

Review existing stories and identify where component interactions need to be made explicit

```
Original: 'User submits order' (1 story)
```

```
Expanded with System/ Technology/ Infrastructure approach (4 stories):
```

```
  1. User submits order with items (user action)
```

```
  2. Order validator validates order details (system)
```

```
  3. Inventory manager reserves items (system)
```

```
  4. System generates order confirmation (system)
```

```
Story count increased from 1 to 4
```

Break down payment and processing flows into discrete system component steps

```
Original: 'User pays for order' (1 story)
```

```
Expanded with System approach (5 stories):
```

```
  1. User enters payment information (user action)
```

```
  2. Payment validator validates payment details (system)
```

```
  3. Payment gateway processes transaction (system)
```

```
  4. Transaction recorder saves payment (system)
```

```
  5. System displays payment confirmation (system)
```

```
Story count increased from 1 to 5
```

**DO NOT**

Don't keep original stories without expansion when new approach requires component-level detail

Don't keep single user story when System approach requires showing component interactions

```
Keeping: 'Group tokens from canvas into mob' as single story
```

```
WRONG when System approach selected
```

```
Should expand to show: User action + Mob manager creates mob + System assigns leader
```

Don't assume story count stays the same when changing granularity approach

```
Planning says: 'Use System approach for component interactions'
```

```
Original count: 8 user stories
```

```
WRONG: Keep count at 8 stories
```

```
RIGHT: Expand to ~20-24 stories showing user actions + system components
```

---

---
title: rule-change-impact
priority: 99
---

## rule-change-impact

Compare current validation violations against a saved baseline to detect the impact of rule or scanner changes. Run validate with --save-baseline before changing rules
then run again after to see the diff.

**DO**

Save a baseline before modifying rules or scanners
then compare after

Baseline captures violation snapshot. After rule/scanner change
diff shows new violations
resolved violations
and severity changes.

```
Before change: save baseline with 12 violations
```

```
After change: 10 violations remain, 2 resolved, 3 new -> net impact visible
```

**DO NOT**

Do not modify rules without checking impact

Changing rules without a baseline means you cannot measure impact. Always save a baseline first.

```
No baseline: 'No baseline found' info message shown
```

```
Stale baseline: results may not reflect recent changes
```

---

---
title: scale-story-map-by-domain
priority: 10
---

## scale-story-map-by-domain

Scaling concern: at small scale
domain objects with similar behavior can live together in a single sub-epic. As domain objects develop distinct behavior
break out by domain into parallel sub-epics with consistent stories under each. Domain First
Operation Second. After expanding stories per review_and_expand_stories
organize the resulting stories by domain
not by technology layer.

**DO**

At small scale keep domains together. As complexity grows
break out by domain with consistent stories. Domain First
Operation Second.

At small scale
keep related domain objects together

```
Single sub-epic 'Process Payment' with stories covering wire, ACH, and check together
```

```
Fine when there are only a few stories and the behavior is similar
```

```
Single sub-epic 'Render Diagram' covering epics, stories, and increments -- fine when each has 1-2 simple stories
```

As complexity grows
break out by domain with consistent stories under each

```
'Make Wire Payment', 'Make ACH Payment', 'Make Check Payment' as parallel sub-epics
```

```
Each has consistent stories: Collect Recipient Info, Validate Payment, Submit Payment
```

```
Plus unique stories where the domain demands it: Wire: Validate Intermediary Bank; ACH: Validate Routing Number
```

```
Signal to break out: domain objects have different behavior that makes shared stories confusing or untestable
```

When scaling
organize Domain First
Operation Second

```
Primary axis is the domain object (wire, ACH, check)
```

```
Operations (collect, validate, submit) are stories within each
```

```
This keeps related domain logic together instead of scattering it across operation-based groupings
```

After expanding stories (per review_and_expand_stories)
organize by domain

```
First expand a story into system/component interactions (per review_and_expand_stories)
```

```
Then group the expanded stories under domain-specific sub-epics -- not under technology-layer sub-epics
```

**DO NOT**

When scaling
do not group by operation or technology. Do not force the break-out prematurely.

When scaling
do not group by operation or technology

```
Sub-epic 'Validate All Payments' with stories for wire, ACH, and check mixed in -- groups by operation, not domain
```

```
Sub-epic 'Database Operations' with stories for saving wire, ACH, and check data -- groups by technology layer
```

Do not force the break-out prematurely

```
Creating 5 sub-epics when you only have 3 stories total -- keep them together until complexity demands separation
```

```
Naming sub-epics as bare nouns: 'Wire Transfer' -- still needs the operation verb: 'Make Wire Payment'
```

---

---
title: small-and-testable
priority: 6
---

## small-and-testable

Stories must be testable as complete interactions and deliverable independently. Balance testability with maintaining value and behavioral focus - stories should be small enough to test but large enough to matter.

**DO**

Create stories that can be tested and delivered independently. Example: 'Customer places order' (testable with clear acceptance criteria: order created
payment processed)

Stories must be testable as complete interactions and deliverable independently - fine-grained enough to enable frequent feedback while maintaining behavioral focus. Must have clear acceptance criteria
can be tested without parent context
complete enough to verify behavior
and small enough to test quickly.

```
Customer --> places order (testable: order created, payment processed)
```

STORY vs STEP distinction - Story = User/system outcome (testable independently with clear acceptance criteria). Step = Implementation detail (not testable alone
verified as part of parent story test).

```
Story: 'User --> renders diagram' â†’ Steps: 'generates XML', 'calculates positions', 'applies styles'
```

**DO NOT**

Don't create stories that can't be tested or delivered independently. Example: 'Add order button' (not testable - can't verify independently without full order flow context)

Don't create stories too small to test meaningfully or make implementation steps into stories - don't sacrifice behavioral value for artificial testability

```
Add order button (can't test without full order flow)
```

```
Display error message (can't test without validation context)
```

```
Convert Diagram to StoryGraph Format (implementation step, no acceptance criteria)
```

```
Serialize Components to JSON (implementation step, not testable alone)
```

```
Calculate Component Positions (implementation step, no user outcome)
```

Implementation operation indicators that are NOT testable as stories - these are steps within larger stories

```
Serialize, deserialize, convert, transform, format
```

```
Calculate, compute, generate (technical artifacts)
```

```
Apply, set, configure (technical settings)
```

```
Save, write, store (without user context)
```

---

---
title: story-map-existing-code
priority: 8
---

## story-map-existing-code

When creating story maps from code
start with the outermost layer (entry points)
analyze operations
create epics from higher-order goals
and lay out the story journey.

**DO**

Start with entry points and trace to epics and stories. Example: Operations 'render-outline
render-increments' → Goal 'Render StoryGraph' → Epic 'Render StoryGraph'

Step 1: Find Entry Points (CLI commands
UI entry points
MCP server tools
API contracts
acceptance tests)

```
CLI commands (main(), argparse)
```

```
UI entry points (routes, handlers, button clicks)
```

```
MCP server tools (names, parameters)
```

```
API contracts (REST, GraphQL, WSDL)
```

```
Acceptance tests (end-to-end, BDD)
```

Step 2: Analyze Operations (list operations
group by functional purpose)

Step 3: Create Epics from Goals (group operations by higher-order goals
create epics from goals NOT class structure)

```
Operations 'render-outline, render-increments' → Goal 'Render StoryGraph' → Epic 'Render StoryGraph'
```

Step 4: Create Sub-Epics from Behaviors (identify distinct behaviors for each epic
group into sub-epics)

```
Epic 'Render StoryGraph' → Sub-Epics 'Render Outline', 'Render Increments'
```

Step 5: Lay Out Story Journey (trace code flow: Start → Middle → End
include WHEN/WHY/OUTCOME/ACTOR
include error handling)

```
User --> invokes command, System --> validates input, System --> processes, System --> confirms
```

**DO NOT**

Don't start with internal classes or create epics from class structure. Example: Creating epics from class structure (WRONG) → Create epics from goals (CORRECT)

Don't start with internal classes instead of entry points - don't create epics from class structure instead of goals - don't create stories from every method call - don't miss context (when/why/outcome) in stories - don't make implementation details into stories

```
Starting with internal classes instead of entry points
```

```
Creating epics from class structure instead of goals
```

```
Creating stories from every method call
```

```
Missing context (when/why/outcome) in stories
```

```
Making implementation details into stories
```

---

---
title: valuable
priority: 5
---

## valuable

Stories must capture discrete behavior that can be described in system or business terms. Each story represents a distinct behavioral unit — not raw data access or isolated operations
but a recognizable action with a describable outcome.

**DO**

Each story must represent a discrete behavior — a recognizable action that can be described in business or system terms. Order by user journey flow
not technical sequence. The test: can you describe what this story DOES as a behavior someone would recognize? If yes
it's a valid story.

```
Developer --> edit epic name (behavior: modify story map element)
```

```
User --> generate DrawIO diagram (behavior: produce visual diagram output)
```

```
System --> initialize configuration on startup (behavior: prepare system for use)
```

```
System --> display recipient bank details (behavior: show bank information after recipient selection)
```

**DO NOT**

Don't create stories that are raw data operations with no describable behavior. Example: 'System --> read all epics from diagram' (no behavior - just data access
what happens next?)

Don't create raw data access operations that lack describable behavior — these are implementation steps
not stories

```
System --> read all epics from diagram (no behavior - just data access, then what?)
```

```
System --> load all features in graph epic (no describable outcome)
```

```
System --> serialize components to JSON (implementation step, not behavior)
```

```
System --> convert diagram to StoryGraph format (data transformation, not behavior)
```

```
System --> calculate component positions (computation, not behavior)
```

Don't create stories too large to describe as a single behavior - split into discrete behavioral units

```
User --> manage entire order lifecycle (multiple behaviors bundled - split)
```

```
System --> process complete checkout workflow (multiple behaviors bundled - split)
```

Don't order stories by technical sequence instead of user journey flow - stories should follow the user's journey
not implementation order

No-behavior indicators to reject - these patterns indicate stories lack describable behavior

```
Just reads/loads data without describable outcome
```

```
Just converts/formats data as an implementation step
```

```
Just calculates/computes as an intermediate operation
```

---

---
title: verb-noun-format
priority: 1
---

## verb-noun-format

Use verb-noun format consistently across all hierarchy levels. Actor --> verb noun [qualifiers]. Actor is documented separately
NOT in the name. Focus on specific actions with context.

**DO**

Use specific verb-noun format with actor documented separately. Example: 'Places Order' with actor=Customer

FORMAT: Actor --> verb noun [optional qualifiers]. Actor is documented separately in story metadata
NOT in name. Use base verb forms (infinitive/imperative)
not gerunds or third-person singular. Include specific objects and context qualifiers where needed. Focus on what users/code CAN DO
not what things ARE.

```
Epic: 'Manage Customer Orders', 'Process Online Payments'
```

```
Sub-Epic: 'Place New Order', 'Validate Credit Card Payment'
```

```
Story: 'User --> processes order payment'
```

```
Story: 'System --> validates submitted payments'
```

Stories describe REAL ACTIONS that can be performed
organized by lifecycle: Load â†’ Read â†’ Edit â†’ Render â†’ Synchronize â†’ Search â†’ Save

```
System --> loads order data
```

```
System --> validates payment
```

```
System --> generates XML
```

Actor is documented separately
NEVER in the story name itself

```
Places Order (actor: Customer)
```

```
Validates Payment (actor: System)
```

```
Updates Stock (actor: InventoryManager)
```

Use base verb forms for consistency across all hierarchy levels. Wrong: 'Selects Tokens' (3rd person)
'Selecting Tokens' (gerund).

```
Select Tokens
```

```
Group Minions
```

```
Process Payment
```

**DO NOT**

Don't include actor in name or use generic operations. Example: 'Customer Places Order' (WRONG) â†’ 'Places Order' with actor=Customer (CORRECT)

Never include actor name in the story/epic/sub-epic name - actor is documented separately in metadata. Wrong: 'Customer Places Order'. Correct: 'Places Order (actor: Customer)'.

```
Places Order (actor: Customer) not 'Customer Places Order'
```

```
Validates Payment (actor: OrderProcessor) not 'OrderProcessor Validates Payment'
```

```
Adds Product (actor: Cart) not 'Cart Adds Product'
```

Don't create generic operations without specificity
use noun-only names
capability-based names
or wrong verb forms

```
User --> processes payment (too generic - which payment?)
```

```
Payment Processing (noun-only, not verb-noun)
```

```
Order Management (capability, not action)
```

```
Selects Tokens (wrong verb form - should be 'Select Tokens')
```

Don't use capability nouns or structural descriptions - describe what things DO
not what they ARE or CONTAIN

```
PaymentValidator Contains Validation Logic
```

```
Cart Hierarchy Foundation
```

```
Product Represents Item
```

Transform capabilities and structural descriptions into concrete actions

```
'Contains Logic' â†’ System --> generates XML or System --> renders diagram
```

```
'Tracks Count' â†’ System --> reads count or System --> updates count
```

```
'Represents X' â†’ System --> creates X or System --> loads X
```