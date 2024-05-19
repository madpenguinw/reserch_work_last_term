const EventEmitter = require('events').EventEmitter;

class Processor extends EventEmitter {
  constructor(targetSum, dataSet) {
    super();
    this.targetSum = targetSum;
    this.dataSet = dataSet;
    this.totalSubsets = 0;
    this.matchCount = 0;
  }

  _generateSubsets(set, subset) {
    for(let i = 0; i < set.length; i++) {
      let newSubset = subset.concat(set[i]);
      this._generateSubsetsImmediate(set.slice(i + 1), newSubset);
      this._processSubset(newSubset);
    }
  }

  _generateSubsetsImmediate(set, subset) {
    this.runningCombine++;
    setImmediate(() => {
      this._generateSubsets(set, subset);
      if(--this.runningCombine === 0) {
        console.log("Subset count: " + this.matchCount);
        this.emit('end', this.matchCount);
      }
    });
  }

  _processSubset(subset) {
    const subsetSum = subset.reduce((prev, item) => (prev + item), 0);
    if(subsetSum == this.targetSum) {
       this.matchCount++;
    }
  }

  initiate() {
    this.runningCombine = 0;
    this._generateSubsetsImmediate(this.dataSet, []);
  }
}

module.exports = Processor;
