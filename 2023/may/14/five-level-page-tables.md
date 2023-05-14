# Five Level Page Tables

Detecting whether or not five level page tables are enabled can be important
for certain operations. This can be done through a couple of different methods
and there are a couple things to note.

Within the Linux kernel documentation, they note that they don't allocate anything
beyond the 4-level virtual address space ceiling currently due to some JITs using
those bits to represent certain things.

### Detection Method 1

First off, we can detect if five level page tables are supported on the CPU and
enabled by calling `mmap()` with `MAP_FIXED`, setting the address to something higher
than the ceiling of the virtual address space for four level page tables. If it fails,
we know that we only have four level page tables enbaled/supported, and if it passed,
we know that we have five level page tables enabled and supported.

### Detection Method 2

We can also detect five level page tables explicitly on Linux by checking for a
flag in the kernel config, CPU support for five level page tables, and whether
or not five level page tables are disabled on the kernel command line.

#### Detecting CPU support

The name for the flag in X86 (Intel at least) CPUs for five level page table
support os `LA57`.

To detect CPU support, we can check for the `LA57` support in a couple of
different places. First off, (probably the canonical way in C), we can use
`cpuid` infrastructure. There is the `X86_FEATURE_LA57` feature macro in the
`cpufeatures.h` header on Linux, and there is a `__cpuid_count` function defined
in `cpuid.h` (compiler provided header). Using these, we can get whether or
not the CPU supports five level page tables.

We can also test CPU support by looking for the `la57` string in `/proc/cpuinfo`.
If it's there, we have five level page table support.

#### Detecting Kernel Support

In addition to CPU support, the current running kernel version also needs to
support five level page tables. We can check for this by seeing if the kernel
was compiled with five level page table support and that this hasn't been
disabled on the kernel command line.

To see if the kernel was compiled with five level page table support, we can
check the kernel config. If the `CONFIG_X86_5LEVEL=y` flag shows up, we know
that we have five level page table support. The kernel config is usually stored
in `/boot/config-$(uname -r)`, but it can also sometimes be found (in a
compressed form) under `/proc/config.gz`. Note that displaying the config in these
places is very distro dependent. To have the config under `/proc` requires kernel
support, and not all distros will place the config in `/boot`.

In addition, we need to make sure that five level page table support hasn't
been disabled using the kernel command line. This can be achieved by simply
trying to find the `no5lvl` flag in the kernel command line, which lives under
`/proc/cmdline`.

#### Notes

Note also that looking at CPU capabilities in `/proc/cpuinfo` won't show the `la57`
capability if there is no compile time support for five level page tables. However,
this doesn't impact what we can get from calling `cpuinfo` directly.

The best course of action is to just do a test as outlined in the first detection
method, and if something static is desired, just going through `/proc/cpuinfo` is
probably the best method because if `la57` shows up under the CPU features, it means
that there is both kernel support and CPU support, in addition to the feature not
being disabled through the kernel command line.

### References

1. [Linux kernel cpufeatures.h](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/arch/x86/include/asm/cpufeatures.h)
2. [Clang cpuid.h](https://clang.llvm.org/doxygen/cpuid_8h_source.html)
3. [Kernel Five Level Paging Doc](https://www.kernel.org/doc/Documentation/x86/x86_64/5level-paging.rst)
4. [Kernel X86 cpuinfo Doc](https://www.kernel.org/doc/Documentation/x86/cpuinfo.rst)
