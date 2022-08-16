# Notes on using LLVM objcopy

Currently in the MLGO tooling we are extracting bitcode corpora and then
compiling that bitcode down to native code when doing RL training. This
bitcode is stored inside a section of the object file that can be
extracted using `llvm-objcopy`. This section contains some notes on
the syntax and commands that are relevant to MLGO.

### Grabbing the .llvmcmd section

```bash
llvm-objcopy --dump-section=.llvmcmd=<output file> <input object file>
```

### Grabbing the .llvmbc section

Very similar to grabbing the command line section, but instead of dumping
the `.llvmcmd` section, we are going to be dumping the `.llvmbc` section.

```bash
llvm-objcopy --dump-section=.llvmbc=<output file> <input object file>
```