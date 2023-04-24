# Corpus Collection/GRANITE/llvm-exegesis meeting notes

### Topics for discussion

* Annotations for basic blocks within llvm-exegesis
  * Annotation for grabbing some page(s)
    * `#LLVM-EXEGESIS-PAGE-DEF`
  * Annotation for mapping page(s) into the execution environment of the BB
    * `#LLVM-EXEGESIS-PAGE-MAP`
  * Annotation for setting the address of the basic block
    * `LLVM-EXEGESIS-SNIPPET-ADDRESS`
    * Might be better to do this at just a stable address.
* RFCs/changes to llvm-exegesis
  * Thinking two phases, one for switching the execution of assembled snippets
  to being in a child process, the other for adding new memory annotations
  (probably split further into some subcomponents).
    * Switching to a separate process might be a good idea anyways.
    * LLVM SafeExecutionContext, potential expansion in the LLVM Support library
    for processes.
  * Draft RFCs, send them over, once we're reasonably happy with them, send
  them to the LLVM Discourse for proper discussion?
  * Might see some pushback from maintainers, but should just need to demonstrate
  that there is a pertinent need.
* Tool for extracting basic blocks from binaries
  * Shoved into the GRANITE repo?
  * Planning on putting it into GRANITE repo.
* Thoughts on collecting new and bigger corpora and how that might impact accuracey
and also thoughts on assembly mutation to further expand the corpus/potentially
augment the corpus in terms of data distribution in ways that current corpora don't
really do (all highly optimized `-O3` builds).
  * Can be a big difference between data sets. How clean the dataset is also
  matters quite a bit.
  * Need to be careful with assembly mutation because even some instructions
  can be change.
* Expected timeline for tool that is finding all memory access locations? Separate
tool under `/llvm/tools` if there's an interest in upstreaming?
  * Planning on putting it into the Gematria repository.
* Update on ReDOT/codelet extraction and replay stuff that I will hopefully get
working.
* Timeline for open sourcing of the training code, if not done already.
* Tool for integrating GRANITE into LLVM, I'm assuming something similar to
`llvm-mca`, but a separate binary?
  * I can work on infrastructure/pushing this through. We should be able to
  take major advantage of the existing infrastructure that we have for MLGO
  in terms of embedding Tensorflow models.
    * C++ library for GRANITE specific stuff already available.
  * Maybe `llvm-lcm` - LLVM learned cost model. If we architect it correctly,
  it should be trivial to add alternative learned (and maybe analytical) cost
  models as well.
* ReDOT
  * Look at memtrace, look at how the sanitizers work. Might be a useful
  design pattern to look at.
* Plans to update the GRANITE training code form Tensorflow v1 to Tensorflow
v2?
  * Runs with the latest version of Tensorflow, so should be fine. Uses
  the tensorflow compat stuff.
* What is BHive doing when looping basic blocks in terms of ensuring memory
consistency?
  * Not doing anything in regards to this.
  * They were just unrolling the loop and then looking at memory accesses
  so they didn't really have to care.
  * We have to care but we can take care of this in the memory instrumentation
  phase.