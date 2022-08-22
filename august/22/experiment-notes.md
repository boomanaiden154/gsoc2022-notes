# Experiments 8/22/22

* Experiment 35
    * Just instruction based features, but this time using a matrix multiplication
    based approach to calculate everything. Branch was `all-features-tooling-only-instructions`
    on the ml-compiler-opt side and `gated-instruction-features-only-instructions` on the
    LLVM side. Seemed to show that it was learning a little bit, but not very well. Loss
    graph looked pretty spiky. Used default ml-compiler-opt BC hyperparameters as of
    8/22/22.
* Experiment 36
    * Same experiment as number 35, but this time changing around the BC settings to
    match experiment 20.
* Experiment 37
    * Cutting batch size in half to 256, doubling learning rate to 0.0005.