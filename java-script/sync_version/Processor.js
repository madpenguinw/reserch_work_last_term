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
     this._generateSubsets(set.slice(i + 1), newSubset);
     this._processSubset(newSubset);
   }
 }

 _processSubset(subset) {
    const subsetSum = subset.reduce((prev, item) => (prev + item), 0);
    if(subsetSum == this.targetSum) {
       this.matchCount++;
       this.emit('match', subset);
    }
 }

 initiate() {
   this._generateSubsets(this.dataSet, []);
   console.log("Subset count: " + this.matchCount);
   this.emit('end', this.matchCount);
 }
}

module.exports = Processor;
