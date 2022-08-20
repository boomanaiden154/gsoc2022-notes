# Experiments 8/19/2022

* Experiment 30
    * Experiment 30 was designed to test the effects of having PGO flags versus not having them as
    passing `-fembed-bitcode=all` doesn't pass profile flags into the `.llvmcmd` section which I just
    realized last night. My chromium corpus has PGO enabled, but none of the flags are in `.llvmcmd`
    section, so they weren't used for actual training. Overall mean differences seem to be pretty
    stark with a model trained on a PGO corpus getting about twice the performance assuming I
    set everything up correctly. 
    * Shows that I definitely need to prioritize getting `-Xclang=-fembed-bitcode=all` working on
    the chromium corpus (although I could probably just add additional profile flags after the
    fact). For some reason the chromium clang refuses to use that flag. More testing needed in
    that area. Everything works with an external toolchain.
* Experiment 31
    * Same experiment as above, except this time testing on a chromium corpus and testing against
    one of the replicates from experiment 7 rather than running the test twice and changing some
    variables. Seems like the two techniques on the chromium corpus are pretty comparable, or the
    non-pgo settings even slightly outperform the pgo settings (assuming I have everything setup
    correctly).