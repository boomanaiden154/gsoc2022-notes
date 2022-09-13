# Meeting Notes 9/12/22

* Chromium patch in `ml-compiler-opt`
  * Should be good to merge immediately
* Regalloc NFC patch
  * Should be good to merge
* Chromium patch
  * Need to ping Hans about doing the clang updates, conversation/discussion
  can continue in the patch review
* Clang IR patch
  * Should be pretty much good to land, but ping Rong and have him look
  at it again.
* Feature importance patch/BC hyperparam tuning patch
  * Yundi wants to review, should be able to go through soon
* LLD issue
  * Investigate why there's a difference in the build process between the
  Chromium Linux build and the Chromium Android build. This might give us
  some more information.
  * If I can't get this figured out over about the next week, just open up
  an issue in the LLVM bug tracker with a minimal reproducer
* Oz inlining demo update
  * Should be able to go through soon.
* Regalloc demo
  * Dependent upon LLD stuff for now
* Lockfile patch
  * Need to address comments
* Instruction features patch
  * Need to address comments from Mircea
* Benchmarking infra
  * Should be good to go soon
* LLVM Meetup
  * Going to be epic.
* Adding my config/gin configs to the repository
  * Should be able to add it into a folder adjacent to the current regalloc
  stuff