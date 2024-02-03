# LLVM PGO+BOLT Benchmarking

### Benchmark Build

```
make -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=/tmp/llvm-install-vanilla-stage2-bolt/bin/clang -DCMAKE_CXX_COMPILER=/tmp/llvm-install-vanilla-stage2-bolt/bin/clang++ ../llvm
```

### Configuration 0

```shell
cmake -G Ninja ../llvm \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;lld" \
  -DCLANG_DEFAULT_LINKER="lld" \
  -DLLVM_TARGETS_TO_BUILD=Native
```

```
real    3m35.714s
user    345m43.495s
sys     14m37.671s
```

### Configuration 1

```shell
cmake -G Ninja ../llvm \
  -C ../clang/cmake/caches/BOLT-PGO.cmake \
  -DBOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DPGO_INSTRUMENT_LTO=Thin \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
  -DCMAKE_INSTALL_PREFIX="/tmp/llvm-install-vanilla-stage2-bolt" \
  -DLLVM_ENABLE_PROJECTS="bolt;clang;lld" \
  -DLLVM_DISTRIBUTION_COMPONENTS="lld;compiler-rt" \
  -DCLANG_DEFAULT_LINKER="lld"
ninja stage2-clang-bolt install-distribution
```

Using the default hello world perf training

```
real    3m2.839s
user    261m9.643s
sys     13m22.997s
```

### Configuration 2

```shell
cmake -G Ninja ../llvm \
  -C ../clang/cmake/caches/BOLT-PGO.cmake \
  -DBOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON \
  -DPGO_INSTRUMENT_LTO=Thin \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
  -DCMAKE_INSTALL_PREFIX="/tmp/llvm-install-test-suite-stage2-bolt" \
  -DLLVM_ENABLE_PROJECTS="bolt;clang;lld" \
  -DLLVM_DISTRIBUTION_COMPONENTS="lld;compiler-rt" \
  -DCLANG_DEFAULT_LINKER="lld" \
  -DBOOTSTRAP_CLANG_PGO_TRAINING_DATA_SOURCE_DIR=/tmp/llvm-test-suite \
  -DBOOTSTRAP_CLANG_PGO_TRAINING_DEPS="runtimes;llvm-size"
ninja stage2-clang-bolt install-distribution
```

Using the LLVM test suite for performance training.

```
real    2m43.356s
user    230m26.469s
sys     13m30.372s
```

### Configuration 3

Building LLVM itself.

### Open Issues
* The clang-generate-profraw target is run while running the stage2-install-distribution target
* The default hello world profile generation is run when using an external project for profile generation
* BOLT doesn't use the external project for profile generation.
