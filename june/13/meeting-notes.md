# Meeting Notes 6/13/2020
### Notes for future directions for benchmarking:
* Build LLVM test suite with perf counters enabled
* Set CPU affinity (eg bind to a specific core)
* Run single threaded (doesn't matter if looking at instruction counts specifically, but for timing performance, definitely matters)
* Counting number of instructions executed (especially loads and stores specifically)
* Looking at instructions executed
### Future Directions
* Get accurate benchmarks on models using perf counters/instruction based metrics
* Work on a new model embedding use/def instructions for all live ranges
* Benchmark said model
* If that is complete, work on another model that encodes all instructions contained within the live range