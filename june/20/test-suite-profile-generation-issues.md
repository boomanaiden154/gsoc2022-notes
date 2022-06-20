# Errors Compiling the Entire Test Suite with Profile Instruction Generation On
Currently when compiling the entirety of the LLVM test suite with profile
instruction generation turned on (with the `-DTEST_SUITE_PROFILE_GENERATE=ON`
CMake flag set), compiling the test suite will fail with the following
linker erros:
```
/usr/bin/ld: SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o: in function `test2':
compare-fp-3.c:(.text+0x49): undefined reference to `link_error0'
/usr/bin/ld: SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o: in function `test3':
compare-fp-3.c:(.text+0x79): undefined reference to `link_error0'
/usr/bin/ld: SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o: in function `test5':
compare-fp-3.c:(.text+0xed): undefined reference to `link_error1'
/usr/bin/ld: SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o: in function `test6':
compare-fp-3.c:(.text+0x13d): undefined reference to `link_error1'
/usr/bin/ld: SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o: in function `all_tests':
compare-fp-3.c:(.text+0x1c5): undefined reference to `link_error0'
/usr/bin/ld: compare-fp-3.c:(.text+0x1f8): undefined reference to `link_error0'
/usr/bin/ld: compare-fp-3.c:(.text+0x2b8): undefined reference to `link_error1'
/usr/bin/ld: compare-fp-3.c:(.text+0x300): undefined reference to `link_error1'
clang-15: error: linker command failed with exit code 1 (use -v to see invocation)
```
This issue has already been reported [here](https://groups.google.com/g/llvm-dev/c/180LAuFPfKs).

### Steps to reproduce
Compile `./SingleSource/Regression/C/gcc-c-torture/execute/ieee/compare-fp-3.c` with the `-fprofile-instr-generate` flag:
```bash
/llvm-build/bin/clang -O3 -fprofile-instr-generate -Wno-implicit-int -Wno-implicit-function-declaration -fno-trapping-math -o SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o -c /llvm-test-suite/SingleSource/Regression/C/gcc-c-torture/execute/ieee/compare-fp-3.c
```
Link the file (errors will occur in this stage):
```bash
/llvm-build/bin/clang -O3 SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o -o SingleSource/Regression/C/gcc-c-torture/execute/ieee/GCC-C-execute-ieee-compare-fp-3
```

### Working Steps
Compile the same file without the `-fprofile-instr-generate` flag:
```bash
/llvm-build/bin/clang -O3 -Wno-implicit-int -Wno-implicit-function-declaration -fno-trapping-math -o SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o -c /llvm-test-suite/SingleSource/Regression/C/gcc-c-torture/execute/ieee/compare-fp-3.c
```
Link the file:
```bash
/llvm-build/bin/clang -O3 SingleSource/Regression/C/gcc-c-torture/execute/ieee/CMakeFiles/GCC-C-execute-ieee-compare-fp-3.dir/compare-fp-3.c.o -o SingleSource/Regression/C/gcc-c-torture/execute/ieee/GCC-C-execute-ieee-compare-fp-3
```

### The Issue
The issue is that all of the conditionals within the file are supposed
to be optimized out as they all evaluate to false. They do get optimized
out normally, but not when instrumentation is enabled. This probably should
get fixed on the compiler side, but I just submitted a patch on the test
suite side to basically just disable this test whenever compiling with
profililing instrumentation. I opened a patch [here](https://reviews.llvm.org/D128225) to fix the issue within the test suite.