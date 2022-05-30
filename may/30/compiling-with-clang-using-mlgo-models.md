# Compiling with Clang using the MLGO models

After LLVM and Clang have been built, building code with clang is pretty much the next important step, but the correct flags need to be set in order to be able to use the MLGO models.

### Compiling using the release mode ML inliner

The command should look like the following (where `$LLVM_SOURCE_DIR` is set to wherever your LLVM source dir is, and assuming that your LLVM build is contained in `$LLVM_SOURCE_DIR/build`):

```bash
$LLVM_SOURCE_DIR/build/bin/clang \
    -mllvm -enable-ml-inliner=release \
    -Oz \
    test.cpp \
    -o test
```

This will build the  file `test.cpp` and compile it into a program called `test`. The main flag to note here is the `-enable-ml-regalloc=release` flag which is passed directly to LLVM using the `-mllvm` flag in clang. The original [RFC](https://lists.llvm.org/pipermail/llvm-dev/2020-April/140763.html) for inlining mentions needing to pass the `--mandatory-inlining-first` (although in the RFC as `-mandatory-inlinings-first`, not sure if this is just a typographical error, or if something changed later on). This flag is not passed in right now from what I can tell for the existing infrastructure (relevant code is in `compiler_opt/rl/inlining/inlining_runner.py` in the ml-compiler-opt repo), and thus I have not included it here.

### Compiling using the development mode ML inliner

To compile with clang using a custom policy, a couple additional flags are needed. Getting training output is required and can be done using the `-training-log` flag with LLVM. `-enable-ml-inliner` needs to be set to `development` rather than `release`. Finally, the LLVM flag `-ml-inliner-model-under-training` needs to be set to the path to the model. There are a couple different models available under the releases section on the ml-compiler-opt Github repo page. A full command that compiles `test.cpp` into the executable `test` assuming the same conditions as before:

```bash
$LLVM_SOURCE_DIR/build/bin/clang \
    -mllvm -enable-ml-inliner=development \
    -mllvm -training-log=./log \
    -mllvm -ml-inliner-model-under-training=./model \
    -Oz \
    test.cpp \
    -o test
```

To download the latest model and set everything up for the previous command:

```bash
curl -L https://github.com/google/ml-compiler-opt/releases/download/inlining-Oz-v1.1/inlining-Oz-99f0063-v1.1.tar.gz > inlining-model.tar.gz
tar -xf inlining-model.tar.gz
```

Make sure that `./log` is not a directory. If it is, clang will crash and spit out a very long stack trace instead of doing what we intend.

### Compiling using release mode ML register allocation

I couldn't find a whole lot of documentation on using release mode ML register allocation. I'm assuming it exists somewhere as thre is a release on Github and there have been references to Google using it internally, but it is not currently well documented. More investigation needed.

### Compiling using development mode ML register allocation

Should just need a couple of flags. The flags passed in by the regalloc runner in the ml-compiler-opt repository include `-mllvm -thinlto-assume-merged`, `-mllvm -regalloc-enable-advisor=development`, `-mllvm -regalloc-training-log`, and `-mllvm -regalloc-model`. Still not 100% of the function of the LLVM flag `-thinlto-assume-merged` here. Might be something training specific. Bypasses function importing. Example command assuming a similar environment to before:

```bash
$LLVM_SOURCE_DIR/build/bin/clang \
    -mllvm -thinlto-assume-merged \
    -mllvm -regalloc-enable-advisor=development \
    -mllvm -regalloc-training-log=./log \
    -mllvm -regalloc-model=./model \
    test.cpp \
    -O1 \
    -o test
```

And again, to download the latest model and set everything up, the following command can be run:

```bash
curl -L https://github.com/google/ml-compiler-opt/releases/download/regalloc-evict-v1.0/regalloc-evict-e67430c-v1.0.tar.gz > regalloc-model.tar.gz
tar -xf regalloc-model.tar.gz
```
