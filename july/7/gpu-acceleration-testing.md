# MLGO GPU Acceleration Testing

Currently, using a GPU to train the MLGO models is not reccomended due to
the high performance burden that copying all the necessary data between
the CPU and GPU entails that actually results in a performance reduction
over just training on the CPU. Most of the time is said to be taken up
by data collection (at least for the smaller inliner model). However, with
the regalloc model and adding many additional features to the regalloc model
(maybe even doubling the size of the model), I think a new look at GPU
acceleration should be taken. Here are some of my results from initial
testing. The specs for the test system:
* Tensorflow 2.7.0, libtensorflow 1.15.0
* Intel Xeon E5-2670 (x2)
* NVIDIA GTX 980

Looking at the currently existing regalloc model, there doesn't seem to be
any performance benefit to moving computation to the GPU (although that
might shift depending upon the CPU/GPU balance in the system and whether
or not faster data copy is available eg through PCIE4.0).

### Current Regalloc Model Results

The current regalloc model trained on the CPU ran the first four training
iterations (200 iterations of the model each) in these times (times in
the parantheses are the times spent in data collection performing compiles),
times are in seconds:
1. 72 (15)
2. 43 (13)
3. 45 (14)
4. 45 (14)

Training this same model on the GPU resulted in performance degradation with
my setup:
1. 54 (15)
2. 52 (12)
3. 57 (15)
4. 56 (15)

### New Regalloc Model Results

These results were obtained by running the first couple training iterations
on a model consisting of the base regalloc features in addition to
instruction features (an extra 16 dimensions per each register, so adding
in total a new 33x16 matrix to the input, along with preprocessing the
instruction matrix extracted on the LLVM side). For the CPU:
1. 173 (19)
2. 146 (16)
3. 145 (16)

And for the GPU:
1. 158 (17)
2. 125 (17)
3. 126 (25)
4. 129 (28)
5. 120 (18)

The GPU on average based on this testing is a decent amount faster than
the CPU (although not by a whole lot). The GPU usage spikes and drops
significantly after the data collection phase, somewhat suggesting a lot
of data being copied back and forth so that some operations can be 
performed on the CPU, but actual profiling data is needed to evaluate
whether or not this is the case. If that copying is actually the case
and isn't embedded too far in the `tf_agents` stuff, then just writing
custom Tensorflow ops where necessary might be able to massively
increase performance which would be extremely helpful in this instance
given the significantly reduced ratio between the data collection time
and the training time compared to the original model.