# Agile Bots Target Architecture — JS/Node-Centric

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Presentation Adapters](#presentation-adapters)
- [Engine Example (Proof of Concept)](#engine-example-proof-of-concept)
  - [Architecture (Domain, Purpose, Flow, Examples)](#architecture-domain-purpose-flow-examples)
  - [CLI](#cli)
  - [Panel](#panel)

---

## Overview

The target architecture moves **all business logic into JavaScript/Node.js**. The server (extension host) talks **directly** to business logic—no CLI, no subprocess, no IPC. The CLI is a **separate entry point** for direct use, also in JS, wrapping the same business logic layer. The webview client extends business logic to wrap the JS DOM with the same logic the server uses.

| Principle | Meaning |
|-----------|---------|
| **Logic in JS** | Business logic in Node.js; no Python, no subprocess |
| **Domain** | Pure JS (Counter, Engine)—no DOM, no VS Code, no persistence. |
| **Server domain** | Inherits from domain; adds persistence (e.g. `CounterServer extends Counter`). |
| **Server view** | EngineView, CounterView—handles postMessage; uses server domain. |
| **Client → domain + DOM** | Webview loads shared domain (bundled); adds DOM only. Same logic, not duplicated. |
| **CLI separate entry point** | `node cli.js` for direct use; wraps same business logic as panel |
| **CLI output adapters** | `counter_adapter = CounterTty(counter)`; `formattedTotal = counter_adapter.total`; same interface as domain; `.internals` for debugging |

---

## Architecture

**Shared domain; server adds persistence, client adds DOM. No duplication.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PRESENTATION ADAPTERS (inherit / compose shared domain)                     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │ SERVER VIEW     │  │ CLIENT          │  │ CLI             │          │
│  │ postMessage     │  │ Domain +        │  │ Domain +         │          │
│  │ uses Server     │  │ DOM only       │  │ TTY|JSON|HTML    │          │
│  │ Domain          │  │ postMessage     │  │ output adapters  │          │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘          │
└───────────┼────────────────────┼────────────────────┼────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SERVER DOMAIN (extends Domain) — adds persistence                           │
│  CounterServer extends Counter; _load(), _save()                             │
└─────────────────────────────────────────────────────────────────────────────┬┘
            │ inherits from
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  DOMAIN (Pure JS — no DOM, no VS Code, no Node APIs)                         │
│  Engine → Counter, Foo. Shared by client and CLI.                            │
└─────────────────────────────────────────────────────────────────────────────┬┘
                                                                              │
                                                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE (File System, Paths)                                         │
│  fs, path, JSON—as needed by business logic                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Presentation Adapters

### Server (Extension Host)

- **Server view:** EngineView, CounterView—webview panel; message routing; postMessage
- **Server domain:** CounterServer extends Counter—adds persistence (_load, _save)
- **Flow:** Webview `postMessage` → view._lookup → server domain (persists) → `postMessage`
- **Example:** `postMessage({ command: 'counter.count', value: 4 })` → CounterView → CounterServer.count(4) [persists] → `postMessage({ total: 4 })`

### Client (Webview / DOM)

- **Domain:** Webview HTML; engine_client.js; **shared Counter** (bundled); DOM elements
- **Purpose:** Render UI; capture user input; immediate display via shared domain; sync to server for persistence
- **Flow:** User action → **counter.count(amount)** (shared logic) → `updateDom(counter.total)` → `syncToServer(command, value)` → server persists and echoes
- **Example:** User changes amount → `counter.count(4)` [shared domain] → `updateDom(counter.total)` → `syncToServer("counter.count", 4)` → receive `{ total: 4 }` [confirmation]
- **No duplication:** Client uses the same Counter class as server; DOM layer only binds to domain state.

#---



## Architecture 

**Flow:** 
CLI → args → lookup(engine, path) → domain. 

or 

Panel → postMessage(command) → view._lookup(command) → domain → postMessage(result).

**Examples:**

```
Domain:     e = new Engine(); e.counter.count(4); e.counter.count(7); e.counter.total → 11
CLI:        cli_engine counter.count --amount 7  → engine.counter.count(7)
            cli_engine counter.total             → 7
            cli_engine counter.foo.bar --value "yum"  → set
Panel:      postMessage({ command: 'counter.count', value: 4 }) → view.counter.count(4) → postMessage({ total: 4 })
```

### Domain
Engine (root) loads Counter; Counter has Foo. Pure JS—no DOM, no VS Code, no CLI. **Foo is defined inside counter.js** (child classes without their own files live in the root file).

```javascript
// counter/counter.js — Counter (root) and Foo (child) in same file
class Foo { constructor() { this.bar = ""; } }

class Counter {
  constructor() { this._total = 0; this.foo = new Foo(); }
  count(amount) { this._total += Number(amount) || 0; }
  get total() { return this._total; }
  reset() { this._total = 0; }
  hydrate(data) { if (data.total !== undefined) this._total = data.total; if (data.fooBar !== undefined) this.foo.bar = data.fooBar; }
}

// engine/engine.js
const Counter = require("../counter/counter.js");
class Engine {
  constructor(counter) { this.counter = counter || new Counter(); }
}
```

**Inheritance:** Server domain extends domain and adds persistence. Client uses domain + DOM adapter.

```javascript
// counter/counter_server.js — server domain: inherits from Counter, adds persistence
const { Counter } = require("./counter.js");
const fs = require("fs");
const path = require("path");

class CounterServer extends Counter {
  constructor(filePath) {
    super();
    this._filePath = filePath;
    this._load();
  }

  _load() {
    try {
      const data = JSON.parse(fs.readFileSync(this._filePath, "utf8"));
      this.hydrate(data);
    } catch (_) {}
  }

  _save() {
    fs.writeFileSync(this._filePath, JSON.stringify({ total: this.total, fooBar: this.foo.bar }));
  }

  count(amount) {
    super.count(amount);
    this._save();
  }

  reset() {
    super.reset();
    this._save();
  }
}

module.exports = { CounterServer };
```

**Server view** (EngineView, CounterView) uses **server domain** (CounterServer). View handles postMessage; domain handles persistence.

---

### CLI

- **Domain:** cli.js; Engine instance; output adapters (CounterTty, CounterMarkdown, CounterJson)
- **Purpose:** Standalone terminal entry point; param parsing; domain lookup on Engine
- **Flow:** `args` → parse `--format` → choose adapter → run commands → `counterAdapter.total` → stdout
- **Where mode is set:** `--format tty|markdown|json` on the command line; default is `tty` if omitted.

```
$ node cli.js count 4 count 7                    → format = "tty"      (default)
$ node cli.js count 4 count 7 --format markdown → format = "markdown"
$ node cli.js count 4 count 7 --format json     → format = "json"

format → adapter:  tty → CounterTty,  markdown → CounterMarkdown,  json → CounterJson
```

- **Data flow:**

```
$ cli_engine counter.count --amount 7
    → lookup(engine, "counter.count") → engine.counter.count(7)
$ cli_engine counter.total
    → lookup(engine, "counter.total") → 7
$ cli_engine counter.foo.bar --value "yum"  # set
$ cli_engine counter.foo.bar                 # get
```

**Example (engine/cli.js):**

```javascript
const { Engine } = require("./engine.js");
const { CounterTty } = require("../counter/adapters/counter_tty.js");
const { CounterMarkdown } = require("../counter/adapters/counter_markdown.js");
const { CounterJson } = require("../counter/adapters/counter_json.js");
const engine = new Engine();  // CLI uses plain Counter (no persistence)

const args = process.argv.slice(2);

// Parse --format (mode) → choose adapter
const formatIdx = args.indexOf("--format");
const format = formatIdx >= 0 ? args[formatIdx + 1] || "tty" : "tty";
const cmdArgs = formatIdx >= 0 ? args.slice(0, formatIdx) : args;

const path = cmdArgs.find(a => !a.startsWith("--")) || "counter.total";
const paramArgs = cmdArgs.filter(a => a.startsWith("--"));
const params = {};
for (let i = 0; i < paramArgs.length; i += 2) {
  if (paramArgs[i + 1] != null) params[paramArgs[i].slice(2)] = paramArgs[i + 1];
}

function lookup(obj, pathStr) {
  const parts = pathStr.split(".");
  let target = obj;
  for (let i = 0; i < parts.length - 1; i++) target = target[parts[i]];
  return [target, parts[parts.length - 1]];
}

const [obj, key] = lookup(engine, path);
const target = obj[key];
let result;
if (typeof target === "function") {
  result = target.apply(obj, Object.values(params));
} else if (params.value !== undefined) {
  obj[key] = params.value;
  result = obj[key];
} else {
  result = target;
}

// Output via adapter chosen from format
const counterAdapter = format === "markdown" ? new CounterMarkdown(engine.counter) :
                       format === "json"     ? new CounterJson(engine.counter) :
                       new CounterTty(engine.counter);
process.stdout.write(counterAdapter.total);
```

**Output adapters:** Same interface as domain object. Pattern: `counter_adapter = <any>Counter(counter)`; `formattedTotal = counter_adapter.total`. Adapters expose `.internals` for debugging. Format parsing and adapter selection are in the code block above.

| Adapter | Role | Example |
|---------|------|---------|
| **CounterTty** | Human-readable terminal output | `counter_adapter.total` → `Total: 11\n` |
| **CounterMarkdown** | Formatted for docs/panels | `counter_adapter.total` → `## Counter\n\n**Total:** 11\n` |
| **CounterJson** | Machine-readable; for tooling | `counter_adapter.total` → `{"total":11}` |

### Panel

**Data flow:**

```
Initial load:
EngineView.createOrShow(extensionUri)
    → new EngineView(panel, extensionUri)
        → _engine = new Engine()
        → this.counter = new CounterView(panel, _engine.counter)
        → panel.webview.html = _getHtml() [includes engine_client.js]
    → onDidReceiveMessage(handler) [registered]
    → [webview loads]
        → Client: postMessage({ command: 'counter.total' }), postMessage({ command: 'counter.foo.bar' })
        → Server: handler delegates to view.counter.total(), view.counter.foo.bar()
            → postMessage({ total: 0 }), postMessage({ fooBar: "" })
        → Client: updateTotal(0), updateFooBar(""), display

User changes amount:
    → Client: _total += 4, updateTotal(_total) [immediate]
    → Client: syncToServer("counter.count", 4) → postMessage({ command: 'counter.count', value: 4 })
    → Server: view.counter.count(4) → engine.counter.count(4), view.counter.total() → postMessage({ total: 4 })
    → Client: updateTotal(4) [confirmation]

User sets foo.bar:
    → Client: syncToServer("counter.foo.bar", "yum")
    → Server: view.counter.foo.bar("yum") → engine.counter.foo.bar = "yum", postMessage({ fooBar: "yum" })
    → Client: updateFooBar("yum") [confirmation]
```

Immediate client feedback; server runs business logic async. 
**Message protocol:** 
`command` maps to view path (e.g. `counter.count`). Handler uses `_lookup(command)` to delegate.

**Layers:**

| Layer | Role |
|-------|------|
| **Engine** | Root domain; accepts counter (Counter or CounterServer). |
| **EngineView** | Server view: owns Engine (with CounterServer), contains CounterView, builds HTML, handles postMessage. |
| **CounterView** | Server view sub-section: delegates to server domain (CounterServer); posts to webview. Persistence is in CounterServer. |
| **engine_client.js** | Client: uses **shared Counter** (bundled); DOM only (`updateDom`); `syncToServer(command, value)`. No duplicate business logic. |
| **HTML** | Input (amount), Reset button, `<span id="total">0</span>`, `<input id="fooBar">` for foo.bar. |

**Code:**

#### EngineView (engine_view.js)

EngineView is the container. It owns Engine and CounterView. Commands use paths like `counter.count`; lookup delegates to sub-sections.

```javascript
const vscode = require("vscode");
const path = require("path");
const { Engine } = require("../engine.js");
const { CounterServer } = require("../../counter/counter_server.js");
const { CounterView } = require("../../counter/view/counter_view.js");

class EngineView {
  constructor(panel, extensionUri) {
    this._panel = panel;
    this._extensionUri = extensionUri;
    const counterPath = path.join(extensionUri.fsPath, "counter.json");
    this._engine = new Engine(new CounterServer(counterPath));  // server domain (persistence)
    this.counter = new CounterView(this._panel, this._engine.counter);  // server view

    this._panel.webview.html = this._getHtml();
    this._panel.webview.onDidReceiveMessage((message) => {
      const { command, ...args } = message;
      const [obj, key] = this._lookup(command);
      const method = obj[key];
      if (typeof method === "function") method.apply(obj, Object.values(args));
    });
  }

  _lookup(pathStr) {
    const parts = pathStr.split(".");
    let target = this;
    for (let i = 0; i < parts.length - 1; i++) target = target[parts[i]];
    return [target, parts[parts.length - 1]];
  }

  _getHtml() {
    const webview = this._panel.webview;
    const bundleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, "counter", "view", "counter_bundle.js"));
    const counterClientUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, "counter", "view", "counter_client.js"));
    const engineClientUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, "engine", "view", "engine_client.js"));
    const nonce = getNonce();
    return `<!DOCTYPE html>
<html>...
  <script nonce="${nonce}" src="${bundleUri}"></script>
  <script nonce="${nonce}" src="${counterClientUri}"></script>
  <script nonce="${nonce}" src="${engineClientUri}"></script>
</body></html>`;
  }

  static createOrShow(extensionUri) { /* create panel, new EngineView(panel, extensionUri) */ }
}
```

#### CounterView (counter_view.js)

CounterView is a sub-section. It receives the counter from Engine and mirrors its API. Methods delegate to domain and post to webview.

```javascript
class CounterView {
  constructor(panel, counter) {
    this._panel = panel;     // for postMessage
    this._counter = counter;  // from Engine
    this.foo = {
      bar: (value) => {
        if (value !== undefined) this._counter.foo.bar = value;
        this._panel.webview.postMessage({ fooBar: this._counter.foo.bar });
      }
    };
  }

  count(amount) {
    this._counter.count(amount);
    this.total();
  }

  reset() {
    this._counter.reset();
    this.total();
  }

  total() {
    this._panel.webview.postMessage({ total: this._counter.total });
  }
}
```

#### engine_client.js

Orchestrator: acquires VS Code API, loads section clients.

```javascript
(function () {
  const vscode = acquireVsCodeApi();
  initCounterClient(vscode);
})();
```

#### counter_client.js

**Same interface as domain** — like CounterTty, CounterMarkdown. Each method runs domain op, then updates only the DOM element that changed.

```javascript
function initCounterClient(vscode) {
  const amountInput = document.getElementById("amount");
  const resetBtn = document.getElementById("resetBtn");
  const totalEl = document.getElementById("total");
  const fooBarInput = document.getElementById("fooBar");

  const counter = new Counter();

  // DOM adapter: same interface as domain; each method updates only the part that changed
  const domCounter = {
    count(amount) {
      counter.count(Number(amount) || 0);
      totalEl.textContent = String(counter.total);
    },
    reset() {
      counter.reset();
      totalEl.textContent = String(counter.total);
    },
    get total() { return counter.total; },
    get foo() {
      return {
        get bar() { return counter.foo.bar; },
        set bar(val) {
          counter.foo.bar = val;
          fooBarInput.value = val;
        }
      };
    },
    hydrate(data) {
      counter.hydrate(data);
      if (data.total !== undefined) totalEl.textContent = String(counter.total);
      if (data.fooBar !== undefined) fooBarInput.value = counter.foo.bar;
    }
  };

  function syncToServer(command, value) {
    vscode.postMessage(value !== undefined ? { command, value } : { command });
  }

  amountInput.addEventListener("change", () => {
    domCounter.count(amountInput.value);
    syncToServer("counter.count", Number(amountInput.value) || 0);
  });

  resetBtn.addEventListener("click", () => {
    domCounter.reset();
    syncToServer("counter.reset");
  });

  fooBarInput.addEventListener("change", () => {
    domCounter.foo.bar = fooBarInput.value;
    syncToServer("counter.foo.bar", domCounter.foo.bar);
  });

  window.addEventListener("message", (event) => {
    if ("total" in event.data || "fooBar" in event.data) domCounter.hydrate(event.data);
  });
  vscode.postMessage({ command: "counter.total" });
  vscode.postMessage({ command: "counter.foo.bar" });
}
```

**Note:** Same pattern as CounterTty: functions with same interface as domain; each updates only the DOM element that changes.

### File Layout

Each domain (engine, counter) has its own folder: domain objects, cli/adapters, view/ (client js + server view).

```
src/
├── engine/
│   ├── engine.js            # Domain; constructor(counter) for injection
│   ├── cli.js               # CLI entry (parse args, lookup on Engine, choose adapter)
│   └── view/
│       ├── engine_view.js   # Server view: owns Engine, builds HTML, postMessage
│       └── engine_client.js # Client orchestrator: loads counter view clients
│
└── counter/
    ├── counter.js           # Domain (Counter + Foo in same file; pure; no DOM, no Node)
    ├── counter_server.js    # Server domain: extends Counter; _load, _save
    ├── adapters/            # CLI output adapters
    │   ├── counter_tty.js
    │   ├── counter_markdown.js
    │   └── counter_json.js
    └── view/
        ├── counter_view.js   # Server view: delegates to ServerCounter; posts to webview
        ├── counter_client.js # Client: DOM adapter, syncToServer()
        └── counter_bundle.js  # Build output: Counter+Foo for webview (from counter.js)
```

### Domain Root Rule

**Classes that have their own files are roots of a domain** and have this scaffolding for themselves and their children. Child classes without their own files (e.g. Foo) live in the root file. See `.cursor/rules/domain-root-scaffolding.mdc`.

### Extension Registration

- Command: `agilebot.viewEngine` → `EngineView.createOrShow(extensionUri)`
- Add to `package.json` contributes.commands

---

## Summary

- **Domain:** Pure JS (Counter, Engine); no DOM, no VS Code, no Node APIs.
- **Server domain:** CounterServer extends Counter; adds persistence (_load, _save).
- **Server view:** EngineView, CounterView; postMessage; uses server domain.
- **Client:** Domain (bundled) + DOM adapter. Webview loads shared Counter; no duplicate logic.
- **CLI:** Same domain; output via TTY, JSON, or HTML adapters.

