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
* Experiment 21 (in progress)
    * Same protocol as above in terms of hyperparameters and model architecture and
    features, but with the number of iterations for each BC training run set to
    100000 as it seemed like the models in experiment 20 weren't really getting
    enough time to train and had some extra room to improve. This decision was not
    made by looking at the graphs though.