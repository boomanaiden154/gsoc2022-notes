# TODO(boomanaiden154): Refactor common parts between this file
# and ../12/pipeline.sh into other files

# This script must be run inside a container that has been
# started in PRIVILEGED mode
# Running docker inspect --format='{{.HostConfig.Privileged}}' <container id>
# on the host should say true

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
    tcl-dev \
    libpfm4-dev

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
git clone https://github.com/boomanaiden154/llvm-project.git

# Unpack the given model
tar xfz $1 -C /tmp

mkdir /llvm-build
cd /llvm-build

cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_ENABLE_PROJECTS="clang" \
    /llvm-project/llvm
cmake --build .

# Build and Run LLVM test suite
git clone https://github.com/llvm/llvm-test-suite.git /llvm-test-suite

mkdir /llvm-test-suite/build
cd /llvm-test-suite/build

cmake -G Ninja \
    -DCMAKE_C_COMPILER="/llvm-build/bin/clang" \
    -DCMAKE_CXX_COMPILER="/llvm-build/bin/clang++" \
    -DTEST_SUITE_BENCHMARKING_ONLY=ON \
    -DCMAKE_C_FLAGS="-mllvm -regalloc-enable-advisor=development -mllvm -regalloc-training-log=./log -mllvm -regalloc-model=/tmp/model -mllvm -regalloc=greedy -O3" \
    -DCMAKE_CXX_FLAGS="-mllvm -regalloc-enable-advisor=development -mllvm -regalloc-training-log=./log -mllvm -regalloc-model=/tmp/model -mllvm -regalloc=greedy -O3" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DBENCHMARK_ENABLE_LIBPFM=ON \
    ../
cmake --build .

testSuites=(
    "harris/harris"
    "SLPVectorization/SLPVectorizationBenchmarks"
    "MemFunctions/MemFunctions"
    "LoopVectorization/LoopVectorizationBenchmarks"
    "LoopInterchange/LoopInterchange"
    "LCALS/SubsetALambdaLoops/lcalsALambda"
    "LCALS/SubsetARawLoops/lcalsARaw"
    "LCALS/SubsetBLambdaLoops/lcalsBLambda"
    "LCALS/SubsetBRawLoops/lcalsBRaw" 
    "LCALS/SubsetCLambdaLoops/lcalsCLambda"
    "LCALS/SubsetCRawLoops/lcalsCRaw"
    "ImageProcessing/AnisotropicDiffusion/AnisotropicDiffusion"
    "ImageProcessing/BilateralFiltering/BilateralFiltering"
    "ImageProcessing/Blur/Blur"
    "ImageProcessing/Dilate/Dilate"
    "ImageProcessing/Dither/Dither"
    "ImageProcessing/Interpolation/Interpolation"
    "Builtins/Int128/Builtins"
)

for testSuite in ${testSuites[@]}; do
    baseName=$(basename $testSuite)
    outFile="/llvm-test-suite/build/$baseName.json"
    /llvm-test-suite/build/MicroBenchmarks/$testSuite --benchmark_perf_counters=INSTRUCTIONS,MEM_UOPS_RETIRED:ALL_LOADS,MEM_UOPS_RETIRED:ALL_STORES --benchmark_out_format=json --benchmark_out=$outFile
done

python3 combine-benchmarks.py output.tmp
mv output.tmp output.json