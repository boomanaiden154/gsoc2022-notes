# Meeting Notes 4/14/2023

* GSoC Stuff
* Exegesis patches
  * Any alternative to an asm test harness? Inline assembly probably still
  won't cover most of the things we need.
    * We should be able to use a JIT to generate all of the necessary code and then
    we can just shove that into an mmaped buffer (potentially at a specifc address)
  * Any updates on GRANITE tooling in relation to this?
    * Application to profile memory accesses of arbitrary BBs
    * No discussion/no updates. Will check back in two weeks when llvm-exegesis
    is hopefully farther along.
* Other updates for GRANITE?
  * Scripts for extraction of BBs using `SHT_LLVM_BB_ADDR_MAP`
    * Might not need this immediately as Ondrej is planning on pushing a tool
    for taking in hex values (i.e., also useful for MLGO stuff)
* Packaging GRANITE as a Python library for consumption in MLGO?
  * Ondrej will look into it, definitely a viable path.
* Upstream patches in `ml-compiler-opt` for alternative reward generation
for regalloc?
  * As soon as we get a signal, we want to move.
