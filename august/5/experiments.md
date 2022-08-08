# Experiments
* Experiment 20 (done, https://drive.google.com/file/d/1kmkLMFgR_3rOOU-MZxvL4mDqtRIAGSdb/view?usp=sharing)
    * Behavioral cloning training of a model that only has instruction based
    features (`regalloc-only-instruction-features` branch on both my fork
    of ml-compiler-opt and LLVM). Using the same training protocol as experiment
    9.2 from the file in the July 28th folder. Trained for 20k iterations as was
    the protocol in that specific experiment.
    * Looking at the loss curves on tensorboard, they don't look particularly great.
    There is definitely some improvement from the baseline and the model learns a little
    bit, but the curve flattens off pretty quickly. Maybe some problems with batch size
    or something as if we're just looking at the min loss value over time, that does go
    down. Potentially increasing the network size might help too as we're just looking
    at the raw features now rather than nicely extracted features that can easily be
    piped into a decision making process.
* Experiment 21 (done, https://drive.google.com/file/d/1LacM__q1I0Hd7OkKp2LFr-xxlvY3_k_E/view?usp=sharing)
    * Same protocol as above in terms of hyperparameters and model architecture and
    features, but with the number of iterations for each BC training run set to
    100000 as it seemed like the models in experiment 20 weren't really getting
    enough time to train and had some extra room to improve. This decision was not
    made by looking at the graphs though.
* Experiment 22 (done, https://drive.google.com/file/d/1XC47KTfo22Jkb2JmreTXu2PN2ahizA9j/view?usp=sharing)
    * Warm start, same protocol as experiment 20, but increasing the network size
    by changing the fully connected layer configuration from (80,40) to (120,60).
* Experiment 23 (done, https://drive.google.com/file/d/1sIy34av769kprirY_qwvhxDafSdI2gVw/view?usp=sharing)
    * Warm start, only a single instance was performed though. Same protocol as
    experiment 22, except setting the fully connected layer config to (120,60,60).
    * Maybe learned a little bit? Loss graph was terrible. Probably needs more data
    thrown at it.
* Experiment 24 (scrapped)
    * Tried changing the calulation from summing the instruction embeddings per LR to 
    calculating an average of these embeddings.
    * Network ended up not training at all. Not a good signal. Probably points to a bad
    implementation.
* Experiment 25 (done, https://drive.google.com/file/d/1DpTH9fH-6618uVZYGICa_LZkN3EvAxa7/view?usp=sharing)
    * Local training of protocol in experiment 22.
    * Seemed to go fairly well. Was able to almost match the performance of the default
    heuristic in about 20k iterations (to within 1%).
* Experiment 26 (planned)
    * Same protocl as experiment 23, but this time only looking at use-def instructions
    instead of all the instructions that the LR covers.