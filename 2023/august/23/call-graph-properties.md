# Call Graph Properties

Yet Another Code Generation System has a lot of different code features that they
use to characterize code. Several of these include call graph specific features.
The call graph features they use are as listed:

1. Number of critical edges in the CFG
2. Number of conditional branches in the method
3. Number of edges in the control flow graph
4. Number of unconditional branches in the method
5. Number of phi nodes

Now going into a bit more detail on how to calculate each of them (along with
definitions where it isn't clear).

### Number of critical edges in the CFG

A critical edge is define as coming from a basic block with multiple successors
and entering a basic block with multiple predecessors. Naive approach for
calculation would be to iterate through all of the successors of a basic block
and count their predecessors. Should be feasible with the `succ_begin` iterator.

### Number of conditional branches

This should just be the sum of the successors of basic blocks that end in a
switch or branch instruction (maybe also include indirect branches?).
This is already implemented in `FunctionPropertiesAnalysis` as
`BlocksReachedFromConditionalInstruction`.

### Number of edges

This should be able to be calculated as just the total number of successors
while iterating through the basic blocks.

### Number of unconditional branches

Should be equivalent to the number of basic blocks that only have a single
successor (does a basic block with a return statement have any successors)?

### Number of phi nodes

Should just be the count of the `phi` instruction.

