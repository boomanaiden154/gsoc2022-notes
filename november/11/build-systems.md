# LLVM Build System Thoughts

Just some random thoughts/TODOs in regards to the LLVM Build System

* Documentation on the advanced build configurations LLVM doc page for building
with BOLT. I can probably work on a patch soon.
    * Patches are now up. Three patches, one with some minor fixes, another
    adding in documentation on (Thin)LTO PGO builds, and another adding in
    information on using the BOLT caches.
* Seeing whether or not the PGO builds (that the BOLT builds directly depend on)
actually run the whole test suite and recompile LLVM or just run a very small
amount of stuff. I only saw it run a couple tests with my configuration today.
    * Just run a very small amount of stuff, particularly the perf training
    data setup as a bunch of files run with llvm-lit somewhere in the LLVM tree.
    Petr Hosek mentioned on a Phabricator comment he was writing a script to
    extract data for perf training from ninja based build systems but I don't
    think anything has come out of that yet.
* Looking at actual benchmarking numbers to see performance personally,
probably just looking at build times of LLVM itself with a specific configuration.
* Maybe also look at quantifying data collection for MLGO corpus collection
and see how much that improves with a more optimized LLVM build.
* BOLT builds currently aren't working with `LLVM_ENABLE_LLD` if using `gcc` without
`lld` installed. Maybe some error in the PGO builds? It fails in the initial
configure step when it should be able to just build `lld` as part of the bootstrap
build. Might just be some weird configuration thing on my side.
    * Makes perfect sense since `LLVM_ENABLE_LLD` would apply to the initial
    bootstrap build which uses the system compiler.