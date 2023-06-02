set -e
git clone https://github.com/llvm/llvm-project
mkdir ./llvm-project/build
cd ./llvm-project/build
cmake -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="all" \
  -DCMAKE_C_FLAGS="-fbasic-block-sections=labels" \
  -DCMAKE_CXX_FLAGS="-fbasic-block-sections=labels" \
  ../llvm
# TODO(boomanaiden154): Add runtime builds, need to figure out how to
# propogate c/c++ compiler flags.
ninja
# TODO(boomanaiden154): Add BB extraction tooling

