# Getting assembly out of clang

Getting raw assembly out of clang can sometimes be useful for debugging purposes, eg seeing what registers were selected in a specific function for comparison against the ML register eviction model versus the manual register eviction heuristics.  Running clang with the `-S` flag will tell it to output assembly. The format of this assembly using the `--[architecture]-asm-syntax` LLVM flag. For x86, it is `--x86-asm-syntax`. A full command exporting everything in the Intel assembly format:

```bash
clang -S -mllvm --x86-asm-sytnax=intel test.cpp -o test
```
