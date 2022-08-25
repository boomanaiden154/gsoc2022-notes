# Experiments 8/25/22

* Experiment 40 (https://drive.google.com/file/d/1i0YE9pDldkJTYpfX19uUXr1zS7JjUa56/view?usp=sharing)
    * Default example on a chromium corpus without PGO data being based to the compiler
    when running the MLGO training. Everything was default except for the fact that the
    RL training was only performed for 100 policy iterations (20k total iterations).
* Experiment 41 (https://drive.google.com/file/d/1-_bqTdjxie4hH9BrIlb_dUTS3O8hKPPb/view?usp=sharing)
    * Same as above, except the profdata paths were set correctly and the compiler was
    allowed to use the prof data.

### Conclusions

With PGO data set correctly, the model does seem to get a slight edge over the model
without PGO data, but the difference isn't super big in the chromium case. Difference
was much larger when looking at the same experiment over a LLVM corpus.