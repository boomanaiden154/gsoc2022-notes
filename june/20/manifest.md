# Manifest - June 20th 2022

* model.tar.gz
    * This is another model, but this trained on a clang/LLVM corpus that was
    built using profile guided optimizations as described in an earlier
    article in this repository on a three stage clang/LLVM build with PGO.
    In contrast to the earlier model, this model was also warmstarted using
    the default heuristic for about 100,000 iterations (10x what the current
    value is set to in the main repository). Not really done for any reason
    in particular.
* output.json
    * Benchmarks results for this new model. Ran under the same process as the
    last benchmarks (other than being built on a clang/LLVM version about 1000
    commits ahead).