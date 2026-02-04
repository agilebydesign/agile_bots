# Domain Model Description: Agile Bots

**File Name**: `agile-bots-domain-model-description.md`
**Location**: `agile_bots/docs/stories/agile-bots-domain-model-description.md`

## Solution Purpose
Domain model for Agile Bots

---

## Domain Model Descriptions

### Module: exit_result


#### ExitResult

**Key Responsibilities:**
- **Get exit code**: This responsibility involves collaboration with Integer.
- **Get exit message**: This responsibility involves collaboration with String.
- **Get should cleanup**: This responsibility involves collaboration with Boolean.

#### JSONExitResult

**Key Responsibilities:**
- **Serialize exit result to JSON**: This responsibility involves collaboration with ExitResult, JSON String.
- **Include exit code**: This responsibility involves collaboration with Integer, JSON.
- **Include exit message**: This responsibility involves collaboration with String, JSON.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

#### MarkdownExitResult

**Key Responsibilities:**
- **Serialize exit result to Markdown**: This responsibility involves collaboration with ExitResult, Markdown String.
- **Format exit documentation**: This responsibility involves collaboration with ExitResult, Markdown String.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

#### TTYExitResult

**Key Responsibilities:**
- **Serialize exit result to TTY**: This responsibility involves collaboration with ExitResult, TTY String.
- **Format exit message**: This responsibility involves collaboration with Message, TTY String.
- **Wraps domain exit result**: This responsibility involves collaboration with ExitResult.

### Module: help


#### JSONHelp

**Key Responsibilities:**
- **Serialize help to JSON**: This responsibility involves collaboration with Help, Dict.
- **Include help sections**: This responsibility involves collaboration with Sections, Array.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### JSONStatus

**Key Responsibilities:**
- **Serialize status to JSON**: This responsibility involves collaboration with Status, JSON String.
- **Include progress path**: This responsibility involves collaboration with Progress Path, String.
- **Include stage name**: This responsibility involves collaboration with Stage Name, String.
- **Include current behavior**: This responsibility involves collaboration with Behavior Name, String.
- **Include current action**: This responsibility involves collaboration with Action Name, String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

#### MarkdownHelp

**Key Responsibilities:**
- **Serialize help to Markdown**: This responsibility involves collaboration with Help, String.
- **Format help sections**: This responsibility involves collaboration with Sections, Markdown.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### MarkdownStatus

**Key Responsibilities:**
- **Serialize status to Markdown**: This responsibility involves collaboration with Status, Markdown String.
- **Format progress section**: This responsibility involves collaboration with Progress Path, Stage Name, Markdown String.
- **Format workflow state**: This responsibility involves collaboration with Status, Markdown String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

#### Status

**Key Responsibilities:**
- **Get progress path**: This responsibility involves collaboration with String.
- **Get stage name**: This responsibility involves collaboration with String.
- **Get current behavior name**: This responsibility involves collaboration with String.
- **Get current action name**: This responsibility involves collaboration with String.
- **Get has current behavior**: This responsibility involves collaboration with Boolean.
- **Get has current action**: This responsibility involves collaboration with Boolean.

#### TTYHelp

**Key Responsibilities:**
- **Serialize help to TTY**: This responsibility involves collaboration with Help, String.
- **Format help sections**: This responsibility involves collaboration with Sections, String.
- **Wraps domain help**: This responsibility involves collaboration with Help.

#### TTYStatus

**Key Responsibilities:**
- **Serialize status to TTY**: This responsibility involves collaboration with Status, TTY String.
- **Format progress line**: This responsibility involves collaboration with Progress Path, Stage Name, TTY String.
- **Format hierarchical status**: This responsibility involves collaboration with Bot, Status, TTY String.
- **Wraps domain status**: This responsibility involves collaboration with Status.

---

## Source Material

**Primary Source:** `input.txt`
**Date Generated:** 2025-01-27
**Context:** Shape phase - Domain model extracted from story-graph.json
