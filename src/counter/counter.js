/**
 * Counter - Pure business logic (no DOM, no VS Code, no CLI)
 * Shared by CLI and panel.
 */

class Counter {
  constructor() {
    this._total = 0;
  }

  count(amount) {
    this._total += Number(amount) || 0;
  }

  get total() {
    return this._total;
  }

  reset() {
    this._total = 0;
  }
}

module.exports = { Counter };
