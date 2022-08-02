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
* Experiment 7 (done, https://drive.google.com/file/d/1WmNaEY9pujl8KP2kTlu8J-95rclHPQCq/view?usp=sharing)
    * Fully default training strategy from the current ml-compiler-opt repository/LLVM repository, but
    instead of running the full 600k iterations, this experiment is only testing up to 20k iterations.
    Performed in triplicate like all other experiments so far.
    * Maybe a slight decrease in performance compared to the models created in experiment 6, but due to
    the fact that the local training process in experiment 6 was also gathering considerably more data,
    it is hard to tell if the changes are occurring because of the changed training hyperparameters or
    because of the new features.
    * The models from this experiment did outperform the models from experiment 5, but again we sort of
    have limited data here on what is actually helping. It could just be (and probably is) that the
    model with the instruction features takes considerably more data to train.
* Experiment 8 (done, https://drive.google.com/file/d/1VQN2MTJLuw3VQcciASGBu7PpP3269qfX/view?usp=sharing)
    * Baseline comparison for experiment 6. Using the same training hyperparameters as that experiment,
    but instead of using the new model with instruction based features, we're using the existing model.
    Behavioral cloning training hyperparameters are also set to their defaults.
    * Comparing the results from experiment 6 with the results from this experiment shows that a lot of
    the variation in terms of performance could probably be explained by the changed training
    hyperparameters. Doesn't mean there necessarily isn't a performance improvement though as these
    tests are limited to 20k iterations and the differences could become larger as time goes on, or
    there could just not be enough processing in terms of layers/nodes to go through all the new
    data.
* Experiment 9 (partially completed, https://drive.google.com/file/d/13-7P7Cqi8BL_6SMQZevYG32gx3o5C54Q/view?usp=sharing)
    * Training a model with instruction based features, but swapping the default `tf.reduce_sum` to
    combine all the instructions for each individual register to `tf.reduce_mean`. Using the same
    training hyperparameters as experiment 6.
    * Current problems with this: need to process the input mapping array for each individual opcode
    so that we exclude a lot of the zeroes at the end that will otherwise probably skew the results
    quite a bit.
    * Used quite a poor implementation of calculating the mean that didn't really resolve the problem
    listed above. Also had problems with loss values after so many training iterations (usually around
    10k) going to NaN, which meant that the model didn't improve any further. Only two replicates
    completed due to the machine shutting down, but there were definitely issues with this approach
    and I don't need any more replicates to confirm that.
* Experiment 9.1 (planned)
    * Behavioral cloning baseline with the current BC settings settled on in experiment 4. Using a mean of
    the instruction embeddings rather than a sum of the embeddings, but this a slightly less naive approach
    than compared to experiment 9.
    * Using a significantly less naive version for calculating the mean that rectifies the problem outlined
    in experiment 9. Might have some interesting issues calculating gradients though with how the zeroes used
    for padding are processed though.
* Experiment 9.2 (planned)
    * Behvaioral cloning with the same protocol as experiment 9.1 except doubling the batch size from 256 to 512,
    halving the learning rate from 0.0005 to 0.00025, and doubling the number of training iterations (moving from
    10k to 20k).
* Experiment 10 (potentially planned)
    * Current regalloc instructions model (with `tf.reduce_sum` or `tf.reduce_mean` depending upon the
    results of experiment 9) but with an increased number of nodes in the hidden layer. Perhaps experimenting
    with what I've done in the past setting the fc layers in the encoding network to 120 units in the first
    layer and 60 in the second layer.
* Experiment 11 (potentially planned)
    * Current model with same training hyperparameters as experiment 10 and the same settings in terms of
    network architecture (minus the instruction stuff) to serve as a control.
* Experiment 12 (potentially planned)
    * LSTM layer operating over the instruction embeddings to get away from a really naive implementation
    like `tf.reduce_*`.
* Experiment 13 (potentially planned)
    * Same setup as experiment 10, but instead of just increasing the numebr of hidden nodes in the existing
    two layers, adding another hidden layer. Perhaps keeping the same number of hidden nodes in the first and
    third layers as the current upstream layer configs and then mirroring the second layer and the third layer
    in terms of number of hidden nodes.
* Experiment 14 (potentially planned)
    * Baseline control for experiment 13
* Experiment 15 (potentially planned)
    * Try training for more iterations per policy iteration (eg 400 instead of 200) with instruction features
* Experiment 16 (potentially planned)
    * Baseline control for experiment 15