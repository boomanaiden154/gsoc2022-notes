# Plans

Sort of just a todo list, hoping to have most of this stuff finished up before
Tuesday June 20th.

* Dataset construction
  * Get the following building:
    * [ ] Python (Only v3 since v2 is now sunsetted)
    * [ ] Firefox
    * [ ] Chrome
    * [ ] Rust Crates
* Gematria tooling
  * [x] Code formatting/clangd/CI ([PR](https://github.com/google/gematria/pull/12)
  * [ ] Make sure BB executable extraction tooling is in Gematria
    * Extension for object files (if necessary)
  * [ ] Script to combine extractions from multiple projects
  * [ ] Add script to automatically get throughput from llvm-exegesis
* LLVM stuff
  * [ ] Validation of llvm-exegesis against uica-eval/BHive
    * Maybe setup Anica to work on llvm-exegesis and compare against nanobench?
    * Comparison against nanobench in addition this?
  * [ ] Multiple performance counters in llvm-exegesis
  * Couple other minor fixups in llvm-exegesis:
    * [ ] Land docs patch
    * [ ] Benchmark code mapping annotation patch
    * [ ] Memory mapping to register annotation patch
  * Finish getting approval for memory annotation stack:
    * [x] [Patch 1](https://reviews.llvm.org/D151019)
    * [x] [Patch 2](https://reviews.llvm.org/D151020)
    * [x] [Patch 3](https://reviews.llvm.org/D151021)
    * [x] [Patch 4](https://reviews.llvm.org/D151022)
    * [x] [Patch 5](https://reviews.llvm.org/D151023)
    * [x] [Patch 6](https://reviews.llvm.org/D151024)
    * [ ] [Patch 7](https://reviews.llvm.org/D151025)
  * [ ] Land memory annotation stack
  * [ ] Test out Petr's patch
* ml-compiler-opt
  * [ ] Finish up integration test PR
    * [x] Get Fuchsia toolchain building again [gist](https://gist.github.com/boomanaiden154/74edd4a321f76aaf64355c5153886113)
    * [ ] Get Fuchsia building
  * [ ] Finish up BC hyperparameter tuning PR
    * [ ] Still need to add some infrastructure to do keras-tuner nightly versions
  * [ ] Test GRANITE with mlregalloc
  * [x] ml-compiler-opt as a python package
    * [ ] compiler\_opt package on pypi [PR](https://github.com/google/ml-compiler-opt/pull/266)
* Custom LLVM toolchain
  * [ ] Maybe experiment with building against LLVM libc?
  * [ ] Evaluate what is missing when building LLVM tools/clang against libc in
  full build mode?
  * [ ] Experiment with building static binaries?

