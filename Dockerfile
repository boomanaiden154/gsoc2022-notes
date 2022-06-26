FROM ubuntu:20.04
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
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
    libpfm4-dev \
    software-properties-common
RUN wget --quiet https://raw.githubusercontent.com/google/ml-compiler-opt/main/requirements.txt -P /tmp && \
    python3 -m pip install -r /tmp/requirements.txt
RUN wget --quiet https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz && \
    mkdir /tmp/tensorflow && \
    tar xfz libtensorflow-cpu-linux-x86_64-1.15.0.tar.gz -C /tmp/tensorflow
RUN git clone https://github.com/llvm/llvm-project.git
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
    echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
    apt-get update && \
    apt-get install -y cmake
RUN git clone https://github.com/llvm/llvm-test-suite.git
RUN apt-add-repository ppa:git-core/ppa && \
    apt-get update
    apt-get install -y git