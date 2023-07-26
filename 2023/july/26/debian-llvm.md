# Building Debian LLVM Packages

To build the debian/ubuntu LLVM packages within a `ubuntu:22.04` container,
first start the container, and then run the following commands to install the
necessary packages:

```bash
apt-get update
apt-get install -y \
  git \
  dpkg-dev \
  time \
  devscripts \
  quilt \
  debhelper \
  dh-ocaml \
  cmake \
  ninja-build \
  python3-sphinx \
  binutils-dev \
  python-recommonmark-doc \
  doxygen \
  chrpath
```

Then clone the `snapshot` branch of the build recipe repository into a directory
called `snapshot` in a directory called `branches` to keep things clean:

```bash
mkdir branches
cd branches
git clone https://salsa.debian.org/pkg-llvm-team/llvm-toolchain.git -b snapshot snapshot
```

Then run the `orig-tar.sh` script to grab the latest sources and repack
everything as a set of tarballs:

```bash
sh ./snapshot/debian/orig-tar.sh
```

Then unpack the created repositories to prepare the build:

```bash
sh ./snapshot/debian/unpack.sh
```

Then go into the directory crated by `unpack.sh` in my case the directory was
`llvm-toolchain-snapshot_18~++20230726074859+fca4a9d5fcdd`. Then run the actual
build:

```bash
cd llvm-toolchain-snapshot_18~++20230726074859+fca4a9d5fcdd
debian/rules binary
```