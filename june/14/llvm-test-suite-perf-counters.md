# LLVM Test Suite with Performance Counters
The LLVM Test Suite has quite a few benchmarks in the `MicroBenchmarks/`
directory that use the Google Benchmark framework to facilitate running
benchmarks. Google Benchmark has support for using perf counters as
outlined in [this](https://github.com/google/benchmark/blob/main/docs/perf_counters.md)
piece of documentation. There are some compile time flags and some run
time flags that need to be enabled to get the performance counters
working.
### Dependencies
In order to use perf counters with Google benchmark, you need to install
the `libpfm4-dev` package (on Debian based distros, or an equivilant).
```bash
apt-get install -y libpfm4-dev
```
### Compiling the Test Suite
The main flag that needs to be included is `-DBENCHMARK_ENABLE_LIBPFM`.
An example CMake command:
```bash
cmake -G Ninja \
    -DCMAKE_C_COMPILER="/llvm-project/build/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-project/build/bin/clang++" \
    -DTEST_SUITE_BENCHMARKING_ONLY=ON \
    -DCMAKE_C_FLAGS="-O3" \
    -DCMAKE_CXX_FLAGS="-O3" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DBENCHMARK_ENABLE_LIBPFM=ON \
    ../
```
### Running the test suite
The main parameter that needs to be passed to the individual tests is
`--benchmark_perf_counters` with some platform dependent values such as
`INSTRUCTIONS` which will grab instruction counts. The flags are most
easily passed directly into an executable built with Google Benchmark.
For example, from the build dir for the llvm-test-suite:
```bash
./MicroBenchmarks/LoopVectorization --benchmark_perf_counters=INSTRUCTIONS
```
Note that these benchmarks will not work by default inside docker
containers as they rely on file descriptors that are not
defaulty available inside of containers. You should be able to get
everything running by running the container in a privileged state
(passing `--privileged` to `docker run`), or by setting a custom
SECCOMP policy that enables the necessary syscalls.