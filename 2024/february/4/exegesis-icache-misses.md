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

Doesn't seem to be an interaction with the flag registers.

### In-process vs subprocess benchmarking mode

The in-process benchmark seems to not suffer from this issue with it being able
to produce results that are still slightly noisy, but around 0.25 cycles per instruction
for the first snippet listed above (cmpl with a R32 operand and an i8 operand), which
matches closely with the info provided by uops.info for cascade lake. It fluctuates
around probably +-0.05 cycles per iteration, with some dipping below 0.25. That seems
like a separate issue however.

The memory setup for the subprocess execution mode is slightly different and it doesn't
really make sense that that is what is causing it, but maybe it is. The number if icache
misses between the two benchmarking modes actually seems pretty similar.
