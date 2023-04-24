# Meeting Notes for 4/25/23

* Hacky implementation in `llvm-exegesis` is mostly ready. Just needs a couple
  minor details to be finalized and then a lot of polishing/splitting up changes. 
  Should be ready for upstreaming in a week or two.
  * Has become a pretty invasive change. Will need to be careful to not break
    anyone else's workflow. Thinking about trying to make it an opt-in through
    a CLI flag at first, not sure how difficult that will end up being.
  * Probably will post an update to the RFC soon since implementation details
    are more fleshed out at this point.
  * A decent amount of the code is architecture dependent. Will need to somehow
    coordinate effort there if we want to make this the default. Getting
    AArch64 working probably won't be too bad (although I don't have access
    to hardware), but there is also PPC and MIPS support in tree. Getting stuff
    setup through QEMU might work though, but I would prefer to avoid.
* No updates on getting GRANITE/UICA ready for MLGO training integration.
  Planning on working on that soon, hopefully this week, probably after I push
  the llvm-exegesis work.
* Fixed the weird segfault issue that I mentioned to Ondrej. It had to do with
  glibc automatically calling the `rseq` system call during initialization.
* Maybe post an RFC on what platforms llvm-exegesis supports? There are things
  like preprocessor directives to deal with different intrinsic headers on
  Windows.
* Updates on cost modelling work. Not perfect on a benchmark with no l1 cache
  misses or branch mispredicts, but varying front-end conditions (even run
  to run) seems to be the main factor that significantly impacts the accuracey. 
* EuroLLVM?
