# Plans

Sort of just a todo list, hoping to have most of this stuff finished up before
Tuesday June 20th.

* Dataset construction
  * Python (Only v3 since v2 is now sunsetted)
  * Firefox
  * Chrome
  * Rust Crates
* Gematria tooling
  * Code formatting/clangd/CI
  * Make sure BB executable extraction tooling is in Gematria
    * Extension for object files (if necessary)
  * Script to combine extractions from multiple projects
  * Get everything working with the datasets, probably upstream build scripts
  * Add script to automatically get throughput from llvm-exegesis
* LLVM stuff
  * Validation of llvm-exegesis against uica-eval/BHive
  * Multiple performance counters in llvm-exegesis
  * Couple other minor fixups in llvm-exegesis
  * Finish landing memory annotation stack
* ml-compiler-opt
  * Finish up integration test PR
  * Finish up BC hyperparameter tuning PR
    * Still need to add some infrastructure to do keras-tuner nightly versions
  * Test GRANITE with mlregalloc

