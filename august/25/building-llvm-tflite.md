# Building LLVM with TFLite

With the recent transition to TFLite for loading models at runtime, there
are some changes to the build steps.

First off, all of the TFLite dependencies need to be compiled. A lot of them
are tagged at a specific hash and need to be compiled from source. There is a
script to automatically do this in the ml-compiler-opt repository,
`./buildbot/build_tflite.sh`. 

This script will compile all the dependencies and install them into the current
working directory. It will also place a cache script, `tflite.cmake`, which can
then be piped into the LLVM CMake process and everything for tflite will be
setup.

Example build command:
```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DLLVM_ENABLE_PROJECTS="clang;lld" \
    -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
    -C /ml-compiler-opt/tflite.cmake \
    /llvm-project/llvm
```