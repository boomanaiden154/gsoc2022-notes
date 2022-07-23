# Memory Leak in worker processes

Currently there seems to be a large memory leak in the worker processes
created by `local_worker_manager.py`. This results in each of the worker
processes taking up gigabytes of memory when all they're really doing
is running the compilations and passing all of the data back to the main
thread so that it can be used for training. This becomes a large problem
as if you're running with the number of worker processes equal to the number
of cores that you have (the default), you can pretty quickly run into OOM
errors even with 4GB of RAM per core. 

### Reproduction

Reproducing is fairly easy. Just start doing a local training using the
`train_locally.py` script and monitor the resident memory usage of the
worker processes that get spawned. When monitoring everything in `htop`,
it can be helpful to use the shift + h keyboard combo to collapse all threads
into their respective processes as each worker process has three threads.
Setting `num_workers` to one using the CLI option will cause that one
worker to eat up more memory a lot more quickly more easily illustrating
the problem.

### Source

After much investigation, it seems like the memory that ends up leaking is
getting allocated in `compilation_runner.py` in the `collect_data(...)` function.
Commenting all of the actual code out and returning a `CompilationResult` object
with all of the fields set equal to `None` results in no net memory increase while
leaving the code in but only returning a `CompilationResult` object set to none
still results in the same massive memory increase.

### Resolution?

More updates still to come.
