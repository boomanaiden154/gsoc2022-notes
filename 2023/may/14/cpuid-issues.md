# CPUID call implementation weirdness

While going through some information on CPUID calls within C code for figuring
out platform support for five level page tables, I came across some odd
calls to CPUID within compiler provided headers and Chromium. They all do
slightly different things and it was hard to figure out who was doing what,
why they were doing what they were doing, and whether or not these implementations
could be simplified/if any were incorrect. This is some documentation of
my findings.

### Chromium CPUID implementation

Chromium has the following implementation for calling CPUID:

```c
#if !defined(COMPILER_MSVC)

#if defined(__pic__) && defined(__i386__)

void __cpuid(int cpu_info[4], int info_type) {
  __asm__ volatile(
      "mov %%ebx, %%edi\n"
      "cpuid\n"
      "xchg %%edi, %%ebx\n"
      : "=a"(cpu_info[0]), "=D"(cpu_info[1]), "=c"(cpu_info[2]),
        "=d"(cpu_info[3])
      : "a"(info_type), "c"(0));
}

#else

void __cpuid(int cpu_info[4], int info_type) {
  __asm__ volatile("cpuid\n"
                   : "=a"(cpu_info[0]), "=b"(cpu_info[1]), "=c"(cpu_info[2]),
                     "=d"(cpu_info[3])
                   : "a"(info_type), "c"(0));
}

#endif
#endif  // !defined(COMPILER_MSVC)
```

This only creates the definitions if we aren't using MSVC (where they're
using the compiler provided implementation), and there is one particularly
unique thing. Particularly the fact that they're zeroing the `%ecx`/`%rcx`
register when calling `cpuid`. The specific change that created the zeroing
of this register was introduced in [this](https://codereview.chromium.org/2611683002)
patch. It was noted that sometimes the value of `cpuid` depends upon the
value in the `%ecx` register and they were getting incorrect results most
of the time because they weren't zeroing it, specifically when detecting AVX
support. This is confirmed by checking the Intel architecture manual and looking
at the section that includes the AVX calls (`07H` within Chromium/Intel
X86 CPUs). The manual does mention that this specific section depends upon the
value of `%ecx`, with different values of `%ecx` returning different "subleafs".

### Clang CPUID implementation

Within Clang's `cpuid.h`, there is another implementation:

```c
#if __i386__
#define __cpuid(__leaf, __eax, __ebx, __ecx, __edx) \
    __asm("cpuid" : "=a"(__eax), "=b" (__ebx), "=c"(__ecx), "=d"(__edx) \
                  : "0"(__leaf))

#define __cpuid_count(__leaf, __count, __eax, __ebx, __ecx, __edx) \
    __asm("cpuid" : "=a"(__eax), "=b" (__ebx), "=c"(__ecx), "=d"(__edx) \
                  : "0"(__leaf), "2"(__count))
#else
/* x86-64 uses %rbx as the base register, so preserve it. */
#define __cpuid(__leaf, __eax, __ebx, __ecx, __edx) \
    __asm("  xchgq  %%rbx,%q1\n" \
          "  cpuid\n" \
          "  xchgq  %%rbx,%q1" \
        : "=a"(__eax), "=r" (__ebx), "=c"(__ecx), "=d"(__edx) \
        : "0"(__leaf))

#define __cpuid_count(__leaf, __count, __eax, __ebx, __ecx, __edx) \
    __asm("  xchgq  %%rbx,%q1\n" \
          "  cpuid\n" \
          "  xchgq  %%rbx,%q1" \
        : "=a"(__eax), "=r" (__ebx), "=c"(__ecx), "=d"(__edx) \
        : "0"(__leaf), "2"(__count))
#endif
```

This one has a slightly different signature, but it doesn't zero out the `%ecx`
register for `__cpuid`. It seems like you're supposed to use the `__cpuid_count`
function if you want to be able to deterministically get access to specific
subleafs from the `cpuid` instruction.

### GCC CPUID implementation

```c
#ifndef __x86_64__
/* At least one cpu (Winchip 2) does not set %ebx and %ecx
   for cpuid leaf 1. Forcibly zero the two registers before
   calling cpuid as a precaution.  */
#define __cpuid(level, a, b, c, d)                    \
  do {                                    \
    if (__builtin_constant_p (level) && (level) != 1)            \
      __asm__ __volatile__ ("cpuid\n\t"                    \
                : "=a" (a), "=b" (b), "=c" (c), "=d" (d)    \
                : "0" (level));                \
    else                                \
      __asm__ __volatile__ ("cpuid\n\t"                    \
                : "=a" (a), "=b" (b), "=c" (c), "=d" (d)    \
                : "0" (level), "1" (0), "2" (0));        \
  } while (0)
#else
#define __cpuid(level, a, b, c, d)                    \
  __asm__ __volatile__ ("cpuid\n\t"                    \
            : "=a" (a), "=b" (b), "=c" (c), "=d" (d)    \
            : "0" (level))
#endif
```

GCC's `__cpuid` implementation is probably the weirdest. There are some odd
idioms that don't really seem to serve any purpose (the `do {} while (0)` loop
in the 32 bit x86 implementation), but this one does zero the `%ecx` register!
However, the reasoning is completely different from why Chromium does so, with
this specifically being patched in gblic so that an older target that conformed
to the specification at the time that was less restrictive would still work. The
mailing list thread for the patch is available [here](https://gcc.gnu.org/pipermail/gcc-patches/2019-May/521977.html).

GCC also implements a `__cpuid_count` function similar to Clang that provides
the exact same functionality, also allowing specification of the specific
subleaf that is being used:

```c
#define __cpuid_count(level, count, a, b, c, d)				\
  __asm__ __volatile__ ("cpuid\n\t"					\
			: "=a" (a), "=b" (b), "=c" (c), "=d" (d)	\
			: "0" (level), "2" (count))
```

However, in addition to this, GCC also provides a `__cpuidex` function later on
that provides a syntax more similar to Chromium's that exactly matches the
signature that MSVC has:

```c
static __inline void
__cpuidex (int __cpuid_info[4], int __leaf, int __subleaf)
{
  __cpuid_count (__leaf, __subleaf, __cpuid_info[0], __cpuid_info[1],
		 __cpuid_info[2], __cpuid_info[3]);
}
```

I'm presuming that this function was implemented for compatibility with code
that also needs to be compiled on Windows with MSVC.

### MSVC CPUID implementation

I don't have MSVC headers handy, so I can't look at the source, but MSVC defines
the following functions:

```c
void __cpuid(
   int cpuInfo[4],
   int function_id
);

void __cpuidex(
   int cpuInfo[4],
   int function_id,
   int subfunction_id
);
```

`__cpuid` as normal, and the `__cpuidex` function that we saw also in the GCC
source. Given that the original Chromium patch reports that Windows targets
seemed to be detecting AVX just fine, the implementation of `__cpuid` on Windows
either zeroes out the `%ecx` register before use, or there is some difference in
a calling convention or something that is causing this change. I'm not sure which
and I'm not particularly interested in investgating it.

### Why does Chromium not user the compiler provided functions?

The main question that was nagging me the most after I learned about the compiler
provided functions in `cpuid.h` was why Chromium wasn't using them. Why they didn't
use them originally I can't really say. Clang doesn't seem to have great compatibility
with other toolchains here. In addition, the syntax is different between GCC/Clang
and MSVC with the function signature for `__cpuid` being different, which might have
been the main reason. Or the developers might just not have known about it. However,
with the `__cpuidex` function, the signatures are the same and it fixes the issue
found earlier that had to be patched by moving to a completely non-standard
`__cpuid` implementation.

### Fixes?

Given that I've already gone down the rabbit hole, I have an idea for how to
make this situation a little bit better. I plan on doing it in two stages:

1. Implement `__cpuidex` within Clang's `cpuid.h`. This will help with being
compatible with GCC in addition to MSVC compatibility and will enable the next
patch. This should be a pretty small and simple patch.
2. Fix up the specific code used in Chromium to use the compiler provided
functions once the clang toolchain gets rolled to one that includes the
`cpuid.h` patches. The main concern here would be how compatible this is
across toolchains, but Chromium only has first class support for ToT clang
as far as I can tell, so getting this through should be fine. Most recent
versions of GCC should also work given that the patch introducing `__cpuidex`
into GCC's `cpuid.h` landed about three years ago.
