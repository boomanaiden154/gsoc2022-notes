# Cost Model Evalution

Currently it seems like we might be experiencing some issues with the cost model
used in the MLRegalloc work. This document contains some processes and notes on
how I'm going to evaluate the cost model against some real world benchmarks to
see how well it works. This will focus a lot specifically on the impact of
register allocation because that's what we're focusing on.

### Generating Different Register Allocations

In order to benchmark how well a cost model evaluates register allocation, we
need to be able to generate the same benchmark with a bunch of different register
allocations, see how the cost model evaluates each benchmark, and then see how
those benchmarks compare when run on real hardware. I'm planning on achieving this
by compiling the same individual benchmarks with the fast allocator, the greedy
allocator, and then against a couple of different ML models (maybe up to 3) so
that we should actually be able to sort them appropriately.

### PGO

Our current cost model does use PGO data in order to provide an answer, so having
accurate PGO data is essential. This means that for each of the benchmarks that
we're looking at, we need to run the benchmark in an instrumentation run, gather
the profdata, and then recompile the benchmark so that the current cost model
will get some accurate results.

### Getting info from the current cost model

The current plan is to have some debug print lines in the regalloc scoring pass
that operates as a machine function, with it printing the score (well, all the
individual components) of the score, and then the number of times the specific
function it is currently operating over get called (should be included in the
PGO data) so that we can correlate that with the overall runtime of the
benchmark.