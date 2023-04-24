# Dumping Basic Blocks

Using the `clang`/`llvm-readobj` tooling discussed in the last
(`basic-block-address-map.md`) article, it is pretty easy to get the exact
location and size of individual basic blocks along with a mapping to their
functions. However, this only works in final executables due to the fact
that a lot of the code in an individual object file is relocatable before
the linking phase. Should just be an implementation detail to get this
tooling working the way we need it within upstream LLVM though and it should
be a fairly concise implementation at that. Here are some of my notes on
getting this process working since getting all of the addresses and offsets
correct is slightly more complicated than in the executable (currently
supported) case.

### The Motivating Example

For this article, we're going to use the following C program:

```c
#include <stdio.h>

int a(int input) {
  return input * 2;
}

int main() {
  int input;
  scanf("%d", &input);
  if(a(input) == 4) {
    printf("answer is 4");
  } else {
    printf("answer is not 4");
  }
}
```

It has two functions to illustrate some functionality and it also has some
if statements within the `main()` function so that we have multiple basic
blocks within the same function. All in all, this simple test program should
have four basic blocks. There's one basic block in `a()` that just performs
the multiplication, and then there's three basic blocks in `main()`, one to
grab input from the user, another that runs if the answer is four, and another
that runs if the answer is not four. When we compile with the following
command:

```bash
clang test.c -fbasic-block-sections=labels -o test
```

And then run the following command to see the basic block map,

```bash
llvm-readobj --bb-addr-map test
```

We can see the actual addresses, offsets, and sizes of each of the basic blocks
in a per-function context:

```
File: ./test
Format: elf64-x86-64
Arch: x86_64
AddressSize: 64bit
LoadName: <Not found>
BBAddrMap [
  Function {
    At: 0x401150
    Name: a
    BB entries [
      {
        Offset: 0x0
        Size: 0x4
        HasReturn: Yes
        HasTailCall: No
        IsEHPad: No
        CanFallThrough: No
      }
    ]
  }
  Function {
    At: 0x401160
    Name: main
    BB entries [
      {
        Offset: 0x0
        Size: 0x5F
        HasReturn: No
        HasTailCall: No
        IsEHPad: No
        CanFallThrough: Yes
      }
      {
        Offset: 0x5F
        Size: 0x7
        HasReturn: Yes
        HasTailCall: No
        IsEHPad: No
        CanFallThrough: No
      }
      {
        Offset: 0x66
        Size: 0x5
        HasReturn: No
        HasTailCall: No
        IsEHPad: No
        CanFallThrough: No
      }
    ]
  }
]
```

### Basic Block Address Maps in Object Files

This works after I landed a couple upstream changes a while ago.
