```
# LLVM-EXEGESIS-DEFREG R15 12345600
cmpl $1, %r15d
```

```
# LLVM-EXEGESIS-DEFREG R15 12345600
addl $1, %r15d
```

The first one throws way more icache misses than the second.

```
# LLVM-EXEGESIS-DEFREG R15 12345600
nop
cmpl $1, %r15d
```

Does fix the issue with cache misses, but impacts the throughput.

Notably, both the `addl` and `cmpl` presneted are encoded in the same number of bytes,
perhaps suggesting that this isn't a code alignment issue.

Changing the instruction the 4-byte immediate variant does make things more consistent (less
cache misses). That is a 7-byte instruction.

The inverse throughput of `cmpl` with a one byte immediate should be 0.25 cycles according to
uops.info.

Certain instructions just seem to screw everything up. More investigation needed.

Interaction with the flags registers?
