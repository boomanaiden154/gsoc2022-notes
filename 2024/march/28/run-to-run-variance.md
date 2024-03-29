# Run to run variance numbers

Corona:
* 48 core, 96 threads
* Hyperthreading enabled
* Eight NUMA nodes

Run to run variance numbers for parallel benchmarking on Corona:

* ~0.8% run to run variance running a single threaded benchmark.
* ~1.2% run to run variance running one benchmark per core.
* ~1.2-1.3% run to run variance running one benchmark for every two cores.
* ~5% run to run variance running one benchmark per thread.

My sandy bridge workstation:
* 16 cores, 32 threads
* Hyperthreading disabled (only 16 cores visible)
* Two NUMA nodes

Numbers for my sandy bridge machine:

* 0.1% run to variance running a single threaded benchmark.
* 0.6% run to run variance running one benchmark per core.
* 0.5% run to run variance running one benchmark for every two cores.
* ~0.2% run to run variance running a single threaded benchmark pinned to a specific core.
* ~0.5% run to run variance running one benchmark per system isolated core.
