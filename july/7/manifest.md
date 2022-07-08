# Manifest 7/7/2022

* model.tar.gz
    * This model was trained based on the new instruction features indices
    model (`regalloc-all-instructions-index-matrix` branch in my LLVM
    fork on github and `all-features-tooling-instruction-indices` on my
    ml-compiler-opt fork). This model was trained on a Chromium corpus
    that was generated with some fairly standard settings listed in
    the chromium-for-corpus documentation file in this repo (although
    I hadn't added in `is_debug=false` and `symbol_level=0` while
    training this corpus and used the `./out/default` directory for
    building). Trained for the standard 600,000 iterations
    as outlined in the gin configs in ml-compiler-opt. Behavior cloning
    warmstart was used with the BC warmstart being trained for 100,000
    iterations. 