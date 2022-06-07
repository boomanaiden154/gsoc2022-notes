# LLVM Benchmarks
LLVM has a pretty extensive [test suite](https://llvm.org/docs/TestSuiteGuide.html), 
and part of this test suite is benchmarks (located in
the `./MicroBenchmarks`) directory within the test
repository. 
### Dependencies
Some dependencies need to be installed in addition
to the LLVM build dependencies so that some of the
benchmarks can be built.
```bash
apt-get install -y tcl-dev
```
### Cloning the code
The LLVM test suite lives out of the main LLVM source
tree. You can download it with the following command:
```bash
git clone https://github.com/llvm/llvm-test-suite.git
```
### Compiling the benchmarks
Compiling the benchmarks is pretty straightforward.
Using a built clang that has all of the options you
need enabled (eg compiling in the regalloc model),
you can run the following CMake command:
```bash
cd llvm-test-suite
mkdir build
cd build
cmake -G Ninja \
    -DCMAKE_C_COMPILER="/llvm-project/build/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-project/build/bin/clang++" \
    -DTEST_SUITE_BENCHMARKING_ONLY=ON \
    -DCMAKE_C_FLAGS="-O3" \
    -DCMAKE_CXX_FLAGS="-O3" \
    -DCMAKE_BUILD_TYPE="Release" \
    ../
cmake --build .
```
### Running the benchmarks
```bash
/llvm-project/build/bin/llvm-lit -v -j 32 -o results.json .
```
This will spit out a `results.json` file with all
the information that was produced by the benchmarks,
including compile and runtime data.