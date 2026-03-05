/**
 * TTYCounter - wraps Counter with same interface; .total returns TTY-formatted string
 * counter_adapter = TTYCounter(counter)
 * formattedTotal = counter_adapter.total  // same interface as domain object
 */

function TTYCounter(counter) {
  this._counter = counter;
}

TTYCounter.prototype = {
  count(amount) {
    this._counter.count(amount);
  },

  get total() {
    return `Total: ${this._counter.total}\n`;
  },

  reset() {
    this._counter.reset();
  },

  /** Expose internals for debugging */
  get internals() {
    return { _total: this._counter._total };
  },
};

module.exports = { TTYCounter };
