# AutoFDO

[AutoFDO](https://github.com/google/autofdo) is a set of tools for generating
and working with sampling based profiles. Information in this document is
current as of 12/17/22.

### Building LLVM for AutoFDO

There are a couple of options that need to be enabled for building LLVM
for AutoFDO, mainly enabling the `LLVM_ENABLE_RTTI` flag. The CMake config
reccomended in the AutoFDO configuration is the following:

```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_ASSERTIONS=ON \
    -DBUILD_SHARED_LIBS=OFF \
    -DLLVM_ENABLE_RTTI=ON \
    -DCMAKE_INSTALL_PREFIX=/llvm-install \
    -DLLVM_ENABLE_PROJECTS="clang" \
    ../llvm
```

Then build the configuration:

```bash
cmake --build .
```

Afterwards, you also need to install it. This will install to wherever
`CMAKE_INSTALL_PREFIX` is set to, so you might need to change the config.

```bash
cmake --build . --target install
```

Note also that the tip of tree AutoFDO stuff doesn't have support for
some recent changes in LLVM, namely the move from `LLVM::Optional` to
`std::optional`, and the deprecation of `LLVM::None`. A commit that
should work if not using a patched build:
```
b9378a60c4d652b016596937d95d73d08415760c
```

I also have a [PR](https://github.com/google/autofdo/pull/155) open to try and
address this problem, but I don't necessarily have a lot of hope for it getting
addressed soon. Might even take until the next internal code sync.

### Building the tools

First off, there are a couple of dependencies that need to be installed:
```bash
apt-get install -y libunwind-dev libgflags-dev libssl-dev libelf-dev protobuf-compiler
```

Next, clone the repository and create a build folder:
```bash
git clone https://github.com/google/autofdo
cd autofdo
mkdir build
cd build
```

Then, configure the build:
```bash
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=. \
    -DLLVM_PATH=/llvm-install \
    ../
```

The `README.md` in the AutoFDO repository says that `CMAKE_INSTALL_PREFIX`
must be used due to some error that they have in one of their CMake lists.

### Using the tools

After building the tools, you should have access to two executables,
namely `