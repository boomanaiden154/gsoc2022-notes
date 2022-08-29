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

## Further experimens with new features

* Experiment 43 (https://drive.google.com/file/d/1JTtjlQYNas1OfjuoBSYtWRb7w1sW70O9/view?usp=sharing)
    * Only new instruction based features. Only BC training. Batch size was set to 1024 and the
    learning rate was set to 0.005. Definitely did learn, but no astounding results or anything.
* Experiment 44 (https://drive.google.com/file/d/1B2BJ_7zWG84AV1JYnOzmzpS_dqvZeVXM/view?usp=sharing)
    * Same hyperparameters for BC training as above, but this time with MBB frequencies added in.
    They were bucketized into 100 different buckets and then those buckets were piped into an
    embedding layer before getting multiplied by the mapping matrix to map everything. Then
    they were concatenated with the instruction based features. Very similar performance to the
    model above, suggesting that at least the way everything is implemented currently, the MBB
    features didn't really help a lot.
* Experiment 45 (https://drive.google.com/file/d/1XhaJFtqd3bFYqbvZIyeAJ2jAPfH9X0Ec/view?usp=sharing)
    * Same as above, except changing the network configuration from (80,40) in terms of the
    FCNN structure to (120,60) to see if an increase in the number of nodes per hidden layer
    will help the network extract the information more effectively. Seemed to have very little
    difference.
* Experiment 46 (https://drive.google.com/file/d/11hbrOXfKC1bA2jX4MTir5oYStiDI1i2o/view?usp=sharing)
    * Same as above, except tried adding another hidden layer rather than expanding the existing
    ones. Changed everything over to a network of size (80,40,40). Definitely didn't produce any
    super good results.
* Experiment 47 (https://drive.google.com/file/d/1ujS3bFq1jDnQza107D3H8glQnTwYKq1J/view?usp=sharing)
    * Tried changing the number of embedding dimensions for the instruction features to 32 rather
    than the current default value of 16. Didn't produce any super amazing results.