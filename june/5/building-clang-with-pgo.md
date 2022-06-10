# Building Clang/LLVM with profile guided optimizations
### Initial Setup
Install all the dependencies as listed in the earlier article on building LLVM.

Inside a fresh ubuntu 20.04 docker container:
```bash
git clone https://github.com/eopXD/LLVM_PGO_CMake
git clone https://github.com/llvm/llvm-project.git
```
### Building Stage 1
Building stage 1 is relatively straightforward using the system gcc and g++:
```bash
mkdir /llvm-stage1
cd /llvm-stage1
cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/llvm-stage1-install \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++ \
    -DLLVM_ENABLE_ASSERTIONS=OFF \
    -C /LLVM_PGO_CMake/stage_instrument.cmake \
    /llvm-project/llvm
cmake --build .
```
### Building Stage 2
Building stage2 is again relatively straightforward.
```bash
mkdir /llvm-stage2
cd /llvm-stage2
cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/llvm-stage1 \
    -DLLVM_BINUTILS_INCDIR=/usr/include \
    -C /LLVM_PGO_CMake/stage_profiling.cmake \
    /llvm-project/llvm
cmake --build .
```
### Generating profile data
To generate profile data, run the following couple commands:
```bash
cmake --build . --target check-llvm
cmake --build . --target check-clang
/llvm-stage1/bin/llvm-profdata merge -output=/profdata.prof \
    /llvm-stage2/profiles/*.profraw
```

**Note:** When generating profile data, the compiler can only generate
profile data for code paths that are executed. So if you want to get
accurate PGO results for ie the ML register allocator eviction advisor
code, you need to make sure that you build this functionality into
stage1 (the instrumenting clang), and then set the appropriate flags
when generating all the profile data (building stage2/running stage2
checks). Otherwise these code paths won't be optimized at all. Then,
make sure to enable all the same features when compiling the final
PGO optimized clang/LLVM.

### Build the PGO optimized clang
To build the PGO optimized clang, run the following build command with
CMake to set the appropriate flags, mainly the PGO profile data:
```bash
mkdir /llvm-stage3
cd /llvm-stage3
cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/profdata.prof \
    -DCMAKE_C_COMPILER=/llvm-stage1/bin/clang \
    -DCMAKE_CXX_COMPILER=/llvm-stage1/bin/clang++ \
    -C /LLVM_PGO_CMake/stage_pgo.cmake \
    /llvm-project/llvm
cmake --build .
```

Now you will have a PGO built clang that you can use for benchmarking
or other purposes (ie distribution).