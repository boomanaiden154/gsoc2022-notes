# Experiments 7/28/2022

* Experiment 1 (done, https://drive.google.com/file/d/1qPsek5OE69wr0r6l1YX72FN4dgwUo7av/view?usp=sharing)
    * Behavioral cloning training of regalloc model on chromium corpus using all default
    parameters and current configs/code of both ml-compiler-opt and LLVM as of today. Each
    time a new BC model was trained, a new 20% default trace was generated to try and
    eliminate variation between different experiments and leave it to within the replicates.
* Experiment 2 (done, https://drive.google.com/file/d/10xdckG4f3RmQqatirdOTnpz1oYXZoA1h/view?usp=sharing)
    * Behavioral cloning training of regalloc model on chromium corpus using new instruction
    features with two tensors passed to the instruction processing model. Same default trace
    strategy as above.
* Experiment 3 (done, https://drive.google.com/file/d/1Strx7dkUKRitliJdPCyHglfFy2_rRGW4/view?usp=sharing)
    * Same as above, except changed the batch size in `compiler_opt/rl/regalloc/gin_configs/behavioral...`
    from 64 to 256.
* Experiment 4 (done, https://drive.google.com/file/d/1qkD6kwALgzBIZmGVc6SJiDeEv4vGTixo/view?usp=sharing)
    * Same as above, but halving the learning rate on the adam optimizer from `0.001` to `0.0005`.
* Experiment 5 (done, https://drive.google.com/file/d/1g_xQoGFdkRMmK6zdMVqb705W5YSUPYj0/view?usp=sharing)
    * Warmstart using the same protocol as experiment 4, 20000 iterations with the default settings
    as of right now for the regalloc ppo agent (`num_modules=512`, learning rate is the same)
* Experiment 6 (done, https://drive.google.com/file/d/1M0nck4bcwQ6U4BMnSGo6dHL2tq4s-PFY/view?usp=sharing)
    * Same protocol as above, except using 2048 modules per policy iteration instead of 512, halving
    the Adam Optimizer learning rate from 0.0003 to 0.00015, and also quadrupling the batch size from
    256 to 1024. Still trained for 20000 iterations. Currently no network architecture changes. Adjusted
    the max timeout time for the data collection phase from 30 to 90 seconds to compensate for the increased
    number of modules being used per policy iteration, but the timeout shouldn't have any effect on the
    actual data outputs. Also changed the `num_workers` CLI flag from undefined (one worker per system thread
    to 32 on a 96 core system) to avoid running out of processes.
* Experiment 7 (in progress)
    * Fully default training strategy from the current ml-compiler-opt repository/LLVM repository, but
    instead of running the full 600k iterations, this experiment is only testing up to 20k iterations.
    Performed in triplicate like all other experiments so far.