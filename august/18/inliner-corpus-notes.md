# Generating an Inliner corpus with LLVM

* Compiling LLVM with the correct flags is kind of finnicky. Not too sure how everything
works in terms of working with `-Os` or `-Oz`. When `CMAKE_BUILD_TYPE` is set to `MinSizeRel`,
everything gets compiled with `-Os`. This might work with the inlining stuff, but I haven't
gotten that working (probably for other issues though). To get everything to compile with
`-Oz`, you have to use the `llvm_replace_compiler_option` macro in the `CMakeLists.txt` in the
root of the llvm folder of the LLVM monorepo.
* When compiling LLVM, the flag `-disable-llvm-passes` gets put into all of the `.llvmcmd`
sections in the embedded bitcode in the object files. This flag prevents the inliner from
actually running as it operates as a pass and when the flag is present there will be no
log output as the inliner isn't even running. The flag (probably?) needs to get deleted
by tuning some settings in the inlining problem configuration in the python tooling.