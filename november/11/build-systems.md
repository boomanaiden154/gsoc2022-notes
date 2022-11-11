# LLVM Build System Thoughts

Just some random thoughts/TODOs in regards to the LLVM Build System

* Documentation on the advanced build configurations LLVM doc page for building
with BOLT. I can probably work on a patch soon.
* Seeing whether or not the PGO builds (that the BOLT builds directly depend on)
actually run the whole test suite and recompile LLVM or just run a very small
amount of stuff. I only saw it run a couple tests with my configuration today.
* Looking at actual benchmarking numbers to see performance personally,
probably just looking at build times of LLVM itself with a specific configuration.
* Maybe also look at quantifying data collection for MLGO corpus collection
and see how much that improves with a more optimized LLVM build.
* BOLT builds currently aren't working with `LLVM_ENABLE_LLD` if using `gcc` without
`lld` installed. Maybe some error in the PGO builds? It fails in the initial
configure step when it should be able to just build `lld` as part of the bootstrap
build. Might just be some weird configuration thing on my side.