#!/usr/bin/env node
/**
 * Counter CLI - wraps same business logic as panel
 * Usage: node cli.js count <amount> [count <amount> ...] [--format tty|markdown|json]
 *
 * Pattern: counter_adapter = <any>Counter(counter); formattedTotal = counter_adapter.total
 */

const { Counter } = require("./counter.js");
const { TTYCounter } = require("./adapters/tty_counter.js");
const { MarkdownCounter } = require("./adapters/markdown_counter.js");
const { JSONCounter } = require("./adapters/json_counter.js");

const args = process.argv.slice(2);
const formatIdx = args.indexOf("--format");
const format = formatIdx >= 0 ? args[formatIdx + 1] || "tty" : "tty";
const cmdArgs = formatIdx >= 0 ? args.slice(0, formatIdx) : args;

const counter = new Counter();
const counterAdapter =
  format === "markdown"
    ? new MarkdownCounter(counter)
    : format === "json"
      ? new JSONCounter(counter)
      : new TTYCounter(counter);

for (let i = 0; i < cmdArgs.length; i++) {
  if (cmdArgs[i] === "count" && cmdArgs[i + 1] != null) {
    counterAdapter.count(Number(cmdArgs[i + 1]));
    i++;
  }
}

process.stdout.write(counterAdapter.total);
