# Meeting Notes 6/7/2022

* Discussion on what the focus is this week (probably model training on all features tooling branch)
* Upstream chromium stuff? Documentation in `ml-compiler-opt`?
* Future directions on features, what else do we want to extract, other ways of feeding things into the network

# Post-meeting notes 

* Get a model trained/keep working on the new feature set
* Upstream the chromium patch, work on documentation for ml-compiler-opt related to chromium corpus/regalloc stuff
* Think about feature engineering/future directions
* Potential future direction in regards to large amount of disk space for embedded IR in object files is to
just run a compressor on it. Maybe some future work to be done in this area?
* Original implementation of embedded IR was by Apple for the appstore so they could recompile for different
targets on their end.
* Meetings for next week cancelled, notify on slack if something comes up. Meeting up on the Google campus
on July 11th for lunch/discussion related to the project.
* Google benchmark isn't used within chromium, but there are plenty of benchmarks present. Running them with
the linux perf tools should be a pretty reliable indicator of performance improvements, but this does need to
be done with some caution as the linux perf tools track the entire process rather than just the benchmark code
so there is a higher chance for noise to get in. Some work needs to be done on making sure that the run to run
variability is within tolerance.

# Work for this week 

* Model training with all instruction embeddings
* Upstream the chromium patch and write a regalloc demo for ml-compiler-opt using the upstreamed patch
* Think about future features/experiments to run.
* Get chromium benchmarking pipeline set up/benchmark created model.
* Integration tests through the gsoc2022 demos?
* Get sparse tensors working on the `instructions_and_mapping` feature.