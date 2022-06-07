# Meeting Notes 6/6/2022
### Premeeting stuff/agenda
- Generating register allocation training corpus
  - ThinTLO nuance, compiling with ThinLTO but still
  getting out object files that can be used for
  extracting MIR (?). Need to discuss the exact correct
  flags needed to get the compile working. Maybe
  also something to do with extracting ldd flags?
- NN architecture
  - Perhaps slightly increase the size of the first
  two layers to better account for more incoming data?
  - Probably run some experiments. Maybe discuss 
  provisioning a machine to run said experiments 
  while leaving my current hardware able to do
  other things?
- Iterating over all instructions contained within
a live range.
  - Building off of previous discussion on Github PR.
  Still need to read some LLVM API documentation. discuss
  approach for actually doing this.
- Future Directions
  - Encoding use/def instructions for all candidate
  registers.
  - Encoding all instructions used within a live range.
  ### During/Post meeting notes
- When running `extract_ir.py`, just use `-fembed-bitcode`, no ThinLTO.
Everything should be able to work without using a ThinLTO corpus.
- LLVM test suite for benchmarking (https://llvm.org/docs/TestSuiteGuide.html)
Specifcally run the microbenchmarks that use google test.
- Iterating through all instructions for a live range should
be as simple as iterating through all the segments in
a specific live range, iterating through all the slot
indices within that segment, and then map the slot
indices to instructions using the `LiveIntervals` class
instance that gets passed to the register allocator/ML
stuff.