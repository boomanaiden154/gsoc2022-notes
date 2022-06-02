# Building Clang With Clang

### Goals

- Build clang/LLVM with current head of tree clang/LLVM

- Build clang with instrumentation for profiling

### Process

Standard setup procedures, clone llvm. Use the following `cmake` command for the initial compile:

```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LTO=OFF \
    -DLLVM_ENABLE_PROJECTS="clang" \
    -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
    ../llvm
```

Then build with:

```bash
cmake --build  .
```

After this is done, install everything to the system:

```bash
cmake --install .
```

Now, delete the current build directory and recreate it. Then, running the following `cmake` command:

```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LTO=OFF \
    -DLLVM_ENABLE_PROJECTS="clang" \
    -DCMAKE_C_COMPILER=/llvm-stage1/build/bin/clang \
    -DCMAKE_CXX_COMPILER=/llvm-stage1/build/bin/clang++ \
    -DCMAKE_C_FLAGS="-fprofile-instr-generate" \
    -DCMAKE_CXX_FLAGS="-fprofile-instr-generate" \
    ../llvm
```
