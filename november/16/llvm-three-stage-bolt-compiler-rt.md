# Issues with a three stage clang PGO build with BOLT in regards to compiler-rt

When doing a three stage clang PGO build and then BOLT on top of that and then
building the compiler-rt target, the resulting compiler is not able to find some
system libraries particularly Zlib when trying to build LLVM again. Not totally
sure why this is happening, seems like it could be bad CMake configuration of the
stage2-bolt binaries, or it might be a bad sysroot or something. Need to go and
do some more experimentation on that.

Dockerfile showing the build:
```Docker
FROM mlgo-development:latest
RUN git clone https://github.com/llvm/llvm-project
RUN mkdir /llvm-build
WORKDIR /llvm-build
RUN cmake -G Ninja /llvm-project/llvm \
        -C /llvm-project/clang/cmake/caches/BOLT-PGO.cmake \
        -DBOOTSTRAP_LLVM_ENABLE_LLD=ON \
        -DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON \
        -DPGO_INSTRUMENT_LTO=Thin
RUN cmake --build . --target stage2-clang++-bolt
# Removing the below line fixes the missing Zlib errors in the next CMake config
RUN cmake --build /llvm-build/tools/clang/stage2-instrumented-bins/tools/clang/stage2-bins --target runtimes
RUN mkdir /llvm-project/build
WORKDIR /llvm-project/build
# This CMake configurtion will error out due to thinking its missing zlib
# Only occurs when using the clang-bolt/clang++-bolt built above
RUN cmake -G Ninja \
       -DCMAKE_BUILD_TYPE=Release \
       -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
       -DLLVM_ENABLE_PROJECTS="clang;lld" \
       -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
       -DLLVM_ENABLE_ASSERTIONS=ON \
       -DCMAKE_C_COMPILER=/llvm-build/tools/clang/stage2-instrumented-bins/tools/clang/stage2-bins/bin/clang-bolt \
       -DCMAKE_CXX_COMPILER=/llvm-build/tools/clang/stage2-instrumented-bins/tools/clang/stage2-bins/bin/clang++-bolt \
       -C /tflite/tflite.cmake \
       /llvm-project/llvm
RUN ninja all
WORKDIR /
```

Need to do some more investigation and fiddle around with the targets, but definitely
some pretty weird behavior. 

Also seems to be occurring with the three stage PGO-only clang build, so I'm not sure
what is going on here. Seems pretty likely I'm screwing something up though and it
doesn't have anything to do with how upstream is doing things.

Simply passing in the actual zlib paths through `-DZLIB_ROOT=/usr/include` and
`-DZLIB_LIBRARY=/usr/lib/x86_64-linux-gnu/libz.so` fixes the issue, so not a high
priority to dig into the root of the issue, but it's still definitely an oddity.
Looking into the `FindZLIB.cmake` script that gets invokved to find the zlib
locations, it seems like absolutely nothing should change with a different compiler,
but maybe I'm missing something (like it gets search paths from the compiler or
something).