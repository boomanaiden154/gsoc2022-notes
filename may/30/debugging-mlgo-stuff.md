# Debugging MLGO stuff

For this article, I'm going to assume that debugging is being done using `gdb` as I'm compiling LLVM/Clang using gcc as I'm using Ubuntu, and I'm going to focus on debugging register allocation stuff as that is what I am focused on. To start off, assuming that `$LLVM_SOURCE_DIR` is set to the source directory for LLVM and you have a build of LLVM/Clang in `$LLVM_SOURCE_DIR/llvm/build`, running the following gdb command should get you a gdb prompt for clang:

```bash
gdb $LLVM_SOURCE_DIR/llvm/build/bin/clang
```

Then, setting some flags will be necessary if you want to start the debugger directly on clang, particularly flags involving forking:

```
set follow-fork-mode child
set detach-on-fork off
```

These are the settings I've tested with. Other configurations might work however. Then, you just need to type in a `run` command with the proper arguments to get everything to work. The following should work decently well:

```
 run -mllvm -regalloc-enable-advisor=development -mllvm -regalloc-training-log=/./log -mllvm -regalloc-model=./model -O1 test.c
```

Before just running the application though, you might want to begin to set some breakpoints. Triggering by file name and line number has worked best for me, but triggering by class name and function name should work as well. Just note that much of the MLGO stuff is inside an anonymous namespace and thus when setting a breakpoint using class/function names, you need to prepend `(anonymous namespace)::` to them to make everything functional. For example, currently I'll set a breakpoint as follows:

```
b MLRegallocEvictAdvisor.cpp:851
```

This will cause the debugger to break upon entering the `tryFindEvictionCandidatePosition` function as implemented by the `DevelopmentModeEvictAdvisor`. Then you can use all the standard GDB debugging commands like `step`, `finish`, `next`, and `continue`.






