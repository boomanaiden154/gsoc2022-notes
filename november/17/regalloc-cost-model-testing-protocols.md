# Regalloc cost model testing protocols

Using the docker files in my `dev-docker-vm-sh` repository or whatever it is
called, specifically the `llvm-pgo-corpus` file. Using some scripts there too,
particularly the `bc_train.sh` script just to automate some of the process.

1. Generating a couple different test models so that we can get some different
register allocations. I'm just doing BC training rather than any reinforcment
learning. I'm also changing the number of iterations for the BC training for
each model that I'm planning on using. Planning on doing one model at 10000
training iterations, one at 5000, one at 2500, one at 1000, and one at 500.
The default trace is regenerated every time, with it currently set to
operate over the entire corpus.
    1. It looks like this technique/protocol will need to be adjusted a little
    bit. After doing this and then compiling a moderate benchmarking example
    with the different models, across five models I'm only getting three different
    register allocations (as shown through the `sha1sum` of each generated
    executable). Maybe just taking the same default trace and training for like
    one iteration (or just completely randomizing) the weights would work a
    lot better.
