# LLVM not passing cc1 flag into .llvmcmd sections in bitcode files when assertions are enabled

### Probable culprit

https://github.com/llvm/llvm-project/blob/main/clang/lib/Frontend/CompilerInvocation.cpp#L647
Seems like it could be here. This function changes behvaior when assertions are enabled
so that it can do additional checks on stuff. But the `Parse` function that is actually
processing the arguments seems to get called with the same arguments for both of the
actual invocations that matter.

### Highly Probable culprit

Changing the value of `DoRoundTripDefault` to `false` regardless of what the debug preprocessor
defines are set to fixes the issue, suggesting this function specifically is what is causing
the problem. Still need to figure out why exactly the value is changing between different
calls of `Parse` with the same exact arguments passed in, but at least we have some progress.

### The actual culprit

Currently in `CompilerInvocation::CreateFromArgs`, the generate function that is used to call
`RoundTrip` calls `CompilerInvocation::generateCC1CommandLine`. This function has documentation
stating "Note that the caller is responsible for inserting the path to the clang executable 
and "-cc1" if desired". However, the "-cc1" flag is never passed.