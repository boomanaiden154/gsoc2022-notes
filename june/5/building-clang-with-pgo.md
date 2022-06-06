# Building Clang/LLVM with profile guided optimizations
### Initial Setup
Install all the dependencies as listed in the earlier article on building LLVM.

Inside a fresh ubuntu 20.04 docker container:
```bash
git clone https://github.com/eopXD/LLVM_PGO_CMake
git clone https://github.com/llvm/llvm-project.git llvm-stage1
cp -r ./llvm-stage1 ./llvm-stage2
cp -r ./llvm-stage1 ./llvm-stage3
```
### Building Stage 1
Building stage 1 is relatively straightforward using the system gcc and g++:
```bash
cd /llvm-stage1
mkdir build
cd build
cmake -G Ninja \
    -DPGO_STAGE_1_INSTALL_PATH=/llvm-stage1-install \
    -C /LLVM_PGO_CMake/stage1.cmake \
    ../llvm
cmake --build .
```
After building stage1, you need to install everything. The install prefix is already set, so you just need to run install using cmake:
```bash
cmake --install .
```
### Building Stage 2
Building stage2 is again relatively straightforward.
```bash
cd /llvm-stage2
mkdir build
cd build
cmake -G Ninja \
    -DPGO_STAGE_1_INSTALL_PATH=/llvm-stage1-install \
    -DPGO_STAGE_2_INSTALL_PATH=/llvm-stage2-install \
    -DLLVM_BINUTILS_INCDIR=/usr/include \
    -C /LLVM_PGO_CMake/stage2.cmake \
    ../llvm
cmake --build . --target all?
cmake --build . --target stage2-instrumented?
```
### Generating profile data
The stage2 build should automatically generate the
appropriate profile data in `/path/to/profile/data`.
