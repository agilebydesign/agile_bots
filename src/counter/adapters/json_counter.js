/**
 * JSONCounter - wraps Counter with same interface; .total returns JSON-formatted string
 * counter_adapter = JSONCounter(counter)
 * formattedTotal = counter_adapter.total  // same interface as domain object
 */

function JSONCounter(counter) {
  this._counter = counter;
}

JSONCounter.prototype = {
  count(amount) {
    this._counter.count(amount);
  },

  get total() {
    return JSON.stringify({ total: this._counter.total });
  },

  reset() {
    this._counter.reset();
  },

  /** Expose internals for debugging */
  get internals() {
    return { _total: this._counter._total };
  },
};

module.exports = { JSONCounter };
