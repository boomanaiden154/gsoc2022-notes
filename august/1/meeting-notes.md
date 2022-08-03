# Meeting Notes 8/1/2022

# Agenda

* Tensorflow versioning after tflite patch
* Model performance, not really a whole lot better than baseline,
but throwing more data at the model does seem to help (more
validation needed)

# Meeting Notes

* Encoding number of LRs in instruction
* opcode use/def mbfi
    * `float Freq = MBFI.getBlockFreqRelativeToEntryBlock(MI->getParent());`

* Dealing with opcode 0

* Potentially adding in a to be continued flag

* Looking at what instructions are encoded in which basic blocks

* Make sure that machine blocks (for machine block indices)/slot indices are stricly increasing
    * Debug asserts

* TF versioning after the TFLite patch
    * Moving to a specific hash that will automatically get bumped every often
    * Maybe this wasn't in reference to the TF versioning but just the TFLite package versioning?

* Might be useful as a baseline comparison to only pass in my instruction features to the model
and see what happens

* Work on gating different feature versions behind different LLVM flags rather than having a
bunch of different features branches
    * Could even potentially work on upstreaming feature extraction pieces assuming they
    are sufficiently gated behind flags.

# Post-meeting directions

* More testing
    * Testing with the modified model that ignores all zeroes
        * Could have actually been a huge problem in the existing implementation
    * Testing with just use/def instructions
* Additional features
    * Machine block frequency information
    * Mappings between instructions and basic blocks
    * To be continued flag when the number of instructions per live range exceeds 100
    * Number of LRs per instruction
* Development docker file
    * Make sure to have disclaimer that it isn't really officially supported.