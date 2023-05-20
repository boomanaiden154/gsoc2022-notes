# Building LLVM with LLVM libc

I've recently worked on getting LLVM to build with LLVM libc in overlay mode.
Here are some performance comparisons:

Baseline Clang building LLVM:
```
real    4m8.886s
user    338m42.503s
sys     12m23.312s
```

Clang built with LLVM libc building LLVM:
```
real    4m0.337s
user    327m36.122s
sys     11m47.184s
```

There isn't a significant difference and on of the runs that I forgot to record
using Clang linked to LLVM libc was within half a second of the baseline. Hard
to really determine the true difference without more runs and statistical
analysis though.

I've opened up some patches to get this working upstream, as it will still be
nice to have even if there aren't any performance gains currently.
* [Patch 1](https://reviews.llvm.org/D151011)
* [Patch 2](https://reviews.llvm.org/D151013)

Here are the current test regressions between a standard build and a build with
LLVM libc:

```
AddressSanitizer-x86_64-linux-dynamic :: TestCases/Linux/asan_preload_test-1.cpp
AddressSanitizer-x86_64-linux-dynamic :: TestCases/Linux/asan_preload_test-2.cpp
AddressSanitizer-x86_64-linux-dynamic :: TestCases/Linux/asan_rt_confict_test-1.cpp
AddressSanitizer-x86_64-linux-dynamic :: TestCases/Linux/preinstalled_signal.cpp
Clang :: Driver/Wframe-larger-than.c
Clang :: Driver/cc-print-options.c
Clang :: Driver/cpath.c
Clang :: Driver/crash-report-clang-cl.cpp
Clang :: Driver/crash-report-header.h
Clang :: Driver/crash-report-modules.m
Clang :: Driver/crash-report-spaces.c
Clang :: Driver/crash-report.cpp
Clang :: Driver/driverkit-path.c
Clang :: Driver/hip-temps-linux.hip
Clang :: Driver/modules.cpp
Clang :: Driver/no-canonical-prefixes.c
Clang :: Driver/response-file.c
Clang :: Index/crash-recovery-modules.m
Clang :: Index/crash-recovery.c
Clang :: Index/create-libclang-parsing-reproducer.c
Clang :: Index/record-parsing-invocation.c
Clang :: Modules/Werror-Wsystem-headers.m
Clang :: Modules/compiler_builtins.m
Clang :: Modules/context-hash.c
Clang :: Modules/crash-vfs-path-emptydir-entries.m
Clang :: Modules/crash-vfs-path-symlink-component.m
Clang :: Modules/crash-vfs-path-symlink-topheader.m
Clang :: Modules/crash-vfs-path-traversal.m
Clang :: Modules/crash-vfs-relative-overlay.m
Clang :: Modules/crash-vfs-umbrella-frameworks.m
Clang :: Modules/cstd.m
Clang :: Modules/darwin_specific_modulemap_hacks.m
Clang :: Modules/dependency-gen.m
Clang :: Modules/pch-used.m
Clang-Unit :: Basic/./BasicTests/SarifDocumentWriterTest/checkSerializingResultsWithCustomRuleConfig
LLVM :: CodeGen/AArch64/GlobalISel/select-to-fmin-fmax.ll
LLVM :: CodeGen/AArch64/aarch64-dup-dot-crash.ll
LLVM :: CodeGen/AArch64/aarch64-matrix-umull-smull.ll
LLVM :: CodeGen/AArch64/aarch64-neon-vector-insert-uaddlv.ll
LLVM :: CodeGen/AArch64/aarch64-smax-constantfold.ll
LLVM :: CodeGen/AArch64/abd-combine.ll
LLVM :: CodeGen/AArch64/argument-blocks-array-of-struct.ll
LLVM :: CodeGen/AArch64/arm64-build-vector.ll
LLVM :: CodeGen/AArch64/arm64-fast-isel-materialize.ll
LLVM :: CodeGen/AArch64/arm64-fmax.ll
LLVM :: CodeGen/AArch64/arm64-fp-contract-zero.ll
LLVM :: CodeGen/AArch64/arm64-memset-inline.ll
LLVM :: CodeGen/AArch64/arm64-neon-copy.ll
LLVM :: CodeGen/AArch64/arm64-raddhn-combine.ll
LLVM :: CodeGen/AArch64/arm64-rev.ll
LLVM :: CodeGen/AArch64/arm64-vabs.ll
LLVM :: CodeGen/AArch64/arm64-vector-ext.ll
LLVM :: CodeGen/AArch64/arm64-vector-insertion.ll
LLVM :: CodeGen/AArch64/arm64-vector-ldst.ll
LLVM :: CodeGen/AArch64/arm64-vshift.ll
LLVM :: CodeGen/AArch64/arm64-zip.ll
LLVM :: CodeGen/AArch64/arm64ec-varargs.ll
LLVM :: CodeGen/AArch64/bitcast.ll
LLVM :: CodeGen/AArch64/build-one-lane.ll
LLVM :: CodeGen/AArch64/build-vector-extract.ll
LLVM :: CodeGen/AArch64/build-vector-to-extract-subvec-crash.ll
LLVM :: CodeGen/AArch64/combine-mul.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-f16-mul.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-f32-mul.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-f64-mul.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-mixed-cases.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-multiuses.ll
LLVM :: CodeGen/AArch64/complex-deinterleaving-uniform-cases.ll
LLVM :: CodeGen/AArch64/ext-narrow-index.ll
LLVM :: CodeGen/AArch64/extend_inreg_of_concat_subvectors.ll
LLVM :: CodeGen/AArch64/f16-imm.ll
LLVM :: CodeGen/AArch64/fcvt_combine.ll
LLVM :: CodeGen/AArch64/fp16-vector-nvcast.ll
LLVM :: CodeGen/AArch64/fpclamptosat_vec.ll
LLVM :: CodeGen/AArch64/fptosi-sat-vector.ll
LLVM :: CodeGen/AArch64/hadd-combine.ll
LLVM :: CodeGen/AArch64/implicitly-set-zero-high-64-bits.ll
LLVM :: CodeGen/AArch64/ldst-opt.ll
LLVM :: CodeGen/AArch64/load-insert-zero.ll
LLVM :: CodeGen/AArch64/mattr-all.ll
LLVM :: CodeGen/AArch64/memset-inline.ll
LLVM :: CodeGen/AArch64/merge-store-dependency.ll
LLVM :: CodeGen/AArch64/movid-no-neon.ll
LLVM :: CodeGen/AArch64/neon-compare-instructions.ll
LLVM :: CodeGen/AArch64/neon-dotreduce.ll
LLVM :: CodeGen/AArch64/neon-fma-FMF.ll
LLVM :: CodeGen/AArch64/neon-rshrn.ll
LLVM :: CodeGen/AArch64/neon-vcmla.ll
LLVM :: CodeGen/AArch64/pr-cf624b2.ll
LLVM :: CodeGen/AArch64/ragreedy-local-interval-cost.ll
LLVM :: CodeGen/AArch64/reduce-or.ll
LLVM :: CodeGen/AArch64/reduce-xor.ll
LLVM :: CodeGen/AArch64/remat-float0.ll
LLVM :: CodeGen/AArch64/select_cc.ll
LLVM :: CodeGen/AArch64/selectiondag-order.ll
LLVM :: CodeGen/AArch64/sinksplat.ll
LLVM :: CodeGen/AArch64/srem-seteq-vec-splat.ll
LLVM :: CodeGen/AArch64/srem-vector-lkk.ll
LLVM :: CodeGen/AArch64/sve-calling-convention-mixed.ll
LLVM :: CodeGen/AArch64/sve-fixed-length-masked-gather.ll
LLVM :: CodeGen/AArch64/sve-fixed-length-masked-loads.ll
LLVM :: CodeGen/AArch64/sve-fixed-length-masked-scatter.ll
LLVM :: CodeGen/AArch64/sve-fixed-length-masked-stores.ll
LLVM :: CodeGen/AArch64/sve-streaming-mode-fixed-length-stores.ll
LLVM :: CodeGen/AArch64/swifterror.ll
LLVM :: CodeGen/AArch64/tbl-loops.ll
LLVM :: CodeGen/AArch64/urem-seteq-vec-splat.ll
LLVM :: CodeGen/AArch64/urem-vector-lkk.ll
LLVM :: CodeGen/AArch64/vec_umulo.ll
LLVM :: CodeGen/AArch64/vecreduce-add-legalization.ll
LLVM :: CodeGen/AArch64/vecreduce-add.ll
LLVM :: CodeGen/AArch64/vecreduce-fadd.ll
LLVM :: CodeGen/AArch64/vecreduce-umax-legalization.ll
LLVM :: CodeGen/AArch64/vector-insert-shuffle-cycle.ll
LLVM :: CodeGen/AArch64/wide-scalar-shift-by-byte-multiple-legalization.ll
LLVM :: CodeGen/AArch64/wide-scalar-shift-legalization.ll
LLVM :: CodeGen/AArch64/zero-call-used-regs.ll
LLVM :: CodeGen/AArch64/zext-to-tbl.ll
LLVM :: CodeGen/AMDGPU/amdpal-callable.ll
LLVM :: CodeGen/AMDGPU/shl.ll
LLVM :: CodeGen/RISCV/double-zfa.ll
LLVM :: CodeGen/RISCV/float-zfa.ll
LLVM :: CodeGen/RISCV/half-zfa-fli.ll
LLVM :: CodeGen/RISCV/rvv/vsplats-zfa.ll
LLVM :: MC/AArch64/basic-a64-instructions.s
LLVM :: MC/RISCV/zfa-valid.s
LLVM :: tools/llvm-mca/AArch64/Exynos/zero-latency-move.s
LLVM :: tools/llvm-size/response-file.test
LLVM-Unit :: Support/./SupportTests/CommandLineTest/ArgumentLimit
LLVM-Unit :: Support/./SupportTests/JSONTest/Constructors
LLVM-Unit :: Support/./SupportTests/JSONTest/Integers
LLVM-Unit :: Support/./SupportTests/JSONTest/Stream
LLVM-Unit :: Support/./SupportTests/JSONTest/Types
LLVM-Unit :: Support/./SupportTests/ScopedPrinterTest/PrintNumber
```

There are quite a few and they definitely need to be investigated, but that's
for another time currently.
