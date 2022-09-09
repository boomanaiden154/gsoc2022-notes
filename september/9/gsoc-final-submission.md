# GSOC Final Submission

This document is intended to serve as a summary of the work that I did during
my participation in GSOC 2022. The surrounding repository contains a lot more
information on the details of what I have done.

## Introduction

The LLVM greedy register allocator has an eviction process where when it runs
out of phyiscal registers, it will sometimes analyze whether or not evicting
a live range that has already been assigned to a register would be beneficial.
When the allocator decides that it wants to try evicting a register, it has
to decide if it should evict at all, but also which register to evict. These
decisions are currently guided by manually crafted heuristics. However, some
work has already been done on replacing these heuristics with a ML model
that outputs an eviction decision ([LLVM RFC](https://lists.llvm.org/pipermail/llvm-dev/2021-November/153639.html)).
This model extracts several fairly specific features about each live range,
passes them to a two layer ML model, and then the model outputs which LR
it thinks should be evicted (or the candidate for insertion, in which case
no LRs currently assigned to a physical register get evicted).

## Goals/Motivation

The goal of my project was to expand upon this feature list by experimenting
with per-instruction features to better encompass the context within which an
individual eviction problem resides. Passing exactly what instructions each LR
spans along with the precise frequency of each instruction relative to the rest
of the function could potentially allow for a performance improvement over the
highly engineered features currently being used due to the additional information
the model then has access to about the problem. One of the big concerns with
register allocation is not even how close to optimal graph coloring you can
achieve, but also what to do once you inevitably have to spill to memory.
Being able to pass what instructions are there, and where exactly they are can
aid in making better eviction decisions so that when you have to rewrite
some parts of the function later to spill some registers, you're not getting
as significant of a reduction in performance.

## Results

While I didn't end up improving upon the performance of the regalloc model
like I had originally intended, I did end up getting some fairly interesting
results. Just simply passing in a sum of opcode embeddings per LR for instructions
spanned by that LR doesn't match the performance of the default register
allocator, but the model with just those features does find some value in them
and it is able to achieve less than a 1% regression (looking at the reward metric
of the model only) compared to the default heuristic. A lot of the tooling is
now also present for future experimentation, and there is still significant
room for experimentation, both in what per-instruction features are being
looked at as well as different model architectures. A lot of the data being
extracted more closely resembles time series data, so a model like a LSTM
might provide some performance improvements, or even just making the current
FFNN bigger.

## Summaries of patches written

* Experimentation with per-instruction based features
  * My original project proposal described passing more context of the eviction
  problem to the ML model through the use of graph based features. We quickly
  scaled back from this inital proposal, focusing on just using per-instruction
  features with a model architecture very similar to the existing one. I did a
  significant amount of experimentation in this area and was able to achieve
  some fairly interesting results. Using just instruction opcodes and
  per-instruction MBB frequencies, I was able to train a model to within 0.8%
  of the default heuristic (looking solely at the model reward metrics). While
  I wasn't able to demonstrate any significant performance improvement, or even
  parity with the existing heuristic (some experiments without PGO data enabled
  showed near parity), this does show that these features show some promise,
  and further experimentation might be worthwhile.
    * https://reviews.llvm.org/D131209
    * https://reviews.llvm.org/D131930
    * MBB feature work will be upstreamed after above lands.
* Benchmarking infrastructure
  * In order to be able to quantify how well the regalloc model performs in
  reality (rather than just looking at the reward metrics which can be somewhat
  artifical), a benchmarking system is needed. I improved significantly upon
  the existing benchmarking infrastructure to automate compilation of either
  Chromium performance tests or microbenchmarks from the LLVM test suite and
  also automate the running of the tests using performance counters to quantify
  some key metrics (loads, stores, and instructions) to evaluate regalloc models.
    * https://github.com/google/ml-compiler-opt/pull/47
    * https://github.com/google/ml-compiler-opt/pull/130
* Chromium performance improvements (WIP)
  * By applying the currently shipped regalloc model to the Chromium build
  process, I was able to achieve about a 1% reduction in loads over many of
  the tests present. I am currently working on upstreaming this change, but
  it might not end up going through due to other factors such as the magnitude
  of the performance improvement or impacts on build time.
    * https://chromium-review.googlesource.com/c/chromium/src/+/3731216
* Hyperparameter tuning script for BC case
  * I wrote a script that utilizes a bayesian optimizer to automatically select
  model hyperparameters for the different models, automatically optimizing for
  performance.
    * https://github.com/google/ml-compiler-opt/pull/93
* Feature importance tooling
  * I wrote a script to compute the importance of certain features and present
  the data visually so that insight on what features the model finds important
  and what features the model does not find important is available.
    * https://github.com/google/ml-compiler-opt/pull/109
* Regalloc demo (WIP)
  * I am currently working on writing a demo for the regalloc case, similar to
  the one already available for the inliner case to make the barrier for entry
  for development work on the regalloc model lower.
    * https://github.com/google/ml-compiler-opt/pull/109
* Integration tests (WIP)
  * I worked on integration tests that will most likely eventually be run nightly
  on buildbots to automatically verify that all of our tooling works in the
  workflows that we support for some of the projects that consume our work to
  validate our code beyond the unit testing that we already do.
    * https://github.com/google/ml-compiler-opt/pull/121
* Minor patches
  * TFUtils error checking on the LLVM side to ensure all features are getting
  passed to the model
    * https://reviews.llvm.org/D133451
  * NFC patch to make a function used in LR priority calculation more clear/
  better documented
    * https://reviews.llvm.org/D133386
  * Bug fix to ensure that an error is thrown when compiling IR with PGO data,
  but the PGO data can't be loaded (eg due to a bad file path)
    * https://reviews.llvm.org/D132991
  * Bug fix to make sure the `-cc1` flag gets added to the `.llvmcmd` section
  of object files when bitcode embedding is enabled and clang/LLVM has been
  built with assertions enabled
    * https://reviews.llvm.org/D130620
  * Bug fix to fix some nondeterministic behavior from the autogenerated
  regalloc test model, taking advantage of some previous work done making it
  possible to extract more features than the model needs
    * https://reviews.llvm.org/D129254
  * Minor changes in the demo to make note of some nuances and make it
  functional
    * https://github.com/google/ml-compiler-opt/pull/22
    * https://github.com/google/ml-compiler-opt/pull/19
  * Slight modification of ML tooling to allow for training the regalloc
  model in the non-thinLTO case.
    * https://github.com/google/ml-compiler-opt/pull/23
    * https://github.com/google/ml-compiler-opt/pull/24
  * Config changes to fix the regalloc BC training and refactoring to
  ensure a similar error doesn't occur again
    * https://github.com/google/ml-compiler-opt/pull/27
    * https://github.com/google/ml-compiler-opt/pull/29
  * Add config options for vocab generation to prevent excessive RAM usage
  from features that don't need to be normalized
    * https://github.com/google/ml-compiler-opt/pull/30
  * Minor CI changes/Dockerization stuff
    * https://github.com/google/ml-compiler-opt/pull/51
    * https://github.com/google/ml-compiler-opt/pull/59
    * https://github.com/google/ml-compiler-opt/pull/49
    * https://github.com/google/ml-compiler-opt/pull/78
    * https://github.com/google/ml-compiler-opt/pull/92
    * https://github.com/google/ml-compiler-opt/pull/122
    * https://github.com/google/ml-compiler-opt/pull/123
    * https://github.com/google/ml-compiler-opt/pull/124
    * https://github.com/google/ml-compiler-opt/pull/128
  * Move the option configuring the number of modules to compile per policy
  iteration to the appropriate gin configs to enhance reproducibility
    * https://github.com/google/ml-compiler-opt/pull/53
  * Made the logging interval adjustable for the tensorboard data to achieve
  a significant speedup, especially during BC training.
    * https://github.com/google/ml-compiler-opt/pull/62
  * Moved additional/deleted flags to each case's problem configuration so
  that they could get picked up by the default trace tooling in preparation
  for using development features gated by a flag on the LLVM side
    * https://github.com/google/ml-compiler-opt/pull/84
  * Explicitly set TF logging level to get rid of a bunch of tensorflow
  logging info that provides no useful info and actively prevents viewing
  data from previous policy iterations
    * https://github.com/google/ml-compiler-opt/pull/93
  * Chromium patch to allow for corpus extraction in the non-thinLTO case
    * https://github.com/google/ml-compiler-opt/pull/117
    * https://chromium-review.googlesource.com/c/chromium/src/+/3731216
  * Update inling demo to work with TFLite
    * https://github.com/google/ml-compiler-opt/pull/131