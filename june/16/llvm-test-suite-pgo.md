# Compiling the LLVM test suite with PGO

**NOTE:** In order to generate the profiles, you need to make sure that
you have the necessary runtimes built in your local LLVM build because
while compiling clang needs to link against them and you will not be
able to get passed the initial compiliation stage in this documentation
without having this runtime (compiler-rt).

Compiling the LLVM test suite with profile guided optimizations is pretty
simple. Start off by doing a profile generating run:
```bash
cd /llvm-test-suite
mkdir build
cd build
cmake -G Ninja \
    -DTEST_SUITE_PROFILE_GENERATE=ON \
    -DTEST_SUITE_RUN_TYPE=train \
    -DCMAKE_C_COMPILER="/llvm-build/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-build/bin/clang++" \
    -DBENCHMARK_ENABLE_LIBPFM=ON \
    ../
cmake --build .
```

Then generate the profile data by running all of the tests using the
`llvm-lit` test runner:
```bash
llvm-lit .
```

Now, use the profile data to compile again:
```bash
cmake -G Ninja \
    -DTEST_SUITE_PROFILE_GENERATE=OFF \
    -DTEST_SUITE_PROFILE_USE=ON \
    -DTEST_SUITE_RUN_TYPE=ref \
    .
cmake --build .
```

Now you can run the benchmarks using optimizations that have been guided by
the profile that was collected earlier.