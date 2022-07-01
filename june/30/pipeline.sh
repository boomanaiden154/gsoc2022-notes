# Compile LLVM with regalloc stuff

mkdir /llvm-build
cd /llvm-build
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_ENABLE_PROJECTS="clang;lld" \
    -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
    ../llvm
cmake --build .

# Compile LLVM test suite with two stage

cd /llvm-test-suite
mkdir /build
cd /build
cmake -G Ninja \
    -DCMAKE_C_COMPILER="/llvm-build/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-build/bin/clang++" \
    -DTEST_SUITE_BENCHMARKING_ONLY=ON \
    -DCMAKE_C_FLAGS="-O3" \
    -DCMAKE_CXX_FLAGS="-O3" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DTEST_SUITE_PROFILE_GENERATE=ON \
    -DTEST_SUITE_RUN_TYPE=train \
    -DBENCHMARK_ENABLE_LIBPFM=ON \
    ../
cmake --build .

/llvm-build/bin/llvm-lit .

cmake -DTEST_SUITE_PROFILE_GENERATE=OFF \
    -DTEST_SUITE_PROFILE_USE=ON \
    -DTEST_SUITE_RUN_TYPE=ref \
    ../
cmake --build .