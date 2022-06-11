# Manifest (6/10/2022)

* `results-base.json`
  * The output from running the LLVM testsuite benchmarks using the
  default register allocator with optimizations (`-O3`) enabled. Also
  run using PGO Clang so that we get a better view of what the compile
  times are like in a release mode setup.
* `results-current-regalloc.json`
  * The output from the LLVM testsuite from using the default
  register allocator at higher optimization levels (greedy) with
  the ML eviction advisor using the current best model that is
  publicly available.
* `model.tar`
  * Contains the model that works with the new instruction features. As
  of writing right now, it still needs to be tested.