set -e
git clone https://github.com/xianyi/OpenBLAS.git
mkdir ./OpenBLAS/build
cd ./OpenBLAS/build
cmake -G Ninja \
    -DCMAKE_C_FLAGS="-fbasic-block-sections=labels" \
    -DCMAKE_CXX_FLAGS="-fbasic-block-sections=labels" \
    ../
ninja
# TODO(boomanaiden154): Add in tooling to extract BBs
