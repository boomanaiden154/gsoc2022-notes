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
wget --quiet https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-2.6.0.tar.gz
mkdir /tmp/tensorflow
tar xfz libtensorflow-cpu-linux-x86_64-2.6.0.tar.gz -C /tmp/tensorflow
```

After this, everything should be set up to build LLVM with ML support.

### Building LLVM

After installing of the necessary dependencies and performing the setup tasks, you should be able to install LLVM using the following commands from inside the llvm source directory:

```bash
mkdir build
cd build
cmake -G Ninja \
    -DLLVM_ENTABLE_LTO=OFF \
    -DLLVM_CACHE_BUILD=ON \
    -DLLVM_ENABLE_ASSERTATIONS=ON \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINUX_PATH=ON
```
