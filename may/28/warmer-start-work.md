# Warmer Start work

Currently, the general process for training a new model using MLGO involves using a behavioral cloning process to mimic the current heuristic so that when the RL algorithm takes over, the model isn't just starting *de novo*. In the past, there hasn't been a ton of need to warm start off of an existing model (except for the additional feature engineering done on the inliner). However, with the register allocator eviction model, starting off of a pre-trained model might prove to be beneficial.

### Current Warm Start Process

Currently, in order to warm start a model, two steps are performed:

1. Run `generate_default_trace.py` to get a bunch of logs that can be used for training.

2. Run `train_bc.py` to actually perform the behavioral cloning.

### Modification to run using previous ML Models

Doesn't actually even require any modification. Should be as simple as running `generate_default_trace.py` with the `policy_path` flag set to a policy (a `saved_model.pb`) file from one of the Github releases/an internally trained model. Maybe some documentation changes on the main repo in order to make things a little bit more clear?

After running the trace with the `policy_path` flag set, all it should tag is running `train_bc.py` on the generated trace and it should work properly.
