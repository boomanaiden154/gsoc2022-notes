# Chromium Benchmarking

Chromium has two different types of benchmarks (neither of which use
the google benchmark library). They are the performance tests run by the
custom Telemetry engine (which don't appear to be able to run in a headless
state) and the perf tests that exists alongside the unit tests within Chromium.
These unit tests do test performance, but they also seem to test a lot of other
things (`net_perftests` for example has a description of testing disk cache
and cookie storage, both of which will probably be IO bound). There are also
only three of these test suites. More info is needed on run to run variability
and what specific tests they run. However, the `base_perftests` at least seem
to do something somewhat similar to google benchmark:
```
*RESULT MemoryAllocation.throughput: MemoryAllocation.SingleBucketWithFree_PartitionAllocWithThreadCache_4_total= 135820496 runs/s
*RESULT MemoryAllocation.time_per_allocation: MemoryAllocation.SingleBucketWithFree_PartitionAllocWithThreadCache_4_total= 7 ns
*RESULT MemoryAllocation.throughput: MemoryAllocation.SingleBucketWithFree_PartitionAllocWithThreadCache_4_worst= 33891628 runs/s
*RESULT MemoryAllocation.time_per_allocation: MemoryAllocation.SingleBucketWithFree_PartitionAllocWithThreadCache_4_worst= 29 ns
```
It does report some other metrics like runs per second. May be
worth at least evaluating how difficult it would be to tie in telemtry directly
rather than having to go through `perfstat` which might suffer from noise since
it isn't only measuring the data from the tests.

### List of currently identified performance tests

This were listed from the `GTEST_CONVERSION_WHITELIST` list in
`testing/scripts/run_performance_tests.py` in the chromium source tree:
```
angle_perftests
base_perftests
blink_heap_perftests
blink_platform_perftests
cc_perftests
components_perftests
command_buffer_perftests
dawn_perf_tests
gpu_perftests
load_library_perf_tests
net_perftests
browser_tests
services_perftests
standalone_angle_perftests
sync_performance_tests
tracing_perftests
views_perftests
viz_perftests
wayland_client_perftests
xr.vr.common_perftests
```

The `base_perftests` executable has a dependency on `test_support_perf`
according to the `base/BUILD.gn` build config.

Tying into the chromium performance benchmarking stuff would be pretty
difficult in order to just get performance counters working. It would
probably be doable, but everything seems to still be run through google
test. Instrumentation could be added in there since using it for performance
tests probably isn't totally out of the question (chromium does it, someone
else has to do it). Might be an interesting addition at some point.

Building just the tests is a pretty decent strategy to manage compile time/
storage space required in order to build the tests. `autoninja` accepts a
target at the end just like a normal build command, so for example, in order
to build the `base_perftests` target, just run:
```
autoninja -C /path/to/output base_perftests
```
This only takes about 3000 compile steps to finish everything up, so everything
is even nice and quick.