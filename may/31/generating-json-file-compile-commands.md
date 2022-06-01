# Generating a JSON file of compile commands

I'm going to run everything here on a clang/LLVM corpus as that is what I am planning on using later for RegAlloc work, and it should be pretty decent for a varietey of different purposes. First, go into the LLVM source directory and create a build directory if you haven't already:

```bash
cd $LLVM_SOURCE_DIR
mkdir build
cd buildw
```

Then it is just a matter of running cmake with the desired flags as well as `-DCMAKE_EXPORT_COMPILE_COMMANDS=1` to get a `compile_commands.json` file that has everything necessary. I'm using the following flags:

```bash
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_LTO=OFF \
    -DLLVM_ENABLE_PROJECTS="clang" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
    ../llvm
```

After the configuring is done, you should be left with a very long `compile_commands.json` file in that same directory that you ran cmake in which is very easily machine parseable and ready to use for whatever you might need.
