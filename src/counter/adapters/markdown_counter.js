/**
 * MarkdownCounter - wraps Counter with same interface; .total returns markdown-formatted string
 * counter_adapter = MarkdownCounter(counter)
 * formattedTotal = counter_adapter.total  // same interface as domain object
 */

function MarkdownCounter(counter) {
  this._counter = counter;
}

MarkdownCounter.prototype = {
  count(amount) {
    this._counter.count(amount);
  },

  get total() {
    return `## Counter\n\n**Total:** ${this._counter.total}\n`;
  },

  reset() {
    this._counter.reset();
  },

  /** Expose internals for debugging */
  get internals() {
    return { _total: this._counter._total };
  },
};

module.exports = { MarkdownCounter };
