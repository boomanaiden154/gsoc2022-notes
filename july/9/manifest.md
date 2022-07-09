# Manifest For 7/9/2022

* model.tar.gz
    * This model was trained on a Chromium PGO corpus compiled without
    CFI and without ThinLTO, but otherwise with the official build
    settings. Debug symbols were explicitly disabled with the
    `is_debug` flag set to false and the `symbol_level` flag set to 0
    and the output directory being set to `./out/Release`. This model
    structure is just the base one specified in the ml-compiler-opt
    repository currently with the standard number of training iterations
    for the behavior cloning warmstart and the actual local training
    (10,000 and 600,000 respectively).