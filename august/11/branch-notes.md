# Current branches for LLVM work/review

All the branches here are on [my LLVM Fork](https://github.com/boomanaiden154/llvm-project) on Github.

* `new-inputs-testing2`
    * This branch contains the base refactorings necessary to add additional
    features later on that are enabled only through a runtime switch.
    * Currently has a [review](https://reviews.llvm.org/D131209) open.
* `gated-instruction-features`
    * Adds in a command line flag for enabling development mode features
    and adds in instruction based features split into two different tensors,
    namely `instructions` and `instructions_mapping`.
    * Branched from the tip of `new-inputs-testing2`.
* `gated-machine-block-features`
    * Uses the same flag from `gated-instruction-features` and adds in
    machine basic block features per instruction.