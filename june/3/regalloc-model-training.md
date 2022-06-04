# RegAlloc Model Training

Based off of the inliner demo, using clang/LLVM as a corpus. Starting off, make sure that you have a LLVM source dir that you're running everything out of and an LLVM source dir that you can use to compile everything for testing.

### Building Clang/LLVM

The config to build Clang/LLVM to get everything ready to compile the corpus:

```bash
cd $LLVM_SOURCE_DIR
mkdir build
cd build
cmake -G Ninja \
    -DLLVM_BINUTILS_INCDIR=/usr/include \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LTO=OFF \
    -DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow \
    -DTENSORFLOW_AOT_PATH=$(python3 -c "import tensorflow; import os; print(os.path.dirname(tensorflow.__file__))") \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
    -DLLVM_ENABLE_PROJECTS="clang" \
    ../llvm
cmake --build .
```

Note the `DLLVM_BINUTILS_INCDIR` flag. This is important as it allows for the `LLVMGold.so` shared object to be built, which is needed for ThinLTO in the next step.

### Building Clang/LLVM for the corpus

Start off by building the clang/LLVM corpus with some custom flags:

```bash
cd $CLANG_LLVM_CORPUS_DIR
mkdir build
cd build
cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LTO=Thin \
    -DLLVM_ENABLE_PROJECTS="clang" \
    -DCMAKE_C_FLAGS="-mllvm -lto-embed-bitcode=post-merge-pre-opt" \
    -DCMAKE_CXX_FLAGS="-mllvm -lto-embed-bitcode=post-merge-pre-opt" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DCMAKE_C_COMPILER=/llvm-project/build/bin/clang \
    -DCMAKE_CXX_COMPILER=/llvm-project/build/bin/clang++ \
    -DCMAKE_RANLIB=/llvm-project/build/bin/llvm-ranlib \
    -DCMAKE_AR=/llvm-project/build/bin/llvm-ar \
    ../llvm
cmake --build .
```

### Install python dependencies

Should already be done if there is an already existing build based on the earlier building LLVM article.

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r ml-compiler-opt/requirements.txt
```

### Extracting the corpus

```bash
cd $ML_COMPILER_OPT_DIR
mkdir /corpus
# Assuming $CLANG_LLVM_CORPUS_DIR is set to /llvm_corpus
# Assuming $LLVM_SOURCE_DIR is set to /llvm-project
python3 compiler_opt/tools/extract_ir.py \
    --cmd_filter="^-O2|-O3$" \
    --input=/llvm_corpus/build/compile_commands.json \
    --input_type=json \
    --llvm_objcopy_path=/llvm-project/build/bin/llvm-objcopy \
    --output_dir=/corpus \
    --thinlto_build=True
```

### Collect the default trace

```bash
mkdir /default_trace
# If /default_trace already exists and contains data, make sure to delete
PYTHONPATH=$PYTHONPATH:. python3 compiler_opt/tools/generate_default_trace.py \
    --data_path=/corpus \
    --output_path=/default_trace \
    --gin_files=compiler_opt/rl/inlining/gin_configs/common.gin \
    --gin_bindings=config_registry.get_configuration.implementation=@configs.RegallocEvictionConfig \
    --gin_bindings=clang_path="'/llvm-project/build/bin/clang'" \
    --sampling_rate=0.2
```
