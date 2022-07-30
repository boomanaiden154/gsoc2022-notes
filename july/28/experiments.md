# Experiments 7/28/2022

* Experiment 1
    * Behavioral cloning training of regalloc model on chromium corpus using all default
    parameters and current configs/code of both ml-compiler-opt and LLVM as of today. Each
    time a new BC model was trained, a new 20% default trace was generated to try and
    eliminate variation between different experiments and leave it to within the replicates.
* Experiment 2
    * Behavioral cloning training of regalloc model on chromium corpus using new instruction
    features with two tensors passed to the instruction processing model. Same default trace
    strategy as above.
* Experiment 3
    * Same as above, except changed the batch size in `compiler_opt/rl/regalloc/gin_configs/behavioral...`
    from 64 to 256.
* Experiment 4
    * Same as above, but halving the learning rate on the adam optimizer from `0.001` to `0.0005`.
* Experiment 5
    * Warmstart using the same protocol as experiment 4, 20000 iterations with the default settings
    as of right now for the regalloc ppo agent (`num_modules=512`, learning rate is the same)
* Experiment 6
    * Same protocol as above, except using 2048 modules per policy iteration instead of 512, halving
    the Adam Optimizer learning rate from 0.0003 to 0.00015, and also quadrupling the batch size from
    256 to 1024. Still trained for 20000 iterations. Currently no network architecture changes. Adjusted
    the max timeout time for the data collection phase from 30 to 90 seconds to compensate for the increased
    number of modules being used per policy iteration, but the timeout shouldn't have any effect on the
    actual data outputs.