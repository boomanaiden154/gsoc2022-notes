# Model Training Log

### Model 1

Just some initial testing. Default settings on everything. Using MSE loss,
performed pretty terribly.

### Model 3

As close to the settings in the paper as possible. Performed reasonably well,
usually under 5% MAPE. Metrics were quite spiky however.

### Model 4

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model4/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=0 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=cosine --gematria_decay_steps=10000
```

Mostly default settings, except using a cosine learing rate schedule instead of
no learning rate schedule. This seemed to perform quite well from very initial
testing.

### Model 5
