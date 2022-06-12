apt-get update

# install all necessary dependencies for building LLVM
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-distutils \
    python-is-python3 \
    python3 \
    python3-pip \
    tmux \
    g++ \
    ccache \
    binutils-gold \
    binutils-dev \
    ninja-build \
    pkg-config \
    gcc-multilib \
    g++-multilib \
    gawk \
    dos2unix \
    libxml2-dev \
    rsync \
    git \
    libtool \
    m4 \
    automake \
    libgcrypt-dev \
    liblzma-dev \
    libssl-dev \
    libgss-dev \
    python3-dev \
    wget \
    zlib1g-dev \
    tcl-dev

# Add CMake repos so that we can use some newer
# functions if necessary
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null
apt-get update
apt-get install -y cmake

# Install necessary python dependencies for building LLVM
wget --quiet https://raw.githubusercontent.com/google/ml-compiler-opt/main/requirements.txt -P /tmp
python3 -m pip install -r /tmp/requirements.txt

# Grab tensorflow libc for compiling LLVM
wget --quiet https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz
mkdir /tmp/tensorflow
tar xfz libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz -C /tmp/tensorflow

# Clone projects
https://github.com/boomanaiden154/llvm-project.git
git clone https://github.com/eopXD/LLVM_PGO_CMake

# Unpack the given model
tar xfz $1 -C /tmp

# Build LLVM Stage1 (instrumentation)
mkdir /llvm-stage1
cd /llvm-stage1

cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/llvm-stage1-install \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++ \
    -DLLVM_ENABLE_ASSERTIONS=OFF \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_RAEVICT_MODEL_PATH=/tmp/model \
    -C /LLVM_PGO_CMake/stage_instrument.cmake \
    /llvm-project/llvm
cmake --build .

# Build LLVM Stage2 (profiling)
mkdir /llvm-stage2
cd /llvm-stage2

cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/llvm-stage1 \
    -DLLVM_BINUTILS_INCDIR=/usr/include \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DCMAKE_C_FLAGS="-mllvm -regalloc-enable-advisor=release -mllvm -regalloc=greedy -O3" \
    -DCMAKE_CXX_FLAGS="-mllvm -regalloc-enable-advisor=release -mllvm -regalloc=greedy -O3" \
    -DLLVM_RAEVICT_MODEL_PATH=/tmp/model \
    -C /LLVM_PGO_CMake/stage_profiling.cmake \
    /llvm-project/llvm
cmake --build .
cmake --build . --target check-llvm
cmake --build . --target check-clang
/llvm-stage1/bin/llvm-profdata merge -output=/profdata.prof \
    /llvm-stage2/profiles/*.profraw

# Build LLVM Stage3 (Final PGO build)
mkdir /llvm-stage3
cd /llvm-stage3

cmake -G Ninja \
    -DPGO_STAGE_INSTRUMENT_INSTALL_PATH=/profdata.prof \
    -DCMAKE_C_COMPILER=/llvm-stage1/bin/clang \
    -DCMAKE_CXX_COMPILER=/llvm-stage1/bin/clang++ \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_RAEVICT_MODEL_PATH=/tmp/model \
    -C /LLVM_PGO_CMake/stage_pgo.cmake \
    /llvm-project/llvm
cmake --build .

# Build and Run LLVM test suite
cd /
git clone https://github.com/llvm/llvm-test-suite.git

mkdir /llvm-test-suite/build
cd /llvm-test-suite/build

cmake -G Ninja \
    -DCMAKE_C_COMPILER="/llvm-stage3/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-stage3/bin/clang++" \
    -DTEST_SUITE_BENCHMARKING_ONLY=ON \
    -DCMAKE_C_FLAGS="-mllvm -regalloc-enable-advisor=release -mllvm -regalloc=greedy -O3" \
    -DCMAKE_CXX_FLAGS="-mllvm -regalloc-enable-advisor=release -mllvm -regalloc=greedy -O3" \
    -DCMAKE_BUILD_TYPE="Release" \
    ../
cmake --build .

/llvm-stage3/bin/llvm-lit -v -j $(nproc) -o results.json .

# There is now a nice results.json file waiting
# to be processed downstream.