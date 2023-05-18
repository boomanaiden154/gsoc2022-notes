# Advanced Build Benchmarking

Some benchmark numbers from doing advanced builds,
particularly a PGO/ThinLTO/BOLT optimized clang against building LLVM itself.

These numbers are based on using LLVM/Clang df64272c7bdba91493a21fc13c7fdedb3686cc77.

CMake configuration for the optimized Clang:

```sh
cmake -G Ninja /llvm-project/llvm \
  -C /llvm-project/clang/cmake/caches/BOLT-PGO.cmake \
  -DBOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DPGO_INSTRUMENT_LTO=Thin \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
  -DCMAKE_INSTALL_PREFIX="/llvm-install" \
  -DLLVM_ENABLE_PROJECTS="bolt;clang;lld;lldb;clang-tools-extra" \
  -DLLVM_DISTRIBUTION_COMPONENTS="lld;clangd;compiler-rt;lldb;liblldb;lldb-argdumper;lldb-server" \
  -DCLANG_DEFAULT_LINKER="lld"
```

Installing the `stage2-distribution` target.

This was built using the default perf-training dataset (just compiling a c++ hello
world program). We could probably expect better results by compiling a bigger file.

Using the stage1 clang as the unoptimized clang. GCC for comparison is the one
that ships with Ubuntu 22.04.

Testing by building the default target in all these cases with the following CMake invocation:

```
cmake -DCMAKE_BUILD_TYPE=Release -GNinja /llvm-project/llvm
```

### Timing for building LLVM with GCC

```
real    3m58.253s
user    283m12.770s
sys     15m31.504s
```

### Timing for building LLVM with unoptimized clang

```
real    3m47.735s
user    304m19.845s
sys     11m39.895s
```

### Timing for building LLVM with optimized clang

```
real    2m56.093s
user    220m47.735s
sys     9m49.051s
```
