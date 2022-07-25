# Meeting Notes 7/24/22

### Agenda

* High memory usage due to large training examples for the regalloc case
    * Some weird memory behavior (protobuf struct should get deallocated, isn't)
    * Discuss design proposals. Loading data from disk after passing the temp
    file name from the data collection worker process
    * https://github.com/protocolbuffers/protobuf/issues/5737
    * Processing everything in one process might help with that issue.
* Regalloc instruction features
    * Currently no improvement. Model trains extremely well initially
    but after a little bit the loss values start to increase before
    they eventually seem to get somewhat consistent.
    * Planning on fiddling around with some hyperparameters (mainly
    the learning rate, but also the number of modules/batch size)
    * Also probably experimenting with some more feature engineering,
    eg more manipulation of instructions, maybe taking a more similar
    approach to what Ondrej is doing currently.
* Cloud compute
    * 128 core n2d quota request got approved so we can create much
    larger instances now.
    * Probably scale the current instance? Unless we make some memory
    improvements we'll probably need at least 8gb/core.
* TFLite patch?
* Regalloc encoding network patch
    * Working on my current tests and should be compatible with the current
    model while allowing for multiple inputs to go to the same layer.
    * Interested in upstreaming this (to ml-compiler-opt)?