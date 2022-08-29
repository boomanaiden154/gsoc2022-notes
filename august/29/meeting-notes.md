# Meeting Notes 8/29/22

### Agenda

* Got the chromium corpus PGO stuff working. If the path is incorrect, it
  seems like clang will just ignore it. Rewriting the path does show some
  difference in terms of model performance.
* Tested out MBB frequencies with the new model for training and it didn't
  seem to have any large impact (only really testing with the BC cloning
  though). Still need to test out use/def info. Think I might also try
  using an ASMWriter to significantly reduce the number of different
  instructions that we're working with.
* Seem to have found a bug in the register allocator with how instruction
  distance is calculated between slot indexes. Fixing the bug does induce
  a functional change in the register allocator (function is used in adjusting
  the weighting of different LRs). Benchmarking shows maybe a slight performance
  improvement to maybe no difference (0.4% improvement in loads in the llvm-test-suite),
  and a 0.02% improvement in loads on the chromium benchmarks). Currently breaks
  about 400 codegen tests.
* Maybe look at using the register allocator in Chromium?