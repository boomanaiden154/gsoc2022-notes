# Model Training Log

### Model 1

Just some initial testing. Default settings on everything. Using MSE loss,
performed pretty terribly.

### Model 3

As close to the settings in the paper as possible. Performed reasonably well,
usually under 5% MAPE. Metrics were quite spiky however.

Accuracey over the entire ~3M dataset: 0.048536944850279914

### Model 4

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model4/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=0 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=cosine --gematria_decay_steps=10000
```

Mostly default settings, except using a cosine learing rate schedule instead of
no learning rate schedule. This seemed to perform quite well from very initial
testing.

Seems to perform slightly better than static learning rate. Model MAPE is definitely
more consistent later on in the training run.

Evaluation invocation:
```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=predict --gematria_checkpoint_file=/data/bbs_20u7_model4/model.ckpt-99327 --gematria_max_blocks_in_batch=1000 --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord --gematria_output_file=/tmp/test.tfrecord --gematria_tokens_file=/data/vocab.txt
```

Accuracy over the entire ~3M dataset ~44k batches in (the best checkpoint): 0.04905960732664462

Accuracy over the entire ~3M dataset: 0.04431880611624217

### Model 5

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model5/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=100000 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=exponential --gematria_decay_steps=10000
```

Same as model 4, except using an exponential learning rate schedule.

Training performs pretty terrible, never really get under ~90% MAPE.

### Model 6

Default settings (same as Model 3), except trained on only 100,000 znver1 BBs
instead of the ~3M the other models are trained on. Intended for an A/B
comparison against data collected with lower variance (~0.5% run to run vs
~1.2%).

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model6/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=100000 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_100k.tfrecord  --gematria_max_blocks_in_batch=100
```

Evaluation invocation:

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=predict --gematria_checkpoint_file=/data/bbs_20u7_model6/model.ckpt-99037 --gematria_max_blocks_in_batch=10000 --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord --gematria_output_file=/tmp/test.tfrecord --gematria_tokens_file=/data/vocab.txt
```

Model seems to just overfit.

Accuracey over the entire ~3M dataset: 0.08773096838236415

### Model 7

Save as Model 4, except trained on 1M BBs instead of ~3M BBs as an ablation
test against dataset size.

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model7/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=100000 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_1M.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=cosine --gematria_decay_steps=10000
```

Model again seems to overfit by quite a bit.

Accuracey over the entire ~3M dataset: 0.09110467848145135

### Model 8

Training on the full ~3M BB dataset with similar settings to model 4, but trying
to change the layer counts/sizes and dimension counts/sizes to better match those
from the paper.

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model8/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=100000 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=cosine --gematria_decay_steps=10000 --gematria_node_embedding_size=256 --gematria_node_update_layers=256 --gematria_edge_embedding_size=256 --gematria_edge_update_layers=256 --gematria_global_embedding_size=256 --gematria_global_update_layers=256 --gematria_task_readout_layers=256
```

For this iteration, I accidentally had the steps for the learning rate to decay
set to 10000 instead of 100000, which caused the model to not make any progress
after 10000 batches. I only caught this after about 40k batches were through,
and the model seemed to perform decently, but definitely appeared to stop
learning significantly.

### Model 9

```
bazel run //gematria/granite/python:run_granite_model -- --gematria_action=train --gematria_checkpoint_dir=/data/bbs_20u7_model8/ --gematria_learning_rate=0.001 --gematria_loss_type=mean_absolute_error --gematria_training_num_epochs=100000 --gematria_tokens_file=/data/vocab.txt  --gematria_input_file=/data/bbs_benchmarked_20u7.tfrecord  --gematria_max_blocks_in_batch=100 --gematria_learning_rate_schedule=cosine --gematria_decay_steps=100000 --gematria_node_embedding_size=256 --gematria_node_update_layers=256 --gematria_edge_embedding_size=256 --gematria_edge_update_layers=256 --gematria_global_embedding_size=256 --gematria_global_update_layers=256 --gematria_task_readout_layers=256
```

Same as model 8, except the number of decay steps has been set to the proper
value.
