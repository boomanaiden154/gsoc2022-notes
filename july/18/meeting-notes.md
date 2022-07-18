# Meeting 7/17/22

### Agenda
* Performance improvements
    * Tensorboard interval seems to work pretty well
    * Other performance improvements have pretty much been a bust
        * tf.function, jit_compile
        * command line settings
    * Probably still performance on the table though
        * CPU/GPU doesn't necessarily seem to be pinned,
        at least beside just looking at htop
* Model training
    * Worked on training a new base model this week to test some
    changes, num_modules patch definitely seems to work
    * What should my reward curves look like for the lower
    percentiles (eg 0.1/1/5/10 percent lows)?
* Compute resources
    * Status update on GCP quota/funding
    * Experimentation with dask/distributed compiling?
* Midterm evaluations
    * Verbal discussion, how are things going?
* Future directions for next week
    * Model training/benchmarking
    * Refactoring tf_agents network to change how
    preprocessing works (passing multiple variables
    to a single preprocessing layer)