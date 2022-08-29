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

### Meeting Notes

* Clang should be throwing an error when it can't find PGO data.
  * Write a patch, ping Mircea on it.
* SlotIndex thing
  * Open an discussion on discourse
  * Don't frame it as a RFC (might just be misunderstanding the point of the code)
* Green light on testing out Chromium patch using their perfbots
  * Still some weird behavior with the tensorflow tree on the chromium side (https://chromium-review.googlesource.com/c/chromium/src/+/3852308)
* Discuss current model implementation with Yundi
* Test Instructions + MBB data on a corpus with PGO that's working correctly.
  * Full RL training (to when the curve doesn't go down anymore)
  * Validation with benchmarking.
* Try and finish up LLVM patch for instruction based features (figuring out weird behavior).