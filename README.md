# Agile Bots

AI-powered bots that inject Agile delivery, product, and engineering best practices directly into your workflow.

## Overview

Agile Bots is a collection of AI-powered tools that guide teams through proven methodologies for story development and object-oriented design. This initial release includes **StoryBot** and **CRC Bot**, two complementary tools that transform how you work with AI assistants.

## What's Included

### StoryBot

Transforms user needs into well-structured, testable user stories through a progressive 7-behavior workflow:

- **Shape:** Create story maps and domain models from user context
- **Prioritization:** Organize stories into increments and prioritize backlogs
- **Discovery:** Elaborate stories with flows, rules, and integration details
- **Exploration:** Define acceptance criteria with Given/When/Then statements
- **Scenarios:** Write detailed BDD scenarios from acceptance criteria
- **Tests:** Generate executable test code from scenarios
- **Code:** Write SOLID level code quality

![StoryBot Behaviors](docs/images/storybot-behaviors.png)  

*Navigate through all 7 StoryBot behaviors with visual progress tracking*

**Best Practices:**
- Progressive refinement from vision to code
- Story mapping and domain modeling
- BDD scenario development
- Vertical slice story decomposition
- Test-driven development workflows
- Acceptance criteria validation

![StoryBot Validation Rules](docs/images/storybot-validation-rules.png)  

*Built-in validation rules ensure scenarios follow BDD best practices*

### CRC Bot

Models solution domains using CRC (Class-Responsibility-Collaborator) cards to define clean object-oriented architectures:

- **Domain:** Extract domain concepts and responsibilities from stories, build initial CRC cards
- **Design:** Apply OOP design principles and patterns to refine object responsibilities
- **Walkthrough:** Validate the CRC model by tracing object flows through real scenarios

![CRC Bot Behaviors](docs/images/crcbot-behaviors.png)  

*Navigate through all 3 CRC Bot behaviors with visual progress tracking*

**Best Practices:**
- Responsibility-driven design
- Object collaboration modeling
- Domain-driven design principles
- OOP pattern application
- Walkthrough-based validation
- Clear separation of concerns

![CRC Bot Validation Rules](docs/images/crcbot-validation-rules.png)  

*Built-in validation rules ensure domain models follow DDD and OOP best practices*

### More Bots Coming Soon

- Domain-Driven Design Bot
- Architecture-Driven Delivery Bot
- Behavior-Driven Development Bot
- Validated Learning Bot
- And much more

## Multiple Interfaces

### Command-Line Interface (CLI)

- Full-featured terminal interface (`story_bot_cli`, `crc_bot_cli`)
- Behavior navigation and action execution
- Scope management to filter work by stories, epics, or increments
- State persistence across sessions
- Multiple output formats: TTY-Terminal, JSON, and Markdown
- JSON output enables programmatic integration and custom tooling

![CLI Terminal Interface](docs/images/cli-terminal-interface.png)  

*Interactive terminal with behavior tree, available commands, and navigation support*

### VSCode Panel Extension

- Visual interface embedded directly in your editor
- Real-time workflow visualization
- Interactive views for behaviors, instructions, and scope
- Click-to-execute actions and navigate workflows
- Live session management with persistent Python backend

<img src="docs/images/panel-interface.png" alt="Panel Interface" width="600"/>

*Full panel view showing workspace, behaviors, scope filtering, and contextual instructions*

### Direct AI Channel

- MCP Server integration for AI assistants (Claude, ChatGPT)
- Natural language invocation via trigger words
- Cursor command/VSCode Chat commands for seamless workflow execution
- Automatic routing to current workflow state

![Direct AI Test Generation](docs/images/direct-ai-test-generation.png)  

*AI generates test files following BDD patterns with scenario validation and proper test structure*

## Guided Workflow System

Both bots follow a consistent 5-action pattern for each behavior:

1. **Clarify** - Gather context through structured questions
2. **Strategy** - Select a strategy to apply specific practices
3. **Build** - Construct story graphs, tests, and code
4. **Validate** - Check against built-in rules and scanners
5. **Render** - Generate story maps, acceptance criteria, scenarios, test cases, domain models, and working code

![Behavior Actions Detail](docs/images/behavior-actions-detail.png)  

*Each behavior expands to show all 5 workflow actions with progress tracking*

### 1. Clarify - Structured Context Gathering

The Clarify action presents targeted questions to ensure the AI has all necessary context:

![Clarify AI Response](docs/images/clarify-ai-response.png)  

*AI generates answers based on context and configurable questions*

![Clarify Questions](docs/images/clarify-questions.png)  

*Edit, refine, and regenerate clarification responses*

### 2. Strategy - Choose Your Approach

The Strategy action helps you select the right approach based on your gathered context. The AI presents structured strategy questions and displays your previous clarification responses to inform strategic decisions:

![Strategy Context Review](docs/images/strategy-clarify-context.png)  

*AI chooses contextually relevant strategies to guide the depth and approach you want to take to shaping and other behaviors*

![Strategy Selection](docs/images/strategy-selection.png)  

*Edit and refine strategies based on your preferred approach*

### 3. Build - Generate story graphs, tests, and code

Construct structured representations of your stories, tests, and code.

![Build Story Map](docs/images/build-story-map.png)  

*Generate story maps, story scenarios, and other artifacts*

### 4. Validate - Automated Quality Checks

Detect violations and correct based on configurable best practices:

![Validation Report Summary](docs/images/validation-report-summary.png)  

*Review scanner execution status, violation details by rule, and access detailed reports*

### 5. Render - Generate Deliverables

The Render action transforms knowledge graphs into documentation, diagrams, and reports for your team. It uses templates and synchronizers to generate various outputs including story maps, domain models, test scenarios, and domain model walk-throughs:

![Workflow Architecture](docs/images/workflow-architecture.png)  

*Generates artifacts simultaneously in multiple formats including JSON knowledge graphs, Markdown documentation, and visual diagrams*

## AI Instructions Panel

The panel provides rich, contextual instructions to guide your AI assistant through each step, including base behavior instructions, action-specific guidance, structured clarification questions, evidence requirements, knowledge graph templates, rules, and output paths.

## Built-In Intelligence

- **Guardrails:** Structured questions and evidence requirements guide you through each phase and validate AI understanding before proceeding
- **Rules Injection:** Configurable agile best practices guide AI work supported by code scanners/evals
- **Story and Domain Graph:** Structured JSON representations of stories, domains, and tests
- **Templates:** Generate Markdown documents, Mermaid diagrams, Drawio diagrams, and more
- **Activity Tracking:** Complete audit trail of all work performed

## Installation

```bash
# Clone the repository
git clone https://github.com/agilebydesign/agile_bots.git
cd agile_bots

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Getting Started

```bash
# Start story mapping
story_bot_cli --behavior shape

# Model your domain objects
crc_bot_cli --behavior domain

# Continue from where you left off
story_bot_cli  # or crc_bot_cli

# Get help
story_bot_cli --help
crc_bot_cli --help
```

## What Makes This Different

Rather than hiring Agile by Design, or any other Agile coaches to help train you on Agile methods and approaches, just install this in Visual Studio or Cursor, use Agile Bots to inject Agile instructions into your AI prompting and you'll never have to speak to another Agile coach again.

In all seriousness, if you are tired of fighting with your AI assistant to deliver well-crafted, simple, story-driven, testable code, then give this tool a try.

## Licensing

This project is **dual-licensed**:

### Option 1: AGPL v3 (Free & Open Source)

- ✅ Free to use, modify, and distribute
- ✅ Use commercially
- ⚠️ **Must share modifications** under AGPL v3
- See [LICENSE](LICENSE) for details

### Option 2: Commercial License

- ✅ Keep modifications private
- ✅ No copyleft obligations
- ✅ Legal indemnification
- 💰 Contact [Agile by Design](https://www.agilebydesign.com/) for pricing

[View Commercial License Terms](LICENSE-COMMERCIAL.md)

## Technical Details

- **Language:** Python 3.10+
- **Core Dependencies:** FastMCP, NLTK
- **Outputs:** JSON knowledge graphs, Markdown docs, Mermaid diagrams, validation reports
- **Testing:** Comprehensive test suites for domain logic, CLI, and panel interfaces

## Contributing

Contributions are welcome! Please ensure your code follows the existing patterns and includes appropriate tests.

## Support

For questions, issues, or commercial licensing inquiries, visit [Agile by Design](https://www.agilebydesign.com/).
