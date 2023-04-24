# Reading a map of Basic Block Addresses With Clang/LLVM

It is possible to easily generate a list of all basic blocks using the
`llvm-readobj` tool, but this requires the use of some specific flags at
compile time that are currently only in `clang`. This is the result of
some of the recent propeller work.

### Embedding the Basic Block Map

To embed the basic block map, we use the `-fbasic-block-sections=labels` flag
when compiling with a recent `clang` (14.0+ should work). For example, if we
have a simple C hello world program:

```c
#include <stdio.h>

int main() {
  printf("Hello World\n");
  return 0;
}
```

And we compile it with `clang hello.c -O3 -fbasic-block-sections=labels -o hello`,
and then we look at the sections in the output binary with
`llvm-readobj --sections hello`, we can see the following section:

```
Section {
  Index: 26
  Name: .llvm_bb_addr_map (250)
  Type: SHT_LLVM_BB_ADDR_MAP (0x6FFF4C08)
  Flags [ (0x80)
    SHF_LINK_ORDER (0x80)
  ]
  Address: 0x0
  Offset: 0x3048
  Size: 12
  Link: 14
  Info: 0
  AddressAlignment: 1
  EntrySize: 0
}
```

### Reading the Basic Block Map After Compile Time

Now we can read the basic block map after compile time by again using the
`llvm-readobj` binary, but this time with the `--bb-addr-map` flag. If we
run the following `llvm-readobj --bb-addr-map hello`, we get the following:

```
File: test.o
Format: elf64-x86-64
Arch: x86_64
AddressSize: 64bit
LoadName: <Not found>
BBAddrMap [
  Function {
    At: 0x401130
    Name: main
    BB entries [
      {
        Offset: 0x0
        Size: 0x18
        HasReturn: Yes
        HasTailCall: No
        IsEHPad: No
        CanFallThrough: No
      }
    ]
  }
]
```

It has a list of each basic block in the `BB entries` section. It is also
possible to get all of this to be output in a machine readable format (like
JSON) using the `--elf-output-style=JSON` flag with `llvm-readobj`.