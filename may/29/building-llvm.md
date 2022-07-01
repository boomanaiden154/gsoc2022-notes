# Building LLVM

There is a full example `cmake` command contained within the demo, but there are quite a few Fuschia specific flags that won't be needed for general development/the corpus that I will be using (clang at this moment in time). The [buildbot_init.sh](https://github.com/google/ml-compiler-opt/blob/main/buildbot/buildbot_init.sh) has some good info on basic development environment setup in regards to dependencies and tensorflow library setup. After this, the builder configurations for the LLVM Zorg testing infrastructure seems to have most of the necessary flags (with the ML specific stuff starting on a comment at line 2247). 

### Setup

On a debian based system, the following packages need to be installed according to the `buildbot_init.sh` script:

```
apt-get install -y \
        python3-distutils \
        python-is-python3 \
        python3 \
        python3-pip \
        tmux \
        g++ \
        cmake \
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
        zlib1g-dev
```

Then, there are some python dependencies that need to be installed that come from ` requirements.txt` contained within the `ml-compiler-opt` repository. They can be downloaded and installed with the following commands:

```bash
wget --quiet https://raw.githubusercontent.com/google/ml-compiler-opt/main/requirements.txt -P /tmp
python3 -m pip install -r /tmp/requirements.txt
```

Now we need to install the Tensorflow C API so that we can reference it in the LLVM build. This can be achieved with the following:

```bash
wget --quiet https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz
mkdir /tmp/tensorflow
tar xfz libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz -C /tmp/tensorflow
```

After this, everything should be set up to build LLVM with ML support.

### Cloning the repository

Clone the llvm repository from the central repository (currently on Github, shown below), or a personal fork:

```bash
git clone https://github.com/llvm/llvm-project.git
```

**Note:** make sure that you are in whatever directory you want to have the LLVM sources in when you run the above command.

### Building LLVM

After installing of the necessary dependencies and performing the setup tasks, you should be able to configure the LLVM build using the following commands from inside the llvm source directory:

```bash
mkdir build
cd build
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DLLVM_ENABLE_LTO=OFF \
    -DLLVM_CCACHE_BUILD=ON \
    -DLLVM_ENABLE_ASSERTIONS=ON \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_ENABLE_PROJECTS="clang" \
    -DLLVM_PARALLEL_LINK_JOBS=24 \
    -DLLVM_USE_SPLIT_DWARF=ON \
    ../llvm
```

**Note:** the above command also configures the build for clang as specified with the `-DLLVM_ENABLE_PROJECTS="clang"` flag. If you don't want to build clang, remove this flag. However, any sort of testing/work with the MLGO stuff will require a build of clang.

**Note:** The above command also restricts the maximum number of parallel linking jobs. When compiling with debug symbols, the memory usage during linking is massive, and linking on only 24 threads should keep memory usage to under 128gb at  any one point (around 110GB from my testing). If you set `LLVM_USE_SPLIT_DWARF` to off, this number needs to be significantly reduced.

**Note:** The above command also sets the `LLVM_USE_SPLIT_DWARF` option. This reduces memory usage during the build process, primarily during linking, and also speeds up builds. The debug symbols are split to a separate file, so if you plan on installing clang or llvm with debug symbols, this is important to note.

Then, running the following command should start a build:

```bash
cmake --build .
```

### Other common configuation options:
Here is a list of a couple other common configuration options so that
they can easily be copied ans pasted.

Release mode, no MLGO:
```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="clang" \
    ../llvm
```
Release mode MLGO:
```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_ENABLE_PROJECTS="clang;lld" \
    -DLLVM_ENABLE_RUNTIMES="compiler-rt" \
    ../llvm
```